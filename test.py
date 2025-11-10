import streamlit as st
import anthropic
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
import time

st.set_page_config(page_title="디베이트 클럽", page_icon="🎭")

# ==================== 설정 ====================

# API 키 및 인증 정보 로드
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    google_creds = st.secrets.get("google_credentials")
    app_id = st.secrets.get("APP_ID") or os.getenv("APP_ID", "idebate")
    record_folder_id = st.secrets.get("RECORD_FOLDER_ID") or os.getenv("RECORD_FOLDER_ID")
except:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    google_creds = None
    app_id = os.getenv("APP_ID", "idebate")
    record_folder_id = os.getenv("RECORD_FOLDER_ID")

if not api_key:
    st.error("⚠️ API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    st.stop()

# Claude 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

# ==================== 구글 시트 관련 함수 ====================

def get_google_credentials():
    """구글 인증 정보 가져오기"""
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    if google_creds:
        return Credentials.from_service_account_info(google_creds, scopes=scopes)
    else:
        return Credentials.from_service_account_file('google_credentials.json', scopes=scopes)

@st.cache_data(ttl=300)
def get_prompts_from_sheet():
    """구글 시트에서 프롬프트 가져오기 (APP_ID에 해당하는 탭)"""
    try:
        credentials = get_google_credentials()
        gc = gspread.authorize(credentials)

        sheet_url = os.getenv("GOOGLE_SHEET_URL") or st.secrets.get("GOOGLE_SHEET_URL")
        if not sheet_url:
            return None

        spreadsheet = gc.open_by_url(sheet_url)

        # APP_ID에 해당하는 워크시트 찾기
        try:
            worksheet = spreadsheet.worksheet(app_id)
        except:
            # 해당 탭이 없으면 첫 번째 시트 사용
            worksheet = spreadsheet.sheet1

        data = worksheet.get_all_values()

        prompts = {
            'system_message': data[0][1] if len(data) > 0 and len(data[0]) > 1 else None,
            'welcome_message': data[1][1] if len(data) > 1 and len(data[1]) > 1 else None,
            'guidelines': data[2][1] if len(data) > 2 and len(data[2]) > 1 else None,
            'debate_topic': data[3][1] if len(data) > 3 and len(data[3]) > 1 else "일반 토론",
            'rubric': data[4][1] if len(data) > 4 and len(data[4]) > 1 else None,
            'feedback_prompt': data[5][1] if len(data) > 5 and len(data[5]) > 1 else None,
        }

        return prompts
    except Exception as e:
        st.warning(f"구글 시트 연동 오류: {str(e)}")
        return None

def auto_save_to_sheet(student_name, messages, debate_topic, is_final=False):
    """구글 시트에 대화 내역 저장 (자동 저장 또는 최종 저장)"""
    try:
        credentials = get_google_credentials()
        gc = gspread.authorize(credentials)

        # 시트 이름: 반_주제_날짜
        date_str = datetime.now().strftime("%Y-%m-%d")
        sheet_name = f"{app_id}_{debate_topic}_{date_str}"

        # 기존 시트 찾거나 새로 생성
        try:
            if record_folder_id:
                # 폴더 내에서 시트 찾기
                spreadsheet = gc.open(sheet_name)
            else:
                # 루트에서 시트 찾기
                spreadsheet = gc.open(sheet_name)
        except:
            # 시트가 없으면 새로 생성
            spreadsheet = gc.create(sheet_name)

            # 폴더로 이동 (폴더 ID가 있는 경우)
            if record_folder_id:
                try:
                    from googleapiclient.discovery import build
                    drive_service = build('drive', 'v3', credentials=credentials)
                    file_id = spreadsheet.id
                    drive_service.files().update(
                        fileId=file_id,
                        addParents=record_folder_id,
                        fields='id, parents'
                    ).execute()
                except:
                    pass  # 폴더 이동 실패해도 계속 진행

            # 헤더 추가
            worksheet = spreadsheet.sheet1
            worksheet.update('A1:G1', [['학생이름', '대화내역', '메시지수', '저장시간', '상태', '평가점수', '평가내용']])

        worksheet = spreadsheet.sheet1

        # 대화 내역을 텍스트로 변환
        conversation_text = "\n\n".join([
            f"{'학생' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
            for msg in messages
        ])

        # 기존 학생 기록 찾기
        all_values = worksheet.get_all_values()
        student_row = None
        for idx, row in enumerate(all_values[1:], start=2):  # 헤더 제외
            if row[0] == student_name:
                student_row = idx
                break

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "최종저장" if is_final else "임시저장"

        if student_row:
            # 기존 기록 업데이트
            worksheet.update(f'B{student_row}:E{student_row}',
                           [[conversation_text, len(messages), current_time, status]])
        else:
            # 새 행 추가
            worksheet.append_row([student_name, conversation_text, len(messages), current_time, status, '', ''])

        return True
    except Exception as e:
        st.error(f"저장 오류: {str(e)}")
        return False

def save_evaluation_to_sheet(student_name, evaluation_score, evaluation_text, debate_topic):
    """루브릭 평가를 구글 시트에 저장"""
    try:
        credentials = get_google_credentials()
        gc = gspread.authorize(credentials)

        date_str = datetime.now().strftime("%Y-%m-%d")
        sheet_name = f"{app_id}_{debate_topic}_{date_str}"

        spreadsheet = gc.open(sheet_name)
        worksheet = spreadsheet.sheet1

        # 학생 행 찾기
        all_values = worksheet.get_all_values()
        for idx, row in enumerate(all_values[1:], start=2):
            if row[0] == student_name:
                # 평가 정보 업데이트
                worksheet.update(f'F{idx}:G{idx}', [[evaluation_score, evaluation_text]])
                break

        return True
    except Exception as e:
        st.error(f"평가 저장 오류: {str(e)}")
        return False

def get_rubric_evaluation(messages, rubric):
    """Claude에게 루브릭 기반 평가 요청"""
    try:
        # 대화 내역을 텍스트로 변환
        conversation = "\n\n".join([
            f"{'학생' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
            for msg in messages
        ])

        evaluation_prompt = f"""다음은 학생의 토론 대화 내역입니다:

{conversation}

아래 루브릭을 기준으로 학생의 토론을 평가해주세요:

{rubric}

다음 형식으로 답변해주세요:
1. 점수: (0-100점 중)
2. 평가 내용: (각 항목별 상세 평가)

답변 형식:
점수: [점수]
평가: [상세 평가 내용]
"""

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{"role": "user", "content": evaluation_prompt}]
        )

        eval_text = response.content[0].text

        # 점수 추출
        score = "평가필요"
        if "점수:" in eval_text:
            try:
                score_line = [line for line in eval_text.split('\n') if '점수:' in line][0]
                score = score_line.split('점수:')[1].strip().split()[0]
            except:
                pass

        return score, eval_text
    except Exception as e:
        return "오류", f"평가 생성 중 오류 발생: {str(e)}"

# ==================== UI ====================

st.title("🎭 디베이트 클럽에 오신 것을 환영합니다")

# 프롬프트 가져오기
sheet_prompts = get_prompts_from_sheet()

# 기본값 설정
default_system_message = """당신은 디베이트 클럽의 전문 토론 진행자입니다.
사용자와 함께 다양한 주제에 대해 깊이 있는 토론을 진행합니다.
논리적이고 균형 잡힌 관점을 제시하며, 사용자의 의견에 대해 건설적인 반론과 질문을 제시합니다.
항상 예의 바르고 존중하는 태도를 유지하면서도 비판적 사고를 촉진합니다."""

default_feedback_prompt = """학생이 방금 한 발언에 대해 간단한 피드백을 주세요:
1. 좋은 점 1가지
2. 개선할 점 1가지
3. 다음 질문 제안

3-4문장으로 간결하게 답변해주세요."""

system_message = sheet_prompts.get('system_message') if sheet_prompts else default_system_message
if not system_message:
    system_message = default_system_message

debate_topic = sheet_prompts.get('debate_topic') if sheet_prompts else "일반 토론"
rubric = sheet_prompts.get('rubric') if sheet_prompts else None
feedback_prompt = sheet_prompts.get('feedback_prompt') if sheet_prompts else default_feedback_prompt

# 환영 메시지
if sheet_prompts and sheet_prompts.get('welcome_message'):
    st.info(sheet_prompts['welcome_message'])

# 가이드라인
if sheet_prompts and sheet_prompts.get('guidelines'):
    with st.expander("📝 토론 가이드라인"):
        st.markdown(sheet_prompts['guidelines'])

# 학생 이름 입력
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if not st.session_state.student_name:
    st.markdown("### 👤 먼저 이름을 입력해주세요")
    name_input = st.text_input("이름:", key="name_input_field")
    if st.button("시작하기") and name_input:
        st.session_state.student_name = name_input
        st.session_state.messages = []
        st.session_state.last_save_count = 0
        st.rerun()
    st.stop()

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_save_count" not in st.session_state:
    st.session_state.last_save_count = 0

# 학생 정보 표시
st.success(f"👤 {st.session_state.student_name}님, 환영합니다!")

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 채팅 입력
if prompt := st.chat_input("토론하고 싶은 주제나 의견을 입력하세요"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Claude 모델 호출
    with st.chat_message("assistant"):
        try:
            with client.messages.stream(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                system=system_message,
                messages=st.session_state.messages,
            ) as stream:
                response = st.write_stream(stream.text_stream)

            st.session_state.messages.append({"role": "assistant", "content": response})

            # 자동 저장 (5개 메시지마다)
            if len(st.session_state.messages) >= st.session_state.last_save_count + 10:
                with st.spinner("💾 자동 저장 중..."):
                    if auto_save_to_sheet(
                        st.session_state.student_name,
                        st.session_state.messages,
                        debate_topic,
                        is_final=False
                    ):
                        st.session_state.last_save_count = len(st.session_state.messages)
                        st.toast("✅ 자동 저장 완료!")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

# ==================== 사이드바 ====================

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.student_name}")
    st.markdown(f"**토론 주제:** {debate_topic}")
    st.markdown(f"**메시지 수:** {len(st.session_state.messages)}")

    st.markdown("---")

    # 피드백 요청 버튼
    if st.button("💬 내 의견 평가받기"):
        if len(st.session_state.messages) > 0:
            with st.spinner("피드백 생성 중..."):
                try:
                    # 최근 대화 기반 피드백
                    recent_messages = st.session_state.messages[-6:]  # 최근 3턴

                    feedback_response = client.messages.create(
                        model="claude-sonnet-4-5-20250929",
                        max_tokens=1024,
                        system=system_message,
                        messages=recent_messages + [
                            {"role": "user", "content": feedback_prompt}
                        ]
                    )

                    feedback = feedback_response.content[0].text

                    # 피드백을 대화에 추가
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"📊 **피드백**\n\n{feedback}"
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"피드백 생성 오류: {str(e)}")
        else:
            st.warning("먼저 토론을 시작해주세요!")

    st.markdown("---")

    # 토론 종료 버튼
    if st.button("🏁 토론 종료 및 평가받기", type="primary"):
        if len(st.session_state.messages) > 0:
            with st.spinner("최종 저장 및 평가 생성 중..."):
                # 최종 저장
                auto_save_to_sheet(
                    st.session_state.student_name,
                    st.session_state.messages,
                    debate_topic,
                    is_final=True
                )

                # 루브릭 평가 (루브릭이 있는 경우)
                if rubric:
                    score, evaluation = get_rubric_evaluation(st.session_state.messages, rubric)
                    save_evaluation_to_sheet(
                        st.session_state.student_name,
                        score,
                        evaluation,
                        debate_topic
                    )

                st.success("✅ 토론이 종료되었습니다!")
                st.info("💾 대화 내역과 평가가 저장되었습니다.")

                # 세션 초기화
                if st.button("🔄 새 토론 시작"):
                    st.session_state.messages = []
                    st.session_state.last_save_count = 0
                    st.rerun()
        else:
            st.warning("먼저 토론을 시작해주세요!")

    st.markdown("---")

    # 관리자 기능
    st.markdown("### ⚙️ 관리")

    if st.button("🔄 프롬프트 새로고침"):
        st.cache_data.clear()
        st.rerun()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.session_state.last_save_count = 0
        st.rerun()

    if st.button("👋 로그아웃"):
        st.session_state.student_name = ""
        st.session_state.messages = []
        st.rerun()
