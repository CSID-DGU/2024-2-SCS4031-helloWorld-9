from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import shutil
from multiprocessing import Queue

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("worker-tester")

router = APIRouter()  # APIRouter 생성

@router.get("/test")
async def add_test_item(task_queue: Queue = Depends(),):
    logger.info(f"FastAPI에서 Queue ID: {id(task_queue)}")
    logger.info("Worker tester GET")
    task_queue.put("worker-test-item")
    logger.info("test enqueued")
    return "test"
