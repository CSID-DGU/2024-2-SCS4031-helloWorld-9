from fastapi import FastAPI, Query, Request, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Union
import shutil
import os
import uvicorn
import logging

app = FastAPI(debug=True)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)  # 기본 로그 레벨을 DEBUG로 설정
logger = logging.getLogger(__name__)     # 로거 객체 생성

# 모델 정의
class FolderInfo(BaseModel):
    Size: int  # 폴더 크기
    Count: int  # 폴더 내 항목 수

class FileSystemInfo(BaseModel):
    free: int  # 남은 공간
    total: int  # 전체 공간
    used: int  # 사용된 공간

@app.get("/files")
async def loadfile_test(directory: str = "./uploads"): # Todo : 실제 경로로 변경하기
    """
    서버의 실제 파일 및 폴더 정보를 반환
    :param directory: 디렉토리를 지정. 기본값은 './uploads'
    """
    
    base_path = Path(directory).resolve()  # 절대 경로로 변환

    if app.debug:
        logger.debug(f"Resolved path: {base_path}")

    if not base_path.exists():
        logger.warning(f"Directory {directory} does not exist")
        return JSONResponse(content={"error": f"Directory {directory} does not exist"}, status_code=404)

    files = []
    for item in base_path.iterdir():
        files.append({
            "id": f"/{item.relative_to(base_path)}",
            "size": item.stat().st_size,
            "date": datetime.fromtimestamp(item.stat().st_mtime).isoformat(timespec="seconds"),
            "type": "folder" if item.is_dir() else "file",
        })
    
    if app.debug:
        logger.debug(f"Files: {files}")

    return JSONResponse(content=files)


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
async def upload_test(file: UploadFile = File(...), id: str = "/"):
    """
    업로드된 파일을 저장
    :param file: 업로드된 파일 객체
    :param id: 저장할 경로 (쿼리 매개변수)
    """
    # 파일 이름과 경로 설정
    save_path = f"./uploads/{id.strip('/')}/{file.filename}"

    # 디렉토리 생성 (없을 경우)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 파일 저장
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "saved_to": save_path}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fileserver:app", host="127.0.0.1", port=8000, reload=True)
