from abc import ABC, abstractmethod


class BaseSummarizer(ABC):
    """Common interface for summarization providers."""

    model_key: str
    display_name: str
    chunk_size_chars: int

    @abstractmethod
    def load(self) -> None:
        """Initialize the summarization provider."""

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Return the source token count."""

    @abstractmethod
    def generate(self, text: str, max_new_tokens: int) -> str:
        """Generate a summary for the supplied text."""
