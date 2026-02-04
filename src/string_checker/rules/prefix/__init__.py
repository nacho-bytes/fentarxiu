"""Prefix rule: filename must start with valid code blocks."""

from string_checker.rules.prefix.failures import InvalidPrefixFailure
from string_checker.rules.prefix.rule import PrefixRule

__all__ = ["InvalidPrefixFailure", "PrefixRule"]
