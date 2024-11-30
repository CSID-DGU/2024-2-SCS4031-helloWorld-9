from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
import uuid
from multiprocessing import Queue

router = APIRouter()  # APIRouter 생성

@router.post("/upload")
async def upload_test(file: UploadFile = File(...), id: str = "/",task_queue: Queue = Depends(),):
    
    # 파일 업로드
    save_path = f"./uploads/{id.strip('/')}/{file.filename}"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 테스크큐에 임베딩 작업을 추가
    task_id = str(uuid.uuid4()) # 업로드된 파일에 고유한 task_id 부여
    task_queue.put({"task_id": task_id, "save_path": save_path})

    return {"task_id": task_id, "message": "작업이 큐에 추가되었습니다."}
