from flask import Flask, render_template

app = Flask(__name__)   # Flask 웹 어플리케이션 객체 생성

# 라우팅 기능
@app.route('/')
def home():
    return render_template('test.html') # templates/test.html 렌더링(프론트엔드와 연결)

# Flask 개발 서버를 켜서 요청을 받을 준비를 함. (즉 이 파일을 실행하면 서버가 켜짐)
if __name__ == '__main__':
    app.run(debug=True) #개발용 디버깅 (debug=True 시 자동 리로드 & 오류 표시)