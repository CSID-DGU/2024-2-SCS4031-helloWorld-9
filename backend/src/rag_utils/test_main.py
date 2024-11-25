from embedding import Embedder
from retrieval import Retriev_Gen

if __name__ == "__main__":
    embedder = Embedder()
    embedder.add_docs("hanhwa-testdata.pdf")

    responser = Retriev_Gen()
    
    question = "보험금 청구 절차는??"
    response = responser.get_response(question)
    print(response)
    responser.print_reference(question)