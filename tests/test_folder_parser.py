"""Tests for parse_folder_name and ParsedFolderName."""

import pytest

from string_checker.data import parse_folder_name


class TestParseFolderNameReturnsNone:
    """parse_folder_name returns None for invalid or non-matching input."""

    def test_empty_string(self) -> None:
        assert parse_folder_name("") is None

    def test_single_part_no_underscore(self) -> None:
        assert parse_folder_name("OnlyWork") is None

    def test_work_name_empty(self) -> None:
        assert parse_folder_name("_Author") is None
        assert parse_folder_name("  _Author") is None

    def test_authors_part_empty(self) -> None:
        assert parse_folder_name("Work_") is None
        assert parse_folder_name("Work_  ") is None

    def test_authors_part_only_plus_or_spaces(self) -> None:
        assert parse_folder_name("Work_+") is None
        assert parse_folder_name("Work_ + ") is None

    def test_two_parts_authors_empty_after_split(self) -> None:
        assert parse_folder_name("Work_  _Arr") is None


class TestParseFolderNameReturnsParsedFolderNameTwoParts:
    """parse_folder_name returns ParsedFolderName for valid two-segment input."""

    def test_work_and_single_author(self) -> None:
        result = parse_folder_name("Work_Author")
        assert result is not None
        assert result.work_name == "Work"
        assert result.authors == ["Author"]
        assert result.arrangers == []

    def test_work_and_multiple_authors(self) -> None:
        result = parse_folder_name("Obra_Joan+Maria")
        assert result is not None
        assert result.work_name == "Obra"
        assert result.authors == ["Joan", "Maria"]
        assert result.arrangers == []


class TestParseFolderNameReturnsParsedFolderNameThreeParts:
    """parse_folder_name returns ParsedFolderName for valid three-segment input."""

    def test_work_author_single_arranger(self) -> None:
        result = parse_folder_name("Work_A_B")
        assert result is not None
        assert result.work_name == "Work"
        assert result.authors == ["A"]
        assert result.arrangers == ["B"]

    def test_work_author_multiple_arrangers(self) -> None:
        result = parse_folder_name("Obra_Aut_Arr1+Arr2")
        assert result is not None
        assert result.work_name == "Obra"
        assert result.authors == ["Aut"]
        assert result.arrangers == ["Arr1", "Arr2"]

    def test_three_parts_arrangers_part_empty_yields_empty_arrangers(self) -> None:
        result = parse_folder_name("Work_Author_")
        assert result is not None
        assert result.work_name == "Work"
        assert result.authors == ["Author"]
        assert result.arrangers == []


class TestParseFolderNameEdgeCases:
    """Trim and frozen behaviour."""

    def test_names_trimmed(self) -> None:
        result = parse_folder_name("  Obra  _  Joan+Maria  ")
        assert result is not None
        assert result.work_name == "Obra"
        assert result.authors == ["Joan", "Maria"]

    def test_parsed_folder_name_is_frozen(self) -> None:
        result = parse_folder_name("Work_Author")
        assert result is not None
        with pytest.raises(AttributeError):
            result.work_name = "Other"  # type: ignore[misc]
