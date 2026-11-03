import time
from app.core.config import Settings
from app.models.base import BaseSummarizer
from app.services.chunking import create_sentence_chunks


class SummarizationService:
    def __init__(self, summarizer: BaseSummarizer, settings: Settings) -> None:
        self.summarizer = summarizer
        self.settings = settings

    def summarize(self, text: str) -> dict:
        started = time.perf_counter()
        source_tokens = self.summarizer.count_tokens(text)

        current_text = text
        total_chunks = 0
        reduction_levels = 0

        chunks = create_sentence_chunks(current_text, self.summarizer)
        if not chunks:
            raise ValueError("No readable text was found to summarize.")

        total_chunks += len(chunks)
        summaries = [
            self.summarizer.generate(chunk, self.settings.max_new_tokens)
            for chunk in chunks
        ]
        summaries = [item for item in summaries if item]

        if not summaries:
            raise RuntimeError("The model did not generate a summary.")

        # Reduce intermediate summaries until the combined text fits one chunk.
        while self.summarizer.count_tokens(" ".join(summaries)) > self.summarizer.chunk_size:
            reduction_levels += 1
            if reduction_levels > self.settings.max_reduction_levels:
                raise RuntimeError(
                    "The document required too many reduction passes. "
                    "Try a shorter document or a smaller chunk size."
                )

            combined = " ".join(summaries)
            reduction_chunks = create_sentence_chunks(combined, self.summarizer)
            if len(reduction_chunks) <= 1:
                # Safety fallback: the chunker should normally make progress.
                break

            total_chunks += len(reduction_chunks)
            new_summaries = [
                self.summarizer.generate(chunk, self.settings.max_new_tokens)
                for chunk in reduction_chunks
            ]
            new_summaries = [item for item in new_summaries if item]

            if not new_summaries or len(" ".join(new_summaries)) >= len(combined):
                # Avoid an infinite loop if a model repeats or expands its input.
                summaries = new_summaries or summaries
                break
            summaries = new_summaries

        final_input = " ".join(summaries)
        if self.summarizer.count_tokens(final_input) > self.summarizer.chunk_size:
            raise RuntimeError(
                "The selected model did not sufficiently reduce the intermediate summaries. "
                "Try a shorter document or adjust the generation/chunk settings."
            )

        final_summary = self.summarizer.generate(
            final_input, self.settings.max_new_tokens
        )

        elapsed = round(time.perf_counter() - started, 3)
        return {
            "summary": final_summary,
            "model": self.summarizer.display_name,
            "model_key": self.summarizer.model_key,
            "source_tokens": source_tokens,
            "initial_chunk_count": len(chunks),
            "total_generation_chunks": total_chunks + 1,
            "reduction_levels": reduction_levels,
            "processing_time_seconds": elapsed,
        }
