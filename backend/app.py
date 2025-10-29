import os
import json
from flask import Flask, jsonify
from flask_cors import CORS     #1. CORS import
# weather_6thWEEK.py의 주요 함수 import
from API.weather_6thWeek import (
    get_short_term_forecast,
    get_mid_term_forecast,
    get_weather_alerts,
    process_short_term_for_current,
    process_short_term_for_weekly,
    process_mid_term_data,
    process_weather_alerts
)

app = Flask(__name__)
CORS(app)  # CORS 허용

# 개발 모드 설정 (True -> dummy_data.json 사용, False -> 실제 API 호출)
IS_DEV_MODE = False

@app.route('/api/weather')
def get_weather():
    try:
        if IS_DEV_MODE:
            # --- 개발 모드 ---
            # dummy_data.json 위치가 API 폴더 안이므로 경로 수정
            dummy_path = os.path.join(os.path.dirname(__file__), '..', 'API', 'dummy_data.json')
            with open(dummy_path, 'r', encoding='utf-8') as f:
                final_data = json.load(f)
        else:
            # --- 실서버 모드 ---
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

        return jsonify(final_data)

    except Exception as e:
        print(f"❌ 서버 처리 중 오류 발생: {e}")
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500


if __name__ == '__main__':
    mode = "개발 모드(dummy data)" if IS_DEV_MODE else "실서버 모드(API 호출)"
    print(f"--- 서버 실행: {mode} ---")
    app.run(debug=True)