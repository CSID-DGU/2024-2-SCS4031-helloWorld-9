import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config();

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000, // Vite 서버는 3000번 포트
    proxy: {
      // API 요청을 FastAPI로 프록시
      '/api': {
        target: 'http://localhost:8000', // FastAPI가 실행 중인 주소
        changeOrigin: true,
      }
    }
  },
  resolve: {
    alias: {
      'pdfjs-dist/build/pdf.worker.mjs': path.resolve(__dirname, 'node_modules/pdfjs-dist/build/pdf.worker.mjs')
    }
  }
});
