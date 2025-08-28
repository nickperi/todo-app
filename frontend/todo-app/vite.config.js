import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    proxy: {
      '/api': {
        target: 'https://stunning-tribble-4xxr55547g72qpx9-5000.app.github.dev', // Flask app public URL
        changeOrigin: true,
        secure: false,
      },
    },
  },
})


