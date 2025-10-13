import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // '/api'로 시작하는 요청을 Flask 서버로 전달
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      }
    }
  }
})
