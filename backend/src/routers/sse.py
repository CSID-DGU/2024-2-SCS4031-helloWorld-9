from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger("chatbot")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

# 비동기 Queue 생성 (공유 이벤트 큐)
event_queue = asyncio.Queue(maxsize=100)  # 최대 100개의 메시지 허용

async def sse_stream():
    """SSE 스트림 생성"""
    while True:
        # Queue에서 이벤트 가져오기
        event = await event_queue.get()
        yield f"서버 : {event}\n\n"

@router.get("/sse_test")
async def sse_endpoint():
    logger.info("SSE Connection Established")
    """SSE 엔드포인트."""
    return EventSourceResponse(sse_stream())

async def sse_message(msg):
    logger.info(f"SSE 메세지 : {msg}")
    await event_queue.put(msg)