#!/usr/bin/env python3
"""Bind the completed page-by-page PDF review to exact release artifacts."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT_ROOT / "publication" / "reviewed-pdfs.sha256"
REVIEW_RECORD = PROJECT_ROOT / "publication" / "PDF_VISUAL_REVIEW_RECORD.md"

EXPECTED_PAGES = {
    "complete-builders-field-manual.pdf": 236,
    "rob-and-the-lost-yellow-ball.pdf": 23,
    "volume-1-meet-rob.pdf": 37,
    "volume-2-circuits-and-signals.pdf": 36,
    "volume-3-motion-workshop.pdf": 36,
    "volume-4-mission-control.pdf": 40,
    "volume-5-ai-robotics-with-codex.pdf": 43,
    "volume-6-amber-dual-arm-robotics.pdf": 34,
    "volume-7-engineering-robcontrollervision.pdf": 38,
    "volume-8-engineering-cerebro.pdf": 50,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdfinfo(path: Path) -> dict[str, str]:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    fields: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    failures: list[str] = []
    entries: dict[str, str] = {}

    if not MANIFEST.is_file():
        print(f"ERROR: missing PDF review manifest: {MANIFEST}", file=sys.stderr)
        return 1

    for line_number, raw_line in enumerate(MANIFEST.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (output/pdf/[^/]+\.pdf)", line)
        if not match:
            failures.append(f"manifest line {line_number} is malformed: {raw_line}")
            continue
        digest, relative_path = match.groups()
        name = Path(relative_path).name
        if name in entries:
            failures.append(f"duplicate manifest entry: {name}")
        entries[name] = digest

    expected_names = set(EXPECTED_PAGES)
    found_names = set(entries)
    if found_names != expected_names:
        failures.append(
            "reviewed PDF set differs from expected set: "
            f"missing={sorted(expected_names - found_names)}, "
            f"unexpected={sorted(found_names - expected_names)}"
        )

    total_pages = 0
    for name, expected_page_count in EXPECTED_PAGES.items():
        path = PROJECT_ROOT / "output" / "pdf" / name
        if not path.is_file():
            failures.append(f"reviewed PDF is missing: {path}")
            continue

        expected_digest = entries.get(name)
        if expected_digest and sha256(path) != expected_digest:
            failures.append(f"reviewed PDF bytes changed: {path.relative_to(PROJECT_ROOT)}")

        try:
            info = pdfinfo(path)
        except (OSError, subprocess.CalledProcessError) as error:
            failures.append(f"pdfinfo failed for {name}: {error}")
            continue

        try:
            actual_page_count = int(info.get("Pages", ""))
        except ValueError:
            failures.append(f"missing or invalid page count for {name}")
            continue

        total_pages += actual_page_count
        if actual_page_count != expected_page_count:
            failures.append(
                f"page count changed for {name}: "
                f"expected {expected_page_count}, found {actual_page_count}"
            )

        page_size = info.get("Page size", "")
        if "612 x 792 pts" not in page_size or "(letter)" not in page_size.lower():
            failures.append(f"page size changed for {name}: {page_size or 'unknown'}")
        if info.get("Encrypted", "").lower() != "no":
            failures.append(f"reviewed PDF is encrypted: {name}")

    if total_pages != 573:
        failures.append(f"reviewed page total changed: expected 573, found {total_pages}")

    if not REVIEW_RECORD.is_file():
        failures.append(f"missing PDF visual review record: {REVIEW_RECORD}")
    elif "**STATUS: COMPLETE**" not in REVIEW_RECORD.read_text():
        failures.append("PDF visual review record is not marked complete")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("PDF review audit passed: 10 byte-matched Letter PDFs, 573 reviewed pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
