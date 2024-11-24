from fastapi import FastAPI
from routers import files, info, upload  # 라우터 모듈 임포트

app = FastAPI(debug=True)

# 라우터 등록
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(info.router, prefix="/info", tags=["Info"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)