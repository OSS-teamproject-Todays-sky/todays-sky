import React from 'react';
import * as Styled from './WeatherPage.styles';

function WeatherPage() {
  // 시간대별 날씨를 위한 샘플 데이터
  const hourlyData = [
    { time: '오전 9시', icon: '01d', temp: 18 },
    { time: '오후 12시', icon: '02d', temp: 24 },
    { time: '오후 3시', icon: '01d', temp: 25 },
    { time: '오후 6시', icon: '03d', temp: 22 },
    { time: '오후 9시', icon: '04n', temp: 20 },
    { time: '오후 12시', icon: '02n', temp: 19 },
  ];

  return (
    <Styled.WeatherContainer>
      <Styled.AppHeader>
        <h1>날씨 앱</h1>
      </Styled.AppHeader>

      <Styled.SearchBox onSubmit={(e) => e.preventDefault()}>
        <Styled.SearchInput
          type="text"
          placeholder="도시 이름을 검색하세요 (예: Seoul)"
        />
        <Styled.SearchButton type="submit">검색</Styled.SearchButton>
      </Styled.SearchBox>

      <Styled.ResultsContainer>
        {/* --- 현재 날씨 (이전과 동일) --- */}
        <Styled.CurrentWeatherSection>
          <Styled.CurrentDetails>
            <h2>서울 (Seoul)</h2>
            <img 
              src={`http://openweathermap.org/img/wn/02d@2x.png`} 
              alt="구름 조금" 
            />
            <Styled.CurrentTemp>25°C</Styled.CurrentTemp>
            <p>구름 조금</p>
          </Styled.CurrentDetails>
        </Styled.CurrentWeatherSection>

        {/* --- 시간대별 예보 (수정된 부분) --- */}
        <Styled.HourlyForecastSection>
          <h3>시간대별 예보</h3>
          <Styled.ForecastContainer>
            {hourlyData.map((hour, index) => (
              <Styled.ForecastCard key={index}>
                <h4>{hour.time}</h4>
                <img 
                  src={`http://openweathermap.org/img/wn/${hour.icon}.png`} 
                  alt="" 
                />
                <Styled.Temp>{hour.temp}°</Styled.Temp>
              </Styled.ForecastCard>
            ))}
          </Styled.ForecastContainer>
        </Styled.HourlyForecastSection>
      </Styled.ResultsContainer>
    </Styled.WeatherContainer>
  );
}

export default WeatherPage;