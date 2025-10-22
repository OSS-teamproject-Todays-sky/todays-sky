// import styled, { createGlobalStyle, keyframes } from 'styled-components';

// // --- Global Styles & Animations (이전과 동일) ---
// export const GlobalStyle = createGlobalStyle`
//   body {
//     margin: 0;
//     background-color: #0d1a26;
//     color: #e0e0e0;
//     font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
//   }
// `;

// const fadeIn = keyframes`
//   from { opacity: 0; transform: translateY(20px); }
//   to { opacity: 1; transform: translateY(0); }
// `;

// const shootingStar = keyframes`
//   0% { transform: translateX(150vw) translateY(-50vh); opacity: 1; }
//   100% { transform: translateX(-50vw) translateY(50vh); opacity: 0; }
// `;


// // --- Styled Components (카드 형식 제거 및 그래프 스타일 추가) ---

// export const WeatherPageContainer = styled.div`
//   position: relative;
//   max-width: 900px;
//   min-height: 100vh;
//   margin: auto;
//   padding: 2rem 3rem;
//   box-sizing: border-box;
//   overflow: hidden;
//   animation: ${fadeIn} 0.8s ease-out;
// `;

// export const StarryBackground = styled.div`
//   position: absolute;
//   top: 0;
//   left: 0;
//   right: 0;
//   bottom: 0;
//   background: #0d1a26 url('https://www.transparenttextures.com/patterns/stardust.png');
//   z-index: -1;

//   &::after {
//     content: '';
//     position: absolute;
//     width: 2px;
//     height: 2px;
//     background: white;
//     border-radius: 50%;
//     box-shadow: 0 0 5px 2px white;
//     animation: ${shootingStar} 15s linear infinite;
//     animation-delay: 2s;
//   }
// `;

// // --- CurrentWeatherSection, WeeklyForecastSection 등 이전 스타일은 그대로 사용 ---
// // ... (이전 코드와 동일한 부분)
// export const CurrentWeatherSection = styled.div`
//   display: flex;
//   justify-content: space-between;
//   align-items: flex-start;
//   padding-bottom: 2rem;
//   margin-bottom: 2rem;
// `;

// export const CurrentTempDetails = styled.div`
//   display: flex;
//   align-items: center;
//   gap: 1rem;

//   img { width: 80px; height: 80px; }
// `;

// export const CurrentTemp = styled.span`
//   font-size: 5rem;
//   font-weight: 200;
//   position: relative;

//   &:after {
//     content: '°C';
//     font-size: 1.5rem;
//     position: absolute;
//     top: 1.5rem;
//     right: -1.5rem;
//     color: #a0a0a0;
//   }
// `;

// export const CurrentInfo = styled.div`
//   text-align: right;

//   h2 { margin: 0; font-size: 1.8rem; font-weight: 600; }
//   p { margin: 0.2rem 0; color: #a0a0a0; font-size: 1rem; }
// `;

// export const WeeklyForecastSection = styled.div`
//   display: grid;
//   grid-template-columns: repeat(6, 1fr);
//   gap: 1.5rem;
//   text-align: center;
//   border-bottom: 1px solid rgba(255, 255, 255, 0.2);
//   padding-bottom: 2rem;
//   margin-bottom: 2rem;
// `;

// export const DayForecast = styled.div<{ active?: boolean }>`
//   padding: 1rem 0.5rem;
//   border-bottom: ${props => props.active ? '3px solid white' : '3px solid transparent'};
//   transition: background-color 0.3s ease;

//   p { margin: 0; font-size: 1rem; }
//   .day-name { font-weight: 600; margin-bottom: 1rem; }
//   img { width: 50px; height: 50px; margin-bottom: 1rem; }
//   .temps { color: #a0a0a0; }
// `;
// // --- 그래프 스타일 추가 ---

// export const GraphSection = styled.div`
//   position: relative;
//   height: 150px;
// `;

// export const YAxisLabels = styled.div`
//   position: absolute;
//   top: 0;
//   left: 0;
//   height: 100%;
//   display: flex;
//   flex-direction: column;
//   justify-content: space-between;
//   color: #a0a0a0;
//   font-size: 0.9rem;
  
//   span {
//     display: block;
//     position: relative;
//     padding-right: 10px;
    
//     &:after {
//       content: '';
//       position: absolute;
//       right: 0;
//       top: 50%;
//       width: 100vw;
//       border-bottom: 1px dotted rgba(255, 255, 255, 0.2);
//     }
//   }
// `;

// export const GraphContainer = styled.svg`
//   width: 100%;
//   height: 100%;
//   overflow: visible;
// `;
import styled, { createGlobalStyle, keyframes } from 'styled-components';

// --- Global Styles (기본 배경색과 폰트만 설정) ---
export const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    background-color: #0d1a26;
    color: #e0e0e0;
    font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  }
`;

// --- Animations (변경 없음) ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const shootingStar = keyframes`
  0% { transform: translateX(150vw) translateY(-50vh); opacity: 1; }
  100% { transform: translateX(-50vw) translateY(50vh); opacity: 0; }
`;

// --- StarryBackground (화면 전체를 덮도록 수정) ---
export const StarryBackground = styled.div`
  position: fixed; /* 화면에 고정 */
  top: 0;
  left: 0;
  width: 100vw; /* 화면 너비 전체 */
  height: 100vh; /* 화면 높이 전체 */
  background-image: url('https://www.transparenttextures.com/patterns/stardust.png');
  z-index: -1; /* 모든 콘텐츠 뒤로 보내기 */

  &::after {
    content: '';
    position: absolute;
    top: 30%;
    left: 0;
    width: 2px;
    height: 2px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 5px 2px white;
    animation: ${shootingStar} 15s linear infinite;
    animation-delay: 2s;
  }
`;

// --- Styled Components ---
export const WeatherPageContainer = styled.div`
  max-width: 1200px;
  min-height: 100vh;
  margin: auto;
  padding: 2rem 3rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  animation: ${fadeIn} 0.8s ease-out;
`;

// --- 나머지 스타일 컴포넌트는 이전과 동일 ---
// ... (CurrentWeatherSection, WeeklyForecastSection, GraphSection 등)
export const CurrentWeatherSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
`;

export const CurrentTempDetails = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  img { width: 80px; height: 80px; }
`;

export const CurrentTemp = styled.span`
  font-size: 5rem;
  font-weight: 200;
  position: relative;
  &:after {
    content: '°C';
    font-size: 1.5rem;
    position: absolute;
    top: 1.5rem;
    right: -1.5rem;
    color: #a0a0a0;
  }
`;

export const CurrentInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;

  h2 { margin: 0; font-size: 1.8rem; font-weight: 600; }
  p { margin: 0; color: #a0a0a0; font-size: 1rem; }
  .location { font-weight: 500; }
`;

export const WeeklyForecastSection = styled.div`
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.5rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 2rem;
  margin-bottom: 2rem;
`;

export const DayForecast = styled.div<{ active?: boolean }>`
  padding: 1rem 0.5rem;
  border-radius: 15px;
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.1)' : 'transparent'};
  transition: background-color 0.3s ease;

  p { margin: 0; font-size: 1rem; }
  .day-name { font-weight: 600; margin-bottom: 1rem; }
  img { width: 50px; height: 50px; margin-bottom: 1rem; }
  .temps { color: #a0a0a0; }
`;

export const GraphSection = styled.div`
  position: relative;
  height: 150px;
`;

export const YAxisLabels = styled.div`
  position: absolute;
  top: 0;
  left: -15px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #a0a0a0;
  font-size: 0.9rem;
  
  span {
    display: block;
    position: relative;
    padding-right: 10px;
    
    &:after {
      content: '';
      position: absolute;
      right: 0;
      top: 50%;
      width: 100vw;
      border-bottom: 1px dotted rgba(255, 255, 255, 0.2);
    }
  }
`;

export const GraphContainer = styled.svg`
  width: 100%;
  height: 100%;
  overflow: visible;
`;