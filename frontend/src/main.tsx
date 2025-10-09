import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom' // 1. import
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* 2. <BrowserRouter>로 <App /> 감싸기 */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)