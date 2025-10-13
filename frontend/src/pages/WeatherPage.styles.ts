import styled, { keyframes } from 'styled-components';

// 나머지 스타일(fadeIn, WeatherContainer, AppHeader 등)은 이전과 동일합니다.
// ... (이전 코드와 동일)

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

export const WeatherContainer = styled.div`
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: linear-gradient(135deg, #6dd5ed, #2193b0);
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: white;
`;

export const AppHeader = styled.header`
  text-align: center;
  margin-bottom: 2rem;

  h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
  }
`;

export const SearchBox = styled.form`
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2.5rem;
`;

export const SearchInput = styled.input`
  flex-grow: 1;
  padding: 0.8rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  transition: background-color 0.3s;

  &::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }

  &:focus {
    outline: none;
    background-color: rgba(255, 255, 255, 0.3);
  }
`;

export const SearchButton = styled.button`
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  color: #2193b0;
  background-color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #f0f0f0;
  }
`;

export const ResultsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  animation: ${fadeIn} 0.5s ease-in-out;
`;

export const CurrentWeatherSection = styled.section`
  background-color: rgba(255, 255, 255, 0.15);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  backdrop-filter: blur(10px);
`;

export const CurrentDetails = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;

  h2 {
    margin: 0;
    font-size: 2rem;
    font-weight: 600;
  }

  img {
    width: 100px;
    height: 100px;
  }

  p {
    font-size: 1.2rem;
    margin: 0;
  }
`;

export const CurrentTemp = styled.span`
  font-size: 4rem;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
`;

// --- 아래부터 변경된 부분 ---

// WeeklyForecastSection -> HourlyForecastSection 으로 이름 변경 및 스타일 수정
export const HourlyForecastSection = styled.section`
  background-color: rgba(255, 255, 255, 0.15);
  padding: 1.5rem;
  border-radius: 15px;
  backdrop-filter: blur(10px);

  h3 {
    margin-top: 0;
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 600;
  }
`;

// ForecastGrid -> Horizontally scrolling Flexbox로 변경
export const ForecastContainer = styled.div`
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 0.5rem;
  /* 스크롤바 디자인 */
  &::-webkit-scrollbar {
    height: 8px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 10px;
  }
`;

// ForecastCard 스타일 약간 수정
export const ForecastCard = styled.div`
  flex: 0 0 100px; /* 카드가 줄어들지 않고 고정된 너비를 갖도록 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 15px;
  background-color: rgba(255, 255, 255, 0.1);

  h4 {
    margin: 0;
    font-weight: 600;
    font-size: 1rem;
  }

  img {
    width: 50px;
    height: 50px;
  }
`;

// ForecastTemps -> 단일 온도를 표시하도록 Temp로 변경
export const Temp = styled.span`
  font-weight: 600;
  font-size: 1.2rem;
`;