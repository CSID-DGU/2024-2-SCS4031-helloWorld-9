from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
import shutil

router = APIRouter()  # APIRouter 생성

@router.get("/check")
async def tester():
    test_json = {
        "test":"OK"
    }
    return JSONResponse(content=test_json)
