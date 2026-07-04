import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
    host: '0.0.0.0',
    allowedHosts: ['y4d3da62.natappfree.cc'],
    proxy: {
      // 前台页面 → 直接走 API 网关 (port 7000)
      '/api': {
        target: 'http://localhost:7000',
        changeOrigin: true
      },
      // 文件下载也走网关
      '/data': {
        target: 'http://localhost:7000',
        changeOrigin: true
      }
    }
  }
})
