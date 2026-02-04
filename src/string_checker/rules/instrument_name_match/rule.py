"""Instrument name must match the code in the prefix."""

import re

import attrs

from string_checker.data import InstrumentCatalogue, parse_filename
from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.instrument_name_match.failures import (
    InstrumentNameMismatchFailure,
)


def _normalize_name_for_match(name: str) -> str:
    """Strip optional voice suffix _X (X = 1, 2, 3, ...) or _Principal."""
    return re.sub(r"_(?:[1-9]\d*|Principal)$", "", name)


@attrs.define
class InstrumentNameMatchRule(RuleChecker):
    """Each instrument name in filename must match catalogue.

    for (instrument_range, prefix_code).
    """

    catalogue: InstrumentCatalogue = attrs.field()
    name: str = "InstrumentNameMatchRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures when a name does not match the catalogue."""
        failures: list[ValidationFailure] = []
        parsed = parse_filename(text)
        if parsed is None:
            return failures
        for (instrument_range, code, _voice), name in zip(
            parsed.blocks, parsed.names, strict=True
        ):
            expected = self.catalogue.get_name(instrument_range, code)
            if expected is None:
                continue
            normalized = _normalize_name_for_match(name)
            if normalized != expected:
                failures.append(
                    InstrumentNameMismatchFailure(
                        instrument_range=instrument_range,
                        prefix_code=code,
                        received_name=name,
                        expected_name=expected,
                    )
                )
        return failures
