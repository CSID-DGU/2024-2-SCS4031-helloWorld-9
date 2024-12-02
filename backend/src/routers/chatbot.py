# routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from rag_utils.embedding import Embedder  # VectorDB 초기화에 필요
from rag_utils.retrieval import Retriev_Gen  # RAG 시스템
from config import DB_PATH, UPLOAD_PATH

router = APIRouter()
logger = logging.getLogger("chatbot")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

chatbot_db_path = DB_PATH
chatbot_upload_path = UPLOAD_PATH

# 이미 업로드된 PDF 파일 임베딩
try:
    logger.info(f"Chatbot initializing...")
    # embedder = Embedder(db_path=chatbot_db_path)
    # pdf_files = [file for file in chatbot_upload_path.rglob("*.pdf") if file.is_file()]

    # if not pdf_files:
    #     logger.info("No PDF files found.")
    #     # PDF 파일이 없는 경우 추가 작업
    # else:
    #     logger.info(f"Found {len(pdf_files)} PDF files:")
    #     for pdf in pdf_files:
    #         logger.info(f"pdf 파일 임베딩 시작 : {pdf}")
    #         embedder.add_docs(pdf)
    #         logger.info(f"pdf 파일 임베딩 완료 : {pdf}")

except Exception as e:
    logger.error(f"Failed to gen embedder: {str(e)}")
    retriev_gen_error = e
    responser = None

# 전역 변수로 RAG 시스템 초기화
try:
    responser = Retriev_Gen(db_path=DB_PATH)
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {str(e)}")
    retriev_gen_error = e
    responser = None

class ChatbotRequest(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str
    references: Optional[List[dict]] = None

@router.post("/get-answer", response_model=ChatbotResponse)
async def get_answer(request: ChatbotRequest):
    logger.info("챗봇 대답 생성 시작...")
    try:
        if responser is None:
            return ChatbotResponse(
                answer=f"Retriev_Gen Failed : {retriev_gen_error}",
                references=None
            )
        
        # Retriev_Gen() 호출 responser 생성 시점 이후에 추가된 문서를 로드
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
        
    except Exception as e:
        logger.error(f"Error processing chatbot request: {str(e)}")
        #raise HTTPException(status_code=500, detail=str(e))
        return ChatbotResponse(
                answer=str(e),
                references=None
            )
        