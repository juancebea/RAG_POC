def test_retriever_returns_documents(fake_vector_store):
    retriever = fake_vector_store.as_retriever(search_kwargs={"k": 2})

    docs = retriever.invoke("When was Sha-Fu III released?")

    assert len(docs) == 2
    assert all(doc.page_content for doc in docs)


def test_retriever_includes_metadata(fake_vector_store):
    retriever = fake_vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke("What mixer does Sha-Fu use?")
    sources = [doc.metadata.get("source") for doc in docs]

    assert "shafu_live_setup.md" in sources
