"""Tests for FolderNameRule."""

from string_checker import FolderNameRule, InvalidFolderNameFailure


class TestFolderNameRulePasses:
    """Valid folder names produce no failures."""

    def test_work_and_single_author(self) -> None:
        rule = FolderNameRule()
        assert rule.check("Work_Author") == []

    def test_work_and_multiple_authors(self) -> None:
        rule = FolderNameRule()
        assert rule.check("Work_A+B") == []

    def test_work_author_single_arranger(self) -> None:
        rule = FolderNameRule()
        assert rule.check("Work_A_Arr") == []

    def test_work_author_multiple_arrangers(self) -> None:
        rule = FolderNameRule()
        assert rule.check("Work_A_Arr1+Arr2") == []


class TestFolderNameRuleFails:
    """Invalid folder names produce InvalidFolderNameFailure."""

    def test_empty_string(self) -> None:
        rule = FolderNameRule()
        result = rule.check("")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderNameFailure)
        assert "Expected format" in result[0].message

    def test_only_work_no_underscore(self) -> None:
        rule = FolderNameRule()
        result = rule.check("OnlyWork")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderNameFailure)

    def test_work_no_author(self) -> None:
        rule = FolderNameRule()
        result = rule.check("Work_")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderNameFailure)

    def test_invalid_character_in_format(self) -> None:
        rule = FolderNameRule()
        result = rule.check("*Author")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderNameFailure)

    def test_authors_part_empty_middle_underscore(self) -> None:
        rule = FolderNameRule()
        result = rule.check("Work__Arr")
        assert len(result) == 1
        assert isinstance(result[0], InvalidFolderNameFailure)
