"""Failure for the folder valid-chars rule.

Emitted by FolderValidCharsRule when a character in the folder name is not
allowed.
"""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InvalidFolderCharacterFailure(ValidationFailure):
    """Failure emitted when a character is not allowed in a folder name.

    Produced by FolderValidCharsRule for each character that is not in the
    allowed set (letters incl. accents, digits, space, _, -, +, ., ·, &).
    """

    code: FailureKind = attrs.field(default=FailureKind.FOLDER_VALID_CHARS, init=False)
    index: int = attrs.field(
        metadata={"doc": "Zero-based index of the invalid character."}
    )
    char: str = attrs.field(metadata={"doc": "The character that was rejected."})
