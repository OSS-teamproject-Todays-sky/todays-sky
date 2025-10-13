import { Routes, Route } from 'react-router-dom';
import WeatherPage from './pages/WeatherPage';

const App = () => {
  return (
      <Routes>
        {/* path="/"는 웹사이트의 루트 경로를 의미합니다.
          element={<WeatherPage />}는 해당 경로로 접속했을 때 보여줄 컴포넌트를 지정합니다.
        */}
        <Route path="/" element={<WeatherPage />} />
        
        {/* 예시: 나중에 "소개" 페이지를 추가하고 싶다면 아래처럼 한 줄만 추가하면 됩니다. */}
        {/* <Route path="/about" element={<AboutPage />} /> */}
      </Routes>
  );
}

export default App;