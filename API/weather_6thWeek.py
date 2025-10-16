import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- [1. 환경변수 및 상수 설정] ---
# .env 파일이 현재 파일과 같은 경로에 있으므로 기본 load_dotenv()로 충분
load_dotenv()
# 환경변수 가져오기
SHORT_TERM_API_KEY = os.getenv("SHORT_TERM_API_KEY")
MID_TERM_API_KEY = os.getenv("MID_TERM_API_KEY")
WEATHER_ALERT_API_KEY = os.getenv("WEATHER_ALERT_API_KEY")

# 환경변수 확인
if not all([SHORT_TERM_API_KEY, MID_TERM_API_KEY, WEATHER_ALERT_API_KEY]):
    raise ValueError("API 키가 .env 파일에 설정되지 않았습니다. .env 파일을 확인해주세요.")

NX, NY = 98, 75
MID_TERM_REG_ID = "11H20201"

# --- [2. 함수 정의] ---

def get_latest_base_time():
    now = datetime.now()
    buffer_time = now - timedelta(minutes=45)
    valid_base_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    base_date, current_hour = buffer_time.strftime('%Y%m%d'), buffer_time.hour
    latest_hour = -1
    for hour in valid_base_hours:
        if current_hour >= hour:
            latest_hour = hour
        else:
            break
    if latest_hour == -1:
        yesterday = buffer_time - timedelta(days=1)
        base_date, latest_hour = yesterday.strftime('%Y%m%d'), 23
    return base_date, f"{latest_hour:02d}00"

def get_short_term_forecast():
    base_date, base_time = get_latest_base_time()
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': SHORT_TERM_API_KEY,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': str(NX),
        'ny': str(NY)
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 단기예보 API 요청 실패: {e}")
        return None

def get_mid_term_forecast():
    now = datetime.now()
    if now.hour < 6:
        tmFc = (now - timedelta(days=1)).strftime('%Y%m%d1800')
    else:
        tmFc = now.strftime('%Y%m%d0600')
    urls = {
        "temp": "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa",
        "land": "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
    }
    params = {
        'serviceKey': MID_TERM_API_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'JSON',
        'regId': MID_TERM_REG_ID,
        'tmFc': tmFc
    }
    try:
        res_temp = requests.get(urls['temp'], params=params, timeout=15)
        res_land = requests.get(urls['land'], params=params, timeout=15)
        res_temp.raise_for_status()
        res_land.raise_for_status()
        return res_temp.json(), res_land.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 중기예보 API 요청 실패: {e}")
        return None, None

def get_weather_alerts():
    url = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnList"
    params = {
        'serviceKey': WEATHER_ALERT_API_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'JSON'
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 기상특보 API 요청 실패: {e}")
        return None

def process_short_term_for_current(res):
    if not res or res['response']['header']['resultCode'] != '00':
        return {}
    items = res['response']['body']['items']['item']
    now, today_str = datetime.now(), datetime.now().strftime('%Y%m%d')
    data = {}
    temps = {item['category']: item['fcstValue'] for item in items if item['fcstDate'] == today_str and item['category'] in ['TMN', 'TMX']}
    data.update({'temp_min': temps.get('TMN'), 'temp_max': temps.get('TMX')})
    if data['temp_min'] is None or data['temp_max'] is None:
        hourly_temps_today = [float(item['fcstValue']) for item in items if item['fcstDate'] == today_str and item['category'] == 'TMP']
        if hourly_temps_today:
            data['temp_min'] = str(min(hourly_temps_today))
            data['temp_max'] = str(max(hourly_temps_today))
    valid_items = [item for item in items if item.get('fcstDate') == today_str]
    if not valid_items:
        return data
    closest_time = min((item['fcstTime'] for item in valid_items), key=lambda t: abs(int(t[:2]) - now.hour))
    for item in valid_items:
        if item['fcstTime'] == closest_time:
            cat, val = item['category'], item['fcstValue']
            if cat == 'TMP': data['temperature'] = val
            elif cat == 'SKY': data['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(val)
            elif cat == 'PTY': data['precip_type'] = {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기'}.get(val)
            elif cat == 'POP': data['precip_prob'] = val
            elif cat == 'REH': data['humidity'] = val
    return data

def process_short_term_for_weekly(res):
    if not res or res['response']['header']['resultCode'] != '00': return []
    items, daily_data = res['response']['body']['items']['item'], {}
    for item in items:
        date = item['fcstDate']
        if date not in daily_data: daily_data[date] = {}
        cat, val, time = item['category'], item['fcstValue'], item['fcstTime']
        if cat == 'TMN': daily_data[date]['temp_min'] = val
        elif cat == 'TMX': daily_data[date]['temp_max'] = val
        elif time == '1200':
            if cat == 'SKY': daily_data[date]['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(val)
            elif cat == 'POP': daily_data[date]['precip_prob'] = val
    weekly_forecast = []
    for i in range(3):
        target_date_dt = datetime.now() + timedelta(days=i)
        target_date_str, day_of_week = target_date_dt.strftime('%Y%m%d'), ['월', '화', '수', '목', '금', '토', '일'][target_date_dt.weekday()]
        if target_date_str in daily_data:
            day_info = daily_data[target_date_str]
            weekly_forecast.append(
                {
                    "date": target_date_dt.strftime('%Y-%m-%d'),
                    "day_of_week": f"{day_of_week}요일",
                    "temp_min": day_info.get('temp_min'),
                    "temp_max": day_info.get('temp_max'),
                    "sky": day_info.get('sky'),
                    "precip_prob": day_info.get('precip_prob')
                }
            )
    return weekly_forecast

def process_mid_term_data(temp_res, land_res):
    if not temp_res or temp_res['response']['header']['resultCode'] != '00' or not land_res or land_res['response']['header']['resultCode'] != '00':
        return []
    temp_item, land_item = temp_res['response']['body']['items']['item'][0], land_res['response']['body']['items']['item'][0]
    weekly_forecast = []
    for day in range(3, 8):
        date, day_of_week = (
            datetime.now() + timedelta(days=day)
        ).strftime('%Y-%m-%d'), ['월', '화', '수', '목', '금', '토', '일'][
            (datetime.now() + timedelta(days=day)).weekday()
        ]
        daily_data = {
            "date": date,
            "day_of_week": f"{day_of_week}요일",
            "temp_min": temp_item.get(f'taMin{day}'),
            "temp_max": temp_item.get(f'taMax{day}'),
            "sky_am": land_item.get(f'wf{day}Am'),
            "sky_pm": land_item.get(f'wf{day}Pm'),
            "precip_prob_am": land_item.get(f'rnSt{day}Am'),
            "precip_prob_pm": land_item.get(f'rnSt{day}Pm')
        }
        weekly_forecast.append(daily_data)
    return weekly_forecast

def process_weather_alerts(res):
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00' or res.get('response', {}).get('body', {}).get('totalCount') == 0:
        return [{"alert": "현재 발효 중인 기상특보가 없습니다."}]
    items = res['response']['body']['items'].get('item', [])
    if not isinstance(items, list):
        items = [items]
    alerts = []
    for item in items:
        if 't1' in item and "부산" in item['t1']:
            alerts.append(
                {
                    "content": item['t1'].replace('o ', ''),
                    "announcement_time": item.get('tmFc', '시간정보 없음')
                }
            )
    if not alerts:
        return [{"alert": "현재 부산광역시에 발효 중인 기상특보가 없습니다."}]
    return alerts

# --- [3. 메인 실행 로직] ---
if __name__ == "__main__":
    IS_DEV_MODE = True # 실제 API를 사용하려면 False로 변경
    final_data = None

    if IS_DEV_MODE:
        print("--- [개발 모드] 더미 데이터를 사용합니다. ---")
        dummy_path = os.path.join(os.path.dirname(__file__), 'dummy_data.json')
        with open(dummy_path, 'r', encoding='utf-8') as f:
            final_data = json.load(f)

    else:
        print("--- [실서버 모드] 실제 API를 호출합니다. ---")
        short_term_raw_data = get_short_term_forecast()
        current_weather_data = process_short_term_for_current(short_term_raw_data)
        weekly_from_short_term = process_short_term_for_weekly(short_term_raw_data)
        mid_temp_raw, mid_land_raw = get_mid_term_forecast()
        weekly_from_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)
        weather_alert_data = process_weather_alerts(get_weather_alerts())
        final_weekly_forecast = weekly_from_short_term + weekly_from_mid_term
        final_data = {
            "current_weather": current_weather_data,
            "weekly_forecast": final_weekly_forecast,
            "weather_alerts": weather_alert_data
        }
    print(json.dumps(final_data, indent=2, ensure_ascii=False))
