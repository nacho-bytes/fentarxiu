"""Google Drive connection: credentials and file listing.

Loads OAuth credentials from env-configured paths and provides an iterator
over files in a folder (optionally recursive). Folders are never yielded
as files; they are only traversed when recursive=True.
"""

from drive_connection.drive import (
    DriveConnectionError,
    list_file_names,
    list_subfolder_names,
    load_credentials_and_build_service,
)

__all__ = [
    "DriveConnectionError",
    "list_file_names",
    "list_subfolder_names",
    "load_credentials_and_build_service",
]
