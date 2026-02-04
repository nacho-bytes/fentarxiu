# Fentarxiu

A set of tools for managing a sheet music archive for a musical group. The main component is a **string checker** that validates instrument-code filenames (e.g. `1010_Flautí.pdf`) against configurable rules: allowed characters, prefix format, instrument catalogue match, and voice digit.

## Features

- **Filename parser**: Parses filenames with a numeric prefix (one or more 4-digit blocks like `1010` or `1010+2002`) and instrument names after an underscore.
- **Validation rules**:
  - **ValidCharsRule**: Allows Catalan letters, digits, and filename-safe symbols; rejects emojis and other characters.
  - **PrefixRule**: Ensures the prefix matches the expected format and that each block’s `(instrument_range, code)` exists in the instrument catalogue.
  - **InstrumentNameMatchRule**: Ensures each instrument name in the filename matches the catalogue entry for the corresponding prefix code.
  - **VoiceRule**: Ensures the voice digit in each 4-digit block is in the valid range (0–9).
  - **PdfExtensionRule**: Ensures the filename ends with the `.pdf` extension.
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

## CLI (Google Drive)

A CLI validates filenames in a Google Drive folder and optionally writes a human-readable log in Valencian (for non-technical users). The log file is only created when the run completes successfully; if credentials or the Drive API fail, the program exits without creating or writing the log.

### Run

```bash
uv run fentarxiu <folder_id> [--recursive] [--log fitxer.log]
```

- **folder_id**: The Google Drive folder ID to scan (from the folder URL in Drive).
- **--recursive** / **-r**: List files in subfolders as well.
- **--log**: Path to the log file. Created if it does not exist. Each line lists a file path and the validation messages in Valencian for that file.

### Google Drive setup

1. Create a [Google Cloud project](https://console.cloud.google.com/) and enable the [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com).
2. Configure the OAuth consent screen (e.g. Internal) and create OAuth 2.0 Desktop app credentials.
3. Download the client secrets JSON and save it as `credentials.json` in your working directory (or set `FENTARXIU_CREDENTIALS_JSON` to its path).

### Environment variables

Optional; loaded from `.env` if present. See `.env.example`.

- **FENTARXIU_CREDENTIALS_JSON**: Path to the OAuth client secrets JSON. Default: `credentials.json` in the current working directory.
- **FENTARXIU_TOKEN_JSON**: Path to the stored token JSON (created after first login). Default: `token.json` in the current working directory.

Do not commit `.env`, `credentials.json`, or `token.json` to version control.

### Log format

The log is in Valencian. For each file that has validation failures, it shows the file path (or name) and a bullet list of short messages explaining what is wrong (e.g. “El nom del fitxer ha d'acabar en .pdf”, “Caràcter no permès: …”).

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
- `src/cli/`: CLI entry point and Valencian failure messages.
- `src/drive_connection/`: Google Drive API (credentials and file listing).
- `tests/`: Pytest tests (checker, parser, catalogue, failures, and per-rule tests).
- `pyproject.toml`: Project metadata, dependencies, Ruff and Pytest config.
- `.env.example`: Example environment variables for the CLI (no secrets).
