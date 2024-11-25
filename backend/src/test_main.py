from rag_utils.embedding import Embedder
from rag_utils.retrieval import Retriev_Gen
from config import DB_PATH

if __name__ == "__main__":
    print(DB_PATH)
    embedder = Embedder()
    embedder.add_docs("hanhwa-testdata.pdf")

    responser = Retriev_Gen()
    
    question = "보험금 청구 절차는??"
    response = responser.get_response(question)
    print(response)
    responser.print_reference(question)
