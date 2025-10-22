// // src/pages/WeatherPage.tsx

// import React from 'react';
// import * as Styled from './WeatherPage.styles';

// function WeatherPage() {
//   const weeklyData = [
//     { day: '화', icon: '10d', max: 21, min: 18 },
//     { day: '수', icon: '02d', max: 23, min: 19 },
//     { day: '목', icon: '09d', max: 23, min: 19 },
//     { day: '금', icon: '01d', max: 24, min: 20 },
//     { day: '토', icon: '03d', max: 25, min: 17 },
//     { day: '일', icon: '04d', max: 21, min: 14 },
//   ];

//   // --- 그래프를 위한 로직 ---
//   const temperatures = weeklyData.map(d => d.max);
//   const minTemp = Math.min(...temperatures) - 2;
//   const maxTemp = Math.max(...temperatures) + 2;
//   const tempRange = maxTemp - minTemp;
//   const graphHeight = 150; // GraphSection의 높이와 동일

//   // 데이터 포인트를 SVG 좌표로 변환하는 함수
//   const getCoordinates = (temps: number[]) => {
//     const points = temps.map((temp, i) => {
//       const x = (i / (temps.length - 1)) * 100;
//       const y = 100 - ((temp - minTemp) / tempRange) * 100;
//       return { x, y };
//     });
//     return points;
//   };

//   const points = getCoordinates(temperatures);
//   const pathData = points.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ');
//   // --- 그래프 로직 끝 ---

//   return (
//     <>
//       <Styled.GlobalStyle />
//       <Styled.WeatherPageContainer>
//         <Styled.StarryBackground />
        
//         {/* Current Weather Section */}
//         <Styled.CurrentWeatherSection>
//           <Styled.CurrentTempDetails>
//             <img src={`http://openweathermap.org/img/wn/02n@4x.png`} alt="약간의 구름" />
//             <Styled.CurrentTemp>20</Styled.CurrentTemp>
//           </Styled.CurrentTempDetails>
//           <Styled.CurrentInfo>
//             <h2>약간의 구름</h2>
//             <p>최고: 21° 최저: 18°</p>
//             <p>Gwangbok-dong, Jung-gu</p>
//           </Styled.CurrentInfo>
//         </Styled.CurrentWeatherSection>

//         {/* Weekly Forecast Section */}
//         <Styled.WeeklyForecastSection>
//           {weeklyData.map((day, index) => (
//             <Styled.DayForecast key={index} active={index === 0}>
//               <p className="day-name">{day.day}</p>
//               <img src={`http://openweathermap.org/img/wn/${day.icon}@2x.png`} alt="" />
//               <p>{day.max}°</p>
//               <p className="temps">{day.min}°</p>
//             </Styled.DayForecast>
//           ))}
//         </Styled.WeeklyForecastSection>

//         {/* Temperature Graph Section */}
//         <Styled.GraphSection>
//           <Styled.YAxisLabels>
//             <span>{maxTemp}°</span>
//             <span>{Math.round(minTemp + tempRange / 2)}°</span>
//             <span>{minTemp}°</span>
//           </Styled.YAxisLabels>
//           <Styled.GraphContainer viewBox="0 0 100 100" preserveAspectRatio="none">
//             <path d={pathData} fill="none" stroke="rgba(255, 255, 255, 0.8)" strokeWidth="0.5" />
//             {points.map((point, i) => (
//               <circle key={i} cx={point.x} cy={point.y} r="1" fill="white" />
//             ))}
//           </Styled.GraphContainer>
//         </Styled.GraphSection>

//       </Styled.WeatherPageContainer>
//     </>
//   );
// }

// export default WeatherPage;
// src/pages/WeatherPage.tsx

import React from 'react';
import * as Styled from './WeatherPage.styles';

function WeatherPage() {
  // ... (데이터 및 그래프 로직은 이전과 동일)
  const weeklyData = [
    { day: '화', icon: '10d', max: 21, min: 18 },
    { day: '수', icon: '02d', max: 23, min: 19 },
    { day: '목', icon: '09d', max: 23, min: 19 },
    { day: '금', icon: '01d', max: 24, min: 20 },
    { day: '토', icon: '03d', max: 25, min: 17 },
    { day: '일', icon: '04d', max: 21, min: 14 },
  ];

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
        {/* 나머지 콘텐츠는 이전과 동일 */}
        {/* ... (CurrentWeatherSection, WeeklyForecastSection, GraphSection) ... */}
        <Styled.CurrentWeatherSection>
          <Styled.CurrentTempDetails>
            <img src={`http://openweathermap.org/img/wn/02n@4x.png`} alt="약간의 구름" />
            <Styled.CurrentTemp>20</Styled.CurrentTemp>
          </Styled.CurrentTempDetails>
          <Styled.CurrentInfo>
            <h2>약간의 구름</h2>
            <p>21° / 18°</p>
            <p className="location">Gwangbok-dong, Jung-gu</p>
            <p>(수요일) 오전 3:03</p>
          </Styled.CurrentInfo>
        </Styled.CurrentWeatherSection>
        <Styled.WeeklyForecastSection>
            {weeklyData.map((day, index) => (
            <Styled.DayForecast key={index} active={index === 0}>
              <p className="day-name">{day.day}</p>
              <img src={`http://openweathermap.org/img/wn/${day.icon}@2x.png`} alt="" />
              <p>{day.max}°</p>
              <p className="temps">{day.min}°</p>
            </Styled.DayForecast>
          ))}
        </Styled.WeeklyForecastSection>
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
      </Styled.WeatherPageContainer>
    </>
  );
}

export default WeatherPage;