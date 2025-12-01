export interface CurrentWeather {
  temp_min: string;
  temp_max: string;
  temperature: string;
  sky: string;
  precip_type: string;
  precip_prob: string;
  humidity: string;
}

export interface DailyForecast {
  date: string;
  day_of_week: string;
  temp_min: number;
  temp_max: number;
  sky_am: string;
  sky_pm: string;
  precip_prob_am:number;
  precip_prob_pm:number;
}

export interface WeatherAlert {
  content: string;
  // announcement_time 필드는 백엔드에서 제거했으므로 주석 처리하거나 제거 가능
  // announcement_time: string;
}


// --- 2. 새로 추가된/업데이트된 타입 정의 ---

export interface AirPollutionData {
  pm2_5: string;
  pm10: string;
  pm2_5_status_kr: string;
  pm10_status_kr: string;
}

export interface HourlyForecast {
  time: string;
  temp: number;
}

export interface WeatherData {
  current_weather: CurrentWeather;
  weekly_forecast: DailyForecast[];
  weather_alerts: WeatherAlert[];
  hourly_forecast: HourlyForecast[];
  air_pollution: AirPollutionData; 
}