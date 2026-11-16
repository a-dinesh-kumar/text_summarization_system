from app.core.config import Settings
from app.models.base import BaseSummarizer
from app.models.gemini_summarizer import GeminiSummarizer


def create_summarizer(settings: Settings) -> BaseSummarizer:
    key = settings.summarization_model.strip().lower()

    if key != "gemini":
        raise ValueError(
            f"Unsupported SUMMARIZATION_MODEL='{key}'. "
            "Choose: gemini."
        )

    if not settings.gemini_api_key.strip():
        raise ValueError(
            "GEMINI_API_KEY must be configured before starting "
            "the Gemini summarization service."
        )

    if settings.gemini_chunk_size_chars < 100:
        raise ValueError(
            "GEMINI_CHUNK_SIZE_CHARS must be at least 100."
        )

    return GeminiSummarizer(
        model_key="gemini",
        model_name=settings.gemini_model,
        display_name=settings.gemini_model,
        api_key=settings.gemini_api_key,
        chunk_size_chars=settings.gemini_chunk_size_chars,
        temperature=settings.gemini_temperature,
    )
