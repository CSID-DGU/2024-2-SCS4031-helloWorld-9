from fastapi import APIRouter, UploadFile, File
import os
import shutil
import logging

router = APIRouter()  # APIRouter 생성

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# FastAPI 의 router function 에서, async def 와 def 는 실행방식의 차이가 있음.
# async def 를 쓰면 single thread event loop 로 처리함. IO bound 에 유리하고 CPU bound 에 불리함.
# 따라서, IO bound 인 upload_test 는 async def 로 구현,
# CPU bound 인 embed_pdf 는 def 로 구현하였음

def embed_pdf(filepath):
    logger.debug(f"start embedding : {filepath}")
    # embedding 수행


@router.post("/upload")
async def upload_test(file: UploadFile = File(...), id: str = "/"):
    """
    업로드된 파일을 저장
    """
    save_path = f"./uploads/{id.strip('/')}/{file.filename}"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    embed_pdf(save_path)

    return {"filename": file.filename, "saved_to": save_path}
