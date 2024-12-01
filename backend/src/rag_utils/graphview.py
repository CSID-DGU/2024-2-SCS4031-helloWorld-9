import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import json

loader = PyMuPDFLoader("1201/backend/src/test_data/hanhwa-testdata.pdf")
docs = loader.load()

# 단계 2: 문서 분할(Split Documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩(Embedding) 생성
embeddings = OpenAIEmbeddings()
print(embeddings.__dict__)

# 단계 4: DB 생성(Create DB) 및 저장
document_vectors = embeddings.embed_documents([doc.page_content for doc in split_documents])

# FAISS 인덱스 생성
dimension = len(document_vectors[0])  # 벡터의 차원
index = faiss.IndexFlatL2(dimension)
index.add(np.array(document_vectors).astype(np.float32))

# 단계 5: docstore와 index_to_docstore_id 생성
index_to_docstore_id = {i: str(i) for i in range(len(split_documents))}

# 문서 저장소 생성 (메모리 내 저장소)
docstore = InMemoryDocstore()

# 문서 목록을 하나씩 추가하기 위해 직접 할당
docstore.add({
    str(i): doc  # 문서 ID와 문서를 매핑하여 추가
    for i, doc in enumerate(split_documents)
})

# 단계 6: FAISS 벡터 스토어 생성
vectorstore = FAISS(
    index=index, 
    embedding_function=embeddings, 
    docstore=docstore, 
    index_to_docstore_id=index_to_docstore_id
)

# 단계 7: 검색기(Retriever) 생성
retriever = vectorstore.as_retriever()

# 문서에 대한 질의를 입력하고, 결과를 출력하는 부분
def retrieve_and_print_documents(question):
    results = retriever.invoke(question)

    # JSON 형식으로 결과를 저장할 리스트
    json_output = {"nodes": [], "links": []}

    # 질문을 노드로 추가 (id를 숫자로 설정)
    json_output["nodes"].append({
        "id": "user_question",  # 질문에 대한 ID 설정
        "label": question,
    })

    # 검색된 문서 내용만 출력
    for idx, result in enumerate(results):
        content = result.page_content
        # 출처 추출
        source = extract_source(content)

        # 내용과 출처를 출력 (내용이 길면 잘라서 출력)
        truncated_content = content[:1000]  # 1000자까지만 출력

        # 노드를 추가 (출처가 있으면 출처, 없으면 내용 추가)
        if source:
            json_output["nodes"].append({
                "id": f"출처{idx+1}",  # "출처1", "출처2" 형식으로 ID 설정
                "label": source
            })
        else:
            json_output["nodes"].append({
                "id": f"출처{idx+1}",  # "출처1", "출처2" 형식으로 ID 설정
                "label": truncated_content
            })

        # 유사도 계산 (질문과 문서 내용 간)
        similarity_score = calculate_similarity(question, truncated_content)

        # 링크(유사도 값) 추가
        json_output["links"].append({
            "source": "user_question",  # 질문의 ID는 "user_question"
            "target": f"출처{idx+1}",  # 결과 ID는 "출처1", "출처2"로 설정
            "value": similarity_score
        })

    # JSON 형식으로 출력
    print(json.dumps(json_output, indent=2))

def extract_source(content):
    # 정규식을 사용하여 '출처 :' 이후의 텍스트를 추출
    match = re.search(r'출처 :(.+)', content)
    if match:
        return match.group(1).strip()  # 출처 이후의 텍스트만 반환
    return None  # 출처 정보가 없으면 None 반환

def calculate_similarity(question, document_text):
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([question, document_text])

    # 두 문서 간의 유사도 계산 (코사인 유사도)
    cosine_similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return cosine_similarity

# 예시 질문
question = "삼성전자가 자체 개발한 AI의 이름은?"
retrieve_and_print_documents(question)
