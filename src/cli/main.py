"""Typer CLI for Fentarxiu: validate filenames in a Google Drive folder.

Loads .env for credential paths, connects to Drive, runs the string_checker
on each file name, and optionally writes a human-readable log in Valencian.
The log file is only created when the run completes successfully (no
credential or API errors).
"""

from pathlib import Path

from dotenv import load_dotenv
from returns.result import Failure
from typer import Option, Typer, echo

from cli.messages_ca import (
    MSG_CONNECTED,
    MSG_FILES_VALIDATED,
    MSG_FILES_WITH_ERRORS,
    MSG_LOG_SAVED,
    failures_to_lines_ca,
)
from drive_connection import (
    DriveConnectionError,
    list_file_names,
    load_credentials_and_build_service,
)
from string_checker import (
    Checker,
    InstrumentCatalogue,
    InstrumentNameMatchRule,
    PdfExtensionRule,
    PrefixRule,
    ValidCharsRule,
    VoiceRule,
)

app = Typer(
    help=(
        "Valida els noms dels fitxers d'una carpeta de Google Drive "
        "amb les regles de Fentarxiu."
    ),
)

_LOG_OPTION = Option(
    None,
    "--log",
    path_type=Path,
    help="Fitxer del log (valencià). Es crea si no existeix.",
)


def _build_checker() -> Checker:
    """Build a Checker with all five rules (including PdfExtensionRule)."""
    catalogue = InstrumentCatalogue.default()
    return Checker(
        rules=[
            ValidCharsRule(),
            PrefixRule(catalogue),
            InstrumentNameMatchRule(catalogue),
            VoiceRule(),
            PdfExtensionRule(),
        ]
    )


def _run(
    folder_id: str,
    *,
    recursive: bool,
    log_path: Path | None,
    verbose: bool,
) -> None:
    """Connect to Drive, validate filenames, and optionally write the log.

    On credential or API error, exits without creating or writing the log file.
    """
    load_dotenv()

    try:
        service = load_credentials_and_build_service()
    except DriveConnectionError as e:
        echo(f"Error de connexió amb Google Drive: {e}", err=True)
        raise SystemExit(1) from e

    echo(MSG_CONNECTED)

    checker = _build_checker()
    results: list[tuple[str, tuple]] = []  # (display_path, failures)
    total = 0

    try:
        for name, display_path in list_file_names(
            service, folder_id, recursive=recursive
        ):
            if verbose:
                echo(display_path)
            result = checker.check(name)
            total += 1
            if isinstance(result, Failure):
                results.append((display_path, result.failure()))
    except DriveConnectionError as e:
        echo(f"Error de Google Drive: {e}", err=True)
        raise SystemExit(1) from e

    echo(MSG_FILES_VALIDATED.format(n=total))
    if results:
        echo(MSG_FILES_WITH_ERRORS.format(n=len(results)))
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as f:
            for display_path, failures in results:
                f.write(f"Fitxer: {display_path}\n")
                f.writelines(line + "\n" for line in failures_to_lines_ca(failures))
                f.write("\n")
        echo(MSG_LOG_SAVED.format(path=log_path))


@app.callback(invoke_without_command=True)
def main(
    folder_id: str = Option(
        ...,
        "--folder-id",
        help="ID de la carpeta de Google Drive a explorar.",
    ),
    recursive: bool = Option(
        False,
        "--recursive",
        "-r",
        help="Explorar les subcarpetes recursivament.",
    ),
    log: Path | None = _LOG_OPTION,
    verbose: bool = Option(
        False,
        "--verbose",
        "-v",
        help="Mostrar cada fitxer a mesura que es valida.",
    ),
) -> None:
    """Valida els noms dels fitxers d'una carpeta de Google Drive."""
    _run(folder_id, recursive=recursive, log_path=log, verbose=verbose)
