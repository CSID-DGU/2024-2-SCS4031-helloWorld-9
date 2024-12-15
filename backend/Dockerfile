FROM python:3.10

WORKDIR /app

# requirements.txt 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8000

# 컨테이너 실행 시 app.py 실행
CMD ["python3", "app.py"]
