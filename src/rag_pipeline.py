"""Main RAG pipeline.

The pipeline retrieves top-k chunks from ChromaDB and asks an LLM to answer
only from those chunks.
"""

from typing import Any
from langchain_openai import ChatOpenAI
from src.config import settings
from src.prompts import build_rag_prompt
from src.vector_store import load_vector_store


def format_context(documents: list[Any]) -> str:
    return "\n\n---\n\n".join(doc.page_content for doc in documents)


def answer_question(question: str, vector_store: Any | None = None, k: int | None = None) -> dict[str, Any]:
    if not question or not question.strip():
        raise ValueError("Question must not be empty")

    store = vector_store or load_vector_store()
    top_k = k or settings.rag_top_k

    retriever = store.as_retriever(search_kwargs={"k": top_k})
    retrieved_docs = retriever.invoke(question)

    context = format_context(retrieved_docs)
    prompt = build_rag_prompt(question=question, context=context)

    llm = ChatOpenAI(model=settings.openai_model, temperature=0)
    response = llm.invoke(prompt)

    return {
        "question": question,
        "answer": response.content,
        "contexts": [doc.page_content for doc in retrieved_docs],
        "sources": [doc.metadata for doc in retrieved_docs],
    }
