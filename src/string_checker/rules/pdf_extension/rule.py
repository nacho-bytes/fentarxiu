"""PDF extension rule: filename must end with .pdf."""

import attrs

from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.pdf_extension.failures import NotPdfFailure


@attrs.define
class PdfExtensionRule(RuleChecker):
    """Validates that the filename ends with the .pdf extension."""

    name: str = "PdfExtensionRule"

    def check(self, text: str) -> list[ValidationFailure]:
        """Return failure when the string does not end with .pdf (case-insensitive)."""
        stripped = text.strip()
        if not stripped.lower().endswith(".pdf"):
            if not stripped:
                message = "Filename is empty; it must end with .pdf."
            else:
                message = "Filename must end with .pdf."
            return [NotPdfFailure(message=message)]
        return []
