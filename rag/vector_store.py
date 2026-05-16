import importlib


def _import_faiss():
    for mod_name in ("langchain_community.vectorstores", "langchain.vectorstores"):
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, "FAISS")
        except Exception:
            continue
    raise ImportError("Could not import FAISS from langchain packages. Install langchain-community or langchain.")


FAISS = _import_faiss()
from rag.embedder import load_embeddings


def create_vectorestore(documents, embedings):
    vectorstore = FAISS.from_documents(
        documents,
        embedings
    )

    return vectorstore