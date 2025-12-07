# 오늘의 하늘

간단하고 직관적인 UI로 도시별 날씨 정보를 제공하는 웹 서비스입니다.

---

## 프로젝트 소개

- 기존 날씨 서비스의 광고 과다 및 복잡한 UI 문제 해결
- Flask 서버와 공공 API 연동으로 실시간 날씨 정보 제공

---

## 기술 스택

- 프론트엔드: Flask + Jinja2 / React
- 백엔드: Flask
- API: OpenWeatherMap API

---

## 주요 기능

- 단기 예보
  - 최저기온, 최고 기온, 체감온도, 날씨, 강수 확률, 습도
  
- 주간 예보 (6일 간)
  - 날짜, 요일, 최저 기온, 최고 기온, 날씨, 강수 확률
- 기상 특보
  - 해당 지역의 기상 특보 발령 여부와 발령된 기상 특보의 종류
- 대기 오염 수치 제공 

---

## Frontend

- 프론트엔드 개발에 관해 적어주세요
---

## Backend
### Backend 기능
- JSON API 엔드포인트 구축 (`/api/weather`)
- Flask 서버 관리 및 구축
- 데이터 전처리 및 변환
- 예외 처리 및 서버 안정성 보장

### Flask 서버 실행 방법
1. cmd(명령 프롬프트) 창을 연다. (맥의 경우 PowerShell 사용)
2. app.py가 있는 백엔드 폴더(backend)를 경로로 이동하는 명령어를 입력한다.
    > cd ...\backend (ex)
3. venv 가상환경을 설치한다. (최초 1회만)
    > python -m venv venv # 새 가상환경 생성
4. venv 가상환경을 구동한다.
    > venv\Scripts\activate   # Windows
    > source venv/bin/activate     # macOS/Linux
5. Python 패키지 설치 (최초 1회만)
    > pip install -r requirements.txt
6. Flask 서버를 실행해서 정상적으로 서버가 실행되는지 확인한다. (정상적으로 실행될 경우 * Running on http://127.0.0.1:5000) 표시
    > flask run
7. 서버를 종료할때는 명령 프롬프트 창에서 ctrl + c 를 입력하여 서버를 닫는다.

---

## API

### 사용한 API

- OpenWeatherMap API
    - 현재 날씨, 단기/주간 예보, 습도, 기상 특보, 대기 오염 정도 등 다양한 날씨 정보 제공
    - 공식 문서: [OpenWeatherMap API] https://openweathermap.org/api
    - API 키 발급 방법: [One Call API] https://openweathermap.org/api/one-call-3
    - API 키 발급 방법: [Air Pollution] https://openweathermap.org/api/air-pollution
    - 일일 호출 제한: 1000 API calls per day for free 0.0012 GBP per API call over the daily limit

### API 사용 예시

- **API 호출**: `requests.get()`을 사용해 OpenWeatherMap의 One Call API와 Air Pollution API에 요청을 보냅니다.
- **파라미터**:
 - `lat`, `lon`: 위치 좌표 - `appid`: API 키 - `units`: 단위 (metric: 섭씨)
 - `lang`: 언어 (kr: 한국어)
 - `exclude`: 불필요한 데이터 제외 (minutely, hourly)
- **응답 처리**: `res.json()`으로 JSON 형식의 응답을 받아 처리합니다.
---

## 설치 및 실행

1. 저장소 클론
2. 의존성 설치
3. API 키 설정
4. 서버 실행

---

## 팀원 및 역할

| 이름 | 역할 | GitHub ID |
| --- | --- | --- |
| 권민준 | 리더 | funky-jun |
| 권상혁 | 커미터 | pttnekh |
| 박성제 | 메인테이너 | seongje973 |