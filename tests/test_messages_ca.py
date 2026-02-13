"""Tests for failure_to_message_ca with folder failure types."""

from cli.messages_ca import failure_to_message_ca
from string_checker import (
    InvalidFolderCharacterFailure,
    InvalidFolderNameFailure,
)


def test_invalid_folder_name_failure_message() -> None:
    """failure_to_message_ca returns Valencian message for InvalidFolderNameFailure."""
    failure = InvalidFolderNameFailure(message="Expected format: Work_Author.")
    result = failure_to_message_ca(failure)
    assert "carpeta" in result
    assert "Expected format" in result or "Work_Author" in result


def test_invalid_folder_character_failure_message() -> None:
    """failure_to_message_ca returns Valencian for InvalidFolderCharacterFailure."""
    failure = InvalidFolderCharacterFailure(index=2, char="@")
    result = failure_to_message_ca(failure)
    assert "carpeta" in result
    assert "«@»" in result
    assert "posició 3" in result
