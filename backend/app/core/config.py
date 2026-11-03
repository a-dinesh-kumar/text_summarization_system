from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Text Summarization System API"
    app_version: str = "1.0.0"
    environment: str = "local"

    # Supported values: bart, flan_t5
    summarization_model: str = "bart"

    hf_home: str = "/app/.cache/huggingface"
    max_upload_size_mb: int = 15
    max_document_characters: int = 500_000
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    max_new_tokens: int = 140
    num_beams: int = 4
    no_repeat_ngram_size: int = 3
    length_penalty: float = 1.0
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
