from flask import Flask, jsonify
from flask_cors import CORS     #1. CORS import
from weather import get_weather_data, process_weather_data  # weather.py에서 함수 import

app = Flask(__name__)   # Flask 웹 어플리케이션 객체 생성
CORS(app)   # 2. 앱에 CORS 적용

# 3. API 라우팅 기능으로 변경
@app.route('/api/weather') # 경로를 '/api/weather'로 변경
def get_weather():
    raw_data = get_weather_data()               # weather.py 함수 호출
    final_data = process_weather_data(raw_data)
    if final_data:
        return jsonify(final_data)
    else:
        return jsonify({"error": "날씨 데이터를 가져올 수 없습니다."}), 500
    
# Flask 개발 서버를 켜서 요청을 받을 준비를 함. (즉 이 파일을 실행하면 서버가 켜짐)
if __name__ == '__main__':
    app.run(debug=True) #개발용 디버깅 (debug=True 시 자동 리로드 & 오류 표시)