from app.services.chunking import create_sentence_chunks, split_sentences
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
    assert create_sentence_chunks("   ", summarizer) == []


def test_sentence_chunking_respects_token_budget_and_overlaps():
    summarizer = FakeSummarizer(chunk_size=5)
    text = "First sentence. Second sentence. Third sentence."

    chunks = create_sentence_chunks(text, summarizer, overlap_sentences=1)

    assert len(chunks) == 2
    assert all(summarizer.count_tokens(chunk) <= 5 for chunk in chunks)
    assert "First sentence." in chunks[0]
    assert "Second sentence." in chunks[0]
    assert "Second sentence." in chunks[1]
    assert "Third sentence." in chunks[1]


def test_long_sentence_is_split_into_token_windows():
    summarizer = FakeSummarizer(chunk_size=3)
    chunks = create_sentence_chunks(
        "one two three four five six seven eight",
        summarizer,
        overlap_sentences=0,
    )

    assert chunks == ["one two three", "four five six", "seven eight"]
