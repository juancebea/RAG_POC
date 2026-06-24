"""Document chunking helpers."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.config import settings


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into overlapping chunks.

    The chunk size is intentionally small for this portfolio project because
    the knowledge base is compact and we want precise retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

    return chunks
