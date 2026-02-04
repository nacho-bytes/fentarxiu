"""Failure for the prefix rule (filename must start with valid code blocks)."""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InvalidPrefixFailure(ValidationFailure):
    """Emitted when the filename does not start with a valid prefix pattern.

    Prefix must be one or more 4-digit blocks (instrument_range+code+voice)
    separated by '+', followed by '_', and each (instrument_range, code)
    must exist in the catalogue.
    """

    code: FailureKind = attrs.field(default=FailureKind.PREFIX, init=False)
    message: str = attrs.field(
        metadata={"doc": "Description of what is wrong with the prefix."}
    )
