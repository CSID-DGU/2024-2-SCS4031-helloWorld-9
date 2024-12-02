from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import logging
from config import BASE_DIR, DB_PATH, UPLOAD_PATH
import os
from rag_utils.embedding import Embedder
from rag_utils.init_rag import try_init_vectorDB_from_uploads, remove_vectorDB
from web_utils.file_manager import get_all_pdfs
from routers.sse import sse_message
from fastapi import BackgroundTasks

router = APIRouter()  # APIRouter 생성
logger = logging.getLogger(__name__)

root_upload_path = f"{BASE_DIR}/uploads"
embedder = Embedder(db_path=DB_PATH)


@router.get("/files")
def loadfile_test(directory: str = root_upload_path, background_tasks: BackgroundTasks = None):
    """
    서버의 실제 파일 및 폴더 정보를 반환
    """
    # logger.info(f"Current working directory: {Path.cwd()}")
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
    logger.info(get_all_pdfs(UPLOAD_PATH))
    return JSONResponse(content=files)

# Todo : 업로드된 파일 삭제
# async def 를 사용하니, 비동기로 인해 race condition 이 유발되는 듯 함. (존재하지 않는 파일을 삭제하려고 시도하여, 프로그램이 죽음)
## try catch 등의 명시적 핸들링을 작성하여 존재하지 않는 파일을 삭제하려고 시도해도 핸들링되거나,
## def (동기함수) 로 재구현해서 오류를 해결해야함.

# 파일 삭제함수는 Race Condition 을 피하기 위하여, def 동기함수로 선언
@router.delete("/files")
def delete_uploaded_file(ids: str = Body(...), background_tasks: BackgroundTasks = None):
    logger.info(f"Received data to delete: {ids}")

    # ids에서 불필요한 문자 제거 후 리스트로 변환
    ids = ids.strip('{}"ids:[]').split(",")
    
    logger.info(f"Files to delete: {ids}")

    for file_path in ids:
        file_path = file_path.strip()  # 공백 제거
        file_to_delete = os.path.join(root_upload_path, file_path.lstrip('/'))  # 경로 결합

        # 파일이 존재하면 삭제
        if os.path.exists(file_to_delete) and os.path.isfile(file_to_delete):
            os.remove(file_to_delete)  # 파일 삭제
            logger.info(f"Deleted file: {file_to_delete}")
        else:
            logger.warning(f"File does not exist or is not a file: {file_to_delete}")
    
    # 파일 삭제 시, 나머지 파일을 재 임베딩 시도
    remove_vectorDB(db_path=DB_PATH)
    try_init_vectorDB_from_uploads(db_path=DB_PATH,upload_path=UPLOAD_PATH)

    background_tasks.add_task(sse_message, f"파일 삭제됨 {ids}")

    return {"message": "Files deletion completed", "deleted_files": ids}

