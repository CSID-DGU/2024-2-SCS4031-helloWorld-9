
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import files, info, upload, chatbot  # 라우터 모듈 임포트

app = FastAPI(debug=True)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터 등록
app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
