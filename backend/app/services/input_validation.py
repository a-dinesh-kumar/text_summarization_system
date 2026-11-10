import re

MIN_MEANINGFUL_CHARACTERS = 50


def count_meaningful_characters(text: str) -> int:
    """
    Count Unicode letters and numbers.
    Ignore whitespace and punctuation.
    """
    return len(re.findall(r"[\w]", text, flags=re.UNICODE)) - len(
        re.findall(r"_", text)
    )


def validate_meaningful_text(text: str) -> None:
    """
    Reject empty, punctuation-only and very short input.
    """
    meaningful_count = count_meaningful_characters(text)

    if meaningful_count == 0:
        raise ValueError(
            "Please provide meaningful text. Spaces and punctuation alone "
            "cannot be summarized."
        )

    if meaningful_count < MIN_MEANINGFUL_CHARACTERS:
        raise ValueError(
            f"Please provide at least {MIN_MEANINGFUL_CHARACTERS} "
            f"meaningful characters. Current input contains "
            f"{meaningful_count}."
        )