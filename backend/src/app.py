
from fastapi import FastAPI, Request
from routers import files, info, upload, chatbot, route_test  # 라우터 모듈 임포트
import logging
import web_utils.log_init
from web_utils.log_init import log_middleware

app = FastAPI(debug=False)

# HTTP 요청 로그 미들웨어 추가
# http_debug=True 로 설정하는 경우, 디버그 메세지로 web request 를 확인 가능
log_middleware(app, http_debug=True)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(route_test.router, prefix="/api/route_test", tags=["route_test"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
