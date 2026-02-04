"""Instrument catalogue: (instrument_range, code) -> normalized name."""

from string_checker.data.catalogue_data import CATALOGUE_TABLE


class InstrumentCatalogue:
    """Maps (instrument_range, code) to normalized instrument name.

    Use default() for the built-in catalogue from catalogue_data.
    """

    def __init__(self, table: dict[tuple[int, str], str] | None = None) -> None:
        """Build catalogue from table or use built-in data.

        Args:
            table: Optional (instrument_range, code) -> normalized instrument name.
                If None, uses CATALOGUE_TABLE.

        """
        self._table = table if table is not None else CATALOGUE_TABLE

    @classmethod
    def default(cls) -> "InstrumentCatalogue":
        """Return the default catalogue (data from catalogue_data.py)."""
        return cls()

    def get_name(self, instrument_range: int, code: str) -> str | None:
        """Return normalized name for (instrument_range, prefix_code),.

        or None if not in catalogue.
        """
        return self._table.get((instrument_range, code))

    def has(self, instrument_range: int, code: str) -> bool:
        """Return True if (instrument_range, code) exists in the catalogue."""
        return (instrument_range, code) in self._table
