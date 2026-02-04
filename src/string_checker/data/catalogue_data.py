"""Instrument catalogue data: instrument_range + code -> normalized instrument name.

Data only; see catalogue.py for InstrumentCatalogue class.
Table: Range, Code, Instrument, Normalized instrument name.
"""

# (instrument_range, code) -> normalized instrument name
# Rang 0: Guió i/o parts
# Rang 1: Fusta
# Rang 2: Metall
# Rang 3: Percussió
# Rang 4: Piano
# Rang 5: Corda
# Rang 6: Cor

CATALOGUE_TABLE: dict[tuple[int, str], str] = {
    (0, "00"): "Guió",
    (1, "00"): "Flauta",
    (1, "01"): "Flautí",
    (1, "02"): "Oboe",
    (1, "03"): "CornAnglès",
    (1, "04"): "Fagot",
    (1, "05"): "Requint",
    (1, "06"): "Clarinet",
    (1, "07"): "ClarinetBaix",
    (1, "08"): "SaxoSoprano",
    (1, "09"): "SaxoAlt",
    (1, "10"): "SaxoTenor",
    (1, "11"): "SaxoBaríton",
    (1, "12"): "Dolçaina",
    (2, "00"): "Corneta",
    (2, "01"): "Piccolo",
    (2, "02"): "Trompeta",
    (2, "03"): "Fliscorn",
    (2, "04"): "Trompa",
    (2, "05"): "Trombó",
    (2, "06"): "TrombóBaix",
    (2, "07"): "Bombardí",
    (2, "08"): "Tuba",
    (3, "00"): "Timbals",
    (3, "01"): "Caixa",
    (3, "02"): "Bombo",
    (3, "03"): "Plats",
    (3, "04"): "Bateria",
    (3, "05"): "Altres",
    (4, "00"): "Piano",
    (5, "00"): "Violoncel",
    (5, "01"): "Contrabaix",
    (6, "00"): "Cor",
    (6, "01"): "Dones",
    (6, "02"): "Homes",
}
