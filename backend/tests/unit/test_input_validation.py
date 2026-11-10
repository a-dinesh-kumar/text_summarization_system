import pytest

from app.services.input_validation import (
    count_meaningful_characters,
    validate_meaningful_text,
)


def test_whitespace_only_input_is_rejected():
    with pytest.raises(ValueError, match="meaningful text"):
        validate_meaningful_text("     \n\t  ")


def test_punctuation_only_input_is_rejected():
    with pytest.raises(ValueError, match="meaningful text"):
        validate_meaningful_text('""""!!!...')


def test_short_input_is_rejected():
    with pytest.raises(ValueError, match="at least 50"):
        validate_meaningful_text("This is a short sentence.")


def test_exactly_50_meaningful_characters_is_accepted():
    text = "A" * 50

    validate_meaningful_text(text)


def test_more_than_50_meaningful_characters_is_accepted():
    text = (
        "This is a meaningful paragraph containing enough "
        "information to test the summarization input validation."
    )

    validate_meaningful_text(text)


def test_punctuation_does_not_count_as_meaningful_characters():
    assert count_meaningful_characters("Hello!!! 123...") == 8


def test_unicode_letters_are_counted():
    assert count_meaningful_characters("こんにちは") == 5