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
  announcement_time: string;
}

export interface WeatherData {
  current_weather: CurrentWeather;
  weekly_forecast: DailyForecast[];
  weather_alerts: WeatherAlert[];
}