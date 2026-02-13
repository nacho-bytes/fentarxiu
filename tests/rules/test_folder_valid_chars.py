"""Tests for FolderValidCharsRule."""

from string_checker import FolderValidCharsRule, InvalidFolderCharacterFailure


class TestFolderValidCharsRuleEmptyAndAllowed:
    """Empty string and allowed characters produce no failures."""

    def test_empty_string_returns_no_failures(self) -> None:
        rule = FolderValidCharsRule()
        assert rule.check("") == []

    def test_letters_including_accents_no_failures(self) -> None:
        rule = FolderValidCharsRule()
        assert rule.check("Obra_Joan") == []
        assert rule.check("àéç·") == []

    def test_ampersand_allowed(self) -> None:
        rule = FolderValidCharsRule()
        assert rule.check("Obra_Joan&Maria_Arr") == []

    def test_digits_space_and_filename_symbols_no_failures(self) -> None:
        rule = FolderValidCharsRule()
        assert rule.check("Work_Author1+Author2_Arranger") == []


class TestFolderValidCharsRuleDisallowed:
    """Disallowed characters produce InvalidFolderCharacterFailure."""

    def test_single_invalid_character(self) -> None:
        rule = FolderValidCharsRule()
        result = rule.check("Obra@Author")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderCharacterFailure)
        assert result[0].index == 4
        assert result[0].char == "@"

    def test_hash_produces_failure(self) -> None:
        rule = FolderValidCharsRule()
        result = rule.check("Work#Name")
        assert len(result) == 1
        assert result[0].char == "#"

    def test_emoji_produces_failure(self) -> None:
        rule = FolderValidCharsRule()
        result = rule.check("Obra🎵Author")
        assert len(result) == 1
        assert result[0].char == "🎵"

    def test_multiple_invalid_ordered_by_index(self) -> None:
        rule = FolderValidCharsRule()
        result = rule.check("a@b#c")
        assert len(result) == 2
        assert result[0].index == 1
        assert result[0].char == "@"
        assert result[1].index == 3
        assert result[1].char == "#"
