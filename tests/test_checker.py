"""Tests for Checker (unit and integration)."""

from returns.result import Failure, Success

from string_checker import (
    Checker,
    InstrumentCatalogue,
    InstrumentNameMatchRule,
    InstrumentNameMismatchFailure,
    InvalidCharacterFailure,
    InvalidPrefixFailure,
    PrefixRule,
    ValidCharsRule,
    VoiceRule,
)
from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker
from string_checker.rules.pdf_extension import NotPdfFailure, PdfExtensionRule


def _fake_rule(failures: list[ValidationFailure]) -> RuleChecker:
    """Rule that always returns the given failures."""

    class FakeRule(RuleChecker):
        def check(self, _text: str) -> list[ValidationFailure]:
            return list(failures)

    return FakeRule()


class TestCheckerUnitEmptyRules:
    """Checker with no rules."""

    def test_any_string_returns_success(self) -> None:
        checker = Checker(rules=[])
        result = checker.check("anything")
        assert isinstance(result, Success)
        assert result.unwrap() is None


class TestCheckerUnitSingleRule:
    """Checker with one rule."""

    def test_rule_passes_returns_success(self) -> None:
        checker = Checker(rules=[_fake_rule([])])
        result = checker.check("x")
        assert isinstance(result, Success)
        assert result.unwrap() is None

    def test_rule_returns_failures_returns_failure(self) -> None:
        f1 = InvalidPrefixFailure(message="Bad.")
        checker = Checker(rules=[_fake_rule([f1])])
        result = checker.check("x")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) == 1
        assert failures[0] is f1

    def test_rule_returns_multiple_failures(self) -> None:
        f1 = InvalidCharacterFailure(index=0, char="!")
        f2 = InvalidCharacterFailure(index=1, char="?")
        checker = Checker(rules=[_fake_rule([f1, f2])])
        result = checker.check("!?")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) == 2
        assert list(failures) == [f1, f2]


class TestCheckerUnitMultipleRules:
    """Checker with several rules; order and aggregation."""

    def test_all_rules_pass_returns_success(self) -> None:
        checker = Checker(rules=[_fake_rule([]), _fake_rule([])])
        result = checker.check("x")
        assert isinstance(result, Success)
        assert result.unwrap() is None

    def test_second_rule_fails_returns_aggregated_failures(self) -> None:
        f1 = InvalidPrefixFailure(message="First.")
        f2 = InvalidPrefixFailure(message="Second.")
        checker = Checker(rules=[_fake_rule([]), _fake_rule([f1, f2])])
        result = checker.check("x")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) == 2
        assert failures[0] is f1
        assert failures[1] is f2

    def test_both_rules_fail_returns_concatenated_failures(self) -> None:
        fa = InvalidCharacterFailure(index=0, char="a")
        fb = InvalidPrefixFailure(message="Bad prefix.")
        checker = Checker(rules=[_fake_rule([fa]), _fake_rule([fb])])
        result = checker.check("x")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) == 2
        assert failures[0] is fa
        assert failures[1] is fb


class TestCheckerIntegration:
    """Full Checker with all five rules (including PdfExtensionRule)."""

    def _full_checker(self) -> Checker:
        catalogue = InstrumentCatalogue.default()
        return Checker(
            rules=[
                ValidCharsRule(),
                PrefixRule(catalogue),
                InstrumentNameMatchRule(catalogue),
                VoiceRule(),
                PdfExtensionRule(),
            ]
        )

    def test_valid_filename_returns_success(self) -> None:
        checker = self._full_checker()
        result = checker.check("1010_Flautí.pdf")
        assert isinstance(result, Success)
        assert result.unwrap() is None

    def test_invalid_character_returns_failure_with_valid_chars(self) -> None:
        checker = self._full_checker()
        result = checker.check("1010_Flautí🎵.pdf")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) >= 1
        assert any(isinstance(f, InvalidCharacterFailure) for f in failures)

    def test_bad_prefix_returns_failure_with_prefix_failure(self) -> None:
        checker = self._full_checker()
        result = checker.check("10_Flautí.pdf")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert any(isinstance(f, InvalidPrefixFailure) for f in failures)

    def test_name_mismatch_returns_failure_with_mismatch_failure(self) -> None:
        checker = self._full_checker()
        result = checker.check("1010_Flauta.pdf")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert any(isinstance(f, InstrumentNameMismatchFailure) for f in failures)

    def test_multiple_errors_returns_multiple_failures(self) -> None:
        checker = self._full_checker()
        # Invalid char + invalid prefix (e.g. no 4-digit block)
        result = checker.check("1o_Flautí🎵.pdf")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert len(failures) >= 2

    def test_filename_without_pdf_returns_not_pdf_failure(self) -> None:
        checker = self._full_checker()
        result = checker.check("1010_Flautí")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert any(isinstance(f, NotPdfFailure) for f in failures)

    def test_filename_with_wrong_extension_returns_not_pdf_failure(self) -> None:
        checker = self._full_checker()
        result = checker.check("1010_Flautí.docx")
        assert isinstance(result, Failure)
        failures = result.failure()
        assert any(isinstance(f, NotPdfFailure) for f in failures)
