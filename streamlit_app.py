import streamlit as st
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import time

# 페이지 설정
st.set_page_config(page_title="💬 Chatbot", layout="wide")

# 제목과 설명
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API 키 입력
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Your OpenAI API key")
    
    # 모델 선택
    model = st.selectbox(
        "Select Model",
        ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        help="Choose which OpenAI model to use"
    )
    
    # 파라미터 설정
    st.subheader("Parameters")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more focused"
    )
    
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=500,
        help="Maximum length of the response"
    )
    
    # 대화 초기화 버튼
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        time.sleep(0.5)
        st.rerun()

# API 키 확인
if not openai_api_key:
    st.info("Please add your OpenAI API key in the sidebar to continue.", icon="🗝️")
else:
    try:
        # OpenAI 클라이언트 생성
        client = OpenAI(api_key=openai_api_key)
        
        # 세션 상태에 메시지 저장 (재실행 시에도 유지)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # 시스템 프롬프트 설정
        system_message = {
            "role": "system",
            "content": "You are a helpful, friendly, and knowledgeable assistant. Provide clear, concise, and accurate responses."
        }
        
        # 기존 채팅 메시지 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 채팅 입력 필드
        if prompt := st.chat_input("What is up?"):
            # 사용자 메시지 저장 및 표시
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # API 호출 및 응답 생성
            try:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    # 메시지 리스트 구성 (시스템 메시지 포함)
                    messages_for_api = [system_message] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                    
                    # OpenAI API 호출 (스트리밍)
                    stream = client.chat.completions.create(
                        model=model,
                        messages=messages_for_api,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                    )
                    
                    # 응답 스트리밍
                    response_text = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
                            message_placeholder.markdown(response_text)
                    
                    # 최종 응답 저장
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
            
            # API 오류 처리
            except RateLimitError:
                st.error(
                    "⚠️ Rate limit exceeded. Please wait a moment and try again.",
                    icon="🚫"
                )
            except APIConnectionError:
                st.error(
                    "⚠️ Connection error. Please check your internet connection and try again.",
                    icon="🌐"
                )
            except APIError as e:
                st.error(
                    f"⚠️ OpenAI API error: {str(e)}",
                    icon="❌"
                )
            except Exception as e:
                st.error(
                    f"⚠️ An unexpected error occurred: {str(e)}",
                    icon="❌"
                )
    
    # API 키 검증 오류
    except Exception as e:
        st.error(
            "❌ Invalid OpenAI API key or connection error. Please check your API key and try again.",
            icon="🔑"
        )
