import pytest

import app.models.factory as factory
from app.core.config import Settings


def test_factory_creates_gemini_adapter(monkeypatch):
    captured = {}

    class FakeAdapter:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(
        factory,
        "GeminiSummarizer",
        FakeAdapter,
    )

    result = factory.create_summarizer(
        Settings(
            summarization_model="gemini",
            gemini_api_key="test-key",
        )
    )

    assert isinstance(result, FakeAdapter)
    assert captured["model_key"] == "gemini"
    assert captured["model_name"] == "gemini-3.5-flash-lite"
    assert captured["api_key"] == "test-key"
    assert captured["chunk_size_chars"] == 12_000


def test_factory_rejects_missing_api_key():
    with pytest.raises(
        ValueError,
        match="GEMINI_API_KEY",
    ):
        factory.create_summarizer(
            Settings(
                summarization_model="gemini",
                gemini_api_key="",
            )
        )


def test_factory_rejects_unsupported_model():
    with pytest.raises(
        ValueError,
        match="Unsupported SUMMARIZATION_MODEL",
    ):
        factory.create_summarizer(
            Settings(
                summarization_model="unknown",
                gemini_api_key="test-key",
            )
        )


def test_factory_rejects_invalid_chunk_size():
    with pytest.raises(
        ValueError,
        match="GEMINI_CHUNK_SIZE_CHARS",
    ):
        factory.create_summarizer(
            Settings(
                summarization_model="gemini",
                gemini_api_key="test-key",
                gemini_chunk_size_chars=50,
            )
        )
