# 🎭 디베이트 클럽 챗봇

Claude API를 활용한 학생용 토론 챗봇 Streamlit 애플리케이션입니다.

## ✨ 주요 기능

- **Claude Sonnet 4.5** 모델을 사용한 지능형 토론 파트너
- **구글 시트 연동**으로 토론 프롬프트와 방식을 실시간으로 조정
- 실시간 스트리밍 응답
- 학생들이 API 키 없이 바로 사용 가능
- 깔끔한 채팅 인터페이스

## 📋 구글 시트 설정

### 1. 구글 시트 생성

새 구글 시트를 만들고 다음과 같이 설정하세요:

| A열 (항목) | B열 (내용) |
|-----------|-----------|
| 시스템 프롬프트 | 당신은 디베이트 클럽의 전문 토론 진행자입니다... |
| 환영 메시지 | 오늘의 토론 주제는 "인공지능의 윤리"입니다. |
| 토론 가이드라인 | 1. 상대방의 의견을 경청하세요\n2. 근거를 제시하세요... |

**예시:**
```
A1: 시스템 프롬프트
B1: 당신은 디베이트 클럽의 전문 토론 진행자입니다. 학생들과 함께 논리적이고 균형 잡힌 토론을 진행하며, 비판적 사고를 촉진합니다.

A2: 환영 메시지
B2: 🎓 오늘의 토론 주제: "인공지능의 발전이 사회에 미치는 영향"

A3: 토론 가이드라인
B3: ## 토론 규칙
- 상대방의 의견을 존중하세요
- 논리적 근거를 제시하세요
- 감정적이지 않고 이성적으로 토론하세요
```

### 2. 구글 서비스 계정 만들기

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스 > 라이브러리**에서 다음 API 활성화:
   - Google Sheets API
   - Google Drive API
4. **API 및 서비스 > 사용자 인증 정보 > 사용자 인증 정보 만들기 > 서비스 계정**
5. 서비스 계정 생성 후 **키 > 키 추가 > 새 키 만들기 > JSON** 선택
6. 다운로드한 JSON 파일 저장

### 3. 구글 시트 공유

- 생성한 구글 시트를 서비스 계정 이메일(`xxxxx@xxxxx.iam.gserviceaccount.com`)과 공유 (읽기 권한)

## 🚀 로컬 개발 환경 설정

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
```

### 3. 구글 서비스 계정 JSON 파일

다운로드한 서비스 계정 JSON 파일을 프로젝트 루트에 `google_credentials.json`으로 저장

### 4. 앱 실행

```bash
streamlit run test.py
```

## ☁️ Streamlit Cloud 배포

### 1. GitHub에 코드 푸시

```bash
git add .
git commit -m "Add debate chatbot"
git push
```

### 2. Streamlit Cloud 설정

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. **New app** 클릭
3. 리포지토리와 브랜치 선택
4. Main file path: `test.py`

### 3. Secrets 설정

Streamlit Cloud의 **Settings > Secrets**에서 다음 추가:

```toml
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id/edit"

[google_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

> **주의:** `google_credentials.json` 파일의 내용을 그대로 복사하되, TOML 형식에 맞게 변환해야 합니다.

### 4. 배포

**Deploy** 버튼 클릭!

## 📖 사용 방법 (학생용)

1. 앱 URL로 접속
2. 구글 시트에 설정된 환영 메시지와 가이드라인 확인
3. 채팅창에 의견 입력
4. Claude와 토론 시작!

## 🔧 관리자 기능

### 프롬프트 업데이트
- 구글 시트의 내용을 수정하면 자동으로 반영됩니다 (5분 캐시)
- 즉시 반영하려면 사이드바의 **🔄 프롬프트 새로고침** 클릭

### 대화 초기화
- 사이드바의 **🗑️ 대화 초기화** 버튼으로 대화 내역 삭제

## 📁 파일 구조

```
streamlit-app/
├── test.py                    # 메인 애플리케이션
├── first.py                   # 간단한 테스트 페이지
├── requirements.txt           # Python 패키지
├── .env.example              # 환경 변수 템플릿
├── .gitignore                # Git 무시 파일
├── google_credentials.json   # 구글 서비스 계정 (로컬용, gitignore됨)
└── README.md                 # 이 파일
```

## 🔐 보안 주의사항

- `.env` 파일과 `google_credentials.json`은 **절대 Git에 커밋하지 마세요**
- `.gitignore`에 이미 추가되어 있으니 확인하세요
- API 키는 환경 변수나 Streamlit Secrets로만 관리하세요

## 🆘 문제 해결

### "API 키가 설정되지 않았습니다"
- `.env` 파일에 `ANTHROPIC_API_KEY`가 올바르게 설정되었는지 확인
- Streamlit Cloud의 경우 Secrets에 추가했는지 확인

### "구글 시트 연동 오류"
- 서비스 계정이 해당 시트에 접근 권한이 있는지 확인
- `GOOGLE_SHEET_URL`이 올바른지 확인
- Google Sheets API와 Drive API가 활성화되었는지 확인

### 프롬프트가 업데이트되지 않음
- 사이드바의 **🔄 프롬프트 새로고침** 클릭
- 구글 시트의 형식이 올바른지 확인 (A1-B1, A2-B2, A3-B3)

## 📝 라이선스

MIT License
