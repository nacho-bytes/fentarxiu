"""Composable string validation for instrument-code filenames.

Example:
    from string_checker import Checker, InstrumentCatalogue, ValidCharsRule
    from string_checker import PrefixRule, InstrumentNameMatchRule, VoiceRule

    catalogue = InstrumentCatalogue.default()
    checker = Checker(rules=[
        ValidCharsRule(),
        PrefixRule(catalogue),
        InstrumentNameMatchRule(catalogue),
        VoiceRule(),
    ])
    result = checker.check("1010_Flautí.pdf")
    # Success(None) or Failure((...failures...))

"""

from string_checker.checker import Checker
from string_checker.data import (
    InstrumentCatalogue,
    ParsedFolderName,
    parse_filename,
    parse_folder_name,
)
from string_checker.failures import FailureKind, ValidationFailure
from string_checker.rules.folder_name import FolderNameRule, InvalidFolderNameFailure
from string_checker.rules.folder_valid_chars import (
    FolderValidCharsRule,
    InvalidFolderCharacterFailure,
)
from string_checker.rules.instrument_name_match import (
    InstrumentNameMatchRule,
    InstrumentNameMismatchFailure,
)
from string_checker.rules.pdf_extension import NotPdfFailure, PdfExtensionRule
from string_checker.rules.prefix import InvalidPrefixFailure, PrefixRule
from string_checker.rules.valid_chars import InvalidCharacterFailure, ValidCharsRule
from string_checker.rules.voice import InvalidVoiceFailure, VoiceRule

__all__ = [
    "Checker",
    "FailureKind",
    "FolderNameRule",
    "FolderValidCharsRule",
    "InstrumentCatalogue",
    "InstrumentNameMatchRule",
    "InstrumentNameMismatchFailure",
    "InvalidCharacterFailure",
    "InvalidFolderCharacterFailure",
    "InvalidFolderNameFailure",
    "InvalidPrefixFailure",
    "InvalidVoiceFailure",
    "NotPdfFailure",
    "ParsedFolderName",
    "PdfExtensionRule",
    "PrefixRule",
    "ValidCharsRule",
    "ValidationFailure",
    "VoiceRule",
    "parse_filename",
    "parse_folder_name",
]
