"""Tests for ValidCharsRule."""

from string_checker import InvalidCharacterFailure, ValidCharsRule


class TestValidCharsRuleEmptyAndAllowed:
    """Empty string and allowed characters produce no failures."""

    def test_empty_string_returns_no_failures(self) -> None:
        rule = ValidCharsRule()
        assert rule.check("") == []

    def test_letters_including_catalan_no_failures(self) -> None:
        rule = ValidCharsRule()
        assert rule.check("Flautí") == []
        assert rule.check("àéç·") == []
        assert rule.check("CornAnglès") == []

    def test_digits_space_and_filename_symbols_no_failures(self) -> None:
        rule = ValidCharsRule()
        assert rule.check("1000_Flauta+Part.pdf") == []
        assert rule.check("  ") == []
        assert rule.check("a-b+c.d·e_1") == []


class TestValidCharsRuleDisallowed:
    """Disallowed characters produce InvalidCharacterFailure per character."""

    def test_single_invalid_character(self) -> None:
        rule = ValidCharsRule()
        result = rule.check("a🎵b")
        assert len(result) == 1
        assert isinstance(result[0], InvalidCharacterFailure)
        assert result[0].index == 1
        assert result[0].char == "🎵"

    def test_multiple_invalid_characters_ordered_by_index(self) -> None:
        rule = ValidCharsRule()
        result = rule.check("a@b#c")
        assert len(result) == 2
        assert result[0].index == 1
        assert result[0].char == "@"
        assert result[1].index == 3
        assert result[1].char == "#"

    def test_emoji_produces_failure(self) -> None:
        rule = ValidCharsRule()
        result = rule.check("😀")
        assert len(result) == 1
        assert result[0].char == "😀"
        assert result[0].index == 0


class TestValidCharsRuleAllowedOverride:
    """allowed_override callable is used when set."""

    def test_override_rejects_specific_char(self) -> None:
        def only_allow_a(c: str) -> bool:
            return c == "a"

        rule = ValidCharsRule(allowed_override=only_allow_a)
        result = rule.check("abc")
        assert len(result) == 2
        assert result[0].index == 1
        assert result[0].char == "b"
        assert result[1].index == 2
        assert result[1].char == "c"

    def test_override_accepts_all_no_failures(self) -> None:
        rule = ValidCharsRule(allowed_override=lambda _: True)
        assert rule.check("!@#🎵") == []
