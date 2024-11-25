# routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from rag_utils.embedding import Embedder  # VectorDB 초기화에 필요
from rag_utils.retrieval import Retriev_Gen  # RAG 시스템

router = APIRouter()
logger = logging.getLogger(__name__)

# 전역 변수로 RAG 시스템 초기화
try:
    responser = Retriev_Gen()
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {str(e)}")
    responser = None

class ChatbotRequest(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str
    references: Optional[List[dict]] = None

@router.post("/get-answer", response_model=ChatbotResponse)
async def get_answer(request: ChatbotRequest):
    try:
        if responser is None:
            raise HTTPException(status_code=500, detail="RAG system not initialized")
            
        # 질문에 대한 응답 생성
        answer = responser.get_response(request.question)
        
        # 참조 문서 검색
        references = []
        results = responser.retriever.invoke(request.question)
        
        for result in results:
            references.append({
                "source": result.metadata.get('source', 'Unknown'),
                "start_index": result.metadata.get('start_index', 'N/A'),
                "end_index": result.metadata.get('end_index', 'N/A'),
                "content": result.page_content
            })
        
        return ChatbotResponse(
            answer=answer,
            references=references
        )
        
    except Exception as e:
        logger.error(f"Error processing chatbot request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))