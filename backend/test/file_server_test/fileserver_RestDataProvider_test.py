from fastapi import FastAPI, Query, Request
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

@app.get("/info", response_model=Union[FolderInfo, FileSystemInfo])
async def loadinfo_test(id: Optional[str] = Query(None)):
    """
    id가 제공되면 폴더 정보 반환, 제공되지 않으면 파일 시스템 정보 반환
    """
    if id:
        # id가 제공된 경우 폴더 정보 반환
        folder_info = {
            "Size": 47597382,  # 폴더 크기
            "Count": 17        # 폴더 내 항목 수
        }
        return JSONResponse(content=folder_info)

    # id가 제공되지 않은 경우 파일 시스템 정보 반환
    file_system_info = {
        "free": 0,                   # 남은 공간
        "total": 467300933632,       # 전체 공간 (Todo : 실제의 서버 용량을 측정하여 반영)
        "used": 239621727232         # 사용된 공간 (Todo : 실제의 서버 용량을 측정하여 반영)
    } 
    return JSONResponse(content=file_system_info)

@app.post("/upload")
async def upload_test(request: Request):
    # 요청 헤더 출력
    headers = request.headers
    print("Headers:", headers)

    # 요청 본문 출력
    body = await request.body()
    print("Raw Body:", body)

    # 요청 쿼리 매개변수 출력 (만약 있다면)
    query_params = request.query_params
    print("Query Params:", query_params)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fileserver_RestDataProvider_test:app", host="127.0.0.1", port=8000, reload=True)