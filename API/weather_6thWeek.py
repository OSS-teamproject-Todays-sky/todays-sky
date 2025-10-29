import os
import requests
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, Any, Tuple, List, Optional

# .env 파일에서 환경 변수 로드
load_dotenv()

# --- API KEY 및 상수 설정 ---
SHORT_TERM_API_KEY = os.getenv("SHORT_TERM_API_KEY")
MID_TERM_API_KEY = os.getenv("MID_TERM_API_KEY")
WEATHER_ALERT_API_KEY = os.getenv("WEATHER_ALERT_API_KEY")

# 부산광역시 기준 (강서구/사상구 근방 격자, 중기예보 지역)
NX, NY = 98, 75
MID_TERM_REG_ID = "11H20101"  # 부산 지역 코드

# API KEY 누락 검사
if not all([SHORT_TERM_API_KEY, MID_TERM_API_KEY, WEATHER_ALERT_API_KEY]):
    print("❌ 환경 변수 (API Key) 설정이 누락되었습니다. .env 파일을 확인해주세요.")
    # 실제 운영 환경이라면 여기서 시스템을 종료하거나 API 호출을 스킵해야 합니다.
    # 현재는 오류가 발생해도 진행되도록 둡니다.

def get_latest_base_time() -> Tuple[str, str]:
    """
    단기예보 API 호출을 위한 가장 최근의 유효한 발표 시간 (Base Time)을 계산합니다.
    발표 시간: 02, 05, 08, 11, 14, 17, 20, 23시 (매 시각 10분에 생성)
    """
    now = datetime.now()
    allowed_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    base_date = now.strftime('%Y%m%d')

    for hour in reversed(allowed_hours):
        # 현재 시각이 (발표 시각 + 10분) 보다 같거나 늦을 경우 해당 시각을 Base Time으로 사용
        if now >= datetime(now.year, now.month, now.day, hour, 10):
            return base_date, f"{hour:02d}00"

    # 해당 날짜에 유효한 시간이 없을 경우 (예: 00:00~02:09 사이)
    # 전날의 마지막 Base Time (23:00)을 사용합니다.
    return (now - timedelta(days=1)).strftime('%Y%m%d'), "2300"

def get_previous_base_time(base_date: str, base_time: str) -> Tuple[str, str]:
    """
    주어진 Base Time 이전의 유효한 Base Time을 반환합니다. (API 재시도용)
    """
    allowed_hours = [2, 5, 8, 11, 14, 17, 20, 23]
    try:
        dt = datetime.strptime(base_date + base_time, '%Y%m%d%H%M')
    except ValueError:
        return base_date, "0000" # 유효하지 않은 포맷일 경우 재시도 방지

    idx = allowed_hours.index(dt.hour) if dt.hour in allowed_hours else -1

    # 이전 유효한 Base Time
    if idx > 0:
        return base_date, f"{allowed_hours[idx-1]:02d}00"

    # 자정을 넘어가야 하는 경우
    return (dt - timedelta(days=1)).strftime('%Y%m%d'), "2300"

def get_short_term_forecast() -> Optional[Dict[str, Any]]:
    """
    단기 예보 API를 호출하고 응답을 반환합니다.
    최대 4번까지 Base Time을 변경하며 재시도합니다.
    """
    if not SHORT_TERM_API_KEY:
        print("❌ 단기예보 API 키가 없습니다.")
        return None

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

    for attempt in range(4):
        print(f"  [단기예보 시도 {attempt + 1}] Base Time: {params['base_date']}{params['base_time']}")
        try:
            # API 호출
            res = requests.get(url, params=params, timeout=30)
            res.raise_for_status() # 4xx, 5xx 에러 발생 시 예외 처리

            data = res.json()
            # KMA API의 ResultCode '00'이 성공을 의미
            result_code = data.get('response', {}).get('header', {}).get('resultCode')

            if result_code == '00':
                return data
            elif result_code == '03':
                print(f"  API 결과 코드 03: BASE_TIME 오류. 이전 Base Time으로 재시도합니다.")
            else:
                print(f"  API 결과 코드 {result_code}: 알 수 없는 오류입니다. 재시도합니다.")

        except requests.exceptions.Timeout:
            print("  API 요청 시간 초과 (Timeout).")
        except requests.exceptions.RequestException as e:
            print(f"  API 요청 오류: {e}")
        except json.JSONDecodeError:
            print("  API 응답 JSON 디코딩 오류.")
        except Exception as e:
            print(f"  예상치 못한 오류: {e}")

        # Base Time 변경 및 대기
        base_date, base_time = get_previous_base_time(base_date, base_time)
        params['base_date'], params['base_time'] = base_date, base_time
        time.sleep(3)

    print("❌ 단기예보 API 최대 재시도 횟수 초과로 실패.")
    return None

def process_short_term_for_current(res: Optional[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    """
    단기 예보 응답에서 현재 시점의 날씨 정보를 추출합니다.
    """
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00':
        return {"error": "단기예보 데이터 없음"}

    items = res['response']['body']['items'].get('item', [])
    now = datetime.now()
    today_str = now.strftime('%Y%m%d')
    # 현재 시각을 정수형으로 변환하여 가장 가까운 예보 시각을 찾습니다.
    now_hm = int(now.strftime('%H%M'))

    element: Dict[str, Optional[str]] = {}
    
    # TMN, TMX는 예보 시각에 관계없이 오늘 일자 데이터 중 첫 번째 항목을 사용하면 됩니다.
    # TMP, SKY, PTY, POP, REH는 현재 시각과 가장 가까운 예보 시각의 데이터를 사용합니다.
    target_categories = ['TMP', 'SKY', 'PTY', 'POP', 'REH', 'TMN', 'TMX']

    for cat in target_categories:
        cat_items = [x for x in items if x['fcstDate'] == today_str and x['category'] == cat]
        
        if not cat_items:
            element[cat] = None
            continue
            
        if cat in ['TMN', 'TMX']:
            # 당일의 최저/최고 기온은 Base Time이 변경되지 않는 한 일정하므로, 첫 번째 값 사용
            element[cat] = cat_items[0]['fcstValue']
        else:
            # 현재 시각에 가장 가까운 예보 시각의 데이터를 찾음
            closest_item = min(
                cat_items, 
                key=lambda x: abs(int(x['fcstTime']) - now_hm)
            )
            element[cat] = closest_item['fcstValue']

    sky_map = {'1': '맑음', '3': '구름많음', '4': '흐림'}
    # PTY (강수 형태): 0: 없음, 1: 비, 2: 비/눈, 3: 눈, 4: 소나기, 5: 빗방울, 6: 빗방울/눈날림, 7: 눈날림
    precip_map = {'0': '강수없음', '1': '비', '2': '비/눈', '3': '눈', '4': '소나기', 
                  '5': '빗방울', '6': '빗방울/눈날림', '7': '눈날림'}

    return {
        "temp_min": element.get("TMN"),
        "temp_max": element.get("TMX"),
        "temperature": element.get("TMP"),
        "sky": sky_map.get(element.get("SKY"), "정보없음"),
        "precip_type": precip_map.get(element.get("PTY"), "정보없음"),
        "precip_prob": element.get("POP"),
        "humidity": element.get("REH")
    }

def process_short_term_for_weekly(res: Optional[Dict[str, Any]]) -> List[Dict[str, Optional[str]]]:
    """
    단기 예보 응답에서 D+0, D+1, D+2 일간의 일별 최고/최저 기온 및 하늘 상태를 추출합니다.
    """
    if not res or res.get('response', {}).get('header', {}).get('resultCode') != '00':
        return []
    
    items = res['response']['body']['items'].get('item', [])
    if not items: return []
    
    daily_data: Dict[str, Dict[str, Optional[str]]] = {}
    
    for item in items:
        date_str, cat, val, time_str = item['fcstDate'], item['category'], item['fcstValue'], item['fcstTime']
        if date_str not in daily_data: daily_data[date_str] = {}

        if cat == 'TMN': 
            daily_data[date_str]['temp_min'] = val
        elif cat == 'TMX': 
            daily_data[date_str]['temp_max'] = val
        elif time_str == '1200': # 12시 기준으로 SKY/POP 데이터 대표값 사용
            if cat == 'SKY': 
                daily_data[date_str]['sky'] = {'1': '맑음', '3': '구름많음', '4': '흐림'}.get(val, '정보 없음')
            elif cat == 'POP': 
                daily_data[date_str]['precip_prob'] = val

    weekly_forecast: List[Dict[str, Optional[str]]] = []
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    
    # D+0, D+1, D+2 (오늘, 내일, 모레)
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

def get_mid_term_forecast() -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    중기 예보 (기온 및 육상) API를 호출하고 응답을 반환합니다.
    """
    if not MID_TERM_API_KEY:
        print("❌ 중기예보 API 키가 없습니다.")
        return None, None

    now = datetime.now()
    # 발표 시각: 오전(06시), 오후(18시). 현재 시간이 06시 이전이면 전날 18시 자료 사용.
    tmFc = (now - timedelta(days=1)).strftime('%Y%m%d1800') if now.hour < 6 else now.strftime('%Y%m%d0600')
    
    urls = {
        "temp": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidTa",
        "land": "https://apihub.kma.go.kr/api/typ02/openApi/MidFcstInfoService/getMidLandFcst"
    }
    params = {
        'authKey': MID_TERM_API_KEY,
        'dataType': 'JSON',
        'regId': MID_TERM_REG_ID,
        'tmFc': tmFc,
        'pageNo': '1',
        'numOfRows': '10'
    }

    temp_res, land_res = None, None
    print(f"[중기예보 시도] 발표 시간: {tmFc}")

    try:
        res_temp = requests.get(urls['temp'], params=params, timeout=30)
        res_temp.raise_for_status()
        temp_res = res_temp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 중기예보 (기온) API 요청 오류: {e}")

    try:
        res_land = requests.get(urls['land'], params=params, timeout=30)
        res_land.raise_for_status()
        land_res = res_land.json()
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 중기예보 (육상) API 요청 오류: {e}")

    # 두 응답 모두 성공 코드 '00'이 아닐 경우 None 반환
    temp_code = temp_res.get('response', {}).get('header', {}).get('resultCode') if temp_res else None
    land_code = land_res.get('response', {}).get('header', {}).get('resultCode') if land_res else None
    
    if temp_code != '00' or land_code != '00':
        print(f"❌ 중기예보 API 응답 코드 오류: 기온={temp_code}, 육상={land_code}")
        return None, None

    return temp_res, land_res

def process_mid_term_data(temp_res: Optional[Dict[str, Any]], land_res: Optional[Dict[str, Any]]) -> List[Dict[str, Optional[Any]]]:
    """
    중기 예보 (D+3 ~ D+7) 응답에서 주간 예보 데이터를 추출합니다.
    """
    # 응답 유효성 검사 (get_mid_term_forecast에서 이미 했지만, 방어적 코드 작성)
    if not temp_res or not land_res:
        return []

    temp_items = temp_res['response']['body']['items'].get('item', [])
    land_items = land_res['response']['body']['items'].get('item', [])
    
    if not temp_items or not land_items:
        return []
        
    temp_item, land_item = temp_items[0], land_items[0]
    weekly_forecast: List[Dict[str, Optional[Any]]] = []
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    
    # 중기 예보는 D+3일부터 D+7일까지 5일치 정보를 제공합니다.
    for day in range(3, 8):
        date_dt = datetime.now() + timedelta(days=day)
        
        # 중기예보에서는 "맑음, 구름많음, 흐림, 비, 비/눈, 눈" 등의 문자열로 제공됨
        sky_am = land_item.get(f'wf{day}Am')
        sky_pm = land_item.get(f'wf{day}Pm')
        
        # rnStXAm/Pm: 강수확률 (%)
        precip_prob_am = land_item.get(f'rnSt{day}Am')
        precip_prob_pm = land_item.get(f'rnSt{day}Pm')

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

def get_weather_alerts() -> Optional[str]:
    """
    기상특보 API를 호출하고 텍스트 응답을 반환합니다.
    (KMA 특보 API는 JSON이 아닌 텍스트/URL 형식으로 제공되므로 응답이 string입니다.)
    """
    if not WEATHER_ALERT_API_KEY:
        print("❌ 기상특보 API 키가 없습니다.")
        return None

    url = "https://apihub.kma.go.kr/api/typ01/url/wrn_now_data_new.php"
    params = {'authKey': WEATHER_ALERT_API_KEY, 'dataType': 'JSON', 'pageNo': '1', 'numOfRows': '10'}

    print("[기상특보 시도]")
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        # KMA 특보 API는 text/plain 응답을 반환할 가능성이 높으므로 .text를 사용
        return res.text
    except requests.exceptions.RequestException as e:
        print(f"❌ 기상특보 API 요청 오류: {e}")
        return None

def process_weather_alerts(text_data: Optional[str]) -> List[Dict[str, str]]:
    """
    기상특보 텍스트 응답을 파싱하여 부산 지역의 특보 정보를 추출합니다.
    KMA 특보 데이터는 비표준 포맷이므로 파싱 로직에 유의해야 합니다.
    """
    if not text_data or '#START7777' not in text_data:
        return [{"alert": "현재 발효 중인 기상특보가 없습니다."}]

    alerts: List[Dict[str, str]] = []
    lines = text_data.split('\n')
    
    # 실제 데이터 라인 필터링 및 부산 지역 특보 추출
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 기상 특보 데이터는 쉼표로 구분되며, 지역명, 특보 종류, 레벨 등의 정보가 포함됨
        # 예시: ... ,202401010000, 해제, , , [translate:부산], , 호우주의보, , 해제 ...
        parts = [p.strip() for p in line.split(',')]
        
        # 최소한의 데이터 유효성 검사 (KMA 포맷이 변경되면 이 인덱스도 변경될 수 있음)
        if len(parts) > 8:
            # parts[3] 또는 parts[5] 등 지역명이 들어갈만한 인덱스를 확인해야 하나,
            # 원본 코드에서 [translate:부산]을 기준으로 필터링하고 있으므로 이를 유지하며 강화
            
            # 부산 지역 데이터인지 확인 (API 응답 포맷에 따라 인덱스 3, 5, 8이 달라질 수 있음)
            is_busan_alert = False
            try:
                # 'translate:부산'이 포함된 라인만 필터링하는 원본 로직 유지
                if "[translate:부산]" in line:
                    is_busan_alert = True
                else:
                    # 또는 특보 데이터 포맷에 따라 지역명이 들어가는 인덱스(예: parts[3] 또는 parts[5])를 검사
                    area_name_index = 3 # KMA 특보 포맷에 따라 달라질 수 있음
                    if len(parts) > area_name_index and "부산" in parts[area_name_index]:
                         is_busan_alert = True
            except IndexError:
                continue

            if is_busan_alert:
                # 안전한 인덱스를 사용하여 특보 정보 추출
                # parts[4]: 발표 시각, parts[6]: 특보 종류, parts[8]: 특보 레벨
                try:
                    announcement_time_raw = parts[4]
                    alert_type = parts[6]
                    alert_level = parts[8]
                    area_name = "부산"
                    
                    # 특보 발령/해제 상태를 확인
                    status = parts[7] # KMA 포맷에 따라 '발효', '해제' 등
                    
                    content = f"{area_name} {alert_type} {alert_level} ({status})"
                    
                    alerts.append({
                        "content": content, 
                        "announcement_time": announcement_time_raw
                    })
                except IndexError:
                    print("  특보 데이터 파싱 중 인덱스 오류 발생.")
                    continue
                    
    if not alerts:
        return [{"alert": "현재 부산광역시에 발효 중이거나 해제된 특보가 없습니다."}]
        
    return alerts

# --- 메인 실행 블록 ---
if __name__ == "__main__":
    IS_DEV_MODE = False  # 실제 API를 사용하려면 False로 변경
    final_data: Dict[str, Any] = {}

    if IS_DEV_MODE:
        print("--- [개발 모드] 더미 데이터를 사용합니다. ---")
        dummy_path = os.path.join(os.path.dirname(__file__), 'dummy_data.json')
        try:
            with open(dummy_path, 'r', encoding='utf-8') as f:
                final_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ 더미 데이터 파일 {dummy_path}을 찾을 수 없습니다.")
            final_data = {"error": "더미 데이터 로드 실패"}
    else:
        print("--- [실서버 모드] 실제 API 호출 시작 ---")

        # 1. 단기 예보 (현재 및 D+0 ~ D+2)
        short_term_raw_data = get_short_term_forecast()
        current_weather_data = process_short_term_for_current(short_term_raw_data)
        weekly_from_short_term = process_short_term_for_weekly(short_term_raw_data)
        
        # 2. 중기 예보 (D+3 ~ D+7)
        mid_temp_raw, mid_land_raw = get_mid_term_forecast()
        weekly_from_mid_term = process_mid_term_data(mid_temp_raw, mid_land_raw)
        
        # 3. 기상 특보
        weather_alert_raw_data = get_weather_alerts()
        weather_alert_data = process_weather_alerts(weather_alert_raw_data)

        # 최종 데이터 결합
        final_weekly_forecast = weekly_from_short_term + weekly_from_mid_term
        final_data = {
            "current_weather": current_weather_data,
            "weekly_forecast": final_weekly_forecast,
            "weather_alerts": weather_alert_data
        }
        print("--- API 호출 및 데이터 처리 완료 ---")

    # 최종 결과 출력
    print("\n--- 최종 JSON 결과 ---")
    print(json.dumps(final_data, indent=2, ensure_ascii=False))