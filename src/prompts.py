"""Prompt templates for the RAG pipeline."""

SYSTEM_PROMPT = """
You are a precise question-answering assistant.
Answer only using the provided context.
If the answer is not present in the context, say exactly:
"I don't know based on the provided documents."
Keep the answer concise and factual.
Do not invent dates, names, locations, or events.
""".strip()


def build_rag_prompt(question: str, context: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
""".strip()
