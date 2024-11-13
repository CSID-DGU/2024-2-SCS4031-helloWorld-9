import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.docstore.in_memory import InMemoryDocstore
import networkx as nx
from pyvis.network import Network
from streamlit import components
import streamlit as st

# FAISS(Facebook AI Similarity Search)는, 그 자체로 AI 모델은 아니고 벡터 검색 라이브러리임.
# 대규모 데이터셋에서 고속으로 유사한 벡터를 찾기 위한 최근접 이웃 검색(Nearest Neighbor Search)을 수행함.

api_key = os.getenv("OPENAI_API_KEY")

# 단계 1: 문서 로드(Load Documents)
loader = PyMuPDFLoader("data/test.pdf")
docs = loader.load()

# 단계 2: 문서 분할(Split Documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩(Embedding) 생성
# 임베딩을 위한 AI 모델이 존재함. OpenAIEmbeddings() 를 호출하면, OpenAI 의 최신 임베딩 모델을 통해 알아서 임베딩을 수행하는 객체를 반환함.
# embeddings = OpenAIEmbeddings(model_name="text-embedding-ada-002") 이런식으로 직접 임베딩 모델을 지정할 수도 있음.
# embeddings 에는 임베딩을 위한 객체가 생성되어 저장됨.

embeddings = OpenAIEmbeddings()
print(embeddings.__dict__)  # embeddings.model = text-embedding-ada-002 -> OpenAI API가 업데이트되면 더 성능 좋은 임베딩 모델로 알아서 바꿔줌.

# 입력한 문서의 출처를 메타데이터에 저장해서, 나중에 답변 시 정확히 어떤 문서의 몇번째 줄로부터 근거한 것인지 추가하는 로직

# 단계 4: DB 생성(Create DB) 및 저장
document_vectors = embeddings.embed_documents([doc.page_content for doc in split_documents])

# FAISS 인덱스 생성
dimension = len(document_vectors[0])  # 벡터의 차원
index = faiss.IndexFlatL2(dimension)
index.add(np.array(document_vectors).astype(np.float32))

# 단계 5: docstore와 index_to_docstore_id 생성
# 문서 ID와 그에 해당하는 문서의 매핑을 생성합니다.
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

# 단계 5: 검색기(Retriever) 생성
# 문서에 포함되어 있는 정보를 검색하고 생성합니다.
# vectorstore.embeddings.model 을 참조하여 어떤 모델을 사용해야할지 결정함. embeddings.model 은 embeddings = OpenAIEmbeddings() 때, 가장 최신의 임베딩 모델로 설정됨.
# retriver : openai.resources.embeddings.Embeddings 형 객체임
retriever = vectorstore.as_retriever()

# 단계 6: 프롬프트 생성(Create Prompt)
# 프롬프트를 생성합니다.

print(retriever.__dict__)

# chatGPT API는 맥락 정보에 해당하는 context를 입력받을 수 있음.
# 그러면 context에 맞는 답변을 알아서 레퍼런스하여 답변을 생성함.
# context로 openai.resources.embeddings.Embeddings 객체를 입력받을 수 있음.

prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in Korean.

#Question: 
{question} 
#Context: 
{context} 

#Answer:"""
)

# 단계 7: 언어모델(LLM) 생성
# 모델(LLM)을 생성합니다.
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 단계 8: 체인(Chain) 생성
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 이때, 체인에서,
# retriever 를 통해 검색된 {context} 를 통해 chatGPT 가 맥락을 파악하고 답변을 한다.

def visualize_search_results_as_tree(question, results, response):
    # 네트워크 그래프 생성
    G = nx.DiGraph()
    net = Network(notebook=True, height="1200px", width="100%", directed=True)
    
    # 초기 트리 구조 배치 및 물리 상호작용 설정
    net.set_options("""
    var options = {
        "physics": {
            "enabled": true,
            "hierarchicalRepulsion": {
                "nodeDistance": 200,
                "springLength": 200,
                "centralGravity": 0.01
            },
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.005,
                "springLength": 300,
                "springConstant": 0.08
            },
            "solver": "forceAtlas2Based",
            "minVelocity": 0.75,
            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 25
            }
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "levelSeparation": 250,
                "nodeSpacing": 200,
                "direction": "UD",
                "sortMethod": "directed"
            }
        }
    }
    """)

    # 노드 그룹별 색상 정의
    colors = {
        'question': '#4B0082',  # 진한 남색
        'answer': '#006400',    # 진한 녹색
        'evidence': '#8B4513',  # 갈색
        'context': '#4682B4'    # 파란색
    }
    
    # 1. 질문 노드 추가 (루트 노드)
    G.add_node("Question", 
               label=f"질문:\n{question}", 
               color=colors['question'],
               shape='box',
               size=80,  # 노드 크기 증가
               font={'size': 20, 'color': 'white'})  # 텍스트 크기 증가
    
    # 2. 메인 답변 노드 추가
    sentences = [s.strip() for s in response.split('.') if s.strip()]
    main_answer = sentences[0] if sentences else response
    G.add_node("Main_Answer", 
               label=f"답변:\n{main_answer}", 
               color=colors['answer'],
               shape='box',
               size=70,
               font={'size': 20, 'color': 'white'})
    G.add_edge("Question", "Main_Answer")  # 루트에서 메인 답변으로 연결

    # 3. 부가 설명 노드 추가
    for i, sent in enumerate(sentences[1:], 1):
        node_id = f"Answer_Detail_{i}"
        G.add_node(node_id, 
                  label=sent, 
                  color=colors['answer'],
                  shape='box',
                  size=60,
                  font={'size': 18, 'color': 'white'})
        G.add_edge("Main_Answer", node_id)  # 메인 답변에서 부가 설명으로 연결

    # 4. 근거 문서와 문서 내용 노드 추가
    for i, result in enumerate(results):
        doc_id = f"Doc_{i+1}"
        source_info = f"출처: {result.metadata.get('source', 'N/A')}\n" \
                     f"위치: {result.metadata.get('start_index', 'N/A')} - {result.metadata.get('end_index', 'N/A')}"
        
        G.add_node(doc_id, 
                  label=source_info,
                  color=colors['evidence'],
                  shape='dot',
                  size=45,
                  font={'size': 16})
        G.add_edge("Main_Answer", doc_id, label="근거")  # 메인 답변에서 근거 문서로 연결

        content_id = f"Content_{i+1}"
        content = result.page_content[:200] + "..."
        content = '\n'.join([content[i:i+50] for i in range(0, len(content), 50)])
        
        G.add_node(content_id, 
                  label=content,
                  color=colors['context'],
                  shape='box',
                  size=45,
                  font={'size': 14})
        G.add_edge(doc_id, content_id)  # 근거 문서에서 문서 내용으로 연결
    
    # NetworkX 그래프를 Pyvis 네트워크로 변환
    net.from_nx(G)

    # 그래프 생성 및 표시
    net.show("keywords_tree_view.html")
    
    # Streamlit에서 트리 형식 시각화 표시
    with open("keywords_tree_view.html", "r", encoding="utf-8") as HtmlFile:
        source_code = HtmlFile.read()
        components.v1.html(source_code, height=1200, scrolling=True)

# 체인 실행(Run Chain)
# 문서에 대한 질의를 입력하고, 답변을 출력합니다.
question = "삼성전자가 자체 개발한 AI 의 이름은?"
response = chain.invoke(question)

# chatGPT 의 답변
print("ChatGPT 답변:", response)

# 검색된 문서와 위치 정보 출력
results = retriever.invoke(question)

for result in results:
    # docstore에서 문서의 세부 내용 출력
    print(f"검색된 문서 출처: {result.metadata['source']}")
    print(f"위치: {result.metadata.get('start_index', 'N/A')} - {result.metadata.get('end_index', 'N/A')}")
    print(f"내용: {result.page_content}")

# 검색 결과를 시각화
visualize_search_results_as_tree(question, results, response)

# 최종 답변 출력
print("ChatGPT의 최종 답변:", response)
