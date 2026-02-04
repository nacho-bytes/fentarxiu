"""Tests for InstrumentNameMatchRule."""

from string_checker import (
    InstrumentCatalogue,
    InstrumentNameMatchRule,
    InstrumentNameMismatchFailure,
)


class TestInstrumentNameMatchRuleParseNone:
    """When parse_filename returns None, no failures."""

    def test_invalid_format_no_failures(self) -> None:
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("not_a_prefix") == []


class TestInstrumentNameMatchRuleMatch:
    """Name matches catalogue for (instrument_range, code) -> no failure."""

    def test_correct_name_single_block(self) -> None:
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1010_Flautí.pdf") == []

    def test_correct_names_multiple_blocks(self) -> None:
        # (1,"00")->Flauta, (2,"02")->Trompeta; blocks 1000 and 2020
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1000+2020_Flauta+Trompeta.pdf") == []


class TestInstrumentNameMatchRuleMismatch:
    """Name does not match catalogue -> InstrumentNameMismatchFailure."""

    def test_wrong_name_single_block(self) -> None:
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        # (1, "01") -> "Flautí" in catalogue
        result = rule.check("1010_Flauta.pdf")
        assert len(result) == 1
        assert isinstance(result[0], InstrumentNameMismatchFailure)
        assert result[0].instrument_range == 1
        assert result[0].prefix_code == "01"
        assert result[0].received_name == "Flauta"
        assert result[0].expected_name == "Flautí"

    def test_multiple_blocks_one_mismatch(self) -> None:
        # (1,"00")->Flauta, (2,"02")->Trompeta; blocks 1000 and 2020
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("1000+2020_Flauta+WrongName.pdf")
        assert len(result) == 1
        assert result[0].received_name == "WrongName"
        assert result[0].expected_name == "Trompeta"


class TestInstrumentNameMatchRuleNotInCatalogue:
    """(instrument_range, prefix_code) not in catalogue -> no failure.

    for that block (skipped).
    """

    def test_unknown_range_code_skipped(self) -> None:
        # Catalogue has no (9, "99"). Parser: "9999_X.pdf" -> (9, "99", 9). Rule skips.
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("9999_Anything.pdf")
        assert result == []
