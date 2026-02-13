"""Parse work folder names: WorkName_Author1+Author2, arrangers optional."""

from dataclasses import dataclass

MIN_SEGMENTS = 2
MAX_SPLITS = 2


@dataclass(frozen=True)
class ParsedFolderName:
    """Result of parsing a valid work folder name."""

    work_name: str
    authors: list[str]
    arrangers: list[str]


def parse_folder_name(text: str) -> ParsedFolderName | None:
    """Parse folder name into work name, authors, and optional arrangers.

    Expected format: WorkName_Author1+Author2+... or
    WorkName_Author1+Author2+..._Arranger1+Arranger2+...
    Two segments (one underscore) or three segments (two underscores);
    authors must be non-empty; arrangers segment is optional.

    Args:
        text: Folder name string.

    Returns:
        ParsedFolderName with work_name, authors, arrangers (possibly empty),
        or None if format does not match.

    """
    parts = text.split("_", MAX_SPLITS)
    if len(parts) < MIN_SEGMENTS:
        return None
    work_name = parts[0].strip()
    authors_part = parts[1].strip()
    if not work_name or not authors_part:
        return None
    authors = [n.strip() for n in authors_part.split("+") if n.strip()]
    if not authors:
        return None
    if len(parts) == MIN_SEGMENTS:
        return ParsedFolderName(
            work_name=work_name,
            authors=authors,
            arrangers=[],
        )
    arrangers = [n.strip() for n in parts[2].split("+") if n.strip()]
    return ParsedFolderName(
        work_name=work_name,
        authors=authors,
        arrangers=arrangers,
    )
