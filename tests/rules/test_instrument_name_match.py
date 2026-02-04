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

    def test_name_with_optional_voice_suffix_1(self) -> None:
        # (1, "06") -> "Clarinet"; _1 is optional voice suffix
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1061_Clarinet_1.pdf") == []

    def test_name_with_optional_voice_suffix_2(self) -> None:
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1062_Clarinet_2.pdf") == []

    def test_name_with_optional_voice_suffix_3(self) -> None:
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1063_Clarinet_3.pdf") == []

    def test_name_with_optional_voice_suffix_10(self) -> None:
        # (1, "06") -> "Clarinet"; _10 is optional voice suffix
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1060_Clarinet_10.pdf") == []

    def test_name_with_voice_suffix_trompeta_and_trombo(self) -> None:
        # (2, "02") -> "Trompeta", (2, "05") -> "Trombó"
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("2021+2050_Trompeta_2+Trombó_1.pdf") == []

    def test_name_with_optional_voice_suffix_principal(self) -> None:
        # (1, "06") -> "Clarinet"; _Principal is special word, same as voice suffix
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1060_Clarinet_Principal.pdf") == []

    def test_name_principal_and_voice_number_combined(self) -> None:
        # 1060+1061 -> Clarinet for both; Clarinet_Principal and Clarinet_1
        # both normalize to Clarinet
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        assert rule.check("1060+1061_Clarinet_Principal+Clarinet_1.pdf") == []


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

    def test_voice_suffix_but_base_name_mismatch(self) -> None:
        # (1, "00") -> "Flauta"; "Clarinet_1" normalizes to "Clarinet" != "Flauta"
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("1000_Clarinet_1.pdf")
        assert len(result) == 1
        assert isinstance(result[0], InstrumentNameMismatchFailure)
        assert result[0].received_name == "Clarinet_1"
        assert result[0].expected_name == "Flauta"


class TestInstrumentNameMatchRuleNotInCatalogue:
    """(instrument_range, prefix_code) not in catalogue -> no failure.

    for that block (skipped).
    """

    def test_unknown_range_code_skipped(self) -> None:
        # Catalogue has no (9, "99"). Parser: "9999_X.pdf" -> (9, "99", 9). Rule skips.
        rule = InstrumentNameMatchRule(catalogue=InstrumentCatalogue.default())
        result = rule.check("9999_Anything.pdf")
        assert result == []
