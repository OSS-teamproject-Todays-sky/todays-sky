import React, { useState }from 'react';
import * as Styled from './WeatherPage.styles';

interface DayData {
  day: string;
  icon: string;
  max: number;
  min: number;
  description: string;
  humidity: number; // 습도 정보 추가
  wind: number;    // 풍속 정보 추가
}

function WeatherPage() {
  // ... (데이터 및 그래프 로직은 이전과 동일)
  const weeklyData = [
    { day: '화', icon: '10d', max: 21, min: 18, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4},
    { day: '수', icon: '02d', max: 23, min: 19, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4 },
    { day: '목', icon: '09d', max: 23, min: 19, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4 },
    { day: '금', icon: '01d', max: 24, min: 20, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4 },
    { day: '토', icon: '03d', max: 25, min: 17, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4 },
    { day: '일', icon: '04d', max: 21, min: 14, description: '가끔 비가 내리겠습니다.', humidity: 85, wind: 4 },
  ];

  const [selectedDay, setSelectedDay] = useState<DayData>(weeklyData[0]);

  const temperatures = weeklyData.map(d => d.max);
  const minTemp = Math.min(...temperatures) - 2;
  const maxTemp = Math.max(...temperatures) + 2;
  const tempRange = maxTemp - minTemp;

  const getCoordinates = (temps: number[]) => {
    return temps.map((temp, i) => {
      const x = (i / (temps.length - 1)) * 100;
      const y = 100 - ((temp - minTemp) / tempRange) * 100;
      return { x, y };
    });
  };

  const points = getCoordinates(temperatures);
  const pathData = points.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ');

  return (
    <>
      <Styled.GlobalStyle />
      <Styled.StarryBackground /> 
      
      <Styled.WeatherPageContainer>
        <Styled.CurrentWeatherSection>
          <Styled.CurrentTempDetails>
            <img src={`http://openweathermap.org/img/wn/02n@4x.png`} alt="약간의 구름" />
            <Styled.CurrentTemp>20</Styled.CurrentTemp>
          </Styled.CurrentTempDetails>
          <Styled.CurrentInfo>
            <h2>약간의 구름</h2>
            <p>21° / 18°</p>
          </Styled.CurrentInfo>
          <Styled.CurrentInfo>
            <p className="location">Gwangbok-dong, Jung-gu</p>
            <p>(수요일) 오전 3:03</p>
          </Styled.CurrentInfo>
        </Styled.CurrentWeatherSection>
        <Styled.GraphSection>
            <Styled.YAxisLabels>
            <span>{maxTemp}°</span>
            <span>{Math.round(minTemp + tempRange / 2)}°</span>
            <span>{minTemp}°</span>
          </Styled.YAxisLabels>
          <Styled.GraphContainer viewBox="0 0 100 100" preserveAspectRatio="none">
            <path d={pathData} fill="none" stroke="rgba(255, 255, 255, 0.7)" strokeWidth="0.4" />
            {points.map((point, i) => (
              <circle key={i} cx={point.x} cy={point.y} r="0.8" fill="white" />
            ))}
          </Styled.GraphContainer>
        </Styled.GraphSection>
        <Styled.WeeklyForecastSection>
            {weeklyData.map((day, index) => (
            <Styled.DayForecast 
              key={index} 
              active={selectedDay.day === day.day}
              onClick={() => setSelectedDay(day)}
              >
              <p className="day-name">{day.day}</p>
              <img src={`http://openweathermap.org/img/wn/${day.icon}@2x.png`} alt="" />
              <p>{day.max}°</p>
              <p className="temps">{day.min}°</p>
            </Styled.DayForecast>
          ))}
        </Styled.WeeklyForecastSection>
        {selectedDay && (
          <Styled.DetailedInfoSection>
            <h3>{selectedDay.day}요일 상세 예보</h3>
            <Styled.DetailContent>
              <img src={`http://openweathermap.org/img/wn/${selectedDay.icon}@2x.png`} alt={selectedDay.description} />
              <Styled.DetailText>
                <p>{selectedDay.description}</p>
                <p>예상 기온: <span>{selectedDay.min}° / {selectedDay.max}°</span></p>
                <p>습도: <span>{selectedDay.humidity}%</span> &nbsp;&nbsp; 풍속: <span>{selectedDay.wind}m/s</span></p>
              </Styled.DetailText>
            </Styled.DetailContent>
          </Styled.DetailedInfoSection>
        )}
      </Styled.WeatherPageContainer>
    </>
  );
}

export default WeatherPage;