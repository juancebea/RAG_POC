"""Vector-store creation and loading."""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from src.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.openai_embedding_model)


def build_vector_store(chunks: list[Document]) -> Chroma:
    """Create and persist a Chroma vector store from document chunks."""
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=settings.chroma_collection_name,
        persist_directory=settings.chroma_persist_dir,
    )
    return vector_store


def load_vector_store() -> Chroma:
    """Load an existing persisted Chroma vector store."""
    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_persist_dir,
    )
