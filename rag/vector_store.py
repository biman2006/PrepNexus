from langchain_community.vectorstores import FAISS 

def create_vectorestore(documents,embedings):
    vectorstore=FAISS.from_documents(
        documents,
        embedings
    )

    return vectorstore