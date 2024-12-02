# routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from rag_utils.embedding import Embedder  # VectorDB 초기화에 필요
from rag_utils.retrieval import Retriever  # RAG 시스템
from config import DB_PATH, UPLOAD_PATH
from rag_utils.init_rag import try_init_vectorDB_from_uploads

router = APIRouter()
logger = logging.getLogger("chatbot")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)


class ChatbotRequest(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str
    references: Optional[List[dict]] = None


# 이미 업로드된 PDF 파일 임베딩
try_init_vectorDB_from_uploads(db_path=DB_PATH,upload_path=UPLOAD_PATH)

@router.post("/get-answer", response_model=ChatbotResponse)
async def get_answer(request: ChatbotRequest):
    logger.info("챗봇 대답 생성 시작...")
    try:
        responser = Retriever(db_path=DB_PATH)
    except Exception as e:
        logger.error(f"Retriever gen Failed : {str(e)}")
        try_init_vectorDB_from_uploads(db_path=DB_PATH,upload_path=UPLOAD_PATH)
        return ChatbotResponse(
                answer=f"RAG 참조 실패. VectorDB를 다시 생성했습니다. 다시 질문해주세요 : {str(e)}",
                references=None
            )
        
    # Retriever() 호출 responser 생성 시점 이후에 추가된 문서를 로드
    responser.update_docs()

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
        