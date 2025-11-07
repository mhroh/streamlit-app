import streamlit as st
import anthropic
import gspread
from google.oauth2.service_account import Credentials
import os

st.title("🎭 디베이트 클럽에 오신 것을 환영합니다")

# API 키를 환경 변수 또는 Streamlit secrets에서 가져오기
try:
    # Streamlit Cloud 배포시 secrets 사용
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    google_creds = st.secrets.get("google_credentials")
except:
    # 로컬 실행시 환경 변수 사용
    api_key = os.getenv("ANTHROPIC_API_KEY")
    google_creds = None

if not api_key:
    st.error("⚠️ API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    st.stop()

# Claude 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

# 구글 시트에서 프롬프트 가져오기
@st.cache_data(ttl=300)  # 5분마다 캐시 갱신
def get_prompts_from_sheet():
    try:
        # 구글 시트 인증
        if google_creds:
            # Streamlit secrets 사용
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            credentials = Credentials.from_service_account_info(google_creds, scopes=scopes)
        else:
            # 로컬에서 서비스 계정 JSON 파일 사용
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            credentials = Credentials.from_service_account_file(
                'google_credentials.json',
                scopes=scopes
            )

        gc = gspread.authorize(credentials)

        # 스프레드시트 열기 (URL 또는 키로)
        sheet_url = os.getenv("GOOGLE_SHEET_URL") or st.secrets.get("GOOGLE_SHEET_URL")
        if not sheet_url:
            return None

        spreadsheet = gc.open_by_url(sheet_url)
        worksheet = spreadsheet.sheet1  # 첫 번째 시트 사용

        # 데이터 읽기 (A1: 시스템 프롬프트, A2: 환영 메시지, A3: 토론 가이드라인)
        data = worksheet.get_all_values()

        prompts = {
            'system_message': data[0][1] if len(data) > 0 and len(data[0]) > 1 else None,
            'welcome_message': data[1][1] if len(data) > 1 and len(data[1]) > 1 else None,
            'guidelines': data[2][1] if len(data) > 2 and len(data[2]) > 1 else None,
        }

        return prompts
    except Exception as e:
        st.warning(f"구글 시트 연동 오류: {str(e)}")
        return None

# 구글 시트에서 프롬프트 가져오기 시도
sheet_prompts = get_prompts_from_sheet()

# 기본 시스템 메시지
default_system_message = """당신은 디베이트 클럽의 전문 토론 진행자입니다.
사용자와 함께 다양한 주제에 대해 깊이 있는 토론을 진행합니다.
논리적이고 균형 잡힌 관점을 제시하며, 사용자의 의견에 대해 건설적인 반론과 질문을 제시합니다.
항상 예의 바르고 존중하는 태도를 유지하면서도 비판적 사고를 촉진합니다."""

# 시스템 메시지 결정 (구글 시트 우선, 없으면 기본값)
if sheet_prompts and sheet_prompts.get('system_message'):
    system_message = sheet_prompts['system_message']
    st.info("📋 현재 구글 시트의 프롬프트가 적용되었습니다.")
else:
    system_message = default_system_message

# 환영 메시지 표시
if sheet_prompts and sheet_prompts.get('welcome_message'):
    st.info(sheet_prompts['welcome_message'])

# 가이드라인 표시
if sheet_prompts and sheet_prompts.get('guidelines'):
    with st.expander("📝 토론 가이드라인"):
        st.markdown(sheet_prompts['guidelines'])

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            # 스트리밍 응답 생성
            with client.messages.stream(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                system=system_message,
                messages=st.session_state.messages,
            ) as stream:
                response = st.write_stream(stream.text_stream)

            # 어시스턴트 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

# 사이드바에 캐시 새로고침 버튼
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    if st.button("🔄 프롬프트 새로고침"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown(f"**메시지 수:** {len(st.session_state.messages)}")
    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()
