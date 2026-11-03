import importlib.util
import sys
import types

import pytest

# The application imports the Hugging Face adapter at startup. For local
# test environments without Transformers installed, provide import-only
# placeholders. No test in this suite performs real model inference.
if importlib.util.find_spec("transformers") is None:
    transformers_stub = types.ModuleType("transformers")
    transformers_stub.AutoModelForSeq2SeqLM = object
    transformers_stub.AutoTokenizer = object
    sys.modules["transformers"] = transformers_stub

from app.core.config import Settings
from app.models.base import BaseSummarizer


class FakeTokenizer:
    def encode(self, text, add_special_tokens=False):
        return text.split()

    def decode(self, token_ids, skip_special_tokens=True):
        return " ".join(token_ids)


class FakeSummarizer(BaseSummarizer):
    def __init__(self, chunk_size=500, fail_generation=False):
        self.model_key = "fake"
        self.display_name = "Fake Test Summarizer"
        self.max_input_tokens = 512
        self.chunk_size = chunk_size
        self.tokenizer = FakeTokenizer()
        self.loaded = False
        self.fail_generation = fail_generation
        self.generate_calls = []

    def load(self):
        self.loaded = True

    def count_tokens(self, text):
        return len(self.tokenizer.encode(text))

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
        summarization_model="bart",
        max_upload_size_mb=15,
        max_document_characters=500_000,
        max_new_tokens=30,
        max_reduction_levels=8,
    )
