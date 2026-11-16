from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Text Summarization System API"
    app_version: str = "1.0.0"
    environment: str = "local"

    # Gemini Developer API configuration
    summarization_model: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_chunk_size_chars: int = 12_000
    gemini_temperature: float = 0.2

    # Document processing
    max_upload_size_mb: int = 15
    max_document_characters: int = 500_000
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    # Generation
    max_new_tokens: int = 140
    max_reduction_levels: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
