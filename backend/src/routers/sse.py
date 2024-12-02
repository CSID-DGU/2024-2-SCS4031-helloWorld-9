from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger("chatbot")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

async def sse_stream():
    """SSE 스트림 생성"""
    for i in range(10):
        await asyncio.sleep(1)  # 1초 대기
        yield f"data: Message {i} from server\n\n"  # SSE 데이터 형식
    yield "data: Stream closed\n\n"

@router.get("/sse_test")
async def sse_endpoint():
    logger.info("sse!")
    """SSE 엔드포인트."""
    return EventSourceResponse(sse_stream())
