from fastapi import FastAPI
from routers import files, info, upload  # 라우터 모듈 임포트
import threading
import time
import os

app = FastAPI(debug=True)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])



"""
추후 rag_utils 하위에 배치할 예정입니다.
1. 스레드를 통해 주기적으로 uploads 폴더 확인
2. 새로운 파일이 있다면 embedding
"""
# 업로드 폴더 경로 설정
UPLOADS_DIR = 'uploads'

def perform_embedding_task(file_path):
    print(f"Performing task on: {file_path}")

    # 임베딩 작업 수행

    completed_path = f"{file_path}.complete"
    os.rename(file_path, completed_path)

def monitor_uploads():
    while True:
        for file_name in os.listdir(UPLOADS_DIR):
            file_path = os.path.join(UPLOADS_DIR, file_name)

            # .complete 파일은 건너뜀
            if not file_name.endswith('.complete'):
                perform_embedding_task(file_path)

        time.sleep(5)  # 5초 간격으로 폴더를 확인

# 백그라운드 모니터링 시작
thread = threading.Thread(target=monitor_uploads, daemon=True)
thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)