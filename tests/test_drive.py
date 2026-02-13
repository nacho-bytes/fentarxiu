"""Tests for list_subfolder_names, create_folder, create_shortcut (mocked Drive API)."""

from unittest.mock import Mock

from drive_connection import (
    create_folder,
    create_shortcut,
    list_subfolder_names,
)


def test_list_subfolder_names_yields_folder_names() -> None:
    """list_subfolder_names yields (name, name) for each direct child folder."""
    response = {
        "files": [
            {"name": "Folder1"},
            {"name": "Folder2"},
        ],
        "nextPageToken": None,
    }
    list_return = Mock()
    list_return.execute = Mock(return_value=response)
    files_return = Mock()
    files_return.list = Mock(return_value=list_return)
    service = Mock(files=Mock(return_value=files_return))

    result = list(list_subfolder_names(service, "parent_id"))

    assert result == [("Folder1", "Folder1"), ("Folder2", "Folder2")]


def test_list_subfolder_names_pagination() -> None:
    """list_subfolder_names follows nextPageToken and yields all pages."""
    first_response = {
        "files": [{"name": "Page1Folder"}],
        "nextPageToken": "tok",
    }
    second_response = {
        "files": [{"name": "Page2Folder"}],
        "nextPageToken": None,
    }
    execute_mock = Mock(side_effect=[first_response, second_response])
    list_return = Mock()
    list_return.execute = execute_mock
    files_return = Mock()
    files_return.list = Mock(return_value=list_return)
    service = Mock(files=Mock(return_value=files_return))

    result = list(list_subfolder_names(service, "parent_id"))

    assert result == [("Page1Folder", "Page1Folder"), ("Page2Folder", "Page2Folder")]
    assert execute_mock.call_count == 2


def test_create_folder_returns_resource_and_uses_root_when_no_parent() -> None:
    """create_folder in root when parent_id is None returns resource."""
    created = {
        "id": "new_folder_id",
        "name": "MyFolder",
        "mimeType": "application/vnd.google-apps.folder",
    }
    create_return = Mock()
    create_return.execute = Mock(return_value=created)
    files_return = Mock()
    files_return.create = Mock(return_value=create_return)
    service = Mock(files=Mock(return_value=files_return))

    result = create_folder(service, "MyFolder", parent_id=None)

    assert result == created
    files_return.create.assert_called_once()
    call_kw = files_return.create.call_args.kwargs
    assert call_kw["body"]["name"] == "MyFolder"
    assert call_kw["body"]["mimeType"] == "application/vnd.google-apps.folder"
    assert call_kw["body"]["parents"] == ["root"]


def test_create_folder_uses_parent_id_when_given() -> None:
    """create_folder passes parent_id in parents when provided."""
    created = {
        "id": "child_id",
        "name": "Child",
        "mimeType": "application/vnd.google-apps.folder",
    }
    create_return = Mock()
    create_return.execute = Mock(return_value=created)
    files_return = Mock()
    files_return.create = Mock(return_value=create_return)
    service = Mock(files=Mock(return_value=files_return))

    result = create_folder(service, "Child", parent_id="parent_123")

    assert result["id"] == "child_id"
    files_return.create.assert_called_once()
    call_kw = files_return.create.call_args.kwargs
    assert call_kw["body"]["parents"] == ["parent_123"]


def test_create_shortcut_returns_resource_and_calls_api() -> None:
    """create_shortcut with targetId returns resource."""
    created = {
        "id": "shortcut_id",
        "name": "My Shortcut",
        "mimeType": "application/vnd.google-apps.shortcut",
    }
    create_return = Mock()
    create_return.execute = Mock(return_value=created)
    files_return = Mock()
    files_return.create = Mock(return_value=create_return)
    service = Mock(files=Mock(return_value=files_return))

    result = create_shortcut(service, "target_file_id", parent_id="folder_456")

    assert result == created
    files_return.create.assert_called_once()
    call_kw = files_return.create.call_args.kwargs
    assert call_kw["body"]["mimeType"] == "application/vnd.google-apps.shortcut"
    assert call_kw["body"]["shortcutDetails"]["targetId"] == "target_file_id"
    assert call_kw["body"]["parents"] == ["folder_456"]


def test_create_shortcut_with_name_and_target_mime_type() -> None:
    """create_shortcut accepts optional name and target_mime_type."""
    created = {
        "id": "sid",
        "name": "Doc link",
        "mimeType": "application/vnd.google-apps.shortcut",
    }
    create_return = Mock()
    create_return.execute = Mock(return_value=created)
    files_return = Mock()
    files_return.create = Mock(return_value=create_return)
    service = Mock(files=Mock(return_value=files_return))

    result = create_shortcut(
        service,
        "doc_id",
        name="Doc link",
        parent_id=None,
        target_mime_type="application/vnd.google-apps.document",
    )

    assert result["id"] == "sid"
    call_kw = files_return.create.call_args.kwargs
    assert call_kw["body"]["name"] == "Doc link"
    assert (
        call_kw["body"]["shortcutDetails"]["targetMimeType"]
        == "application/vnd.google-apps.document"
    )
    assert call_kw["body"]["parents"] == ["root"]
