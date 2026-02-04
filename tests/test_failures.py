"""Tests for FailureKind and concrete ValidationFailure types."""

from string_checker import (
    FailureKind,
    InstrumentNameMismatchFailure,
    InvalidCharacterFailure,
    InvalidPrefixFailure,
    InvalidVoiceFailure,
    NotPdfFailure,
    ValidationFailure,
)


class TestFailureKind:
    """FailureKind enum has expected members."""

    def test_valid_chars_exists(self) -> None:
        assert FailureKind.VALID_CHARS.value == "valid_chars"

    def test_prefix_exists(self) -> None:
        assert FailureKind.PREFIX.value == "prefix"

    def test_instrument_name_mismatch_exists(self) -> None:
        assert FailureKind.INSTRUMENT_NAME_MISMATCH.value == "instrument_name_mismatch"

    def test_voice_invalid_exists(self) -> None:
        assert FailureKind.VOICE_INVALID.value == "voice_invalid"

    def test_not_pdf_exists(self) -> None:
        assert FailureKind.NOT_PDF.value == "not_pdf"


class TestConcreteFailuresCodeAndInstance:
    """Each concrete failure has correct code and can be instantiated."""

    def test_invalid_character_failure(self) -> None:
        f = InvalidCharacterFailure(index=0, char="!")
        assert isinstance(f, ValidationFailure)
        assert f.code == FailureKind.VALID_CHARS
        assert f.index == 0
        assert f.char == "!"

    def test_invalid_prefix_failure(self) -> None:
        f = InvalidPrefixFailure(message="Filename is empty.")
        assert isinstance(f, ValidationFailure)
        assert f.code == FailureKind.PREFIX
        assert f.message == "Filename is empty."

    def test_invalid_voice_failure(self) -> None:
        f = InvalidVoiceFailure(
            instrument_range=1,
            prefix_code="00",
            voice=10,
            message="Voice must be 0-9.",
        )
        assert isinstance(f, ValidationFailure)
        assert f.code == FailureKind.VOICE_INVALID
        assert f.instrument_range == 1
        assert f.prefix_code == "00"
        assert f.voice == 10
        assert f.message == "Voice must be 0-9."

    def test_instrument_name_mismatch_failure(self) -> None:
        f = InstrumentNameMismatchFailure(
            instrument_range=1,
            prefix_code="01",
            received_name="Flauta",
            expected_name="Flautí",
        )
        assert isinstance(f, ValidationFailure)
        assert f.code == FailureKind.INSTRUMENT_NAME_MISMATCH
        assert f.instrument_range == 1
        assert f.prefix_code == "01"
        assert f.received_name == "Flauta"
        assert f.expected_name == "Flautí"

    def test_not_pdf_failure(self) -> None:
        f = NotPdfFailure(message="Filename must end with .pdf.")
        assert isinstance(f, ValidationFailure)
        assert f.code == FailureKind.NOT_PDF
        assert f.message == "Filename must end with .pdf."
