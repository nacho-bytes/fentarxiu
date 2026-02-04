"""Tests for parse_filename and ParsedFilename."""

import pytest

from string_checker.data import parse_filename


class TestParseFilenameReturnsNone:
    """parse_filename returns None for invalid or non-matching input."""

    def test_empty_string(self) -> None:
        assert parse_filename("") is None

    def test_no_prefix_match_no_leading_digits(self) -> None:
        assert parse_filename("abc_foo.pdf") is None

    def test_no_prefix_match_missing_underscore(self) -> None:
        assert parse_filename("1000") is None
        assert parse_filename("1000Flautí") is None

    def test_prefix_block_length_not_four(self) -> None:
        # Parser matches _PREFIX_RE first; full prefix is 4 digits + _ . So "123_"
        # would match and prefix_part = "123" which has len 3 -> None
        assert parse_filename("123_Ab.pdf") is None
        assert parse_filename("12345_Ab.pdf") is None

    def test_prefix_block_non_numeric(self) -> None:
        assert parse_filename("10a0_Ab.pdf") is None

    def test_names_count_mismatch_fewer_names_than_blocks(self) -> None:
        # One block, zero names (e.g. "1000_.pdf" -> rest empty -> names [])
        assert parse_filename("1000_.pdf") is None
        assert parse_filename("1000_") is None

    def test_names_count_mismatch_more_names_than_blocks(self) -> None:
        # One block, two names
        assert parse_filename("1000_A+B.pdf") is None


class TestParseFilenameReturnsParsedFilename:
    """parse_filename returns ParsedFilename for valid input."""

    def test_single_block_without_pdf(self) -> None:
        result = parse_filename("1010_Flautí")
        assert result is not None
        assert result.blocks == [(1, "01", 0)]
        assert result.names == ["Flautí"]

    def test_single_block_with_pdf(self) -> None:
        result = parse_filename("1010_Flautí.pdf")
        assert result is not None
        assert result.blocks == [(1, "01", 0)]
        assert result.names == ["Flautí"]

    def test_multiple_blocks(self) -> None:
        result = parse_filename("1000+2010_Guia+Trompeta.pdf")
        assert result is not None
        assert result.blocks == [(1, "00", 0), (2, "01", 0)]
        assert result.names == ["Guia", "Trompeta"]

    def test_blocks_range_code_voice_parsed_correctly(self) -> None:
        # instrument_range=2, code="02", voice=3
        result = parse_filename("2023_Trompeta.pdf")
        assert result is not None
        assert result.blocks == [(2, "02", 3)]
        assert result.names == ["Trompeta"]

    def test_names_trimmed(self) -> None:
        result = parse_filename("1000_  Flauta  .pdf")
        assert result is not None
        assert result.names == ["Flauta"]

    def test_names_with_plus_split_correctly(self) -> None:
        result = parse_filename("1000+2002_Flauta+Trompeta.pdf")
        assert result is not None
        assert len(result.blocks) == 2
        assert result.names == ["Flauta", "Trompeta"]


class TestParseFilenameEdgeCases:
    """Limit cases: empty name after underscore, etc."""

    def test_one_block_one_empty_name(self) -> None:
        # rest must split to one element that can be stripped (e.g. space only)
        result = parse_filename("1000_ .pdf")
        assert result is not None
        assert result.blocks == [(1, "00", 0)]
        assert result.names == [""]

    def test_parsed_filename_is_frozen(self) -> None:
        result = parse_filename("1000_Flauta.pdf")
        assert result is not None
        with pytest.raises(AttributeError):
            result.blocks = []  # type: ignore[misc]
