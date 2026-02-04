"""Rule definitions and checker protocol.

RuleChecker is the abstract base class that all rules (e.g. ValidCharsRule)
must inherit from and implement. Checker composes a list of RuleCheckers
and aggregates their failures.
"""

from abc import ABC, abstractmethod

from string_checker.failures.base import ValidationFailure


class RuleChecker(ABC):
    """Abstract base for a rule that validates a string and returns failures.

    Subclasses must implement ``check``. They should also define a ``name``
    attribute or property for display (e.g. for logging or user messages).
    The checker runs each rule and collects all failures; no exceptions are
    raised for validation errors.
    """

    @abstractmethod
    def check(self, text: str) -> list[ValidationFailure]:
        """Run the rule on the given string.

        Args:
            text: The string to validate.

        Returns:
            List of validation failures; empty if the string passes this rule.

        """
        ...
