"""Tests for PrefixRule."""

from string_checker import InstrumentCatalogue, PrefixRule


class TestPrefixRuleEmptyAndPattern:
    """Empty string and invalid prefix pattern."""

    def test_empty_string(self) -> None:
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("")
        assert len(result) == 1
        assert result[0].message == "Filename is empty."

    def test_no_prefix_pattern(self) -> None:
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("abc_foo.pdf")
        assert len(result) == 1
        assert "4-digit blocks" in result[0].message
        assert "_" in result[0].message

    def test_missing_underscore(self) -> None:
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("1000")
        assert len(result) == 1
        assert "4-digit blocks" in result[0].message


class TestPrefixRuleParseFailure:
    """Format that parser rejects."""

    def test_names_count_mismatch_parse_fails(self) -> None:
        # Parser returns None when names count != blocks count
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("1000_.pdf")
        assert len(result) == 1
        msg = result[0].message
        assert "could not be parsed" in msg or "parsed" in msg


class TestPrefixRuleUnknownRangeCode:
    """(instrument_range, prefix_code) not in catalogue."""

    def test_unknown_range_code_single_block(self) -> None:
        # (9, "99") not in catalogue. "9999_Unknown.pdf" yields one failure.
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("9999_Unknown.pdf")
        assert len(result) == 1
        assert "Unknown (instrument_range, prefix_code)" in result[0].message
        msg = result[0].message
        assert "(9, '99')" in msg or ("9" in msg and "99" in msg)

    def test_multiple_blocks_one_unknown(self) -> None:
        # 1000 in catalogue, 9999 not. One failure for unknown block.
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("1000+9999_Flauta+Other.pdf")
        assert len(result) == 1
        assert "Unknown (instrument_range, prefix_code)" in result[0].message


class TestPrefixRuleValid:
    """Valid prefix with (instrument_range, prefix_code) in catalogue."""

    def test_valid_single_block(self) -> None:
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1010_Flautí.pdf") == []

    def test_valid_multiple_blocks_all_known(self) -> None:
        rule = PrefixRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1000+2002_Flauta+Trompeta.pdf") == []
