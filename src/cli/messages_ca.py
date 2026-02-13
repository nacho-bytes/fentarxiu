"""Translate validation failures to human-readable messages in Valencian.

Used by the CLI log so non-technical users can understand what is wrong
with each filename. Does not modify failure classes; only reads their
attributes to build messages.
"""

from collections.abc import Callable, Sequence

from string_checker.failures.base import ValidationFailure
from string_checker.rules.folder_name.failures import InvalidFolderNameFailure
from string_checker.rules.folder_valid_chars.failures import (
    InvalidFolderCharacterFailure,
)
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
MSG_FOLDERS_VALIDATED = "Validades {n} carpetes."
MSG_FOLDERS_WITH_ERRORS = "{n} carpetes amb errors."
MSG_LOG_SAVED = "Log guardat a {path}."

_FALLBACK_MESSAGE = "El nom del fitxer no compleix les regles de validació."

_FormatterMap = list[tuple[type[ValidationFailure], Callable[[ValidationFailure], str]]]


def _format_failure_message(failure: ValidationFailure) -> str | None:
    """Return Valencian message for a known failure type, or None for fallback."""
    formatters: _FormatterMap = [
        (
            InvalidFolderNameFailure,
            lambda f: f"El nom de la carpeta no és vàlid: {f.message}",
        ),
        (
            InvalidFolderCharacterFailure,
            lambda f: (
                f"Caràcter no permès al nom de la carpeta: «{f.char}» "
                f"(posició {f.index + 1})."
            ),
        ),
        (
            InvalidCharacterFailure,
            lambda f: f"Caràcter no permès: «{f.char}» (posició {f.index + 1}).",
        ),
        (
            InvalidPrefixFailure,
            lambda f: f"El prefix del nom no és vàlid: {f.message}",
        ),
        (
            InstrumentNameMismatchFailure,
            lambda f: (
                f"El nom de l'instrument «{f.received_name}» no coincideix "
                f"amb el del catàleg (s'esperava «{f.expected_name}»)."
            ),
        ),
        (InvalidVoiceFailure, lambda f: f"La veu del bloc no és vàlida: {f.message}"),
        (
            NotPdfFailure,
            lambda f: (
                "El nom del fitxer ha d'acabar en .pdf."
                if "empty" not in f.message.lower()
                else "El nom del fitxer no pot estar buit; ha d'acabar en .pdf."
            ),
        ),
    ]
    for failure_type, formatter in formatters:
        if isinstance(failure, failure_type):
            return formatter(failure)
    return None


def failure_to_message_ca(failure: ValidationFailure) -> str:
    """Return a short, clear message in Valencian for the given failure.

    Dispatches on the concrete failure type and formats a non-technical
    description. Unknown failure types get a generic fallback message.

    Args:
        failure: A validation failure from the checker.

    Returns:
        A single-line message in Valencian.

    """
    msg = _format_failure_message(failure)
    return msg if msg is not None else _FALLBACK_MESSAGE


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
