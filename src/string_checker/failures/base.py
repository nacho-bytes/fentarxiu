"""Base types for validation failures.

Defines the failure kind enum and the abstract base class that all concrete
failure types must inherit from and implement so the checker can aggregate
and expose them uniformly.
"""

from abc import ABC, abstractmethod
from enum import Enum


class FailureKind(Enum):
    """Kind of validation failure.

    Used as a discriminant for failure types. Extend this enum when adding
    new rule-specific failure kinds.
    """

    VALID_CHARS = "valid_chars"
    PREFIX = "prefix"
    INSTRUMENT_NAME_MISMATCH = "instrument_name_mismatch"
    VOICE_INVALID = "voice_invalid"
    NOT_PDF = "not_pdf"


class ValidationFailure(ABC):
    """Abstract base for a validation failure.

    Concrete failures (e.g. InvalidCharacterFailure) must inherit from this
    and implement the abstract property ``code`` so consumers can identify
    the failure kind. Additional attributes are rule-specific.
    """

    @property
    @abstractmethod
    def code(self) -> FailureKind:
        """Failure kind identifier."""
        ...
