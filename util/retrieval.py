from langchain_community.vectorstores import FAISS
from langchain_teddynote.retrievers import KiwiBM25Retriever
from langchain_teddynote.retrievers import EnsembleRetriever, EnsembleMethod
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
DB_PATH = os.path.join(script_dir, '..', 'vectorDB')
DB_INDEX = "faiss"

class Retrieval:
    def __init__(self, search_kwargs):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},  # cuda, cpu
            encode_kwargs={"normalize_embeddings": True},
        )

        self.search_kwargs = search_kwargs
        self.db = None
        #self.bm25 = None
        #self.cc_ensemble_retriever = None
        self.update_docs()

    def search(self, query):
        searched = self.faiss_retriever.invoke(query)
        return searched

    def update_docs(self):
        # 로컬 DB 로드
        self.db = FAISS.load_local(
            folder_path=DB_PATH,
            index_name=DB_INDEX,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

        self.faiss_retriever = self.db.as_retriever(search_kwargs={"k": self.search_kwargs})
        
"""
        # 문서 리스트 가져오기
        #self.documents = [self.db.docstore.search(doc_id) for doc_id in self.db.index_to_docstore_id.values()]

        # BM25 리트리버 설정
        #self.bm25_retriever = KiwiBM25Retriever.from_documents(documents=self.documents)
        #self.bm25_retriever.k = self.search_kwargs

        # Ensemble 리트리버 설정
        #self.cc_ensemble_retriever = EnsembleRetriever(
        #    retrievers=[self.faiss_retriever, self.bm25_retriever], method=EnsembleMethod.CC  # method 지정: CC
        #)

ret = Retrieval(search_kwargs=3)
print(ret.search("보험금 청구 절차"))
"""