"""Failure when instrument name in filename does not match the code."""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InstrumentNameMismatchFailure(ValidationFailure):
    """Name in filename does not match catalogue for (instrument_range, code)."""

    code: FailureKind = attrs.field(
        default=FailureKind.INSTRUMENT_NAME_MISMATCH, init=False
    )
    instrument_range: int = attrs.field(
        metadata={"doc": "Range from the prefix block."}
    )
    prefix_code: str = attrs.field(metadata={"doc": "Code from the prefix block."})
    received_name: str = attrs.field(metadata={"doc": "Name found in the filename."})
    expected_name: str = attrs.field(
        metadata={"doc": "Name from catalogue for (instrument_range, code)."}
    )
