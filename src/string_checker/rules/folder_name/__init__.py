"""Folder-name validation rule."""

from string_checker.rules.folder_name.failures import InvalidFolderNameFailure
from string_checker.rules.folder_name.rule import FolderNameRule

__all__ = ["FolderNameRule", "InvalidFolderNameFailure"]
