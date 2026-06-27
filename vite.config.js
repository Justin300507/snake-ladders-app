import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8001', rewrite: p => p.replace(/^\/api/, '') },
      '/auth': { target: 'http://localhost:8001' },
      '/games': { target: 'http://localhost:8001' },
      '/players': { target: 'http://localhost:8001' },
      '/moves': { target: 'http://localhost:8001' },
      '/leaderboard': { target: 'http://localhost:8001' },
      '/stats': { target: 'http://localhost:8001' },
      '/health': { target: 'http://localhost:8001' },
    }
  }
})
