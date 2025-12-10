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

  /* UI 가독성을 위한 반투명 배경 추가 */
  background: rgba(0, 0, 0, 0.2);  /* 투명도 조절 */
  backdrop-filter: blur(6px);     /* 블러 처리 */
  border-radius: 20px;
`;

// --- 나머지 스타일 컴포넌트는 이전과 동일 ---
// ... (CurrentWeatherSection, WeeklyForecastSection, GraphSection 등)
export const CurrentWeatherSection = styled.div`
  display: grid;
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
    color: #ffffffff;
  }
`;

export const CurrentInfo = styled.div`
  display: flex;
  flex-direction: column; /* 세로 배치 */
  align-items: flex-start; /* 왼쪽 정렬 */
  gap: 0; /* 세로 배치이므로 기본 gap 제거 */

  h2 { margin: 0; font-size: 1.8rem; font-weight: 600; }
  p { margin: 0; color: #ffffffff; font-size: 1rem; }
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
  border-radius: 15px; /* 배경색을 위해 추가 */
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.1)' : 'transparent'};
  cursor: pointer; /* 클릭 가능하다는 것을 알려줌 */
  transition: background-color 0.3s ease;

  &:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }

  p { margin: 0; font-size: 1rem; }
  .day-name { font-weight: 600; margin-bottom: 1rem; }
  img { width: 50px; height: 50px; margin-bottom: 1rem; }
  .temps { color: #ffffffff; }
`;

export const GraphSection = styled.div`
  position: relative;
  height: 200px;
  margin-bottom: 3rem;
`;

export const GraphScrollWrapper = styled.div`
  width: 100%;
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding-left: 50px;
  cursor: grab;

  &:active {
    cursor: grabbing;
  }
  
  &::-webkit-scrollbar {
    display: none;
  }
  scrollbar-width: none;
`;

export const GraphContent = styled.div`
  position: relative; /* 자식(SVG, 점)의 기준점 */
  height: 100%;
  padding-top: 20px;
  padding-bottom: 40px; 
  box-sizing: border-box;
`;

export const YAxisLabels = styled.div`
  position: absolute;
  top: 20px;
  left: 0;
  width: 40px;
  height: calc(100% - 60px);
  z-index: 20;
  pointer-events: none;

  span {
    position: absolute; /* 절대 위치로 배치 */
    width: 100%;
    text-align: right;
    padding-right: 10px;
    transform: translateY(-50%); /* 텍스트 수직 중앙 정렬 */
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.8rem;
  }
`;

export const GraphContainer = styled.svg`
  width: 100%;
  height: 100%;
  overflow: visible;
`;

export const PointWrapper = styled.div`
  position: absolute;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  pointer-events: none; 
`;

export const TempLabel = styled.span`
  position: absolute;
  bottom: 15px; /* 점보다 15px 위에 위치 */
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  white-space: nowrap;
`;

export const TimePositioner = styled.div`
  position: absolute;
  top: 100%;
  margin-top: 10px;
  transform: translateX(-50%); /* 해당 지점의 중앙에 텍스트 정렬 */
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
  white-space: nowrap;
  pointer-events: none;
`;

export const DetailedInfoSection = styled.section`
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem 2rem;
  border-radius: 15px;
  margin-bottom: 2rem;
  animation: ${fadeIn} 0.5s ease-out; /* 부드럽게 나타나는 효과 */

  h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-weight: 600;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding-bottom: 1rem;
  }
`;

export const DetailContent = styled.div`
  display: flex;
  align-items: center;
  gap: 1.5rem;
  
  img {
    width: 70px;
    height: 70px;
  }
`;

export const DetailText = styled.div`
  p {
    margin: 0.4rem 0;
    font-size: 1rem;
  }
  span {
    color: #ffffffff;
  }
`;

export const WeatherAlertSection = styled.section`
  background: rgba(192, 57, 43, 0.2);
  border: 1px solid rgba(231, 76, 60, 0.5);
  padding: 1rem 1.5rem;
  border-radius: 15px;
  margin-top: 1rem;
  animation: ${fadeIn} 0.5s ease-out;

  h3 {
    margin: 0 0 0.5rem 0;
    color: #e74c3c;
    font-size: 1.1rem;
  }
  
  ul {
    margin: 0;
    padding-left: 1.5rem;
  }

  li {
    font-size: 0.95rem;
    color: #ffffffff;
    line-height: 1.5;
  }
`;

export const Background = styled.div<{ sky: string }>`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -10;
  background-image: url('/backgrounds/${({ sky }) => sky}.png');
`;

const STATUS_DOT_COLORS: Record<string, string> = {
  '최고': '#38a1f6',
  '좋음': '#51c4d4',
  '양호': '#8c81e3',
  '보통': '#65b839',
  '나쁨': '#f7a036',
  '상당히 나쁨': '#f77836',
  '매우 나쁨': '#ff5656',
  '위험': '#b73939',
  '정보없음': '#6b7280',
};

export const AirInlineContainer = styled.div`
    font-size: 0.9rem;
    margin-top: 5px;
    color: #ffffffff;
    font-weight: 400;
    display: flex; 
    flex-direction: row;
    gap: 15px; 
    align-items: center;
`;

export const PollutantItem = styled.span`
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 500;
`;

export const StatusDot = styled.span<{ $status: string }>`
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    vertical-align: middle;
    background-color: ${(props) => STATUS_DOT_COLORS[props.$status] || STATUS_DOT_COLORS['정보없음']};
`;