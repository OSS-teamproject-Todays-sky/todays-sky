from flask import Flask, jsonify
from flask_cors import CORS #1. CORS import

app = Flask(__name__)   # Flask 웹 어플리케이션 객체 생성
CORS(app) # 2. 앱에 CORS 적용

# 3. API 라우팅 기능으로 변경
@app.route('/api/weather') # 경로를 '/api/weather'로 변경
def get_weather():
    # TODO: 여기에 실제 날씨 데이터를 가져오는 로직 구현
    # 지금은 테스트를 위해 임시 데이터(딕셔너리) 를 반환합니다.
    dummy_data = {
        "current" : {
            "city": "Busan",
            "temp": 23.5,
            "description": "맑음",
            "icon": "01d"
        },
        "hourly": [
            { "time": "오전 9시", "icon": "01d", "temp": 18 },
            { "time": "오후 12시", "icon": "02d", "temp": 24 },
            { "time": "오후 3시", "icon": "01d", "temp": 25 },
        ]
    }
    return jsonify(dummy_data) # 4. JSON 형식으로 데이터 응답
    
# Flask 개발 서버를 켜서 요청을 받을 준비를 함. (즉 이 파일을 실행하면 서버가 켜짐)
if __name__ == '__main__':
    app.run(debug=True) #개발용 디버깅 (debug=True 시 자동 리로드 & 오류 표시)