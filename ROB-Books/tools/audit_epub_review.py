#!/usr/bin/env python3
"""Bind EPUB accessibility and browser-visual review to exact artifacts."""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT_ROOT / "publication" / "reviewed-epubs.sha256"
REVIEW_RECORD = PROJECT_ROOT / "publication" / "EPUB_ACCESSIBILITY_REVIEW_RECORD.md"
EXPECTED_NAMES = {
    "complete-builders-field-manual.epub",
    "rob-and-the-lost-yellow-ball.epub",
    "volume-1-meet-rob.epub",
    "volume-2-circuits-and-signals.epub",
    "volume-3-motion-workshop.epub",
    "volume-4-mission-control.epub",
    "volume-5-ai-robotics-with-codex.epub",
    "volume-6-amber-dual-arm-robotics.epub",
    "volume-7-engineering-robcontrollervision.epub",
    "volume-8-engineering-cerebro.epub",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    entries: dict[str, str] = {}
    if not MANIFEST.is_file():
        print(f"ERROR: missing EPUB review manifest: {MANIFEST}", file=sys.stderr)
        return 1

    for line_number, raw_line in enumerate(MANIFEST.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (output/apple-books/epub/[^/]+\.epub)", line)
        if not match:
            failures.append(f"manifest line {line_number} is malformed: {raw_line}")
            continue
        digest, relative_path = match.groups()
        name = Path(relative_path).name
        if name in entries:
            failures.append(f"duplicate manifest entry: {name}")
        entries[name] = digest

    found_names = set(entries)
    if found_names != EXPECTED_NAMES:
        failures.append(
            "reviewed EPUB set differs from expected set: "
            f"missing={sorted(EXPECTED_NAMES - found_names)}, "
            f"unexpected={sorted(found_names - EXPECTED_NAMES)}"
        )

    for name in sorted(EXPECTED_NAMES):
        path = PROJECT_ROOT / "output" / "apple-books" / "epub" / name
        if not path.is_file():
            failures.append(f"reviewed EPUB is missing: {path}")
            continue
        expected_digest = entries.get(name)
        if expected_digest and sha256(path) != expected_digest:
            failures.append(f"reviewed EPUB bytes changed: {path.relative_to(PROJECT_ROOT)}")
        try:
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is not None:
                    failures.append(f"reviewed EPUB contains a corrupt member: {name}")
                if archive.namelist()[:1] != ["mimetype"]:
                    failures.append(f"reviewed EPUB does not begin with mimetype: {name}")
        except zipfile.BadZipFile:
            failures.append(f"reviewed EPUB is not a valid ZIP package: {name}")

    if not REVIEW_RECORD.is_file():
        failures.append(f"missing EPUB accessibility review record: {REVIEW_RECORD}")
    elif "**AUTOMATED AND BROWSER VISUAL PREFLIGHT: COMPLETE**" not in REVIEW_RECORD.read_text():
        failures.append("EPUB accessibility review record is not marked complete")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("EPUB review audit passed: 10 byte-matched EPUB 3 packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
