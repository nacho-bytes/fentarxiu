"""Prefix rule: filename must start with valid instrument_range+code+voice blocks."""

import re

import attrs

from string_checker.data import InstrumentCatalogue, parse_filename
from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.prefix.failures import InvalidPrefixFailure

_PREFIX_PATTERN = re.compile(r"^\d{4}(?:\+\d{4})*_")


@attrs.define
class PrefixRule(RuleChecker):
    """String must start with one or more valid 4-digit blocks and underscore.

    Each block is (instrument_range, code, voice); (instrument_range, code)
    must exist in the catalogue.
    """

    catalogue: InstrumentCatalogue = attrs.field()
    name: str = "PrefixRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures for invalid or missing prefix."""
        failures: list[ValidationFailure] = []
        if not text:
            failures.append(InvalidPrefixFailure(message="Filename is empty."))
            return failures
        if not _PREFIX_PATTERN.match(text):
            failures.append(
                InvalidPrefixFailure(
                    message=(
                        "Filename must start with one or more 4-digit blocks "
                        "(instrument_range+code+voice) followed by '_'."
                    )
                )
            )
            return failures
        parsed = parse_filename(text)
        if parsed is None:
            failures.append(
                InvalidPrefixFailure(message="Prefix or name part could not be parsed.")
            )
            return failures
        for instrument_range, code, _voice in parsed.blocks:
            if not self.catalogue.has(instrument_range, code):
                failures.append(
                    InvalidPrefixFailure(
                        message=f"Unknown (instrument_range, prefix_code) "
                        f"({instrument_range}, {code}) in catalogue."
                    )
                )
        return failures
