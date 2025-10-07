import requests
import json
from datetime import datetime, timedelta

API_KEY = "1o00nZt0TaGNNJ2bdH2hZw"

# 부산광역시 남구 대연동의 격자 좌표
NX = 98
NY = 75

def get_latest_base_time():
    """API의 가장 최신 데이터 발표 시간을 더 정교하게 계산하는 함수"""
    now = datetime.now()
    
    # 데이터 발표는 2시, 5시, 8시... 이며, 준비 시간은 약 15분 소요됨
    # 만약 현재 시간이 새벽 2시 15분 이전이라면, 전날 23시 데이터를 사용
    if now.hour < 2 or (now.hour == 2 and now.minute < 30):
        target_time = now - timedelta(days=1)
        base_date_str = target_time.strftime('%Y%m%d')
        base_time_str = "2300"
    else:
        # 그 외의 시간에는 가장 가까운 과거의 발표 시간을 찾음
        # (예: 9시 30분 -> 8시 데이터 / 8시 5분 -> 5시 데이터)
        target_time = now - timedelta(minutes=30) # 처리 시간 15분을 빼고 계산
        base_hour = (target_time.hour // 3) * 3
        base_date_str = target_time.strftime('%Y%m%d')
        if base_hour < 10:
            base_time_str = f"0{base_hour}00"
        else:
            base_time_str = f"{base_hour}00"
            
    return base_date_str, base_time_str

def get_weather_data():
    """기상청 단기예보 API를 호출하는 함수"""
    base_date, base_time = get_latest_base_time()
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': API_KEY, 'pageNo': '1', 'numOfRows': '1000',
        'dataType': 'JSON', 'base_date': base_date, 'base_time': base_time,
        'nx': str(NX), 'ny': str(NY)
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return None

def process_weather_data(api_response):
    """API 응답 데이터를 가공하여 최종 형식으로 만드는 함수"""
    if not api_response or api_response['response']['header']['resultCode'] != '00':
        print("API 응답에 문제가 있어 데이터를 처리할 수 없습니다.")
        # 디버깅을 위해 어떤 에러가 왔는지 출력
        if api_response:
             print(f"에러 코드: {api_response['response']['header']['resultCode']}, 메시지: {api_response['response']['header']['resultMsg']}")
        return None

    items = api_response['response']['body']['items']['item']
    now = datetime.now()
    today_str = now.strftime('%Y%m%d')
    processed_data = {}
    temp_min, temp_max = None, None

    for item in items:
        category, value, fcst_date = item['category'], item['fcstValue'], item['fcstDate']
        if fcst_date == today_str:
            if category == 'TMN': temp_min = value
            elif category == 'TMX': temp_max = value

    closest_fcst_time = min((item['fcstTime'] for item in items), 
                            key=lambda t: abs(int(t[:2]) - now.hour))

    for item in items:
        if item['fcstTime'] == closest_fcst_time:
            category, value = item['category'], item['fcstValue']
            if category == 'SKY':
                processed_data['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(value, '정보없음')
            elif category == 'PTY':
                processed_data['precip_type'] = {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기'}.get(value, '정보없음')
            elif category == 'TMP': processed_data['temperature'] = value
            elif category == 'POP': processed_data['precip_prob'] = value
            elif category == 'REH': processed_data['humidity'] = value

    if temp_min: processed_data['temp_min'] = temp_min
    if temp_max: processed_data['temp_max'] = temp_max
    return processed_data

if __name__ == "__main__":
    raw_data = get_weather_data()
    if raw_data:
        final_data = process_weather_data(raw_data)
        if final_data:
            print("--- [최종 가공 데이터 (Final Data)] ---")
            print(json.dumps(final_data, indent=2, ensure_ascii=False))