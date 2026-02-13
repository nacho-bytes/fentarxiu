"""Data and parsing for instrument-code filenames."""

from string_checker.data.catalogue import InstrumentCatalogue
from string_checker.data.catalogue_data import CATALOGUE_TABLE
from string_checker.data.folder_parser import ParsedFolderName, parse_folder_name
from string_checker.data.parser import ParsedFilename, parse_filename

__all__ = [
    "CATALOGUE_TABLE",
    "InstrumentCatalogue",
    "ParsedFilename",
    "ParsedFolderName",
    "parse_filename",
    "parse_folder_name",
]
