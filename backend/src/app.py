
from fastapi import FastAPI, Request
from routers import files, info, upload, chatbot, route_test, graphview_router  # 라우터 모듈 임포트
import logging

app = FastAPI(debug=True)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(route_test.router, prefix="/api/route_test", tags=["route_test"])
app.include_router(graphview_router.graphview_router, prefix="/api/graphview", tags=["GraphView"])
# 전역 로그 제어
# level=logging.INFO -> logger.info 출력
# level=loggin.DEBUG -> logger.info, logger.debug 둘다 출력
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
http_debug = False
@app.middleware("http")
async def log_request(request: Request, call_next):
    if http_debug:  # http_debug가 True일 때만 로그를 출력
        # 요청 본문 출력
        try:
            body = await request.body()
            logger.info(f"Request body: {body.decode('utf-8', errors='replace')}")  # 오류가 있는 바이트는 'replace'로 대체
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode request body: {e}")
        
        # 요청 헤더 출력
        headers = dict(request.headers)
        logger.info(f"Request headers: {headers}")
    
    # 요청을 처리하고, 응답을 반환
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
