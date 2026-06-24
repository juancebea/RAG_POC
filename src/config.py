from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    docs_directory: str = "docs"
    chroma_persist_directory: str = "chroma_db"

    chunk_size: int = 500
    chunk_overlap: int = 100

    embedding_provider: str = "local"
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    llm_provider: str = "retrieval_only"
    ollama_model: str = "llama3.2:3b"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()