from embedding import Embedder
from retrieval import Retriev_Gen

if __name__ == "__main__":
    embedder = Embedder()
    embedder.add_docs("C:/Users/hj780/Desktop/2024-2-SCS4031-helloWorld-9/backend/data/한화생명 간편가입 시그니처 암보험(갱신형) 무배당_2055-001_002_약관_20220601_.pdf")

    responser = Retriev_Gen()
    
    question = "보험금 청구 절차는??"
    response = responser.get_response(question)
    print(response)
    responser.print_reference(question)