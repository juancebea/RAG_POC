from src.config import settings
from src.vector_store import load_vector_store


SYSTEM_PROMPT = """
You are a question-answering assistant.

Answer only using the provided context.
If the answer is not in the context, say:
"I don't know based on the provided documents."

Keep the answer concise.
"""


def build_prompt(question: str, contexts: list[str]) -> str:
    context_text = "\n\n".join(contexts)

    return f"""
{SYSTEM_PROMPT}

Context:
{context_text}

Question:
{question}

Answer:
""".strip()


def generate_answer(question: str, contexts: list[str]) -> str:
    if settings.llm_provider.lower() == "retrieval_only":
        return (
            "Retrieval-only mode is enabled. "
            "The most relevant context chunks are shown below. "
            "Use them as the grounded evidence for the answer."
        )

    if settings.llm_provider.lower() == "ollama":
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=settings.ollama_model,
            temperature=0,
        )

        prompt = build_prompt(question, contexts)
        response = llm.invoke(prompt)
        return response.content

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}. "
        "Use LLM_PROVIDER=retrieval_only or LLM_PROVIDER=ollama."
    )


def answer_question(question: str, k: int = 3) -> dict:
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    retrieved_docs = retriever.invoke(question)

    contexts = [doc.page_content for doc in retrieved_docs]
    sources = [doc.metadata for doc in retrieved_docs]

    if not contexts:
        answer = "I don't know based on the provided documents."
    else:
        answer = generate_answer(question, contexts)

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "sources": sources,
    }