#!/usr/bin/env python3
"""Extract CS2 crosshair codes from a demo file."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


LOCAL_DEPS = Path(__file__).resolve().parent / ".codex_pydeps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))

try:
    from demoparser2 import DemoParser
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: demoparser2\n"
        "Install it with:\n"
        "  python -m pip install -r requirements.txt\n"
        "or install locally with:\n"
        "  python -m pip install -r requirements.txt -t .codex_pydeps"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract unique Counter-Strike 2 crosshair codes from a .dem file."
    )
    parser.add_argument("demo", type=Path, help="Path to the .dem file")
    parser.add_argument(
        "--event",
        default="round_freeze_end",
        help="Game event whose ticks should be sampled (default: round_freeze_end)",
    )
    parser.add_argument(
        "--format",
        choices=("table", "csv", "json"),
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file to write CSV or JSON output to",
    )
    parser.add_argument(
        "--include-tick",
        action="store_true",
        help="Include the first tick where each player's code was found",
    )
    parser.add_argument(
        "--detect-changes",
        action="store_true",
        help=(
            "Show each player's first crosshair code and any later round where "
            "their code changes"
        ),
    )
    return parser.parse_args()


def extract_crosshairs(
    demo_path: Path, event_name: str, detect_changes: bool = False
) -> list[dict[str, str | int]]:
    if not demo_path.exists():
        raise FileNotFoundError(f"Demo file not found: {demo_path}")

    parser = DemoParser(str(demo_path))
    events = parser.parse_event(event_name)
    if "tick" not in events.columns:
        raise ValueError(f'Event "{event_name}" did not include a tick column')

    ticks = [int(tick) for tick in events["tick"].dropna().tolist()]
    if not ticks:
        return []
    round_by_tick = {tick: round_number for round_number, tick in enumerate(ticks, 1)}

    rows = parser.parse_ticks(["crosshair_code"], ticks=ticks)
    required_columns = {"steamid", "name", "crosshair_code", "tick"}
    missing_columns = required_columns.difference(rows.columns)
    if missing_columns:
        raise ValueError(
            "Parser output is missing expected columns: "
            + ", ".join(sorted(missing_columns))
        )

    results: list[dict[str, str | int]] = []
    seen_steamids: set[str] = set()
    latest_code_by_steamid: dict[str, str] = {}
    for row in rows.sort_values("tick").to_dict("records"):
        steamid = str(row.get("steamid") or "")
        code = str(row.get("crosshair_code") or "")
        if not steamid or not code:
            continue
        if detect_changes:
            if latest_code_by_steamid.get(steamid) == code:
                continue
            latest_code_by_steamid[steamid] = code
        elif steamid in seen_steamids:
            continue

        seen_steamids.add(steamid)
        tick = int(row.get("tick") or 0)
        result: dict[str, str | int] = {
            "steamid": steamid,
            "name": str(row.get("name") or ""),
            "crosshair_code": code,
            "tick": tick,
        }
        if detect_changes:
            result["round"] = round_by_tick.get(tick, 0)
        results.append(result)

    return results


def format_table(rows: list[dict[str, str | int]], include_tick: bool) -> str:
    columns = ["steamid", "name"]
    if rows and "round" in rows[0]:
        columns.append("round")
    columns.append("crosshair_code")
    if include_tick:
        columns.append("tick")

    widths = {
        column: max(len(column), *(len(str(row[column])) for row in rows))
        for column in columns
    }
    header = "  ".join(column.ljust(widths[column]) for column in columns)
    divider = "  ".join("-" * widths[column] for column in columns)
    body = [
        "  ".join(str(row[column]).ljust(widths[column]) for column in columns)
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_output(
    rows: list[dict[str, str | int]],
    output_format: str,
    include_tick: bool,
    output_path: Path | None,
) -> str:
    if not include_tick:
        rows = [
            {key: value for key, value in row.items() if key != "tick"}
            for row in rows
        ]

    if output_format == "json":
        text = json.dumps(rows, indent=2)
    elif output_format == "csv":
        fieldnames = (
            [key for key in ("steamid", "name", "round", "crosshair_code", "tick") if key in rows[0]]
            if rows
            else ["steamid", "name", "crosshair_code"]
        )
        if include_tick and "tick" not in fieldnames:
            fieldnames.append("tick")
        from io import StringIO

        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        text = buffer.getvalue().rstrip()
    else:
        text = format_table(rows, include_tick) if rows else "No crosshair codes found."

    if output_path:
        output_path.write_text(text + "\n", encoding="utf-8")

    return text


def main() -> int:
    args = parse_args()
    try:
        rows = extract_crosshairs(args.demo, args.event, args.detect_changes)
        text = write_output(rows, args.format, args.include_tick, args.output)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        print(f"Wrote {len(rows)} crosshair code(s) to {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
