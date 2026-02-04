"""Voice digit in each prefix block must be valid (0-9)."""

import attrs

from string_checker.data import parse_filename
from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.voice.failures import InvalidVoiceFailure

MAX_VOICE_DIGIT = 9


@attrs.define
class VoiceRule(RuleChecker):
    """Validates that the voice digit in each prefix block is 0-9."""

    name: str = "VoiceRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failures when a block's voice digit is not 0-9."""
        failures: list[ValidationFailure] = []
        parsed = parse_filename(text)
        if parsed is None:
            return failures
        for instrument_range, code, voice in parsed.blocks:
            if not (0 <= voice <= MAX_VOICE_DIGIT):
                failures.append(
                    InvalidVoiceFailure(
                        instrument_range=instrument_range,
                        prefix_code=code,
                        voice=voice,
                        message=f"Voice must be a single digit 0-9, got {voice}.",
                    )
                )
        return failures
