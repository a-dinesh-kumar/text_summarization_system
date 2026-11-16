from app.services.chunking import (
    create_sentence_chunks,
    split_long_sentence,
    split_sentences,
)
from tests.conftest import FakeSummarizer


def test_split_sentences_preserves_sentence_content():
    sentences = split_sentences(
        "First sentence. Second sentence! Third sentence?"
    )

    assert sentences == [
        "First sentence.",
        "Second sentence!",
        "Third sentence?",
    ]


def test_empty_text_returns_no_chunks():
    summarizer = FakeSummarizer()

    assert create_sentence_chunks(
        "   ",
        summarizer,
    ) == []


def test_sentence_chunking_respects_character_budget():
    summarizer = FakeSummarizer(chunk_size_chars=35)

    text = (
        "First sentence. "
        "Second sentence. "
        "Third sentence."
    )

    chunks = create_sentence_chunks(text, summarizer)

    assert len(chunks) == 2
    assert all(
        len(chunk) <= 35
        for chunk in chunks
    )

    assert "First sentence." in chunks[0]
    assert "Second sentence." in chunks[0]
    assert "Second sentence." in chunks[1]
    assert "Third sentence." in chunks[1]


def test_long_sentence_is_split_into_character_windows():
    summarizer = FakeSummarizer(chunk_size_chars=13)

    chunks = create_sentence_chunks(
        "one two three four five six seven eight",
        summarizer,
        overlap_sentences=0,
    )

    assert chunks == [
        "one two three",
        "four five six",
        "seven eight",
    ]

    assert all(
        len(chunk) <= 13
        for chunk in chunks
    )


def test_individual_long_word_is_split():
    pieces = split_long_sentence(
        "extraordinarilylongword",
        max_chars=8,
    )

    assert pieces == [
        "extraord",
        "inarilyl",
        "ongword",
    ]
