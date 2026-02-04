"""Translate validation failures to human-readable messages in Valencian.

Used by the CLI log so non-technical users can understand what is wrong
with each filename. Does not modify failure classes; only reads their
attributes to build messages.
"""

from collections.abc import Sequence

from string_checker.failures.base import ValidationFailure
from string_checker.rules.instrument_name_match.failures import (
    InstrumentNameMismatchFailure,
)
from string_checker.rules.pdf_extension.failures import NotPdfFailure
from string_checker.rules.prefix.failures import InvalidPrefixFailure
from string_checker.rules.valid_chars.failures import InvalidCharacterFailure
from string_checker.rules.voice.failures import InvalidVoiceFailure

# Progress messages for the CLI (Valencian).
MSG_CONNECTED = "Connectat a Google Drive. Explorant la carpeta…"
MSG_FILES_VALIDATED = "Validats {n} fitxers."
MSG_FILES_WITH_ERRORS = "{n} fitxers amb errors."
MSG_LOG_SAVED = "Log guardat a {path}."


def failure_to_message_ca(failure: ValidationFailure) -> str:
    """Return a short, clear message in Valencian for the given failure.

    Dispatches on the concrete failure type and formats a non-technical
    description. Unknown failure types get a generic fallback message.

    Args:
        failure: A validation failure from the checker.

    Returns:
        A single-line message in Valencian.

    """
    if isinstance(failure, InvalidCharacterFailure):
        return f"Caràcter no permès: «{failure.char}» (posició {failure.index + 1})."
    if isinstance(failure, InvalidPrefixFailure):
        return f"El prefix del nom no és vàlid: {failure.message}"
    if isinstance(failure, InstrumentNameMismatchFailure):
        return (
            f"El nom de l'instrument «{failure.received_name}» no coincideix "
            f"amb el del catàleg (s'esperava «{failure.expected_name}»)."
        )
    if isinstance(failure, InvalidVoiceFailure):
        return f"La veu del bloc no és vàlida: {failure.message}"
    if isinstance(failure, NotPdfFailure):
        return (
            "El nom del fitxer ha d'acabar en .pdf."
            if "empty" not in failure.message.lower()
            else "El nom del fitxer no pot estar buit; ha d'acabar en .pdf."
        )
    return "El nom del fitxer no compleix les regles de validació."


def failures_to_lines_ca(failures: Sequence[ValidationFailure]) -> list[str]:
    """Convert a sequence of failures to a list of Valencian log lines.

    Each failure becomes one line prefixed with "  - " for use under
    a "Fitxer: <path>" header.

    Args:
        failures: Sequence of validation failures for one file.

    Returns:
        List of lines to write to the log (without trailing newlines).

    """
    return [f"  - {failure_to_message_ca(f)}" for f in failures]
