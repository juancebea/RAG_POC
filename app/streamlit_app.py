import streamlit as st
from src.rag_pipeline import answer_question
from src.vector_store import load_vector_store

st.set_page_config(page_title="RAG Evaluation Lab", page_icon="🧪", layout="wide")

st.title("RAG Evaluation Lab")
st.caption("A small Q&A app with retrieval, grounded answers, and evaluation-ready outputs.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Retrieved chunks", min_value=1, max_value=6, value=3)
    st.markdown(
        """
        **How to use**
        1. Ask a question about the knowledge base.
        2. Review the generated answer.
        3. Inspect the retrieved context and sources.
        """
    )

question = st.text_input("Ask a question", placeholder="Example: When was Sha-Fu III released?")

if question:
    try:
        vector_store = load_vector_store()
        result = answer_question(question=question, vector_store=vector_store, k=top_k)

        st.subheader("Answer")
        st.write(result["answer"])

        left, right = st.columns([2, 1])

        with left:
            st.subheader("Retrieved context")
            for index, context in enumerate(result["contexts"], start=1):
                with st.expander(f"Context chunk {index}"):
                    st.write(context)

        with right:
            st.subheader("Sources")
            st.json(result["sources"])

    except Exception as exc:
        st.error(str(exc))
        st.info("Run `python -m src.ingest` before starting the app.")
