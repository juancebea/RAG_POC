from pathlib import Path
from src.ingest import load_markdown_documents
from src.chunking import chunk_documents


def test_load_markdown_documents_reads_files(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "example.md").write_text("# Example\n\nA test document.", encoding="utf-8")

    docs = load_markdown_documents(str(docs_dir))

    assert len(docs) == 1
    assert docs[0].metadata["source"] == "example.md"
    assert "A test document" in docs[0].page_content


def test_chunk_documents_preserves_source_metadata(sample_documents):
    chunks = chunk_documents(sample_documents)

    assert chunks
    assert all("source" in chunk.metadata for chunk in chunks)
