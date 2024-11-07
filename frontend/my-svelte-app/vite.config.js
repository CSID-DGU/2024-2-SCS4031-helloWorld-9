import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config();

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 3000 // 3000 포트로 변경
  },
  resolve: {
    alias: {
      'pdfjs-dist/build/pdf.worker.mjs': path.resolve(__dirname, 'node_modules/pdfjs-dist/build/pdf.worker.mjs')
    }
  }
  
});
