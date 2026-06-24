import streamlit as st

from src.rag_pipeline import answer_question


st.set_page_config(
    page_title="RAG Evaluation Lab",
    page_icon="🧪",
    layout="wide",
)

st.title("RAG Evaluation Lab")
st.caption(
    "Free local retrieval mode using Chroma + sentence-transformers. "
    "No OpenAI API key required."
)

question = st.text_input(
    "Ask a question about the knowledge base",
    placeholder="Example: Who are the members of Sha-Fu?",
)

k = st.slider(
    "Number of context chunks to retrieve",
    min_value=1,
    max_value=5,
    value=3,
)

if question:
    with st.spinner("Retrieving relevant context..."):
        result = answer_question(question=question, k=k)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Retrieved Context")

    for index, context in enumerate(result["contexts"], start=1):
        source = result["sources"][index - 1]

        source_name = source.get("source", "unknown source")
        chunk_id = source.get("chunk_id", "unknown chunk")

        with st.expander(f"Context chunk {index} | {source_name} | chunk {chunk_id}"):
            st.write(context)

    st.subheader("Sources")
    st.json(result["sources"])
else:
    st.info("Ask a question to retrieve grounded context from the local knowledge base.")