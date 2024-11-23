import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import pdfmanager as pm
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
DIMENSION_SIZE = 1024
DB_PATH = os.path.join(script_dir, '..', 'vectorDB')
DB_INDEX = "faiss"

class VectorDB:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name= EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},  # cuda, cpu
            encode_kwargs={"normalize_embeddings": True},
        )

        self.db = FAISS(
            embedding_function=self.embeddings,
            index=faiss.IndexFlatL2(DIMENSION_SIZE),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

    def add_docs(self):
        loader = PDFPlumberLoader("data/한화생명 간편가입 시그니처 암보험(갱신형) 무배당_2055-001_002_약관_20220601_.pdf")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0)
        split_documents = loader.load_and_split(text_splitter)

        self.db.add_documents(
            [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in split_documents]
        )
    
    def remove_docs(self):
        pass
    
    def save_db(self):
        self.db.save_local(folder_path=DB_PATH, index_name=DB_INDEX)

db = VectorDB()
db.add_docs()
db.save_db()