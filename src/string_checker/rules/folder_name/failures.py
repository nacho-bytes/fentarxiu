"""Failure for the folder-name rule."""

import attrs

from string_checker.failures.base import FailureKind, ValidationFailure


@attrs.frozen
class InvalidFolderNameFailure(ValidationFailure):
    """Emitted when the folder name does not match the expected format.

    Expected format: WorkName_Author1+Author2_Arranger1+Arranger2
    """

    code: FailureKind = attrs.field(default=FailureKind.FOLDER_NAME, init=False)
    message: str = attrs.field(
        metadata={"doc": "Description of what is wrong with the folder name."}
    )
