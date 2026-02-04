"""Parse instrument-code filenames: prefix blocks and instrument names."""

import re
from dataclasses import dataclass

# Prefix: one or more blocks of 4 digits, optional + more blocks, then underscore.
BLOCK_LEN = 4
_PREFIX_RE = re.compile(r"^(\d{4})(?:\+\d{4})*_")


@dataclass(frozen=True)
class ParsedFilename:
    """Result of parsing a valid instrument-code filename."""

    blocks: list[tuple[int, str, int]]
    """List of (instrument_range, code, voice) for each prefix block."""

    names: list[str]
    """Instrument names after the underscore, split by '+'."""


def parse_filename(text: str) -> ParsedFilename | None:
    """Parse filename into prefix blocks and names.

    Expected format: {instrument_range}{code}{voice}_Name.pdf or
    {block1}+{block2}+..._{Name1}+{Name2}+....pdf
    Each block is 4 digits: 1 digit instrument_range, 2 digit code, 1 digit voice.

    Args:
        text: Filename with or without .pdf.

    Returns:
        ParsedFilename with blocks and names, or None if format does not match.

    """
    match = _PREFIX_RE.match(text)
    if not match:
        return None
    prefix_full = match.group(0)
    # Extract all 4-digit blocks from the prefix (before the final _)
    prefix_part = prefix_full.rstrip("_")
    block_strs = prefix_part.split("+")
    blocks: list[tuple[int, str, int]] = []
    for bs in block_strs:
        if len(bs) != BLOCK_LEN or not bs.isdigit():
            return None
        instrument_range = int(bs[0])
        code = bs[1:3]
        voice = int(bs[3])
        blocks.append((instrument_range, code, voice))
    # Rest of string after underscore
    rest = text[len(prefix_full) :]
    rest = rest.removesuffix(".pdf")
    names = [n.strip() for n in rest.split("+")] if rest else []
    if len(names) != len(blocks):
        return None
    return ParsedFilename(blocks=blocks, names=names)
