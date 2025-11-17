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
- 백엔드 개발에 관해 적어주세요

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

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

LAT = 35.1384  # 대연동 위도
LON = 129.1066  # 대연동 경도

def get_weather_data(lat=LAT, lon=LON):
    """OpenWeatherMap One Call API 3.0을 사용하여 날씨 데이터를 가져옵니다."""
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr",
        "exclude": "minutely,hourly"
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()

def get_air_pollution_data(lat=LAT, lon=LON):
    """OpenWeatherMap Air Pollution API 2.5를 사용하여 대기 오염 데이터를 가져옵니다."""
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()
```



### API 응답 예시

```
{
  "current_weather": {
    "temp_min": 5.8,
    "temp_max": 14.8,
    "temperature": 11.0,
    "sky": 맑음,
    "precip_type": 강수없음,
    "precip_prob": 0,
    "humidity": 20
  },
  "weekly_forecast": [
    {
      "date": "2025-11-18",
      "day_of_week": "화요일",
      "temp_min": 4.2,
      "temp_max": 8.9,
      "sky_am": "맑음",
      "sky_pm": "맑음",
      "precip_prob_am": 0,
      "precip_prob_pm": 0
    },
    {
      "date": "2025-11-19",
      "day_of_week": "수요일",
      "temp_min": 4.9,
      "temp_max": 9.7,
      "sky_am": "맑음",
      "sky_pm": "맑음",
      "precip_prob_am": 0,
      "precip_prob_pm": 0
    }
  ],
  "weather_alerts": [
    {
      "content": "[기상특보] 현재 발효된 특보가 없습니다."
    }
  ],
  "air_pollution": {
    "aqi": 1,
    "aqi_status": "좋음",
    "pm2_5": 4.8,
    "pm10": 9.89,
    "co": 193.55,
    "no2": 19.62
  }
}
```
참고: 위 예시는 일부 데이터만 보여주며, 실제 응답에는 더 많은 데이터가 포함됩니다.

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