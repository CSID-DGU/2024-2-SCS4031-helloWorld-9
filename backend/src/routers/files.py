from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import logging

router = APIRouter()  # APIRouter 생성
logger = logging.getLogger(__name__)

@router.get("/")
async def loadfile_test(directory: str = "./uploads"):
    """
    서버의 실제 파일 및 폴더 정보를 반환
    """
    base_path = Path(directory).resolve()

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
    return JSONResponse(content=files)
