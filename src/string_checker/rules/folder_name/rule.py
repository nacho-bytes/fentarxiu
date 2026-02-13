"""Folder-name rule: WorkName_Author1+... or +_Arranger1+... (optional)."""

import attrs

from string_checker.data.folder_parser import parse_folder_name
from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.folder_name.failures import InvalidFolderNameFailure


@attrs.define
class FolderNameRule(RuleChecker):
    """String must match WorkName_Author1+Author2 or +_Arranger1+... (optional)."""

    name: str = "FolderNameRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures when folder name format is invalid."""
        if parse_folder_name(text) is None:
            return [
                InvalidFolderNameFailure(
                    message=(
                        "Expected format: WorkName_Author1+Author2 or "
                        "WorkName_Author1+Author2_Arranger1+Arranger2 "
                        "(authors required; arrangers optional)."
                    )
                )
            ]
        return []
