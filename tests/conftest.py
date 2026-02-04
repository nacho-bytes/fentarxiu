"""Shared pytest fixtures."""

import pytest

from string_checker import InstrumentCatalogue


@pytest.fixture
def default_catalogue() -> InstrumentCatalogue:
    """Default instrument catalogue (built-in data)."""
    return InstrumentCatalogue.default()
