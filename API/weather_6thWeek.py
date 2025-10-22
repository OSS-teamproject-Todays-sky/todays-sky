import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

load_dotenv()
SHORT_TERM_API_KEY = os.getenv("SHORT_TERM_API_KEY")
MID_TERM_API_KEY = os.getenv("MID_TERM_API_KEY")
WEATHER_ALERT_API_KEY = os.getenv("WEATHER_ALERT_API_KEY")

NX, NY = 98, 75
MID_TERM_REG_ID = "11H20101"

def get_latest_base_time():
    now = datetime.now()
    allowed_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    base_date = now.strftime('%Y%m%d')
    for hour in reversed(allowed_hours):
        if now >= datetime(now.year, now.month, now.day, hour, 10):
            return base_date, f"{hour:02d}00"
    return (now - timedelta(days=1)).strftime('%Y%m%d'), "2300"

def get_previous_base_time(base_date, base_time):
    allowed_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    dt = datetime.strptime(base_date + base_time, '%Y%m%d%H%M')
    idx = allowed_hours.index(dt.hour) if dt.hour in allowed_hours else -1
    if idx > 0:
        return base_date, f"{allowed_hours[idx-1]:02d}00"
    return (dt - timedelta(days=1)).strftime('%Y%m%d'), "2300"

def get_short_term_forecast():
    base_date, base_time = get_latest_base_time()
    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'authKey': SHORT_TERM_API_KEY,
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': str(NX),
        'ny': str(NY),
        'pageNo': '1',
        'numOfRows': '1000'
    }
    for _ in range(4):
        try:
            res = requests.get(url, params=params, timeout=(10, 60))
            res.raise_for_status()
            data = res.json()
            if data.get('response', {}).get('header', {}).get('resultCode') == '00':
                return data
        except Exception as e:
            print(f"단기예보 API 오류: {e}")
        base_date, base_time = get_previous_base_time(base_date, base_time)
        params['base_date'], params['base_time'] = base_date, base_time
        time.sleep(5)
    print("❌ 단기예보 API 실패")
    return None

def process_short_term_for_current(res):
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00': return {}
    items = res['response']['body']['items'].get('item')
    now = datetime.now()
    today_str = now.strftime('%Y%m%d')
    now_hm = int(now.strftime('%H%M'))
    element = {}
    for cat in ['TMP', 'SKY', 'PTY', 'POP', 'REH', 'TMN', 'TMX']:
        cat_items = [x for x in items if x['fcstDate'] == today_str and x['category'] == cat]
        if cat_items:
            closest_item = min(cat_items, key=lambda x: abs(int(x['fcstTime']) - now_hm))
            element[cat] = closest_item['fcstValue']
    sky_map = {'1': '맑음', '3': '구름많음', '4': '흐림'}
    precip_map = {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기'}
    return {
        "temp_min": element.get("TMN"),
        "temp_max": element.get("TMX"),
        "temperature": element.get("TMP"),
        "sky": sky_map.get(element.get("SKY", ""), "정보없음"),
        "precip_type": precip_map.get(element.get("PTY", ""), "정보없음"),
        "precip_prob": element.get("POP"),
        "humidity": element.get("REH")
    }

def process_short_term_for_weekly(res):
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00': return []
    items = res['response']['body']['items'].get('item')
    if not items: return []
    daily_data = {}
    for item in items:
        date, cat, val, time = item['fcstDate'], item['category'], item['fcstValue'], item['fcstTime']
        if date not in daily_data: daily_data[date] = {}
        if cat == 'TMN': daily_data[date]['temp_min'] = val
        elif cat == 'TMX': daily_data[date]['temp_max'] = val
        elif time == '1200':
            if cat == 'SKY': daily_data[date]['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(val, '정보 없음')
            elif cat == 'POP': daily_data[date]['precip_prob'] = val
    weekly_forecast = []
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    for i in range(3):
        target_date_dt = datetime.now() + timedelta(days=i)
        target_date_str = target_date_dt.strftime('%Y%m%d')
        day_of_week = days_of_week[target_date_dt.weekday()]
        if target_date_str in daily_data:
            day_info = daily_data[target_date_str]
            weekly_forecast.append({
                "date": target_date_dt.strftime('%Y-%m-%d'),
                "day_of_week": f"{day_of_week}요일",
                "temp_min": day_info.get('temp_min'),
                "temp_max": day_info.get('temp_max'),
                "sky": day_info.get('sky'),
                "precip_prob": day_info.get('precip_prob')
            })
    return weekly_forecast

def get_mid_term_forecast():
    now = datetime.now()
    tmFc = (now - timedelta(days=1)).strftime('%Y%m%d1800') if now.hour < 6 else now.strftime('%Y%m%d0600')
    urls = {"temp": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidTa",
            "land": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidLandFcst"}
    params = {'authKey': MID_TERM_API_KEY, 'dataType': 'JSON', 'regId': MID_TERM_REG_ID,
              'tmFc': tmFc, 'pageNo': '1', 'numOfRows': '10'}
    try:
        res_temp = requests.get(urls['temp'], params=params, timeout=30)
        res_land = requests.get(urls['land'], params=params, timeout=30)
        res_temp.raise_for_status()
        res_land.raise_for_status()
        return res_temp.json(), res_land.json()
    except Exception as e:
        print(f"❌ 중기예보 API 오류: {e}")
        return None, None

def process_mid_term_data(temp_res, land_res):
    if not temp_res or temp_res.get('response', {}).get('header', {}).get('resultCode') != '00': return []
    if not land_res or land_res.get('response', {}).get('header', {}).get('resultCode') != '00': return []
    temp_item, land_item = temp_res['response']['body']['items']['item'][0], land_res['response']['body']['items']['item'][0]
    weekly_forecast = []
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    for day in range(3, 8):
        date_dt = datetime.now() + timedelta(days=day)
        sky_am = land_item.get(f'wf{day}Am') or "흐림"
        sky_pm = land_item.get(f'wf{day}Pm') or "흐림"
        precip_prob_am = land_item.get(f'rnSt{day}Am', 0)
        precip_prob_pm = land_item.get(f'rnSt{day}Pm', 0)
        weekly_forecast.append({
            "date": date_dt.strftime('%Y-%m-%d'),
            "day_of_week": f"{days_of_week[date_dt.weekday()]}요일",
            "temp_min": temp_item.get(f'taMin{day}'),
            "temp_max": temp_item.get(f'taMax{day}'),
            "sky_am": sky_am,
            "sky_pm": sky_pm,
            "precip_prob_am": precip_prob_am,
            "precip_prob_pm": precip_prob_pm
        })
    return weekly_forecast

def get_weather_alerts():
    url = "https://apihub.kma.go.kr/api/typ01/url/wrn_now_data_new.php"
    params = {'authKey': WEATHER_ALERT_API_KEY, 'dataType': 'JSON', 'pageNo': '1', 'numOfRows': '10'}
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"❌ 기상특보 API 오류: {e}")
        return None

def process_weather_alerts(text_data):
    if not text_data or not text_data.strip() or '#START7777' not in text_data:
        return [{"alert": "현재 발효 중인 기상특보가 없습니다."}]
    alerts = []
    lines = text_data.split('\n')
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        if "[translate:부산]" in line:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) > 8:
                area_name, alert_type, alert_level = parts[3], parts[6], parts[8]
                content = f"{area_name} {alert_type} {alert_level}"
                alerts.append({"content": content, "announcement_time": parts[4]})
    if not alerts:
        return [{"alert": "현재 부산광역시에 발효 중인 기상특보가 없습니다."}]
    return alerts

if __name__ == "__main__":
    IS_DEV_MODE = False  # 실제 API를 사용하려면 False로 변경
    final_data = None

    if IS_DEV_MODE:
        print("--- [개발 모드] 더미 데이터를 사용합니다. ---")
        dummy_path = os.path.join(os.path.dirname(__file__), 'dummy_data.json')
        with open(dummy_path, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
    else:
        print("---[실서버 모드] 실제 API 호출---")
        short_term_raw_data = get_short_term_forecast()
        mid_temp_raw, mid_land_raw = get_mid_term_forecast()
        weather_alert_raw_data = get_weather_alerts()

        current_weather_data = process_short_term_for_current(short_term_raw_data)
        weekly_from_short_term = process_short_term_for_weekly(short_term_raw_data)
        weekly_from_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)
        weather_alert_data = process_weather_alerts(weather_alert_raw_data)

        final_weekly_forecast = weekly_from_short_term + weekly_from_mid_term
        final_data = {
            "current_weather": current_weather_data,
            "weekly_forecast": final_weekly_forecast,
            "weather_alerts": weather_alert_data
        }

    print(json.dumps(final_data, indent=2, ensure_ascii=False))
