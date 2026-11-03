import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.models.base import BaseSummarizer


class HuggingFaceSummarizer(BaseSummarizer):
    def __init__(
        self,
        *,
        model_key: str,
        model_name: str,
        display_name: str,
        max_input_tokens: int,
        chunk_size: int,
        prompt_prefix: str = "",
        num_beams: int = 4,
        no_repeat_ngram_size: int = 3,
        length_penalty: float = 1.0,
    ) -> None:
        self.model_key = model_key
        self.model_name = model_name
        self.display_name = display_name
        self.max_input_tokens = max_input_tokens
        self.chunk_size = chunk_size
        self.prompt_prefix = prompt_prefix
        self.num_beams = num_beams
        self.no_repeat_ngram_size = no_repeat_ngram_size
        self.length_penalty = length_penalty

        self.tokenizer = None
        self.model = None
        self.device = torch.device("cpu")

    def load(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()

    def _prepare(self, text: str) -> str:
        return f"{self.prompt_prefix}{text}" if self.prompt_prefix else text

    def count_tokens(self, text: str) -> int:
        prepared = self._prepare(text)
        return len(self.tokenizer.encode(prepared, add_special_tokens=False))

    def generate(self, text: str, max_new_tokens: int) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Summarization model has not been loaded.")

        prepared = self._prepare(text)
        inputs = self.tokenizer(
            prepared,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_input_tokens,
        )
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.inference_mode():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=self.num_beams,
                no_repeat_ngram_size=self.no_repeat_ngram_size,
                length_penalty=self.length_penalty,
                early_stopping=True,
            )

        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
