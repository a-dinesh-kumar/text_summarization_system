import pytest

import app.models.factory as factory
from app.core.config import Settings


def test_factory_creates_bart_adapter(monkeypatch):
    captured = {}

    class FakeAdapter:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(factory, "HuggingFaceSummarizer", FakeAdapter)
    result = factory.create_summarizer(Settings(summarization_model="bart"))

    assert isinstance(result, FakeAdapter)
    assert captured["model_key"] == "bart"
    assert captured["model_name"] == "facebook/bart-large-cnn"
    assert captured["display_name"] == "BART-large-CNN"


def test_factory_creates_flan_t5_adapter(monkeypatch):
    captured = {}

    class FakeAdapter:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(factory, "HuggingFaceSummarizer", FakeAdapter)
    factory.create_summarizer(Settings(summarization_model="flan_t5"))

    assert captured["model_key"] == "flan_t5"
    assert captured["model_name"] == "google/flan-t5-small"
    assert captured["prompt_prefix"] == "summarize: "


def test_factory_rejects_unsupported_model():
    with pytest.raises(ValueError, match="Unsupported SUMMARIZATION_MODEL"):
        factory.create_summarizer(Settings(summarization_model="unknown"))
