
from fastapi import FastAPI
from routers import files, info, upload, chatbot, route_test  # 라우터 모듈 임포트
import logging

app = FastAPI(debug=True)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(route_test.router, prefix="/api/route_test", tags=["route_test"])

# 전역 로그 제어
# level=logging.INFO -> logger.info 출력
# level=loggin.DEBUG -> logger.info, logger.debug 둘다 출력
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
