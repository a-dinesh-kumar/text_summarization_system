import re
from app.models.base import BaseSummarizer


def split_sentences(text: str) -> list[str]:
    """
    Lightweight sentence splitter. It preserves sentence punctuation and avoids
    requiring a downloaded NLTK model at container startup. It is a practical
    baseline, not a linguistic parser; unusual abbreviations may split imperfectly.
    """
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    # Split after sentence-ending punctuation when followed by whitespace and
    # an uppercase/digit/opening quote. Also split at paragraph boundaries.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", normalized)
    return [part.strip() for part in parts if part.strip()]


def create_sentence_chunks(
    text: str,
    summarizer: BaseSummarizer,
    overlap_sentences: int = 1,
) -> list[str]:
    sentences = split_sentences(text)
    if not sentences:
        return []

    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0
    budget = summarizer.chunk_size

    for sentence in sentences:
        sentence_tokens = summarizer.count_tokens(sentence)

        # Split a single unusually long sentence into token windows.
        if sentence_tokens > budget:
            if current:
                chunks.append(" ".join(current))
                current = []
                current_tokens = 0

            token_ids = summarizer.tokenizer.encode(
                sentence, add_special_tokens=False
            )
            start = 0
            while start < len(token_ids):
                window = token_ids[start : start + budget]
                piece = summarizer.tokenizer.decode(
                    window, skip_special_tokens=True
                ).strip()
                if piece:
                    chunks.append(piece)
                start += budget
            continue

        if current and current_tokens + sentence_tokens > budget:
            chunks.append(" ".join(current))
            overlap = current[-overlap_sentences:] if overlap_sentences else []
            overlap_tokens = sum(summarizer.count_tokens(item) for item in overlap)
            # Keep overlap only when it still leaves room for the next sentence.
            if overlap_tokens + sentence_tokens <= budget:
                current = list(overlap)
                current_tokens = overlap_tokens
            else:
                current = []
                current_tokens = 0

        current.append(sentence)
        current_tokens += sentence_tokens

    if current:
        final_chunk = " ".join(current)
        if not chunks or final_chunk != chunks[-1]:
            chunks.append(final_chunk)

    return chunks
