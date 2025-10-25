import streamlit as st
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import time

# 페이지 설정
st.set_page_config(page_title="나의 첫번째 챗봇", layout="wide", initial_sidebar_state="expanded")

# 커스텀 CSS 스타일
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5em;
            animation: fadeIn 1s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #666;
            margin-bottom: 2em;
            font-weight: 500;
        }
        
        .description-box {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-left: 4px solid #667eea;
            padding: 1.5em;
            border-radius: 8px;
            margin-bottom: 2em;
            font-size: 1.05em;
            line-height: 1.6;
        }
        
        .feature-list {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1em;
            margin-top: 1.5em;
        }
        
        .feature-item {
            background: white;
            padding: 1em;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            text-align: center;
        }
        
        .feature-icon {
            font-size: 2em;
            margin-bottom: 0.5em;
        }
    </style>
""", unsafe_allow_html=True)

# 제목과 설명
st.markdown('<div class="main-title">🚀 나의 첫번째 챗봇</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI와 대화하며 새로운 경험을 만들어보세요</div>', unsafe_allow_html=True)

# 설명 박스
st.markdown("""
    <div class="description-box">
        <b>✨ 당신의 AI 어시스턴트에 오신 것을 환영합니다!</b><br><br>
        이 챗봇은 OpenAI의 최신 GPT 모델을 활용하여 당신의 질문에 즉시 답변하고, 
        창의적인 작업을 도와주며, 복잡한 개념을 쉽게 설명해줍니다.<br><br>
        <b>🎯 지금 바로 시작해보세요!</b>
    </div>
""", unsafe_allow_html=True)

# 기능 소개
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">💡</div>
            <b>똑똑한 응답</b><br>
            최신 AI 기술이 당신의 질문을 완벽하게 이해하고 정확한 답변을 제공합니다.
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <b>실시간 응답</b><br>
            AI의 대답이 실시간으로 화면에 나타나 빠르고 자연스러운 대화 경험을 제공합니다.
        </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">🎨</div>
            <b>다양한 활용</b><br>
            글쓰기, 코드 작성, 아이디어 기획, 학습 등 무엇이든 가능합니다.
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <b>완벽한 보안</b><br>
            API 키는 안전하게 관리되며, 당신의 개인정보는 철저히 보호됩니다.
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ Settings")

    # API 키 설정
    st.subheader("🔑 API Key")

    # secrets.toml에서 API 키 자동 로드 시도
    api_key_from_secrets = None
    try:
        api_key_from_secrets = st.secrets["OPENAI_API_KEY"]
        st.success("✅ API Key loaded from secrets.toml", icon="🔑")
    except (KeyError, FileNotFoundError):
        st.info("💡 secrets.toml 파일이 없습니다. 아래에 API 키를 직접 입력하세요.", icon="ℹ️")

    # 사용자 입력 필드
    user_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="OpenAI API 키를 입력하세요. https://platform.openai.com/api-keys 에서 발급받을 수 있습니다.",
        value=""
    )

    # API 키 우선순위: 사용자 입력 > secrets.toml
    openai_api_key = user_api_key if user_api_key else api_key_from_secrets
    
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
    st.warning("⚠️ OpenAI API 키가 필요합니다!", icon="🗝️")
    st.info("""
    **API 키를 입력하는 방법:**

    1. 좌측 사이드바의 'OpenAI API Key' 필드에 직접 입력하거나
    2. `.streamlit/secrets.toml` 파일에 다음과 같이 설정하세요:

    ```toml
    OPENAI_API_KEY = "sk-your-api-key-here"
    ```

    API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.
    """, icon="💡")
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
            "❌ Invalid OpenAI API key or connection error. Please check your configuration.",
            icon="🔑"
        )
