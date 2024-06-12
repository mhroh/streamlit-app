import streamlit as st

st.title("디베이트 클럽에 오신 것을 환영합니다")

api_key = st.text_input("API 키를 입력하세요:", type="password")

if api_key:
    st.session_state["api_key"] = api_key

# API 클라이언트 초기화
if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])

    # 시스템 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

# 챗 메시지 출력
for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI 모델 호출
    if "api_key" in st.session_state:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant",