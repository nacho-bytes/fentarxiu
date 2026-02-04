"""PDF extension rule: filename must end with .pdf."""

from string_checker.rules.pdf_extension.failures import NotPdfFailure
from string_checker.rules.pdf_extension.rule import PdfExtensionRule

__all__ = ["NotPdfFailure", "PdfExtensionRule"]
