"""Valid-chars rule and its failure type.

Use ValidCharsRule to restrict input to allowed characters. Invalid
characters produce InvalidCharacterFailure instances with index and span.
"""

from string_checker.rules.valid_chars.failures import InvalidCharacterFailure
from string_checker.rules.valid_chars.rule import ValidCharsRule

__all__ = ["InvalidCharacterFailure", "ValidCharsRule"]
