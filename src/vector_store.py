from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import settings


def get_embeddings():
    """
    Returns the embedding function used by Chroma.

    This local provider avoids OpenAI API billing/quota during ingestion
    and retrieval.
    """
    if settings.embedding_provider.lower() == "local":
        return HuggingFaceEmbeddings(
            model_name=settings.local_embedding_model
        )

    raise ValueError(
        f"Unsupported embedding provider: {settings.embedding_provider}. "
        "Use EMBEDDING_PROVIDER=local."
    )


def normalize_chunks(chunks: list) -> list[Document]:
    """
    Accepts either LangChain Document objects or dict-based chunks.

    This keeps the vector store compatible with both chunking styles:
    - Document(page_content=..., metadata=...)
    - {"content": "...", "metadata": {...}}
    """
    normalized_documents = []

    for chunk in chunks:
        if isinstance(chunk, Document):
            normalized_documents.append(chunk)
        elif isinstance(chunk, dict):
            normalized_documents.append(
                Document(
                    page_content=chunk["content"],
                    metadata=chunk.get("metadata", {}),
                )
            )
        else:
            raise TypeError(
                f"Unsupported chunk type: {type(chunk)}. "
                "Expected Document or dict."
            )

    return normalized_documents


def build_vector_store(chunks: list) -> Chroma:
    documents = normalize_chunks(chunks)

    return Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        persist_directory=settings.chroma_persist_directory,
    )


def load_vector_store() -> Chroma:
    return Chroma(
        persist_directory=settings.chroma_persist_directory,
        embedding_function=get_embeddings(),
    )