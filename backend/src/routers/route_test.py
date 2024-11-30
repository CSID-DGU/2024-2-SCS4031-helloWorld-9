from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
import shutil
import logging


router = APIRouter()  # APIRouter 생성

# 로그 테스트
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@router.get("/check")
async def tester():
    test_json = {
        "test":"OK"
    }
    logger.debug(f"loggin system works...")
    return JSONResponse(content=test_json)
