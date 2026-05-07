from langchain_community.vectorstores import FAISS 
from rag.embedder import load_embeddings

def create_vectorestore(documents,embedings):
    vectorstore=FAISS.from_documents(
        documents,
        embedings
    )

    return vectorstore