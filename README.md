# 🚀 나의 첫번째 챗봇

OpenAI의 최신 GPT 모델을 활용한 한국어 AI 챗봇 애플리케이션입니다.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

## ✨ 특징

- 💡 **똑똑한 응답**: 최신 AI 기술로 정확한 답변 제공
- ⚡ **실시간 스트리밍**: 빠르고 자연스러운 대화 경험
- 🎨 **다양한 활용**: 글쓰기, 코드 작성, 학습 등 다목적 활용
- 🔒 **보안**: API 키 안전 관리

## 🚀 설치 및 실행 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd chatbot-20251025
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. API 키 설정

OpenAI API 키를 설정하는 방법은 3가지가 있습니다:

#### 옵션 1: 사이드바에서 직접 입력 (웹 배포에 권장)
- 앱 실행 후 왼쪽 사이드바에서 API 키 입력
- 가장 간단하고 빠른 방법

#### 옵션 2: Streamlit Cloud Secrets (Streamlit Cloud 배포용)
1. Streamlit Cloud에서 앱 설정으로 이동
2. "Secrets" 섹션에 다음 내용 추가:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

#### 옵션 3: 로컬 secrets.toml (로컬 개발용)
1. `.streamlit/secrets.toml.example` 파일을 복사:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
2. `secrets.toml` 파일을 열고 실제 API 키 입력:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key"
   ```

> 🔑 OpenAI API 키는 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

### 4. 앱 실행

```bash
streamlit run streamlit_app.py
```

브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

## 📝 주요 파라미터

사이드바에서 다음 설정을 조정할 수 있습니다:

- **Model**: GPT 모델 선택 (gpt-4-turbo, gpt-4, gpt-3.5-turbo)
- **Temperature**: 응답의 창의성 조절 (0.0 ~ 2.0)
- **Max Tokens**: 응답의 최대 길이 설정

## 🔧 문제 해결

### "API Key Required" 오류
- API 키가 설정되지 않았습니다
- 위의 "3. API 키 설정" 섹션을 참조하세요

### 로컬에서는 되는데 웹에서 안 될 때
- Streamlit Cloud의 Secrets 설정을 확인하세요
- 또는 사이드바에서 직접 API 키를 입력하세요

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
