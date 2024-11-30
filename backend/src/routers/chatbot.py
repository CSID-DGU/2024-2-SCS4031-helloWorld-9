# routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from rag_utils.embedding import Embedder  # VectorDB 초기화에 필요
from rag_utils.retrieval import Retriev_Gen  # RAG 시스템
from config import DB_PATH

router = APIRouter()
logger = logging.getLogger(__name__)

# 전역 변수로 RAG 시스템 초기화
# Todo : router 에서 실패가능성이 있는 init 로직을 분리하기
try:
    responser = Retriev_Gen(db_path=DB_PATH)
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
            return ChatbotResponse(
                answer="Retriev_Gen Failed", # Todo : 구체적인 오류메세지를 반환하도록 변경
                references=None
            )
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
        #raise HTTPException(status_code=500, detail=str(e))
        return ChatbotResponse(
                answer=str(e),
                references=None
            )
        