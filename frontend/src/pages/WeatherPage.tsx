import { useState, useEffect }from 'react';
import * as Styled from './WeatherPage.styles';
import type { WeatherData, DailyForecast } from '../types/weather';
import { BackgroundKey } from '../utils/BackgroundKey';

const getIconForSky = (sky: string | undefined): string => {
  if (!sky) return '01d'; // 기본값 (맑음)
  if (sky.includes('맑음')) return '01d';
  if (sky.includes('구름많음')) return '03d';
  if (sky.includes('흐림')) return '04d';
  if (sky.includes('비')) return '10d';
  if (sky.includes('눈')) return '13d';
  if (sky.includes('소나기')) return '09d';
  if (sky.includes('이슬비')) return '09d';
  if (sky.includes('뇌우')) return '11d';
  return '01d';
};

function WeatherPage() {
  // ... (데이터 및 그래프 로직은 이전과 동일)
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [selectedDay, setSelectedDay] = useState<DailyForecast | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('/api/weather');
        if (!response.ok) {
          throw new Error('날씨 데이터를 불러오는 데 실패했습니다.');
        }
        const data: WeatherData = await response.json();
        setWeatherData(data);
        setSelectedDay(data.weekly_forecast[0]);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  } , []);

  useEffect(() => {
    // 1초(1000ms)마다 currentTime 상태를 현재 시간으로 업데이트합니다.
    const timerId = setInterval(() => {
      setCurrentTime(new Date());
    }, 30000);

    // 컴포넌트가 사라질 때 타이머를 정리(cleanup)합니다. (메모리 누수 방지)
    return () => {
      clearInterval(timerId);
    };
  }, []);

  const formatCurrentTime = (date: Date) => {
  const days = ['일', '월', '화', '수', '목', '금', '토'];
  const dayName = days[date.getDay()];
  
  const options: Intl.DateTimeFormatOptions = {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true, // '오전/오후' 사용
  };
  
  const timeString = date.toLocaleTimeString('ko-KR', options);
  
  return `(${dayName}요일) ${timeString}`;
};
  
  const getCoordinates = (temps: number[]) => {
    if(temps.length <2) {
      return [{ x: 50, y: 50 }];
    }
    
    return temps.map((temp, i) => {
      const x = (i / (temps.length - 1)) * 100;
      const y = 100 - ((temp - graphMinTemp) / graphTempRange) * 100;
      return { x, y };
    });
  };

  if (loading) {
    return (
      <>
        <Styled.GlobalStyle />
        <Styled.StarryBackground />
        <Styled.WeatherPageContainer style={{ justifyContent: 'center', alignItems: 'center' }}>
          <h2>날씨 정보를 불러오는 중...</h2>
        </Styled.WeatherPageContainer>
      </>
    );
  }
  if (error) {
    return (
      <>
        <Styled.GlobalStyle />
        <Styled.StarryBackground />
        <Styled.WeatherPageContainer style={{ justifyContent: 'center', alignItems: 'center' }}>
          <h2>오류가 발생했습니다: {error}</h2>
          <p>백엔드 서버가 켜져 있는지, API가 정상인지 확인해주세요.</p>
        </Styled.WeatherPageContainer>
      </>
    );
  }
  if (!weatherData) return null;
  
  const { current_weather, weekly_forecast, hourly_forecast, weather_alerts } = weatherData;
  const currentIcon = getIconForSky(current_weather.sky);

  const graphData = hourly_forecast || [];
  const itemWidth = 60;
  const totalGraphWidth = Math.max(graphData.length * itemWidth, 1000);

  const temperatures = graphData.map(d => d.temp);
  const minTemp = Math.min(...temperatures);
  const maxTemp = Math.max(...temperatures);

  const graphMinTemp = Math.floor(minTemp / 5) * 5; 
  const graphMaxTemp = Math.ceil(maxTemp / 5) * 5; 
  let graphTempRange = graphMaxTemp - graphMinTemp;

  if (graphTempRange === 0) {
    graphTempRange = 5; // 임의로 5도 범위를 줌
  }

  const yAxisLabels = [];
  for (let temp = graphMaxTemp; temp >= graphMinTemp; temp -= 5) {
    yAxisLabels.push(temp);
  }

  const points = getCoordinates(temperatures);
  const pathData = points.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ');
  const bgKey = BackgroundKey(current_weather.sky);
  
  return (
    <>
      <Styled.GlobalStyle />
      {/* 이미지가 존재할 때 */}
      {bgKey !== "__NO_IMAGE__" ? (
        <Styled.Background sky={bgKey} />
      ) : (
        /* 이미지가 없을 때 → 기본 별 배경 표시 */
        <Styled.StarryBackground />
      )}
      
      <Styled.WeatherPageContainer>
        <Styled.CurrentWeatherSection>
          <Styled.CurrentTempDetails>
            <img src={`http://openweathermap.org/img/wn/${currentIcon}@4x.png`} alt={current_weather.sky} />
            <Styled.CurrentTemp>{Math.round(Number(current_weather.temperature))}</Styled.CurrentTemp>
          </Styled.CurrentTempDetails>
          <Styled.CurrentInfo>
            <h2>{current_weather.sky}</h2>
            <p>{current_weather.temp_max}° / {current_weather.temp_min}°</p>
          </Styled.CurrentInfo>
          <Styled.CurrentInfo>
            {/* TODO: 이 정보는 백엔드 JSON에 추가해야 함 */}
            <p className="location">Daeyeon-dong, Nam-gu</p>
            <p>{formatCurrentTime(currentTime)}</p>
          </Styled.CurrentInfo>
          {weather_alerts.length > 0 && !weather_alerts[0].content.includes("발효된 특보가 없습니다") && (
          <Styled.WeatherAlertSection>
            <h3>기상 특보</h3>
            <ul>
              {weather_alerts.map((alert, index) => (
                <li key={index}>{alert.content}</li>
              ))}
            </ul>
          </Styled.WeatherAlertSection>
        )}
        </Styled.CurrentWeatherSection>

        <Styled.GraphSection>
          <Styled.YAxisLabels>
            {yAxisLabels.map(temp => (
              <span key={temp}>{temp}°</span>
            ))}
          </Styled.YAxisLabels>
          <Styled.GraphScrollWrapper>
            <Styled.GraphContent style={{ width: `${totalGraphWidth}px` }}>
              <Styled.GraphContainer viewBox="0 0 100 100" preserveAspectRatio="none">
                {yAxisLabels.map((temp) => {
                  const y = 100 - ((temp - graphMinTemp) / graphTempRange) * 100;
                  return (
                    <line 
                      key={`grid-${temp}`}
                      x1="0" y1={y} x2="100" y2={y} 
                      stroke="rgba(255, 255, 255, 0.8)"
                      strokeWidth="0.3" 
                      strokeDasharray="0.5 2"
                      vectorEffect="non-scaling-stroke"
                    />
                  );
                })}
                <path d={pathData} fill="none" stroke="rgba(255, 255, 255, 0.7)" strokeWidth="0.4" vectorEffect="non-scaling-stroke" />
                {points.map((point, i) => (
                  <path
                    key={`dot-${i}`}
                    d={`M ${point.x} ${point.y} L ${point.x} ${point.y}`} 
                    stroke="white" 
                    strokeWidth="8px"
                    strokeLinecap="round"
                    vectorEffect="non-scaling-stroke"
                  />
                ))}
              </Styled.GraphContainer>
              {points.map((point, i) => (
                <Styled.PointWrapper 
                  key={i} 
                  style={{ 
                    left: `${point.x}%`, 
                    top: `${point.y}%` 
                  }}>
                  <Styled.TempLabel>
                    {Math.round(temperatures[i])}°
                  </Styled.TempLabel>
                </Styled.PointWrapper>
              ))}
            </Styled.GraphContent>
          </Styled.GraphScrollWrapper>
        </Styled.GraphSection>
        
        <Styled.WeeklyForecastSection>
            {weekly_forecast.map((day) => {
              const dayIcon = getIconForSky(day.sky_am);
              return (
                <Styled.DayForecast 
                  key={day.date} 
                  active={selectedDay?.date === day.date}
                  onClick={() => setSelectedDay(day)}
                >
                  <p className="day-name">{day.day_of_week.charAt(0)}</p>
                  <img src={`http://openweathermap.org/img/wn/${dayIcon}@2x.png`} alt="" />
                  <p>{Math.round(Number(day.temp_max))}°</p>
                  <p className="temps">{Math.round(Number(day.temp_min))}°</p>
                </Styled.DayForecast>
              );
            })}
        </Styled.WeeklyForecastSection>
        {selectedDay && (
          <Styled.DetailedInfoSection>
            <h3>{selectedDay.day_of_week} 상세 예보</h3>
            <Styled.DetailContent>
              <Styled.DetailText>
                <p>오전: <span>{selectedDay.sky_am} (강수: {selectedDay.precip_prob_am}%)</span></p>
                <p>오후: <span>{selectedDay.sky_pm} (강수: {selectedDay.precip_prob_pm}%)</span></p>
              </Styled.DetailText>
            </Styled.DetailContent>
          </Styled.DetailedInfoSection>
        )}
      </Styled.WeatherPageContainer>
    </>
  );
}

export default WeatherPage;