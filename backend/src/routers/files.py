from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import logging
from config import BASE_DIR, DB_PATH
import os
from rag_utils.embedding import Embedder

router = APIRouter()  # APIRouter 생성
logger = logging.getLogger(__name__)

root_upload_path = f"{BASE_DIR}/uploads"
embedder = Embedder(db_path=DB_PATH)


# Todo : vectorDB 삭제
# 동기로 작동해야하는 부분을 def 로 구현
def vector_db_restore():
    # Todo : vectorDB 제거 후, 나머지 pdf 다시 임베딩


    # pdf_file 을 모두 읽어서 vectorDB 복구
    pdf_files = [f for f in os.listdir(root_upload_path) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(root_upload_path, pdf_file)
        logger.info(f"start embedding : {pdf_path}")
        # embedding 수행
        embedder.add_docs(pdf_path)
        logger.info(f"embeding complete : {pdf_path}")
    logger.info(f"VectorDB restored after file delete : {pdf_path}")


@router.get("/files")
async def loadfile_test(directory: str = root_upload_path):
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
    return JSONResponse(content=files)

# 업로드된 파일 삭제
@router.delete("/files")
async def delete_uploaded_file(ids: str = Body(...)):  # str 타입으로 받음
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

        vector_db_restore()

    return {"message": "Files deletion completed", "deleted_files": ids}