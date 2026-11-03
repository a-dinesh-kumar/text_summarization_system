from app.core.config import Settings
from app.models.base import BaseSummarizer
from app.models.huggingface_summarizer import HuggingFaceSummarizer


MODEL_CONFIGS = {
    "bart": {
        "model_name": "facebook/bart-large-cnn",
        "display_name": "BART-large-CNN",
        "max_input_tokens": 1024,
        "chunk_size": 900,
        "prompt_prefix": "",
    },
    "flan_t5": {
        "model_name": "google/flan-t5-small",
        "display_name": "FLAN-T5-small",
        "max_input_tokens": 512,
        "chunk_size": 440,
        "prompt_prefix": "summarize: ",
    },
}


def create_summarizer(settings: Settings) -> BaseSummarizer:
    key = settings.summarization_model.strip().lower()
    if key not in MODEL_CONFIGS:
        supported = ", ".join(MODEL_CONFIGS)
        raise ValueError(
            f"Unsupported SUMMARIZATION_MODEL='{key}'. Choose one of: {supported}."
        )

    config = MODEL_CONFIGS[key]
    return HuggingFaceSummarizer(
        model_key=key,
        **config,
        num_beams=settings.num_beams,
        no_repeat_ngram_size=settings.no_repeat_ngram_size,
        length_penalty=settings.length_penalty,
    )
