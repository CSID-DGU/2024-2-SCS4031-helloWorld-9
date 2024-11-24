from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
import shutil

router = APIRouter()  # APIRouter 생성

@router.get("/")
async def loadinfo_test(id: Optional[str] = Query(None)):
    """
    id가 제공되면 폴더 정보 반환, 제공되지 않으면 파일 시스템 정보 반환
    """
    if id:
        folder_info = {
            "Size": 47597382,
            "Count": 17
        }
        return JSONResponse(content=folder_info)

    total, used, free = shutil.disk_usage("/")
    file_system_info = {
        "free": free,
        "total": total,
        "used": used
    }
    return JSONResponse(content=file_system_info)
