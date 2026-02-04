# Fentarxiu

A set of tools for managing a sheet music archive for a musical group. The main component is a **string checker** that validates instrument-code filenames (e.g. `1010_Flautí.pdf`) against configurable rules: allowed characters, prefix format, instrument catalogue match, and voice digit.

## Features

- **Filename parser**: Parses filenames with a numeric prefix (one or more 4-digit blocks like `1010` or `1010+2002`) and instrument names after an underscore.
- **Validation rules**:
  - **ValidCharsRule**: Allows Catalan letters, digits, and filename-safe symbols; rejects emojis and other characters.
  - **PrefixRule**: Ensures the prefix matches the expected format and that each block’s `(instrument_range, code)` exists in the instrument catalogue.
  - **InstrumentNameMatchRule**: Ensures each instrument name in the filename matches the catalogue entry for the corresponding prefix code.
  - **VoiceRule**: Ensures the voice digit in each 4-digit block is in the valid range (0–9).
- **Instrument catalogue**: Built-in mapping from `(instrument_range, code)` to normalized instrument names (woodwind, brass, percussion, etc.).

## Requirements

- Python 3.14.2
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

With **uv** (recommended):

```bash
uv sync
```

This installs the project and dev dependencies (pytest, ruff) from `pyproject.toml` and `uv.lock`.

With **pip** (in a venv with Python 3.14.2):

```bash
pip install -e ".[dev]"
```

## Usage

Use the library from Python:

```python
from string_checker import (
    Checker,
    InstrumentCatalogue,
    ValidCharsRule,
    PrefixRule,
    InstrumentNameMatchRule,
    VoiceRule,
)

catalogue = InstrumentCatalogue.default()
checker = Checker(rules=[
    ValidCharsRule(),
    PrefixRule(catalogue),
    InstrumentNameMatchRule(catalogue),
    VoiceRule(),
])

result = checker.check("1010_Flautí.pdf")
# Success(None) or Failure((...failures...))
```

## Development

### Lint (check)

```bash
uv run ruff check .
```

### Format

```bash
uv run ruff format .
```

### Test

```bash
uv run pytest
```

Run with verbose output:

```bash
uv run pytest -v
```

## Project layout

- `src/string_checker/`: Main package (checker, parser, catalogue, rules, failures).
- `tests/`: Pytest tests (checker, parser, catalogue, failures, and per-rule tests).
- `pyproject.toml`: Project metadata, dependencies, Ruff and Pytest config.
