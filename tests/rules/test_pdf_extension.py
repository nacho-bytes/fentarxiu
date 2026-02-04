"""Tests for PdfExtensionRule.

Covers: text ending with .pdf (any case) passes; empty or non-.pdf fails with
NotPdfFailure.
"""

from string_checker.rules.pdf_extension import NotPdfFailure, PdfExtensionRule


class TestPdfExtensionRulePasses:
    """When the filename ends with .pdf, the rule returns no failures."""

    def test_lowercase_pdf(self) -> None:
        rule = PdfExtensionRule()
        assert rule.check("1010_Flautí.pdf") == []

    def test_uppercase_pdf(self) -> None:
        rule = PdfExtensionRule()
        assert rule.check("document.PDF") == []

    def test_mixed_case_pdf(self) -> None:
        rule = PdfExtensionRule()
        assert rule.check("file.Pdf") == []

    def test_stripped_whitespace_around_pdf_passes(self) -> None:
        """Whitespace is stripped; if result ends with .pdf, the rule passes."""
        rule = PdfExtensionRule()
        assert rule.check("  1010_Flautí.pdf  ") == []


class TestPdfExtensionRuleFails:
    """When the filename does not end with .pdf, the rule returns NotPdfFailure."""

    def test_empty_string(self) -> None:
        rule = PdfExtensionRule()
        failures = rule.check("")
        assert len(failures) == 1
        assert isinstance(failures[0], NotPdfFailure)
        assert "empty" in failures[0].message.lower() or ".pdf" in failures[0].message

    def test_whitespace_only(self) -> None:
        rule = PdfExtensionRule()
        failures = rule.check("   ")
        assert len(failures) == 1
        assert isinstance(failures[0], NotPdfFailure)

    def test_no_extension(self) -> None:
        rule = PdfExtensionRule()
        failures = rule.check("1010_Flautí")
        assert len(failures) == 1
        assert isinstance(failures[0], NotPdfFailure)
        assert failures[0].message == "Filename must end with .pdf."

    def test_wrong_extension(self) -> None:
        rule = PdfExtensionRule()
        failures = rule.check("1010_Flautí.docx")
        assert len(failures) == 1
        assert isinstance(failures[0], NotPdfFailure)
