import pytest
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import DeterministicFakeEmbedding


@pytest.fixture
def sample_documents():
    return [
        Document(
            page_content="Sha-Fu released the album III on September 13, 2024. The album explores time and space.",
            metadata={"source": "shafu_discography.md"},
        ),
        Document(
            page_content="Sha-Fu uses a Soundcraft Ui24 mixer for live routing and monitor mixes.",
            metadata={"source": "shafu_live_setup.md"},
        ),
        Document(
            page_content="Sha-Fu is an instrumental progressive doom metal band from Córdoba, Argentina.",
            metadata={"source": "shafu_band_bio.md"},
        ),
    ]


@pytest.fixture
def fake_vector_store(sample_documents):
    embeddings = DeterministicFakeEmbedding(size=1536)
    return InMemoryVectorStore.from_documents(sample_documents, embeddings)
