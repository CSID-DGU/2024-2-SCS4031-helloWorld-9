from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Union
import uvicorn

app = FastAPI()

# 모델 정의
class FolderInfo(BaseModel):
    Size: int  # 폴더 크기
    Count: int  # 폴더 내 항목 수

class FileSystemInfo(BaseModel):
    free: int  # 남은 공간
    total: int  # 전체 공간
    used: int  # 사용된 공간

@app.get("/files")
async def loadfile_test():
    dummy_data = [
        {
            "id": "/Code",
            "size": 4096,
            "date": datetime(2023, 12, 2, 17, 25).isoformat(),  # ISO 8601 형식으로 날짜 직렬화
            "type": "folder",
        },
        {
            "id": "/Music",
            "size": 4096,
            "date": datetime(2023, 12, 1, 14, 45).isoformat(),
            "type": "folder",
        },
        {
            "id": "/Info.txt",
            "size": 1000,
            "date": datetime(2023, 11, 30, 6, 13).isoformat(),
            "type": "file",
        },
        {
            "id": "/Code/Datepicker/Year.svelte",
            "size": 1595,
            "date": datetime(2023, 12, 7, 15, 23).isoformat(),
            "type": "file",
        },
        {
            "id": "/Pictures/162822515312968813.png",
            "size": 510885,
            "date": datetime(2023, 12, 1, 14, 45).isoformat(),
            "type": "file",
        },
    ]

    return JSONResponse(content=dummy_data)

@app.get("/info")
async def loadinfo_test():
    return "hello"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fileserver_RestDataProvider_test:app", host="127.0.0.1", port=8000, reload=True)