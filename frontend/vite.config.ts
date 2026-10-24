import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

// Backend FastAPI chạy ở cổng 8000. Mọi lời gọi /api đi qua proxy này
// nên frontend không cần biết địa chỉ backend và không vướng CORS khi dev.
// Trong docker compose, biến VITE_API_PROXY_TARGET trỏ tới service api (http://api:8000).
const BACKEND_URL = process.env.VITE_API_PROXY_TARGET ?? 'http://localhost:8000';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, './src'),
    },
    dedupe: ['react', 'react-dom'],
  },
  server: {
    port: 5173,
    strictPort: true,
    host: process.env.VITE_HOST ?? 'localhost',
    proxy: {
      '/api': {
        target: BACKEND_URL,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  test: {
    environment: 'node',
    include: ['src/**/*.test.ts'],
  },
});
