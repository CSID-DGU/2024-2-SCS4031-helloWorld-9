import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv(override=True)
script_dir = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS = OpenAIEmbeddings()
DB_PATH = os.path.abspath(os.path.join(script_dir, '..', 'vectorDB'))

class Embedder:
    def add_docs(self, docs_path):
        # 기존 벡터스토어 로드 여부 확인
        index_file_path = os.path.join(DB_PATH, "index.faiss")
        if os.path.exists(index_file_path):
            vectorstore = FAISS.load_local(DB_PATH, embeddings=EMBEDDINGS, allow_dangerous_deserialization=True)
        else:
            vectorstore = FAISS(
                index=faiss.IndexFlatL2(1536),  # 벡터 차원 사용
                embedding_function=EMBEDDINGS,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )

        # 문서 로드 및 처리
        loader = PyMuPDFLoader(docs_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        split_documents = text_splitter.split_documents(docs)

        vectorstore.add_documents(
            [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in split_documents]
        )

        # 벡터스토어 저장
        vectorstore.save_local(DB_PATH)
    
    def remove_docs(self):
        pass