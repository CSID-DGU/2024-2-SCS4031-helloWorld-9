from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv(override=True)
script_dir = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS = OpenAIEmbeddings()
DB_PATH = os.path.join(script_dir, '..', 'vectorDB')
DB_INDEX = "faiss"
LLM = ChatOpenAI(model_name="gpt-4o", temperature=0)
PROMPT = PromptTemplate.from_template(
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

class Retriev_Gen:
    def __init__(self):
        self.vectorstore = None
        self.chain = None
        self.update_docs()
    
    def get_response(self, question):
        return self.chain.invoke(question)
    
    def print_reference(self, question):
        results = self.retriever.invoke(question)

        for result in results:
            # docstore에서 문서의 세부 내용 출력
            print(f"검색된 문서 출처: {result.metadata['source']}")
            print(f"위치: {result.metadata.get('start_index', 'N/A')} - {result.metadata.get('end_index', 'N/A')}")
            print(f"내용: {result.page_content}")

    def update_docs(self):
        self.vectorstore = FAISS.load_local(DB_PATH, embeddings=EMBEDDINGS, allow_dangerous_deserialization=True)
        self.retriever = self.vectorstore.as_retriever()
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | PROMPT
            | LLM
            | StrOutputParser()
        )