import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 도시 검색 기능 추가 전까지 임시로 사용되는 좌표
LAT = 35.1384  # 부산 대연동 위도
LON = 129.1066 # 부산 대연동 경도

# OpenWeatherMap 날씨 코드 -> 한국어 번역 딕셔너리
weather_translate = {
    # ... (생략: 기존 코드와 동일)
    "Clear": "맑음",
    "Clouds": "구름많음",
    "Rain": "비",
    "Snow": "눈",
    "Drizzle": "이슬비",
    "Thunderstorm": "뇌우",
    "Mist": "안개",
    "Smoke": "연기",
    "Haze": "실안개",
    "Dust": "먼지",
    "Fog": "안개",
    "Sand": "모래",
    "Ash": "화산재",
    "Squall": "돌풍",
    "Tornado": "토네이도",
}

# ⚠️ AQI 5단계 기준 딕셔너리(aqi_translate)는 이제 사용되지 않습니다. 
# 대신 한국 환경부 8단계 기준이 사용됩니다.

# --- [새로 추가된 한국 환경부 8단계 기준] ---

# 한국 환경부 PM2.5 (초미세먼지) 8단계 기준 (단위: $\mu g/m^3$)
PM25_KOREA_STANDARDS = {
    '최고': (0, 8),
    '좋음': (8, 16),
    '양호': (16, 21),
    '보통': (21, 36),
    '나쁨': (36, 76),
    '상당히 나쁨': (76, 101),
    '매우 나쁨': (101, 251),
    '위험': (251, 10000),
}

# 한국 환경부 PM10 (미세먼지) 8단계 기준 (단위: $\mu g/m^3$)
PM10_KOREA_STANDARDS = {
    '최고': (0, 15),
    '좋음': (15, 31),
    '양호': (31, 41),
    '보통': (41, 71),
    '나쁨': (71, 151),
    '상당히 나쁨': (151, 201),
    '매우 나쁨': (201, 301),
    '위험': (301, 10000),
}

def get_korea_air_status(value, standards):
    """주어진 농도 값과 한국 기준 딕셔너리를 사용하여 상태를 반환합니다."""
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "정보없음"
    
    for status, (min_val, max_val) in standards.items():
        # OpenWeatherMap 농도가 한국 기준 범위 내에 있는지 확인
        if min_val <= value < max_val:
            return status
    return "정보없음"

# ------------------------------------------------------------------
# get_weather_data, get_air_pollution_data, process_hourly_data, process_data 함수 생략
# ------------------------------------------------------------------

def get_weather_data(lat=LAT, lon=LON):
    # ... (기존 코드와 동일)
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr",
        "exclude": "minutely"
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()

def get_air_pollution_data(lat=LAT, lon=LON):
    # ... (기존 코드와 동일)
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()

def process_hourly_data(data):
    # ... (기존 코드와 동일)
    hourly_forecast = []
    hourly_list = data.get("hourly", []) 
    for item in hourly_list[:24]: 
        dt = datetime.fromtimestamp(item.get("dt"))
        hourly_forecast.append({
            "time": dt.strftime("%H:%M"), 
            "temp": round(item.get("temp", 0), 1), 
            "weather_icon": item.get("weather", [{}])[0].get("icon", "")
        })
    return hourly_forecast

def process_data(data):
    # ... (기존 코드와 동일)
    curr = data.get("current", {})
    daily = data.get("daily", [])
    
    # 1. 현재 날씨
    weather = curr.get("weather", [{}])[0]
    sky = weather_translate.get(weather.get("main"), weather.get("description", "정보없음"))
    temperature = curr.get("temp")
    humidity = curr.get("humidity")
    temp_min = daily[0].get("temp", {}).get("min") if daily else None
    temp_max = daily[0].get("temp", {}).get("max") if daily else None
    weather_id = weather.get("id", 0)
    rain = curr.get("rain")
    snow = curr.get("snow")
    
    if rain or (200 <= weather_id < 700):
        precip_type = "비"
    elif snow:
        precip_type = "눈"
    else:
        precip_type = "강수없음"

    precip_prob = daily[0].get("pop", 0) if daily else 0

    current_weather = {
        "temp_min": str(round(temp_min, 1)) if temp_min is not None else "정보없음",
        "temp_max": str(round(temp_max, 1)) if temp_max is not None else "정보없음",
        "temperature": str(round(temperature, 1)) if temperature is not None else "정보없음",
        "sky": sky,
        "precip_type": precip_type,
        "precip_prob": str(int(round(precip_prob * 100))),
        "humidity": str(humidity) if humidity is not None else "정보없음"
    }

    # 2. 주간 예보 (내일부터 6일간의 예보)
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    weekly_forecast = []
    for day in daily[1:7]: 
        dt = datetime.fromtimestamp(day.get("dt"))
        day_of_week = f"{days_of_week[dt.weekday()]}요일"
        temp_info = day.get("temp", {})
        sky_main = day.get("weather", [{}])[0].get("main", "")
        sky_desc = weather_translate.get(sky_main, sky_main)

        precip_prob_am = int(round(day.get("pop", 0) * 100))
        precip_prob_pm = precip_prob_am
        weekly_forecast.append({
            "date": dt.strftime("%Y-%m-%d"),
            "day_of_week": day_of_week,
            "temp_min": round(temp_info.get("min", 0), 1),
            "temp_max": round(temp_info.get("max", 0), 1),
            "sky_am": sky_desc,
            "sky_pm": sky_desc,
            "precip_prob_am": precip_prob_am,
            "precip_prob_pm": precip_prob_pm
        })

   # 3. 기상특보
    weather_alerts = []
    alerts = data.get("alerts")
    if alerts:
        for alert in alerts:
            weather_alerts.append({
                "content": alert.get("event", "특보 정보 없음")
            })
    else:
        weather_alerts.append({
            "content": "[기상특보] 현재 발효된 특보가 없습니다."
        })

    return {
        "current_weather": current_weather,
        "weekly_forecast": weekly_forecast,
        "weather_alerts": weather_alerts
    }

def process_air_pollution_data(data):
    """
    Air Pollution API 데이터(미세먼지)를 처리하고, 
    한국 환경부 8단계 기준 상태를 추가합니다.
    """
    current_aqi = data.get("list", [{}])[0]
    
    if not current_aqi:
        return {
            "aqi": "정보없음",
            "pm2_5": "정보없음",
            "pm10": "정보없음",
            "pm2_5_status_kr": "정보없음",
            "pm10_status_kr": "정보없음",
        }

    components = current_aqi.get("components", {})
    # OpenWeatherMap AQI (1~5)는 유지하지만, 상태는 한국 기준으로 대체됩니다.
    aqi_value = current_aqi.get("main", {}).get("aqi")
    
    # PM 농도 값 추출 (str로 저장)
    pm2_5_val = str(round(components.get("pm2_5", 0), 2))
    pm10_val = str(round(components.get("pm10", 0), 2))

    return {
        # OpenWeatherMap AQI 값은 유지
        "aqi": str(aqi_value) if aqi_value else "정보없음", 
        
        # 미세먼지 농도 (단위: $\mu g/m^3$)
        "pm2_5": pm2_5_val,
        "pm10": pm10_val,
        
        # 🆕 한국 환경부 8단계 기준 상태 추가
        "pm2_5_status_kr": get_korea_air_status(pm2_5_val, PM25_KOREA_STANDARDS),
        "pm10_status_kr": get_korea_air_status(pm10_val, PM10_KOREA_STANDARDS),
        
        # 기타 오염 물질
        "co": str(round(components.get("co", 0), 2)),
        "no2": str(round(components.get("no2", 0), 2)),
    }


if __name__ == "__main__":
    weather_data = get_weather_data()
    result = process_data(weather_data)
    
    # 시간별 기온 데이터 처리 및 통합
    hourly_result = process_hourly_data(weather_data)
    result["hourly_forecast"] = hourly_result

    # 미세먼지 데이터 가져오기 및 처리
    try:
        pollution_data = get_air_pollution_data()
        air_pollution_result = process_air_pollution_data(pollution_data)
        result["air_pollution"] = air_pollution_result
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching air pollution data: {e}. Check your API key and permissions.")
        result["air_pollution"] = {"error": "미세먼지 데이터를 가져오는 중 오류 발생"}
    except Exception as e:
        print(f"An unexpected error occurred with air pollution data: {e}")
        result["air_pollution"] = {"error": "미세먼지 데이터를 가져오는 중 예기치 않은 오류 발생"}

    print(json.dumps(result, ensure_ascii=False, indent=2))