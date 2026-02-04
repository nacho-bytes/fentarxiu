"""Failure when the filename does not end with .pdf."""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class NotPdfFailure(ValidationFailure):
    """Emitted when the filename does not have the .pdf extension."""

    code: FailureKind = attrs.field(default=FailureKind.NOT_PDF, init=False)
    message: str = attrs.field(
        metadata={
            "doc": "Description of the failure (e.g. missing or wrong extension)."
        }
    )
