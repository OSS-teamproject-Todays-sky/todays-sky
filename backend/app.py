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
# -----------------------------
# [1] 단기 예보
# -----------------------------
@app.route("/api/weather/current")
def get_current_weather():
    res = get_short_term_forecast()
    data = process_short_term_for_current(res)
    return jsonify(data)

# -----------------------------
# [2] 중기 예보
# -----------------------------
@app.route("/api/weather/weekly")
def get_weekly_weather():
    short_res = get_short_term_forecast()
    mid_temp, mid_land = get_mid_term_forecast()

    weekly_short = process_short_term_for_weekly(short_res)
    weekly_mid = process_mid_term_data(mid_temp, mid_land)

    return jsonify(weekly_short + weekly_mid)

# -----------------------------
# [3] 기상특보
# -----------------------------
@app.route("/api/weather/alerts")
def get_alerts():
    alert_text = get_weather_alerts()
    data = process_weather_alerts(alert_text)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
