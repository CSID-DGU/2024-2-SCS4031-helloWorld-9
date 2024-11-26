from rag_utils.embedding import Embedder
from rag_utils.retrieval import Retriev_Gen
from config import DB_PATH

if __name__ == "__main__":
    print(DB_PATH)
    embedder = Embedder(db_path=DB_PATH)
    embedder.add_docs("test_data/hanhwa-testdata.pdf")

    responser = Retriev_Gen(db_path=DB_PATH)
    
    question = "보험금 청구 절차는??"
    response = responser.get_response(question)
    print(response)
    responser.print_reference(question)
