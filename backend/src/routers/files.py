from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import logging
from config import BASE_DIR

router = APIRouter()  # APIRouter 생성
logger = logging.getLogger(__name__)

root_upload_path = f"{BASE_DIR}/uploads"

@router.get("/files")
async def loadfile_test(directory: str = root_upload_path):
    """
    서버의 실제 파일 및 폴더 정보를 반환
    """
    logger.info(f"Current working directory: {Path.cwd()}")
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

# # 업로드된 파일 삭제
# @router.delete("/files")
# async def delete_uploaded_file(file_path: str):

#     # 파일 경로 생성
#     file_to_delete = Path(root_upload_path) / Path(file_path)

#     try:
#         # 파일 삭제
#         file_to_delete.unlink()  # 파일 삭제
#         logger.info(f"File {file_to_delete} has been deleted successfully.")
#         return JSONResponse(content={"message": f"File {file_to_delete} deleted successfully."})
#     except Exception as e:
#         logger.error(f"Error deleting file {file_to_delete}: {e}")
#         return JSONResponse(content={"message": f"ERROR : File {file_to_delete} deleted failed."})