import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

# OpenWeather API 모듈 import
from API.weather_0616 import (
    get_weather_data,
    process_data,
    get_air_pollution_data,
    process_air_pollution_data,
    process_hourly_data
)

app = Flask(__name__)
CORS(app)

@app.route('/api/weather')
def get_weather():
    try:
        # 날씨 데이터 가져오기 & 처리
        raw_weather = get_weather_data()
        final_data = process_data(raw_weather)

        # 1시간 단위 데이터 가져오기 & 처리
        hourly_forecast = process_hourly_data(raw_weather)
        final_data["hourly_forecast"] = hourly_forecast

        # 미세먼지 데이터 가져오기 & 처리
        try:
            raw_pollution = get_air_pollution_data()
            air_pollution_data = process_air_pollution_data(raw_pollution)
            final_data["air_pollution"] = air_pollution_data
        except Exception as e:
            print(f"미세먼지 API 오류: {e}")
            final_data["air_pollution"] = {"error": "미세먼지 데이터를 가져오는 중 오류 발생"}

        return jsonify(final_data)

    except Exception as e:
        print(f"서버 내부 오류: {e}")
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500


if __name__ == '__main__':
    print("--- 서버 실행: OpenWeather API ---")
    app.run(debug=True)
