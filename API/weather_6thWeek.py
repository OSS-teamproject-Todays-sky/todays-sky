import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
SHORT_TERM_API_KEY = os.getenv("SHORT_TERM_API_KEY")
MID_TERM_API_KEY = os.getenv("MID_TERM_API_KEY")
WEATHER_ALERT_API_KEY = os.getenv("WEATHER_ALERT_API_KEY")

NX, NY = 98, 75
MID_TERM_REG_ID = "11H20101"

def get_latest_base_time():
    """[translate:단기예보 API의 유효한 발표 시간만을 생성하는 가장 안정적인 함수.]"""
    now = datetime.now()
    base_datetime = now - timedelta(minutes=45)
    base_date = base_datetime.strftime('%Y%m%d')
    available_times = [2, 5, 8, 11, 14, 17, 20, 23]
    target_hour = base_datetime.hour
    latest_hour = None
    for t in reversed(available_times):
        if target_hour >= t:
            latest_hour = t
            break
    if latest_hour is None:
        latest_hour = 23
        base_date = (base_datetime - timedelta(days=1)).strftime('%Y%m%d')
    return base_date, f"{latest_hour:02d}00"

def get_previous_base_time(base_date, base_time):
    """주어진 base_time으로부터 3시간 이전의 유효한 base_time을 계산하는 함수."""
    current_dt = datetime.strptime(base_date + base_time, '%Y%m%d%H%M')
    available_times = [2, 5, 8, 11, 14, 17, 20, 23]
    current_hour = current_dt.hour
    try:
        current_index = available_times.index(current_hour)
        if current_index > 0:
            prev_hour = available_times[current_index - 1]
            return base_date, f"{prev_hour:02d}00"
        else: # [translate:현재가 2시이면, 전날 23시로]
            prev_date = (current_dt - timedelta(days=1)).strftime('%Y%m%d')
            return prev_date, "2300"
    except ValueError: # [translate:비정상적인 base_time이 들어온 경우, 안전하게 보정]
        target_hour = current_hour
        for t in reversed(available_times):
            if target_hour > t:
                return base_date, f"{t:02d}00"
        return (current_dt - timedelta(days=1)).strftime('%Y%m%d'), "2300"

def get_short_term_forecast():
    """단기예보 API 호출 (궁극의 4단계 자동 재시도 로직 포함)"""
    base_date, base_time = get_latest_base_time()
    url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-dfs_shrt_grd"
    
    for i in range(4): # [translate:최대 4번 (약 12시간 전 데이터까지) 재시도]
        print(f"INFO: 단기예보 시도 {i+1} -> base_date: {base_date}, base_time: {base_time}")
        params = {'authKey': SHORT_TERM_API_KEY, 'dataType': 'JSON', 'base_date': base_date, 'base_time': base_time, 'nx': str(NX), 'ny': str(NY), 'pageNo': '1', 'numOfRows': '1000'}
        
        try:
            res = requests.get(url, params=params, timeout=30)
            res.raise_for_status()

            if not res.text.strip():
                print(f"경고: 단기예보 API가 빈 응답을 반환했습니다. (base_time: {base_time})")
                base_date, base_time = get_previous_base_time(base_date, base_time)
                continue

            # [translate:성공적으로 JSON 파싱이 되면, 데이터를 반환하고 함수 종료]
            return res.json()

        except json.JSONDecodeError:
            if '# input variable error' in res.text:
                print(f"INFO: 입력 변수 오류 감지. 이전 시간으로 재시도합니다.")
                base_date, base_time = get_previous_base_time(base_date, base_time)
                continue
            else:
                print(f"❌ 단기예보 API JSON 디코딩 오류. 응답 내용:\n'{res.text}'")
                return None # [translate:복구 불가능한 오류로 판단하고 종료]
        except requests.exceptions.RequestException as e:
            print(f"❌ 단기예보 API 요청 실패: {e}")
            return None # [translate:네트워크 오류는 복구 불가능으로 판단하고 종료]

    print("❌ 최종적으로 모든 단기예보 API 재시도에 실패했습니다.")
    return None

def get_mid_term_forecast():
    """중기예보 API 호출 (정상 작동)"""
    now = datetime.now()
    tmFc = (now - timedelta(days=1)).strftime('%Y%m%d1800') if now.hour < 6 else now.strftime('%Y%m%d0600')
    urls = {"temp": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidTa", "land": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidLandFcst"}
    params = {'authKey': MID_TERM_API_KEY, 'dataType': 'JSON', 'regId': MID_TERM_REG_ID, 'tmFc': tmFc, 'pageNo': '1', 'numOfRows': '10'}
    
    try:
        res_temp, res_land = requests.get(urls['temp'], params=params, timeout=30), requests.get(urls['land'], params=params, timeout=30)
        res_temp.raise_for_status(); res_land.raise_for_status()
        return res_temp.json(), res_land.json()
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"❌ 중기예보 API 요청 실패: {e}"); return None, None

def get_weather_alerts():
    """기상특보 API 호출 (텍스트 파싱 방식)"""
    url = "https://apihub.kma.go.kr/api/typ01/url/wrn_now_data_new.php"
    params = {'authKey': WEATHER_ALERT_API_KEY, 'dataType': 'JSON', 'pageNo': '1', 'numOfRows': '10'}
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        return res.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 기상특보 API 요청 실패: {e}")
        return None

# --- [3. 데이터 처리 함수 정의] ---

def process_short_term_for_current(res):
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00': return {}
    items = res['response']['body']['items'].get('item')
    if not items: return {}
    now, today_str, data = datetime.now(), datetime.now().strftime('%Y%m%d'), {}
    temps = {item['category']: item['fcstValue'] for item in items if item['fcstDate'] == today_str and item['category'] in ['TMN', 'TMX']}
    data.update({'temp_min': temps.get('TMN'), 'temp_max': temps.get('TMX')})
    if not all(data.values()):
        hourly_temps_today = [float(item['fcstValue']) for item in items if item['fcstDate'] == today_str and item['category'] == 'TMP']
        if hourly_temps_today: data.update({'temp_min': str(min(hourly_temps_today)), 'temp_max': str(max(hourly_temps_today))})
    valid_items = [item for item in items if item.get('fcstDate') == today_str and item.get('fcstTime')]
    if not valid_items: return data
    closest_item = min(valid_items, key=lambda item: abs(int(item['fcstTime']) - int(now.strftime("%H%M"))))
    for item in valid_items:
        if item['fcstTime'] == closest_item['fcstTime']:
            cat, val = item['category'], item['fcstValue']
            if cat == 'TMP': data['temperature'] = val
            elif cat == 'SKY': data['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(val, '정보 없음')
            elif cat == 'PTY': data['precip_type'] = {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기'}.get(val, '정보 없음')
            elif cat == 'POP': data['precip_prob'] = val
            elif cat == 'REH': data['humidity'] = val
    return data

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
    weekly_forecast, days_of_week = [], {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기'}.get(val, '정보 없음')
    for i in range(3):
        target_date_dt = datetime.now() + timedelta(days=i)
        target_date_str, day_of_week = target_date_dt.strftime('%Y%m%d'), days_of_week[target_date_dt.weekday()]
        if target_date_str in daily_data:
            day_info = daily_data[target_date_str]
            weekly_forecast.append({"date": target_date_dt.strftime('%Y-%m-%d'), "day_of_week": f"{day_of_week}요일", "temp_min": day_info.get('temp_min'), "temp_max": day_info.get('temp_max'), "sky": day_info.get('sky'), "precip_prob": day_info.get('precip_prob')})
    return weekly_forecast

def process_mid_term_data(temp_res, land_res):
    if not temp_res or temp_res.get('response', {}).get('header', {}).get('resultCode') != '00' or not land_res or land_res.get('response', {}).get('header', {}).get('resultCode') != '00': return []
    temp_item, land_item = temp_res['response']['body']['items']['item'][0], land_res['response']['body']['items']['item'][0]
    weekly_forecast, days_of_week = [], ['월','화','수','목','금','토','일']
    for day in range(3, 8):
        date_dt = datetime.now() + timedelta(days=day)
        sky_am, sky_pm = land_item.get(f'wf{day}Am') or "흐림", land_item.get(f'wf{day}Pm') or "흐림"
        precip_prob_am, precip_prob_pm = land_item.get(f'rnSt{day}Am', 0), land_item.get(f'rnSt{day}Pm', 0)
        daily_data = {"date": date_dt.strftime('%Y-%m-%d'), "day_of_week": f"{days_of_week[date_dt.weekday()]}요일", "temp_min": temp_item.get(f'taMin{day}'), "temp_max": temp_item.get(f'taMax{day}'), "sky_am": sky_am, "sky_pm": sky_pm, "precip_prob_am": precip_prob_am, "precip_prob_pm": precip_prob_pm}
        weekly_forecast.append(daily_data)
    return weekly_forecast

def process_weather_alerts(text_data):
    if not text_data or not text_data.strip() or '#START7777' not in text_data:
        return [{"alert": "현재 발효 중인 기상특보가 없습니다."}]
    alerts = []
    lines = text_data.split('\n')
    for line in lines:
        if line.startswith('#') or not line.strip(): continue
        if "[translate:부산]" in line:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) > 8:
                area_name, alert_type, alert_level = parts[3], parts[6], parts[8]
                content = f"{area_name} {alert_type} {alert_level}"
                alerts.append({"content": content, "announcement_time": parts[4]})
    if not alerts: return [{"alert": "현재 부산광역시에 발효 중인 기상특보가 없습니다."}]
    return alerts

# --- [4. 메인 실행 로직] ---
if __name__ == "__main__":
    print("---[실서버 모드] 실제 API를 호출합니다. ---")
    short_term_raw_data = get_short_term_forecast()
    mid_temp_raw, mid_land_raw = get_mid_term_forecast()
    weather_alert_raw_data = get_weather_alerts()
    
    current_weather_data = process_short_term_for_current(short_term_raw_data)
    weekly_from_short_term = process_short_term_for_weekly(short_term_raw_data)
    weekly_from_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)
    weather_alert_data = process_weather_alerts(weather_alert_raw_data)
    
    final_weekly_forecast = weekly_from_short_term + weekly_from_mid_term
    final_data = {"current_weather": current_weather_data, "weekly_forecast": final_weekly_forecast, "weather_alerts": weather_alert_data}
        
    print(json.dumps(final_data, indent=2, ensure_ascii=False))
