import importlib

from rag.embedder import load_embeddings


def _import_faiss():
    for mod_name in ("langchain_community.vectorstores", "langchain.vectorstores"):
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, "FAISS")
        except Exception:
            continue
    return None


def create_vectorestore(documents, embedings):
    FAISS = _import_faiss()
    if FAISS is None:
        raise ImportError(
            "Could not import FAISS from langchain packages. Install langchain-community or langchain."
        )

    vectorstore = FAISS.from_documents(
        documents,
        embedings
    )

    return vectorstore