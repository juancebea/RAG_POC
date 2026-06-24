import pytest
from src.rag_pipeline import format_context, answer_question


def test_format_context_joins_document_text(sample_documents):
    context = format_context(sample_documents)

    assert "---" in context
    assert "Sha-Fu released" in context
    assert "Soundcraft Ui24" in context


def test_answer_question_rejects_empty_question(fake_vector_store):
    with pytest.raises(ValueError):
        answer_question("", vector_store=fake_vector_store)
