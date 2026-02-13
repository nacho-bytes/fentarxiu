"""Google Drive connection: credentials, file listing, folder and shortcut creation.

Loads OAuth credentials from env-configured paths and provides iterators
over files in a folder (optionally recursive), plus creation of folders
and shortcuts. Folders are never yielded as files; they are only traversed
when recursive=True.
"""

from drive_connection.drive import (
    FOLDER_MIMETYPE,
    SHORTCUT_MIMETYPE,
    DriveConnectionError,
    create_folder,
    create_shortcut,
    list_file_names,
    list_subfolder_names,
    load_credentials_and_build_service,
)

__all__ = [
    "FOLDER_MIMETYPE",
    "SHORTCUT_MIMETYPE",
    "DriveConnectionError",
    "create_folder",
    "create_shortcut",
    "list_file_names",
    "list_subfolder_names",
    "load_credentials_and_build_service",
]
