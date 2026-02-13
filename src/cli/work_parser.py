"""Typer CLI for Fentarxiu: validate folder names in Google Drive.

Accepts a list of Drive folder IDs, lists direct child folders (no recursion),
validates each folder name against WorkName_Author+..._Arranger+..., and
optionally writes a human-readable log in Valencian.
"""

from pathlib import Path

from dotenv import load_dotenv
from returns.result import Failure
from typer import Option, Typer, echo

from cli.messages_ca import (
    MSG_CONNECTED,
    MSG_FOLDERS_VALIDATED,
    MSG_FOLDERS_WITH_ERRORS,
    MSG_LOG_SAVED,
    failures_to_lines_ca,
)
from drive_connection import (
    DriveConnectionError,
    list_subfolder_names,
    load_credentials_and_build_service,
)
from string_checker import Checker, FolderNameRule, FolderValidCharsRule

app = Typer(
    help=(
        "Valida els noms de les carpetes (fills directes) de les carpetes "
        "de Google Drive indicades. Format: NomObra_Autor1+Autor2_Arreglista1+..."
    ),
)

_LOG_OPTION = Option(
    None,
    "--log",
    path_type=Path,
    help="Fitxer del log (valencià). Es crea si no existeix.",
)
_FOLDER_ID_OPTION = Option(
    ...,
    "--folder-id",
    help="ID de la carpeta de Google Drive. Es pot repetir per diverses carpetes.",
)
_VERBOSE_OPTION = Option(
    False,
    "--verbose",
    "-v",
    help="Mostrar cada carpeta a mesura que es valida.",
)


def _build_checker() -> Checker:
    return Checker(
        rules=[
            FolderValidCharsRule(),
            FolderNameRule(),
        ]
    )


def _run(
    folder_ids: list[str],
    *,
    log_path: Path | None,
    verbose: bool,
) -> None:
    load_dotenv()

    try:
        service = load_credentials_and_build_service()
    except DriveConnectionError as e:
        echo(f"Error de connexió amb Google Drive: {e}", err=True)
        raise SystemExit(1) from e

    echo(MSG_CONNECTED)

    checker = _build_checker()
    results: list[tuple[str, tuple]] = []
    total = 0

    try:
        for folder_id in folder_ids:
            for name, display_path in list_subfolder_names(service, folder_id):
                if verbose:
                    echo(display_path)
                result = checker.check(name)
                total += 1
                if isinstance(result, Failure):
                    results.append((display_path, result.failure()))
    except DriveConnectionError as e:
        echo(f"Error de Google Drive: {e}", err=True)
        raise SystemExit(1) from e

    echo(MSG_FOLDERS_VALIDATED.format(n=total))
    if results:
        echo(MSG_FOLDERS_WITH_ERRORS.format(n=len(results)))
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as f:
            for display_path, failures in results:
                f.write(f"Carpeta: {display_path}\n")
                f.writelines(line + "\n" for line in failures_to_lines_ca(failures))
                f.write("\n")
        echo(MSG_LOG_SAVED.format(path=log_path))


@app.callback(invoke_without_command=True)
def main(
    folder_id: list[str] = _FOLDER_ID_OPTION,
    log: Path | None = _LOG_OPTION,
    verbose: bool = _VERBOSE_OPTION,
) -> None:
    """Valida els noms de les carpetes fills directes de les carpetes indicades."""
    _run(folder_id, log_path=log, verbose=verbose)
