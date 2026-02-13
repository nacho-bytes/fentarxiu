"""Folder valid-chars rule: same as sheet rule plus & for work folder names."""

import re

import attrs

from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.folder_valid_chars.failures import (
    InvalidFolderCharacterFailure,
)

# Letters (incl. accents via \w), digits, space, _ - + . · and &
_FOLDER_ALLOWED_RE = re.compile(
    r"[\w\s\-+.\u00B7&]",
    re.UNICODE,
)


@attrs.define
class FolderValidCharsRule(RuleChecker):
    """Allow characters for work folder names: sheet set plus &."""

    name: str = "FolderValidCharsRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures for each disallowed character."""
        failures: list[ValidationFailure] = []
        for i, char in enumerate(text):
            if _FOLDER_ALLOWED_RE.fullmatch(char) is None:
                failures.append(InvalidFolderCharacterFailure(index=i, char=char))
        return failures
