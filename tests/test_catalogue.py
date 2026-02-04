"""Tests for InstrumentCatalogue."""

from string_checker.data import InstrumentCatalogue


class TestInstrumentCatalogueDefault:
    """default() and built-in catalogue behaviour."""

    def test_default_returns_instance(self) -> None:
        cat = InstrumentCatalogue.default()
        assert isinstance(cat, InstrumentCatalogue)

    def test_default_has_expected_entries(self) -> None:
        cat = InstrumentCatalogue.default()
        assert cat.has(0, "00") is True
        assert cat.get_name(0, "00") == "Guia"
        assert cat.has(1, "00") is True
        assert cat.get_name(1, "00") == "Flauta"
        assert cat.has(1, "01") is True
        assert cat.get_name(1, "01") == "Flautí"
        assert cat.has(2, "02") is True
        assert cat.get_name(2, "02") == "Trompeta"
        assert cat.has(6, "02") is True
        assert cat.get_name(6, "02") == "Homes"


class TestInstrumentCatalogueCustomTable:
    """Constructor with custom or empty table."""

    def test_empty_table_has_returns_false(self) -> None:
        cat = InstrumentCatalogue(table={})
        assert cat.has(1, "00") is False
        assert cat.has(0, "00") is False

    def test_empty_table_get_name_returns_none(self) -> None:
        cat = InstrumentCatalogue(table={})
        assert cat.get_name(1, "00") is None
        assert cat.get_name(0, "99") is None

    def test_custom_table_returns_given_data(self) -> None:
        table: dict[tuple[int, str], str] = {
            (1, "00"): "CustomFlauta",
            (2, "01"): "CustomPiccolo",
        }
        cat = InstrumentCatalogue(table=table)
        assert cat.has(1, "00") is True
        assert cat.get_name(1, "00") == "CustomFlauta"
        assert cat.has(2, "01") is True
        assert cat.get_name(2, "01") == "CustomPiccolo"

    def test_custom_table_unknown_returns_false_and_none(self) -> None:
        table: dict[tuple[int, str], str] = {(1, "00"): "Flauta"}
        cat = InstrumentCatalogue(table=table)
        assert cat.has(1, "01") is False
        assert cat.get_name(1, "01") is None
        assert cat.has(0, "00") is False
        assert cat.get_name(0, "00") is None
