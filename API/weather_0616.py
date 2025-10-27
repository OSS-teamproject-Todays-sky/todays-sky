import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

LAT = 35.1796
LON = 129.0756

weather_translate = {
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

def get_weather_data():
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr",
        "exclude": "minutely,hourly"
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()

def process_data(data):
    curr = data.get("current", {})
    daily = data.get("daily", [])

    # 현재 날씨
    weather = curr.get("weather", [{}])[0]
    sky = weather_translate.get(weather.get("main"), weather.get("description", "정보없음"))
    temperature = curr.get("temp")
    humidity = curr.get("humidity")
    temp_min = daily[0].get("temp", {}).get("min") if daily else None
    temp_max = daily[0].get("temp", {}).get("max") if daily else None
    rain = curr.get("rain")
    snow = curr.get("snow")

    if rain or (200 <= weather.get("id", 0) < 700):
        precip_type = "비"
    elif snow:
        precip_type = "눈"
    else:
        precip_type = "강수없음"

    precip_prob = daily[0].get("pop", 0) if daily else 0

    current_weather = {
        "temp_min": str(round(temp_min,1)) if temp_min is not None else "정보없음",
        "temp_max": str(round(temp_max,1)) if temp_max is not None else "정보없음",
        "temperature": str(round(temperature,1)) if temperature is not None else "정보없음",
        "sky": sky,
        "precip_type": precip_type,
        "precip_prob": str(int(round(precip_prob*100))),
        "humidity": str(humidity) if humidity is not None else "정보없음"
    }

    # 주간 예보(7일, 오전/오후 구분은 대략적으로 같은 값으로 세팅)
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    weekly_forecast = []
    for day in daily[:7]:
        dt = datetime.fromtimestamp(day.get("dt"))
        day_of_week = f"{days_of_week[dt.weekday()]}요일"
        temp_info = day.get("temp", {})
        sky_main = day.get("weather", [{}])[0].get("main", "")
        sky_desc = weather_translate.get(sky_main, sky_main)

        precip_prob_am = int(round(day.get("pop", 0)*100))
        precip_prob_pm = precip_prob_am  # 실제 api에서 따로 분리값 없으니 같게 처리
        weekly_forecast.append({
            "date": dt.strftime("%Y-%m-%d"),
            "day_of_week": day_of_week,
            "temp_min": round(temp_info.get("min", 0),1),
            "temp_max": round(temp_info.get("max", 0),1),
            "sky_am": sky_desc,
            "sky_pm": sky_desc,
            "precip_prob_am": precip_prob_am,
            "precip_prob_pm": precip_prob_pm
        })

    # 기상특보
    weather_alerts = []
    alerts = data.get("alerts")
    if alerts:
        for alert in alerts:
            announcement_time = ""
            if alert.get("start"):
                announcement_time = datetime.fromtimestamp(alert.get("start")).strftime("%Y%m%d%H%M")
            weather_alerts.append({
                "content": alert.get("event", "특보 정보 없음"),
                "announcement_time": announcement_time
            })
    else:
        weather_alerts.append({
            "content": "[기상특보] 현재 발효된 특보가 없습니다.",
            "announcement_time": ""
        })

    return {
        "current_weather": current_weather,
        "weekly_forecast": weekly_forecast,
        "weather_alerts": weather_alerts
    }

if __name__ == "__main__":
    data = get_weather_data()
    result = process_data(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
