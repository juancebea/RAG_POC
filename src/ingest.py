"""Load Markdown documents, chunk them, and persist them in ChromaDB."""

from pathlib import Path
import shutil
from langchain_core.documents import Document
from src.chunking import chunk_documents
from src.config import settings
from src.vector_store import build_vector_store


def load_markdown_documents(docs_dir: str | None = None) -> list[Document]:
    base_dir = Path(docs_dir or settings.docs_dir)

    if not base_dir.exists():
        raise FileNotFoundError(f"Docs directory does not exist: {base_dir}")

    documents: list[Document] = []

    for file_path in sorted(base_dir.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=content,
                metadata={"source": file_path.name},
            )
        )

    if not documents:
        raise ValueError(f"No Markdown documents found in {base_dir}")

    return documents


def ingest_documents(reset: bool = True) -> int:
    if reset:
        shutil.rmtree(settings.chroma_persist_dir, ignore_errors=True)

    documents = load_markdown_documents()
    chunks = chunk_documents(documents)
    build_vector_store(chunks)
    return len(chunks)


if __name__ == "__main__":
    chunk_count = ingest_documents(reset=True)
    print(f"Ingested {chunk_count} chunks into {settings.chroma_persist_dir}")
