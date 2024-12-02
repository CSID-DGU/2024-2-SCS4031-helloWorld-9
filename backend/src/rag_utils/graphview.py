import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
import os

class GraphView:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.vectorstore = self.create_faiss_index(pdf_path)

    def create_faiss_index(self, pdf_path: str):
        # PDF 파일 로드
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()

        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        split_documents = text_splitter.split_documents(docs)

        # OpenAI Embeddings 사용
        embeddings = OpenAIEmbeddings()

        # 임베딩 생성
        document_vectors = embeddings.embed_documents([doc.page_content for doc in split_documents])

        # FAISS 인덱스 생성
        dimension = len(document_vectors[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(document_vectors).astype(np.float32))

        # 문서 저장소 생성
        index_to_docstore_id = {i: str(i) for i in range(len(split_documents))}
        docstore = InMemoryDocstore()
        docstore.add({
            str(i): doc
            for i, doc in enumerate(split_documents)
        })

        # FAISS 벡터 스토어 생성
        vectorstore = FAISS(
            index=index, 
            embedding_function=embeddings, 
            docstore=docstore, 
            index_to_docstore_id=index_to_docstore_id
        )
        
        return vectorstore

    def retrieve_documents(self, question: str):
        retriever = self.vectorstore.as_retriever()

        # 문서 검색
        results = retriever.retrieve(query=question)

        # 결과를 JSON 형식으로 변환
        json_output = {"nodes": [], "links": []}
        
        # 질문을 노드로 추가
        json_output["nodes"].append({
            "id": "user_question",  
            "label": question,
        })
        
        # 검색된 문서 내용과 링크 추가
        for idx, result in enumerate(results):
            content = result.page_content
            source = self.extract_source(content)
            truncated_content = content[:1000]  # 1000자까지만 출력

            if source:
                json_output["nodes"].append({
                    "id": f"출처{idx+1}",  
                    "label": source
                })
            else:
                json_output["nodes"].append({
                    "id": f"출처{idx+1}",  
                    "label": truncated_content
                })

            similarity_score = self.calculate_similarity(question, truncated_content)
            json_output["links"].append({
                "source": "user_question",  
                "target": f"출처{idx+1}",  
                "value": similarity_score
            })

        return json_output

    def extract_source(self, content: str):
        import re
        match = re.search(r'출처 :(.+)', content)
        if match:
            return match.group(1).strip()
        return None

    def calculate_similarity(self, question: str, document_text: str):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([question, document_text])
        cosine_similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
        return cosine_similarity
