import pytest
from app.core.config import Settings
from app.models.base import BaseSummarizer

class FakeSummarizer(BaseSummarizer):
    def __init__(
        self,
        chunk_size_chars=12_000,
        fail_generation=False,
    ):
        self.model_key = "fake"
        self.display_name = "Fake Test Summarizer"
        self.chunk_size_chars = chunk_size_chars
        self.fail_generation = fail_generation
        self.loaded = False
        self.generate_calls = []

    def load(self):
        self.loaded = True

    def count_tokens(self, text):
        return len(text.split())

    def generate(self, text, max_new_tokens):
        if self.fail_generation:
            raise RuntimeError("Simulated model failure")

        self.generate_calls.append(text)
        return "brief summary"


@pytest.fixture
def fake_summarizer():
    return FakeSummarizer()


@pytest.fixture
def settings():
    return Settings(
        summarization_model="gemini",
        gemini_api_key="test-api-key",
        gemini_model="gemini-3.5-flash-lite",
        gemini_chunk_size_chars=12_000,
        max_upload_size_mb=15,
        max_document_characters=500_000,
        max_new_tokens=30,
        max_reduction_levels=8,
    )
