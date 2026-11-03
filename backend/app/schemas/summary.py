from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    summary: str
    source_type: str
    source_name: str | None = None
    source_characters: int
    model: str
    model_key: str
    source_tokens: int
    initial_chunk_count: int
    total_generation_chunks: int
    reduction_levels: int
    processing_time_seconds: float
