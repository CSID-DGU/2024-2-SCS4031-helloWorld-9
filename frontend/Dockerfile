# Node.js 이미지를 기반으로
FROM node:18

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 소스 복사
COPY . .

# 의존성 설치
RUN npm install

# 환경 변수 설정
ENV VITE_PORT=3000
ENV VITE_API_BASE_URL=http://localhost:8000

# 컨테이너 실행 시 Svelte 개발 서버 실행
CMD ["npm", "run", "dev"]