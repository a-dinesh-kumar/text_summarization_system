import re
from app.models.base import BaseSummarizer


def split_sentences(text: str) -> list[str]:
    """Split text into sentences while preserving punctuation."""

    normalized = re.sub(r"\s+", " ", text).strip()

    if not normalized:
        return []

    parts = re.split(
        r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])",
        normalized,
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def split_long_sentence(
    sentence: str,
    max_chars: int,
) -> list[str]:
    """Split an unusually long sentence into character-limited pieces."""

    words = sentence.split()

    pieces: list[str] = []
    current = ""

    for word in words:
        if len(word) > max_chars:
            if current:
                pieces.append(current)
                current = ""

            for start in range(0, len(word), max_chars):
                pieces.append(word[start:start + max_chars])

            continue

        candidate = f"{current} {word}".strip()

        if current and len(candidate) > max_chars:
            pieces.append(current)
            current = word
        else:
            current = candidate

    if current:
        pieces.append(current)

    return pieces


def create_sentence_chunks(
    text: str,
    summarizer: BaseSummarizer,
    overlap_sentences: int = 1,
) -> list[str]:
    sentences = split_sentences(text)

    if not sentences:
        return []

    budget = summarizer.chunk_size_chars

    chunks: list[str] = []
    current: list[str] = []

    for sentence in sentences:
        if len(sentence) > budget:
            if current:
                chunks.append(" ".join(current))
                current = []

            chunks.extend(
                split_long_sentence(sentence, budget)
            )
            continue

        candidate = " ".join(current + [sentence])

        if current and len(candidate) > budget:
            chunks.append(" ".join(current))

            overlap = (
                current[-overlap_sentences:]
                if overlap_sentences > 0
                else []
            )

            overlap_text = " ".join(overlap)
            overlap_candidate = (
                f"{overlap_text} {sentence}".strip()
            )

            if (
                overlap
                and len(overlap_candidate) <= budget
            ):
                current = list(overlap)
            else:
                current = []

        current.append(sentence)

    if current:
        final_chunk = " ".join(current)

        if not chunks or final_chunk != chunks[-1]:
            chunks.append(final_chunk)

    return chunks
