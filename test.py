import streamlit as st
import anthropic

st.title("🎭 디베이트 클럽에 오신 것을 환영합니다")

# 시스템 메시지 정의
system_message = """당신은 디베이트 클럽의 전문 토론 진행자입니다.
사용자와 함께 다양한 주제에 대해 깊이 있는 토론을 진행합니다.
논리적이고 균형 잡힌 관점을 제시하며, 사용자의 의견에 대해 건설적인 반론과 질문을 제시합니다.
항상 예의 바르고 존중하는 태도를 유지하면서도 비판적 사고를 촉진합니다."""

# API 키 입력
api_key = st.text_input("Claude API 키를 입력하세요:", type="password")

if api_key:
    st.session_state["api_key"] = api_key

# API 클라이언트 초기화
if "api_key" in st.session_state:
    client = anthropic.Anthropic(api_key=st.session_state["api_key"])

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 챗 메시지 출력
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
    if "api_key" in st.session_state:
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
                st.info("API 키가 올바른지 확인해주세요.")
    else:
        st.warning("먼저 Claude API 키를 입력해주세요.")
