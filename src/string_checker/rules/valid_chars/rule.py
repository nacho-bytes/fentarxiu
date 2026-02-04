"""Valid-chars rule: Catalan letters, filename symbols, no emojis.

Opinionated: the rule knows the allowed character set (regex-based).
"""

import re
from collections.abc import Callable

import attrs

from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.valid_chars.failures import InvalidCharacterFailure

# One allowed char: letters (incl. Catalan), digits, space, _ - + . and ·
# \w in Unicode mode = letters, digits, underscore (covers à, é, ç, etc.)
# We add space, -, +, ., and · (U+00B7)
_ALLOWED_CHAR_RE = re.compile(
    r"[\w\s\-+.\u00B7]",  # \w = letters/digits/_ ; \s = space
    re.UNICODE,
)


def _is_allowed_char(char: str) -> bool:
    return _ALLOWED_CHAR_RE.fullmatch(char) is not None


@attrs.define
class ValidCharsRule(RuleChecker):
    """Allow Catalan letters, digits, filename symbols; no emojis.

    Opinionated: allowed set is fixed (letters incl. accents, ç, ·, digits,
    space, _, -, +, .). Optional override for tests.
    """

    name: str = "ValidCharsRule"
    """Rule name for display or logging."""

    _allowed_override: Callable[[str], bool] | None = attrs.field(
        default=None, alias="allowed_override"
    )
    """Optional (char -> bool) override for testing; if set, used instead."""

    def _is_allowed(self, char: str) -> bool:
        if self._allowed_override is not None:
            return self._allowed_override(char)
        return _is_allowed_char(char)

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures for each disallowed character."""
        failures: list[ValidationFailure] = []
        for i, char in enumerate(text):
            if not self._is_allowed(char):
                failures.append(InvalidCharacterFailure(index=i, char=char))
        return failures
