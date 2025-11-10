# 🎭 디베이트 클럽 챗봇

Claude API를 활용한 학생용 토론 챗봇 Streamlit 애플리케이션입니다.

## ✨ 주요 기능

### 학생용 기능
- **Claude Sonnet 4.5** 모델을 사용한 지능형 토론 파트너
- 실시간 스트리밍 응답으로 자연스러운 대화
- **학급 + 번호 + 이름** 입력으로 체계적인 학생 관리
- **자동 저장**: 10개 메시지마다 자동으로 구글 시트에 임시 저장
- API 키 입력 없이 바로 사용 가능

### 교사용 기능
- **구글 시트 통합 관리**: 하나의 시트로 30개 앱 모두 관리
- **앱별 프롬프트 설정**: 각 반/그룹마다 다른 토론 주제와 방식 설정
- **자동 기록 저장**: "반_주제_날짜" 형식으로 자동 시트 생성
- **루브릭 기반 평가**: 토론 종료 시 자동으로 평가 생성 및 저장
- **실시간 업데이트**: 구글 시트 수정 시 5분 이내 자동 반영

## 📊 시스템 구조

### 프롬프트 관리 (하나의 구글 시트)
```
📄 디베이트_통합_관리 (하나의 구글 시트)
├─ 탭 "idebate"    → idebate.streamlit.app용 설정
├─ 탭 "idebate01"  → idebate01.streamlit.app용 설정
├─ 탭 "idebate02"  → idebate02.streamlit.app용 설정
└─ ...
└─ 탭 "idebate30"  → idebate30.streamlit.app용 설정

각 탭 구조:
A1: 시스템 프롬프트 | B1: (내용)
A2: 환영 메시지 | B2: (내용)
A3: 토론 가이드라인 | B3: (내용)
A4: 토론 주제 | B4: AI윤리
A5: 루브릭 | B5: (평가 기준)
```

### 학생 기록 저장 (자동 생성)
```
📁 구글 드라이브 폴더 (선택)
  ├─ 📄 idebate_AI윤리_2025-01-15
  │   학생정보 (학급_번호_이름) | 대화내역 | 메시지수 | 저장시간 | 상태 | 평가점수 | 평가내용
  │   예: 1반_5_김철수 | (전체 대화) | 24 | 2025-01-15 10:30 | 최종저장 | 85 | 논리성 우수...
  ├─ 📄 idebate01_기후변화_2025-01-15
  └─ 📄 idebate02_민주주의_2025-01-16
```

## 🚀 설정 방법

### 1. 구글 시트 설정 (프롬프트 관리용)

#### 1-1. 구글 시트 생성
1. 새 구글 시트 만들기: "디베이트_통합_관리"
2. 각 앱별로 탭 생성: `idebate`, `idebate01`, `idebate02`, ..., `idebate30`
3. 각 탭에 다음과 같이 설정:

| A열 | B열 |
|-----|-----|
| 시스템 프롬프트 | 당신은... |
| 환영 메시지 | 오늘의 토론... |
| 토론 가이드라인 | 규칙: ... |
| 토론 주제 | AI윤리 |
| 루브릭 | 평가 기준... |

자세한 예시는 `google_sheet_template.md` 참고!

#### 1-2. 구글 서비스 계정 만들기
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. **API 및 서비스 > 라이브러리**에서 활성화:
   - Google Sheets API
   - Google Drive API
4. **사용자 인증 정보 > 서비스 계정** 생성
5. JSON 키 다운로드

#### 1-3. 구글 시트 공유
- 생성한 시트를 서비스 계정 이메일과 공유 (편집 권한)

### 2. 구글 드라이브 폴더 설정 (기록 저장용, 선택사항)

1. 구글 드라이브에서 "디베이트_기록" 폴더 생성
2. 폴더 URL에서 ID 복사
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
                                           ↑ 이 부분
   ```
3. 폴더를 서비스 계정과 공유 (편집 권한)

### 3. 환경 변수 설정

#### 로컬 개발
```bash
cp .env.example .env
```

`.env` 파일 편집:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
APP_ID=idebate
RECORD_FOLDER_ID=your_folder_id
```

#### Streamlit Cloud 배포
각 앱의 **Settings > Secrets**:

```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxx"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id/edit"
APP_ID = "idebate01"  # 각 앱마다 다르게!
RECORD_FOLDER_ID = "your_folder_id"

[google_credentials]
type = "service_account"
project_id = "your-project"
private_key_id = "xxx"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "xxx@xxx.iam.gserviceaccount.com"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"
```

**중요:**
- `APP_ID`만 각 앱마다 다르게 설정 (idebate, idebate01, idebate02, ...)
- 나머지는 모두 동일하게 설정

## 💻 로컬 실행

```bash
# 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run test.py
```

## 📖 사용 방법

### 학생용
1. 앱 URL 접속
2. **학급, 번호, 이름** 입력 (예: 1반, 5, 김철수)
3. 토론 시작!
4. 토론 끝나면 **"🏁 토론 종료 및 평가받기"** 클릭

**팁:** 실시간 피드백이 필요하면 프롬프트에 "내 의견 어때?"라고 물어보세요!

### 교사용
1. **프롬프트 수정**: 구글 시트에서 원하는 탭 편집 → 5분 이내 자동 반영
2. **기록 확인**: 구글 드라이브 폴더에서 "반_주제_날짜" 시트 열기
3. **평가 확인**: 각 시트의 "평가점수", "평가내용" 열 확인

## 🔧 주요 기능 상세

### 학생 정보 관리
- **학급, 번호, 이름** 3가지 정보 입력
- 구글 시트에 "학급_번호_이름" 형식으로 자동 저장
- 예: `1반_5_김철수`

### 자동 저장
- 10개 메시지마다 자동으로 구글 시트에 임시 저장
- 학생이 브라우저를 닫아도 데이터 보존
- 토스트 알림으로 저장 확인

### 토론 종료 및 평가
- "🏁 토론 종료 및 평가받기" 버튼
- 전체 대화 기반 루브릭 평가 자동 생성
- 구글 시트에 평가 저장 (교사만 확인 가능)

### 다중 앱 관리
- 하나의 구글 시트로 30개 앱 관리
- 각 앱은 독립적인 서버로 실행 (부하 분산)
- APP_ID로 자동 구분

## 📁 파일 구조

```
streamlit-app/
├── test.py                    # 메인 애플리케이션
├── first.py                   # 간단한 테스트 페이지
├── requirements.txt           # Python 패키지
├── .env.example              # 환경 변수 템플릿
├── .gitignore                # Git 무시 파일
├── google_credentials.json   # 구글 서비스 계정 (로컬, gitignore됨)
├── google_sheet_template.md  # 구글 시트 설정 가이드
└── README.md                 # 이 파일
```

## 🔐 보안 주의사항

- `.env`, `google_credentials.json`은 **절대 Git에 커밋 금지**
- `.gitignore`에 이미 추가되어 있음
- API 키와 인증 정보는 환경 변수나 Streamlit Secrets로만 관리

## 🆘 문제 해결

### "API 키가 설정되지 않았습니다"
- `.env` 파일에 `ANTHROPIC_API_KEY` 확인
- Streamlit Cloud: Secrets에 추가 확인

### "구글 시트 연동 오류"
- 서비스 계정이 시트에 접근 권한 있는지 확인
- `GOOGLE_SHEET_URL`이 올바른지 확인
- Google Sheets API, Drive API 활성화 확인

### "저장 오류"
- 서비스 계정이 폴더에 편집 권한 있는지 확인
- `RECORD_FOLDER_ID`가 올바른지 확인

### 프롬프트가 업데이트 안 됨
- 사이드바 **"🔄 프롬프트 새로고침"** 클릭
- 구글 시트 형식 확인 (A1-B1, A2-B2, ...)
- 탭 이름이 `APP_ID`와 일치하는지 확인

### 자동 저장이 안 됨
- 10개 메시지 이상 대화했는지 확인
- 네트워크 연결 확인
- 브라우저 콘솔에서 오류 확인

## 🎓 학생 경험 vs 교사 경험

| 기능 | 학생 | 교사 |
|------|------|------|
| 토론 중 피드백 | ✅ 대화 중 요청 가능 | ❌ |
| 루브릭 평가 | ❌ | ✅ 구글 시트에서 확인 |
| 대화 기록 | ✅ 앱 내에서만 | ✅ 구글 시트 영구 보관 |
| 프롬프트 수정 | ❌ | ✅ 구글 시트 편집 |
| 학생 정보 | ✅ 학급+번호+이름 입력 | ✅ 체계적으로 확인 |

## 🚀 배포 팁

### 30개 앱을 빠르게 배포하는 방법
1. Streamlit Cloud에서 첫 번째 앱 생성
2. Settings에서 Secrets 설정 (`APP_ID=idebate`)
3. 같은 방식으로 29개 앱 더 생성
4. **중요**: 각 앱의 `APP_ID`만 변경 (idebate01, idebate02, ...)
5. 나머지 Secrets는 모두 동일

### 구글 시트 탭 빠르게 만들기
1. 첫 번째 탭 완성
2. 탭 우클릭 → 복사
3. 29번 붙여넣기
4. 각 탭 이름을 idebate, idebate01, ... 로 변경
5. 각 탭의 "토론 주제"만 수정

## 📝 라이선스

MIT License

---

## 🙋 FAQ

**Q: 학생이 토론 종료 버튼을 안 누르면?**
A: 10개 메시지마다 자동 저장되므로 데이터는 보존됩니다. 다만 루브릭 평가는 생성되지 않으므로, 교사가 나중에 수동으로 평가하거나 학생에게 다시 종료하도록 안내하세요.

**Q: 여러 학생이 같은 이름을 쓰면?**
A: 학급과 번호를 함께 입력받으므로 중복 문제가 해결됩니다. 구글 시트에는 "학급_번호_이름" 형식으로 저장됩니다.

**Q: 구글 시트가 느려지면?**
A: 하루에 100명 이상 사용하면 느려질 수 있습니다. 그럴 경우 주제별로 시트를 분리하거나, 주기적으로 오래된 기록을 아카이브하세요.

**Q: 자동 저장이 답답하게 느껴지면?**
A: `test.py`의 313번 줄 `>= st.session_state.last_save_count + 10`에서 `10`을 `20`으로 변경하면 20개 메시지마다 저장됩니다.
