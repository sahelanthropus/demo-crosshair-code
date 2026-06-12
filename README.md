# CS2 Demo Crosshair Parser

A small fork/refactor of **Demo Crosshair Code** for extracting Counter-Strike 2 crosshair codes from `.dem` files.

The original project was a web app, but the build/project structure was no longer working cleanly for my use case. This fork keeps the original project files for reference and adds a simplified Python command-line workflow for parsing CS2 demo files directly.

> **CS2 only. CSGO demos are not supported.**

## What this fork adds

- A simple Python script for parsing CS2 `.dem` files
- Dependency setup through `requirements.txt`
- Command-line output in table, CSV, or JSON format
- Optional detection of round-to-round crosshair changes
- A simpler setup path for people who just want to extract crosshair codes

## Repository layout

The original project files have been moved into their own folder for reference.

The new Python parser files are in their own folder and include:

```text
parse_crosshairs.py
requirements.txt
README.md
```

Use the README inside the Python parser folder for the most direct script-specific instructions.

## Quick setup

Open PowerShell or a terminal in the folder that contains `parse_crosshairs.py` and `requirements.txt`, then install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Basic usage

Print one crosshair code per player:

```powershell
python parse_crosshairs.py "path\to\demo.dem"
```

Detect round-to-round crosshair changes:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes
```

Export detected changes to CSV:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes --include-tick --format csv --output crosshair_changes.csv
```

Export detected changes to JSON:

```powershell
python parse_crosshairs.py "path\to\demo.dem" --detect-changes --format json --output crosshair_changes.json
```

## Notes

- The default mode shows each player once.
- `--detect-changes` shows each player's first crosshair and any later round where the code changes.
- Round numbers are based on `round_freeze_end` events in the demo.
- If a demo is compressed, extract it first so you have the `.dem` file.
- This tool is intended for CS2 demos only.

## Original project

This repository is based on the original **Demo Crosshair Code** project:

- Original site: https://beepisla.github.io/demo-crosshair-code/
- Original credits:
  - LaihoE's demoparser
  - Svelte
  - Tailwind

The original web app files are preserved in this fork for reference, but the main supported workflow in this fork is the Python command-line parser.