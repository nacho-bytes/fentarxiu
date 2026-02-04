"""Tests for VoiceRule.

With the current parser, voice is always a single digit 0-9, so InvalidVoiceFailure
cannot be triggered from the rule without mocking. We test: parse None -> no failures;
valid parsed blocks (voice 0-9) -> no failures. InvalidVoiceFailure type/contract
is covered in test_failures.py.
"""

from string_checker import VoiceRule


class TestVoiceRuleParseNone:
    """When parse_filename returns None, VoiceRule adds no failures."""

    def test_empty_string_no_failures(self) -> None:
        rule = VoiceRule()
        assert rule.check("") == []

    def test_invalid_format_no_failures(self) -> None:
        rule = VoiceRule()
        assert rule.check("not_a_prefix_here") == []


class TestVoiceRuleValidBlocks:
    """When parse returns blocks with voice digit 0-9, no failures."""

    def test_single_block_valid_voice(self) -> None:
        rule = VoiceRule()
        assert rule.check("1010_Flautí.pdf") == []

    def test_multiple_blocks_valid_voices(self) -> None:
        rule = VoiceRule()
        assert rule.check("1000+2002+3099_Guia+Trompeta+Altres.pdf") == []
