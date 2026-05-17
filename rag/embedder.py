import streamlit as st

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    HuggingFaceEmbeddings = None

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings as CommunityHuggingFaceEmbeddings
    if HuggingFaceEmbeddings is None:
        HuggingFaceEmbeddings = CommunityHuggingFaceEmbeddings
except ImportError:
    pass

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class LocalSentenceTransformerEmbeddings:
    def __init__(self, model_name: str):
        if SentenceTransformer is None:
            raise ImportError(
                "sentence_transformers is not installed. Install it to use local model embeddings."
            )
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        return [self.model.encode(text, convert_to_numpy=True) for text in texts]

    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True)

    def __call__(self, texts):
        if isinstance(texts, str):
            return self.embed_query(texts)
        if isinstance(texts, (list, tuple)):
            return self.embed_documents(texts)
        return self.embed_query(texts)


@st.cache_resource
def load_embeddings():
    if SentenceTransformer is not None:
        try:
            return LocalSentenceTransformerEmbeddings(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
        except Exception:
            pass

    if HuggingFaceEmbeddings is not None:
        try:
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        except Exception:
            pass

    raise ImportError(
        "Unable to load embeddings. Install `langchain-huggingface`, `langchain-community`, or `sentence-transformers`."
    )
