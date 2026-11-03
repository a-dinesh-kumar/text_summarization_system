from abc import ABC, abstractmethod
from typing import Any


class BaseSummarizer(ABC):
    """Common interface used by the API, regardless of the underlying model."""

    model_key: str
    display_name: str
    max_input_tokens: int
    chunk_size: int

    @abstractmethod
    def load(self) -> None:
        """Load tokenizer and model into memory."""

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens using this model's tokenizer."""

    @abstractmethod
    def generate(self, text: str, max_new_tokens: int) -> str:
        """Generate one summary for a text chunk."""
