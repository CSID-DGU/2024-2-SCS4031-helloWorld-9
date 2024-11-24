# from embedding import Embedder
# from retrieval import Retriev_Gen

# if __name__ == "__main__":
#     embedder = Embedder()
#     embedder.add_docs("hanhwa-testdata.pdf")

#     responser = Retriev_Gen()
    
#     question = "보험금 청구 절차는??"
#     response = responser.get_response(question)
#     print(response)
#     responser.print_reference(question)

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from embedding import Embedder
from retrieval import Retriev_Gen
from pdfmanager import PDFManager
from io import BytesIO
import shutil
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

app = FastAPI()

# CORS 설정

# 질문을 받을 데이터 모델 정의
class Question(BaseModel):
    question: str

# PDF 업로드 엔드포인트
@app.post("/upload-doc/")
async def upload_doc(files: UploadFile = File(...)):
    """사용자가 업로드한 PDF 파일을 처리하고 벡터 스토어에 추가"""
    pdf_manager = PDFManager()
    message, _ = pdf_manager.process_pdf(files)  # PDF 처리
    if "성공적으로 처리된 파일" in message:
        # 파일이 성공적으로 처리된 경우, 벡터화
        embedder = Embedder()
        for file in pdf_manager.get_loaded_files():
            embedder.add_docs(file)  # 업로드된 파일을 벡터화하여 저장
        return {"message": message}
    return {"error": message}

# 질문에 대한 답변을 반환하는 엔드포인트
@app.post("/get-answer/")
async def get_answer(question: Question):
    """사용자가 입력한 질문에 대해 벡터화된 문서에서 답변을 생성"""
    embedder = Embedder()
    embedder.add_docs("hanhwa-testdata.pdf")
    responser = Retriev_Gen()
    response = responser.get_response(question.question)
    return {"answer": response}
