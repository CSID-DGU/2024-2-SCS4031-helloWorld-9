from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from rag_utils.graphview_utils import create_faiss_index, extract_source, calculate_similarity  # Importing from utils

# Define the request body model
class QuestionRequest(BaseModel):
    question: str

# Initialize FastAPI app and router
app = FastAPI()
graphview_router = APIRouter()

# Route to handle retrieving answers
@graphview_router.post("/retrieve/")
async def retrieve_keywords(request: QuestionRequest):
    question = request.question
    
    # Create the FAISS index if not already created
    vectorstore = create_faiss_index()
    
    # You can then use `vectorstore` to perform the retrieval logic as needed
    # For example, performing a search with the question:
    results = vectorstore.similarity_search(question, k=5)  # Adjust 'k' as needed

    # Prepare the response data
    json_output = {"nodes": [], "links": []}
    json_output["nodes"].append({"id": "user_question", "label": question})
    
    # Process results and add nodes, links to the JSON response
    for idx, result in enumerate(results):
        content = result.page_content
        source = extract_source(content)
        
        # Truncate content for display
        truncated_content = content[:1000]
        
        # Add source/content as nodes
        if source:
            json_output["nodes"].append({
                "id": f"출처{idx+1}", "label": source
            })
        else:
            json_output["nodes"].append({
                "id": f"출처{idx+1}", "label": truncated_content
            })

        # Calculate similarity and add links
        similarity_score = calculate_similarity(question, truncated_content)
        json_output["links"].append({
            "source": "user_question",
            "target": f"출처{idx+1}",
            "value": similarity_score
        })

    # Return the JSON response
    return json_output

# Register the router with FastAPI
app.include_router(graphview_router)


# from fastapi import APIRouter
# from pydantic import BaseModel
# import os
# from rag_utils.graphview import GraphView

# # 요청 Body 모델 정의
# class QuestionRequest(BaseModel):
#     question: str

# graphview_router = APIRouter()

# @graphview_router.post("/retrieve/")
# async def retrieve_keywords(request: QuestionRequest):
#     # 업로드된 파일이 있는 폴더 경로 지정
#     uploads_folder = "uploads"
    
#     # 'uploads' 폴더 안에 있는 PDF 파일들 가져오기
#     pdf_files = [f for f in os.listdir(uploads_folder) if f.endswith('.pdf')]

#     if not pdf_files:
#         return {"error": "No PDF files found in the uploads folder"}

#     # 첫 번째 PDF 파일을 선택 (여러 개일 경우, 원하는 방식으로 선택 가능)
#     pdf_path = os.path.join(uploads_folder, pdf_files[0])

#     # GraphView 인스턴스 생성 (FAISS 인덱스 생성 및 로드)
#     graph_view = GraphView(pdf_path)

#     # 질문을 기반으로 문서 검색
#     question = request.question
#     result = graph_view.retrieve_documents(question)

#     # 결과 반환
#     return result  # JSON 형식의 결과 반환
