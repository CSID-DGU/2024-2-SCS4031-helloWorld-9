import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Path to the uploads folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../uploads')

def extract_source(content: str):
    match = re.search(r'출처 :(.+)', content)
    if match:
        return match.group(1).strip()
    return None

# Helper function to calculate cosine similarity between question and document
def calculate_similarity(question: str, document_text: str):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([question, document_text])
    cosine_similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return cosine_similarity

# Helper function to load and process files from the uploads folder and create the FAISS index
def create_faiss_index():
    documents = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            loader = PyMuPDFLoader(filepath)
            docs = loader.load()
            documents.extend(docs)

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings()
    document_vectors = embeddings.embed_documents([doc.page_content for doc in split_documents])

    # Create FAISS index
    dimension = len(document_vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(document_vectors).astype(np.float32))

    # Create a mapping from index to document ID
    index_to_docstore_id = {i: str(i) for i in range(len(split_documents))}

    # Create docstore
    docstore = InMemoryDocstore()
    docstore.add({str(i): doc for i, doc in enumerate(split_documents)})

    # Create FAISS vectorstore
    vectorstore = FAISS(
        index=index,
        embedding_function=embeddings,
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id
    )

    return vectorstore
