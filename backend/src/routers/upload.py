from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter()  # APIRouter 생성

@router.post("/upload")
async def upload_test(file: UploadFile = File(...), id: str = "/"):
    """
    업로드된 파일을 저장
    """
    save_path = f"./uploads/{id.strip('/')}/{file.filename}"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "saved_to": save_path}
