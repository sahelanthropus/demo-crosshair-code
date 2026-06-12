# CS2 Demo Crosshair Parser

Small command-line tool for extracting Counter-Strike 2 crosshair codes from `.dem` files.

## Requirements

- Python 3.10 or newer
- Internet access the first time you install dependencies

## Setup

Open PowerShell in this folder and run:

```powershell
python -m pip install -r requirements.txt
```

## Usage

Print one crosshair code per player:

```powershell
python parse_crosshairs.py "path\to\demo.dem"
```

Detect round-to-round crosshair changes:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes
```

Export changes to CSV:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes --include-tick --format csv --output crosshair_changes.csv
```

Export JSON:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes --format json --output crosshair_changes.json
```

## Notes

- The default mode shows each player once.
- `--detect-changes` shows each player's first crosshair and any later round where the code changes.
- Round numbers are based on `round_freeze_end` events in the demo.
- If a demo is compressed, extract it first so you have the `.dem` file.