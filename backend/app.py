
from fastapi import FastAPI, Request
from routers import files, info, upload, chatbot, route_test, graphview_router,sse   # 라우터 모듈 임포트
import logging
import web_utils.log_init
from web_utils.log_init import log_middleware
import os

app = FastAPI(debug=False)

# HTTP 요청 로그 미들웨어 추가
# http_debug=True 로 설정하는 경우, 디버그 메세지로 web request 를 확인 가능
log_middleware(app, http_debug=False)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(route_test.router, prefix="/api/route_test", tags=["route_test"])
app.include_router(sse.router, prefix="/api/sse", tags=["sse"])
app.include_router(graphview_router.graphview_router, prefix="/api/graphview", tags=["GraphView"])

if __name__ == "__main__":
    import uvicorn
    env_port = int(os.getenv("PORT", 8000))
    print(os.getenv("OPENAI_API_KEY"))
    uvicorn.run("app:app", host="0.0.0.0", port=env_port, reload=True)
