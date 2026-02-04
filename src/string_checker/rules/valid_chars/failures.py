"""Concrete failure for the valid-chars rule.

Emitted by ValidCharsRule when a character in the input string is not
allowed (not in the set or failing the predicate).
"""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InvalidCharacterFailure(ValidationFailure):
    """Failure emitted when a character is not allowed.

    Produced by ValidCharsRule for each character that is not in the
    allowed set or does not pass the allowed predicate. Use ``index``
    or ``span`` to locate the character in the original string.
    """

    code: FailureKind = attrs.field(default=FailureKind.VALID_CHARS, init=False)
    index: int = attrs.field(
        metadata={"doc": "Zero-based index of the invalid character."}
    )
    char: str = attrs.field(metadata={"doc": "The character that was rejected."})
