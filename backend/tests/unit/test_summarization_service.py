import pytest
from app.services.summarization_service import SummarizationService
from tests.conftest import FakeSummarizer


def test_summarize_returns_expected_metadata(settings):
    summarizer = FakeSummarizer()
    service = SummarizationService(summarizer, settings)

    result = service.summarize(
        "This is a short test document."
    )

    assert result["summary"] == "brief summary"
    assert result["model"] == "Fake Test Summarizer"
    assert result["model_key"] == "fake"
    assert result["source_tokens"] == 6
    assert result["initial_chunk_count"] == 1
    assert result["total_generation_chunks"] == 2
    assert result["reduction_levels"] == 0
    assert result["processing_time_seconds"] >= 0


def test_long_input_uses_map_reduce(settings):
    summarizer = FakeSummarizer(
        chunk_size_chars=30,
    )

    service = SummarizationService(
        summarizer,
        settings,
    )

    result = service.summarize(
        "one two three four five six seven eight nine ten "
        "eleven twelve thirteen fourteen fifteen"
    )

    assert result["initial_chunk_count"] == 4
    assert result["reduction_levels"] == 1
    assert result["total_generation_chunks"] == 7
    assert len(summarizer.generate_calls) == 7
    assert result["summary"] == "brief summary"


def test_empty_input_is_rejected(settings):
    service = SummarizationService(
        FakeSummarizer(),
        settings,
    )

    with pytest.raises(
        ValueError,
        match="No readable text",
    ):
        service.summarize("   ")


def test_generation_failure_is_propagated(settings):
    service = SummarizationService(
        FakeSummarizer(fail_generation=True),
        settings,
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated model failure",
    ):
        service.summarize(
            "This is a test document with enough content."
        )
