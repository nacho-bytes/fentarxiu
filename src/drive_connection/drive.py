"""Google Drive API: credential loading and recursive file listing.

Uses OAuth 2.0 Desktop app flow. Credential and token paths are read from
environment variables (e.g. after loading .env with python-dotenv).
"""

import os
from collections.abc import Iterator
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scope for listing file metadata (names, ids, mime types).
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# Default paths relative to current working directory.
DEFAULT_CREDENTIALS_PATH = "credentials.json"
DEFAULT_TOKEN_PATH = "token.json"

# Mime type for Drive folders.
FOLDER_MIMETYPE = "application/vnd.google-apps.folder"


class DriveConnectionError(Exception):
    """Raised when credentials are missing, invalid, or the API call fails."""


def _get_credentials_path() -> Path:
    """Return the path to the OAuth client credentials JSON."""
    path = os.environ.get("FENTARXIU_CREDENTIALS_JSON", DEFAULT_CREDENTIALS_PATH)
    return Path(path).expanduser()


def _get_token_path() -> Path:
    """Return the path to the stored token JSON."""
    path = os.environ.get("FENTARXIU_TOKEN_JSON", DEFAULT_TOKEN_PATH)
    return Path(path).expanduser()


def load_credentials_and_build_service(
    credentials_path: Path | None = None,
    token_path: Path | None = None,
) -> object:
    """Load OAuth credentials and build the Drive v3 service.

    Uses token_path if it exists and is valid; otherwise runs the
    installed app flow (browser) and saves the token to token_path.
    Callers should catch DriveConnectionError for missing/invalid
    credentials or HttpError for API failures.

    Args:
        credentials_path: Override for the client secrets JSON path.
        token_path: Override for the stored token JSON path.

    Returns:
        The Google Drive API v3 service object (build('drive', 'v3', ...)).

    Raises:
        DriveConnectionError: If credentials file is missing or auth fails.

    """
    creds_path = credentials_path or _get_credentials_path()
    tok_path = token_path or _get_token_path()

    if not creds_path.is_file():
        msg = (
            f"Credentials file not found: {creds_path}. "
            "Set FENTARXIU_CREDENTIALS_JSON or place credentials.json in cwd."
        )
        raise DriveConnectionError(msg)

    creds: Credentials | None = None
    if tok_path.is_file():
        try:
            creds = Credentials.from_authorized_user_file(str(tok_path), SCOPES)
        except (ValueError, OSError) as e:
            msg = f"Could not load token from {tok_path}: {e}"
            raise DriveConnectionError(msg) from e

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                msg = f"Token refresh failed: {e}"
                raise DriveConnectionError(msg) from e
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_path), SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                msg = (
                    f"OAuth flow failed: {e}. "
                    "Ensure credentials.json is a valid Desktop app OAuth client."
                )
                raise DriveConnectionError(msg) from e
        # Save token for next run.
        tok_path.parent.mkdir(parents=True, exist_ok=True)
        tok_path.write_text(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
    except Exception as e:
        msg = f"Failed to build Drive service: {e}"
        raise DriveConnectionError(msg) from e
    return service


def list_file_names(
    service: object,
    folder_id: str,
    *,
    recursive: bool,
) -> Iterator[tuple[str, str]]:
    """Yield (file_name, display_path) for each file under the given folder.

    Folders are never yielded; they are only entered when recursive is True.
    display_path is the file name alone at top level, or "Parent/Child/name"
    when recursive, for use in the log.

    Args:
        service: The Drive v3 service from load_credentials_and_build_service.
        folder_id: The Drive folder ID to list.
        recursive: If True, descend into subfolders and prefix paths.

    Yields:
        (file_name, display_path) for each non-folder item.

    """
    yield from _list_file_names_impl(
        service, folder_id, recursive=recursive, prefix_parts=()
    )


def list_subfolder_names(
    service: object,
    folder_id: str,
) -> Iterator[tuple[str, str]]:
    """Yield (folder_name, display_path) for each direct child folder.

    Only direct children are listed; no recursion. display_path is the
    folder name (no path prefix).

    Args:
        service: The Drive v3 service from load_credentials_and_build_service.
        folder_id: The Drive folder ID to list.

    Yields:
        (folder_name, display_path) for each direct subfolder.

    """
    page_token: str | None = None
    while True:
        try:
            response = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents and mimeType = '{FOLDER_MIMETYPE}'",
                    pageSize=100,
                    fields="nextPageToken, files(name)",
                    pageToken=page_token or "",
                    supportsAllDrives=True,
                )
                .execute()
            )
        except HttpError as e:
            msg = f"Drive API error: {e}"
            raise DriveConnectionError(msg) from e

        for item in response.get("files", []):
            name = item.get("name", "")
            yield (name, name)

        page_token = response.get("nextPageToken")
        if not page_token:
            break


def _list_file_names_impl(
    service: object,
    folder_id: str,
    *,
    recursive: bool,
    prefix_parts: tuple[str, ...],
) -> Iterator[tuple[str, str]]:
    """Recursively list file names with path prefix."""
    page_token: str | None = None
    while True:
        try:
            response = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    pageSize=100,
                    fields="nextPageToken, files(id, name, mimeType)",
                    pageToken=page_token or "",
                    supportsAllDrives=True,
                )
                .execute()
            )
        except HttpError as e:
            msg = f"Drive API error: {e}"
            raise DriveConnectionError(msg) from e

        for item in response.get("files", []):
            file_id = item.get("id")
            name = item.get("name", "")
            mime = item.get("mimeType", "")

            if mime == FOLDER_MIMETYPE:
                if recursive:
                    new_prefix = (*prefix_parts, name)
                    yield from _list_file_names_impl(
                        service, file_id, recursive=recursive, prefix_parts=new_prefix
                    )
                continue

            display_path = "/".join(prefix_parts) + "/" + name if prefix_parts else name
            yield (name, display_path)

        page_token = response.get("nextPageToken")
        if not page_token:
            break
