import time
from app.core.config import Settings
from app.models.base import BaseSummarizer
from app.services.chunking import create_sentence_chunks


class SummarizationService:
    def __init__(
        self,
        summarizer: BaseSummarizer,
        settings: Settings,
    ) -> None:
        self.summarizer = summarizer
        self.settings = settings

    def summarize(self, text: str) -> dict:
        started = time.perf_counter()

        # One remote token-count request for the original document.
        source_tokens = self.summarizer.count_tokens(text)

        chunks = create_sentence_chunks(
            text,
            self.summarizer,
        )

        if not chunks:
            raise ValueError(
                "No readable text was found to summarize."
            )

        total_chunks = len(chunks)

        summaries = [
            self.summarizer.generate(
                chunk,
                self.settings.max_new_tokens,
            )
            for chunk in chunks
        ]

        summaries = [
            item.strip()
            for item in summaries
            if item and item.strip()
        ]

        if not summaries:
            raise RuntimeError(
                "The model did not generate a summary."
            )

        reduction_levels = 0

        # Reduce summaries until they fit within one chunk.
        while len(" ".join(summaries)) > (
            self.summarizer.chunk_size_chars
        ):
            reduction_levels += 1

            if (
                reduction_levels
                > self.settings.max_reduction_levels
            ):
                raise RuntimeError(
                    "The document required too many reduction "
                    "passes. Try a shorter document or a larger "
                    "chunk size."
                )

            combined = " ".join(summaries)

            reduction_chunks = create_sentence_chunks(
                combined,
                self.summarizer,
                overlap_sentences=0,
            )

            if len(reduction_chunks) <= 1:
                raise RuntimeError(
                    "Unable to split intermediate summaries "
                    "within the configured chunk size."
                )

            total_chunks += len(reduction_chunks)

            new_summaries = [
                self.summarizer.generate(
                    chunk,
                    self.settings.max_new_tokens,
                )
                for chunk in reduction_chunks
            ]

            new_summaries = [
                item.strip()
                for item in new_summaries
                if item and item.strip()
            ]

            if not new_summaries:
                raise RuntimeError(
                    "The model returned empty reduction summaries."
                )

            reduced_text = " ".join(new_summaries)

            if len(reduced_text) >= len(combined):
                raise RuntimeError(
                    "The model did not sufficiently reduce "
                    "the intermediate summaries."
                )

            summaries = new_summaries

        final_input = " ".join(summaries)

        final_summary = self.summarizer.generate(
            final_input,
            self.settings.max_new_tokens,
        )

        if not final_summary or not final_summary.strip():
            raise RuntimeError(
                "The model returned an empty final summary."
            )

        elapsed = round(
            time.perf_counter() - started,
            3,
        )

        return {
            "summary": final_summary.strip(),
            "model": self.summarizer.display_name,
            "model_key": self.summarizer.model_key,
            "source_tokens": source_tokens,
            "initial_chunk_count": len(chunks),
            "total_generation_chunks": total_chunks + 1,
            "reduction_levels": reduction_levels,
            "processing_time_seconds": elapsed,
        }
