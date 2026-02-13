"""Tests for list_subfolder_names with mocked Drive API."""

from unittest.mock import Mock

from drive_connection import list_subfolder_names


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
