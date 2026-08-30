#!/usr/bin/env python3
"""Run DAISY Ace against every final Building R.O.B. EPUB."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPUB_DIR = PROJECT_ROOT / "output" / "apple-books" / "epub"


def ace_failures(report: object) -> list[tuple[str, str, str]]:
    failures: list[tuple[str, str, str]] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            result = value.get("earl:result")
            test = value.get("earl:test")
            if isinstance(result, dict) and isinstance(test, dict) and result.get("earl:outcome") == "fail":
                failures.append(
                    (
                        str(test.get("earl:impact", "unknown")),
                        str(test.get("dct:title", "unnamed-rule")),
                        str(result.get("dct:description", "no description")),
                    )
                )
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(report)
    return failures


def run(ace: str, reports: Path) -> int:
    epubs = sorted(EPUB_DIR.glob("*.epub"))
    if len(epubs) != 10:
        print(f"ERROR: expected 10 final EPUBs, found {len(epubs)}", file=sys.stderr)
        return 1
    reports.mkdir(parents=True, exist_ok=True)
    all_failures: list[str] = []
    for epub in epubs:
        subprocess.run(
            [ace, "--silent", "--force", "--subdir", "--outdir", str(reports), str(epub)],
            check=True,
            cwd=PROJECT_ROOT,
        )
        report_path = reports / epub.stem / "report.json"
        if not report_path.is_file():
            all_failures.append(f"{epub.name}: Ace did not create report.json")
            continue
        failures = ace_failures(json.loads(report_path.read_text(encoding="utf-8")))
        print(f"{epub.name}: {len(failures)} automated violation(s)")
        for impact, rule, description in failures:
            all_failures.append(f"{epub.name}: {impact}: {rule}: {description}")
    if all_failures:
        for failure in all_failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print("DAISY Ace audit passed: 10 EPUBs, zero automated violations.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ace", default=shutil.which("ace"), help="path to the DAISY Ace CLI")
    parser.add_argument("--reports", type=Path, help="retain reports in this directory instead of a temporary directory")
    args = parser.parse_args()
    if not args.ace:
        print("ERROR: DAISY Ace is not installed; supply --ace /path/to/ace", file=sys.stderr)
        return 2
    if args.reports:
        return run(args.ace, args.reports.resolve())
    with tempfile.TemporaryDirectory(prefix="rob-daisy-ace-") as temporary:
        return run(args.ace, Path(temporary))


if __name__ == "__main__":
    raise SystemExit(main())
