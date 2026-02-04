"""Validation failure types.

Re-exports the base failure kind and protocol. Import concrete failure
classes from their rule subpackages (e.g. InvalidCharacterFailure from
rules.valid_chars).
"""

from string_checker.failures.base import FailureKind, ValidationFailure

__all__ = ["FailureKind", "ValidationFailure"]
