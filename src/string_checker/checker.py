"""Checker: runs multiple rules and aggregates failures into a Result.

Compose several RuleCheckers and run them on a string; the result is
either Success(None) when all rules pass or Failure(sequence of failures).
"""

from collections.abc import Sequence

from returns.result import Failure, Result, Success

from string_checker.failures.base import ValidationFailure
from string_checker.rules import RuleChecker


class Checker:
    """Runs a list of rule checkers and aggregates all validation failures.

    Pass a list of RuleChecker instances (e.g. ValidCharsRule). check(text)
    runs every rule and returns a Result: Success(None) if there are no
    failures, or Failure with a sequence of all failures from every rule.
    """

    def __init__(self, rules: list[RuleChecker]) -> None:
        """Build a checker that runs the given rules in order.

        Args:
            rules: List of rule checkers to run on each validated string.

        """
        self._rules = rules

    def check(self, text: str) -> Result[None, Sequence[ValidationFailure]]:
        """Validate the string with all rules and return a Result.

        Args:
            text: The string to validate.

        Returns:
            Success(None) if all rules pass; Failure(failures) with the
            aggregated sequence of validation failures otherwise.

        """
        failures: list[ValidationFailure] = []
        for rule in self._rules:
            failures.extend(rule.check(text))
        if not failures:
            return Success(None)
        return Failure(tuple(failures))
