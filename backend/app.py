import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

# 기상청 API 관련 함수들
from API.weather_6thWeek import (
    get_short_term_forecast,
    get_mid_term_forecast,
    get_weather_alerts,
    process_short_term_for_current,
    process_short_term_for_weekly,
    process_mid_term_data,
    process_weather_alerts
)

# OpenWeather API 관련 함수들
from API.weather_0616 import (
    get_weather_data as get_openweather_data,
    process_data as process_openweather_data
)

app = Flask(__name__)
CORS(app)

# -------------------- 설정 --------------------
# 개발 모드 설정 (True -> dummy_data.json 사용, False -> 실제 API 호출)
IS_DEV_MODE = False     # ← True로 바꾸면 개발 모드

# 데이터 소스 선택 ("KMA" -> 기상청 API 사용, "OPENWEATHER" -> OpenWeather API 사용)
SOURCE_MODE = "OPENWEATHER"  # ← "KMA"로 바꾸면 기상청 API 사용
# ---------------------------------------------

@app.route('/api/weather')
def get_weather():
    try:
        if IS_DEV_MODE:
            # --- 개발 모드 (dummy_data.json 사용) ---
            dummy_path = os.path.join(os.path.dirname(__file__), '..', 'API', 'dummy_data.json')
            with open(dummy_path, 'r', encoding='utf-8') as f:
                final_data = json.load(f)

        elif SOURCE_MODE.upper() == "OPENWEATHER":
            # --- OpenWeather API 사용 ---
            raw_data = get_openweather_data()
            final_data = process_openweather_data(raw_data)

        elif SOURCE_MODE.upper() == "KMA":
            # --- 기상청(KMA) API 사용 ---
            short_term_raw = get_short_term_forecast()
            current_weather = process_short_term_for_current(short_term_raw)
            weekly_short_term = process_short_term_for_weekly(short_term_raw)

            mid_temp_raw, mid_land_raw = get_mid_term_forecast()
            weekly_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)

            weather_alert_raw = get_weather_alerts()
            weather_alerts = process_weather_alerts(weather_alert_raw)

            final_data = {
                "current_weather": current_weather,
                "weekly_forecast": weekly_short_term + weekly_mid_term,
                "weather_alerts": weather_alerts
            }

        else:
            return jsonify({"error": f"알 수 없는 SOURCE_MODE 설정: {SOURCE_MODE}"}), 400

        return jsonify(final_data)

    except Exception as e:
        print(f"❌ 서버 처리 중 오류 발생: {e}")
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500


if __name__ == '__main__':
    mode = (
        "개발 모드(dummy data)"
        if IS_DEV_MODE
        else f"실서버 모드 ({'OpenWeather' if SOURCE_MODE == 'OPENWEATHER' else 'KMA'})"
    )
    print(f"--- 서버 실행: {mode} ---")
    app.run(debug=True)
