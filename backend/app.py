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

@app.route('/api/weather')
def get_weather():
    """최종 통합 날씨 데이터를 JSON 형태로 반환하는 Flask 엔드포인트"""
    try:
        # 1️⃣ 단기예보 (현재/3일)
        short_term_raw = get_short_term_forecast()
        current_weather = process_short_term_for_current(short_term_raw)
        weekly_short_term = process_short_term_for_weekly(short_term_raw)

        # 2️⃣ 중기예보 (4~7일)
        mid_temp_raw, mid_land_raw = get_mid_term_forecast()
        weekly_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)

        # 3️⃣ 기상특보
        weather_alert_raw = get_weather_alerts()
        weather_alerts = process_weather_alerts(weather_alert_raw)

        # 4️⃣ 최종 데이터 통합
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
    app.run(debug=True)