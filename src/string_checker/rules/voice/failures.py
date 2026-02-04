"""Failure when voice digit in prefix is invalid."""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InvalidVoiceFailure(ValidationFailure):
    """Emitted when the voice digit in a prefix block is invalid."""

    code: FailureKind = attrs.field(default=FailureKind.VOICE_INVALID, init=False)
    instrument_range: int = attrs.field(
        metadata={"doc": "Range from the prefix block."}
    )
    prefix_code: str = attrs.field(metadata={"doc": "Code from the prefix block."})
    voice: int = attrs.field(metadata={"doc": "Voice value that failed validation."})
    message: str = attrs.field(metadata={"doc": "Description of the failure."})
