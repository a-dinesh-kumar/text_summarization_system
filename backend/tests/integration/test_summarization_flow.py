from app.services.summarization_service import SummarizationService
from tests.conftest import FakeSummarizer


def test_complete_service_flow_with_test_model(settings):
    """Exercise chunking, generation, reduction and response metadata together."""
    model = FakeSummarizer(chunk_size=6)
    service = SummarizationService(model, settings)

    result = service.summarize(
        "Alpha introduces the topic. Beta explains the details. "
        "Gamma describes the outcome. Delta provides the conclusion."
    )

    assert result["summary"] == "brief summary"
    assert result["initial_chunk_count"] >= 1
    assert result["total_generation_chunks"] >= result["initial_chunk_count"] + 1
    assert len(model.generate_calls) == result["total_generation_chunks"]
