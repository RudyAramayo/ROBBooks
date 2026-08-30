#!/usr/bin/env python3
"""Verify the exact image bytes that received publication preflight review."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ASSETS = PROJECT / "assets"
CHECKSUMS = PROJECT / "publication" / "reviewed-assets.sha256"
REVIEW = PROJECT / "publication" / "ASSET_REVIEW_RECORD.md"
REPORT_DIR = PROJECT / "tmp" / "asset-audit"

EXPECTED_COUNTS = {
    "photos": 46,
    "generated": 15,
    "slides": 8,
    "posters/book-covers": 6,
    "posters": 1,
    "root": 1,
}

SENSITIVE_OCR_PATTERNS = {
    "private macOS path": re.compile(r"/Users/[^/\s]+/", re.IGNORECASE),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "IPv4 address": re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"),
    "credential wording": re.compile(
        r"\b(?:api[_ -]?key|access[_ -]?token|auth[_ -]?token|password|passwd|secret|ssid)\b",
        re.IGNORECASE,
    ),
    "common access-key form": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"ERROR: {message}")


def load_checksums(failures: list[str]) -> dict[str, str]:
    records: dict[str, str] = {}
    if not CHECKSUMS.is_file():
        fail(f"reviewed checksum manifest is missing: {CHECKSUMS}", failures)
        return records
    for line_number, line in enumerate(CHECKSUMS.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (assets/.+)", line)
        if not match:
            fail(f"invalid checksum entry at line {line_number}", failures)
            continue
        digest, relative = match.groups()
        if relative in records:
            fail(f"duplicate checksum path: {relative}", failures)
            continue
        records[relative] = digest
    return records


def asset_group(relative: str) -> str:
    parts = Path(relative).parts
    if len(parts) == 2:
        return "root"
    if parts[1] == "posters" and len(parts) > 3 and parts[2] == "book-covers":
        return "posters/book-covers"
    return parts[1]


def image_properties(path: Path) -> tuple[int, int, str]:
    result = subprocess.run(
        ["magick", "identify", "-quiet", "-format", "%w\t%h\t%[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, color_space = result.stdout.split("\t")
    return int(width), int(height), color_space


def validate_geometry(relative: str, width: int, height: int, color_space: str, failures: list[str]) -> None:
    if color_space.lower() != "srgb":
        fail(f"{relative} is {color_space}, expected sRGB", failures)
    short_edge = min(width, height)
    if relative.startswith("assets/photos/") and short_edge < 2400:
        fail(f"{relative} short edge is {short_edge}px; expected at least 2400px", failures)
    elif relative.startswith("assets/slides/") and (width < 3200 or height < 1800):
        fail(f"{relative} is {width}x{height}; expected at least 3200x1800", failures)
    elif relative.startswith("assets/generated/") and short_edge < 1024:
        fail(f"{relative} short edge is {short_edge}px; expected at least 1024px", failures)
    elif relative.startswith("assets/posters/book-covers/") and (width < 1275 or height < 1650):
        fail(f"{relative} is {width}x{height}; expected at least 1275x1650", failures)


def audit_metadata(photo_paths: list[Path], failures: list[str]) -> None:
    if not shutil.which("exiv2"):
        fail("exiv2 is required for prepared-photo metadata review", failures)
        return
    result = subprocess.run(["exiv2", "-pa", *map(str, photo_paths)], capture_output=True, text=True)
    if result.returncode:
        fail(f"exiv2 metadata scan failed: {result.stderr.strip()}", failures)
        return
    forbidden = re.compile(r"Exif\.GPSInfo|Exif\.Image\.(?:Make|Model)|Xmp\.exif\.GPS")
    if match := forbidden.search(result.stdout):
        fail(f"prepared photos retain forbidden metadata ({match.group(0)})", failures)


def audit_ocr(paths: list[Path], failures: list[str]) -> None:
    if not shutil.which("tesseract"):
        fail("tesseract is required for the requested OCR privacy scan", failures)
        return
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_lines = ["path\tcharacters\tfindings"]
    for path in paths:
        result = subprocess.run(
            ["tesseract", str(path), "stdout", "--psm", "11"],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(f"OCR failed for {path.relative_to(PROJECT)}: {result.stderr.strip()}", failures)
            continue
        text = result.stdout
        findings: list[str] = []
        for label, pattern in SENSITIVE_OCR_PATTERNS.items():
            if pattern.search(text):
                findings.append(label)
                fail(f"OCR found possible {label} in {path.relative_to(PROJECT)}", failures)
        report_lines.append(
            f"{path.relative_to(PROJECT)}\t{len(text)}\t{','.join(findings) if findings else 'none'}"
        )
    (REPORT_DIR / "ocr-privacy-scan.tsv").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr", action="store_true", help="rerun OCR privacy screening on real photos and slides")
    parser.add_argument(
        "--release",
        action="store_true",
        help="also require the author-rights questions recorded in the review ledger to be cleared",
    )
    args = parser.parse_args()
    failures: list[str] = []

    if not shutil.which("magick"):
        fail("magick is required for asset inspection", failures)
        return 1

    reviewed = load_checksums(failures)
    actual = {
        str(path.relative_to(PROJECT))
        for path in ASSETS.rglob("*")
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    }
    expected = set(reviewed)
    for relative in sorted(actual - expected):
        fail(f"unreviewed image is present: {relative}", failures)
    for relative in sorted(expected - actual):
        fail(f"reviewed image is missing: {relative}", failures)

    group_counts = {key: 0 for key in EXPECTED_COUNTS}
    inventory_lines = ["path\tsha256\twidth\theight\tcolorspace"]
    for relative in sorted(expected & actual):
        path = PROJECT / relative
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != reviewed[relative]:
            fail(f"reviewed bytes changed: {relative}", failures)
        try:
            width, height, color_space = image_properties(path)
        except (subprocess.CalledProcessError, ValueError) as error:
            fail(f"could not inspect {relative}: {error}", failures)
            continue
        validate_geometry(relative, width, height, color_space, failures)
        group = asset_group(relative)
        if group not in group_counts:
            fail(f"unexpected asset group for {relative}: {group}", failures)
        else:
            group_counts[group] += 1
        inventory_lines.append(f"{relative}\t{digest}\t{width}\t{height}\t{color_space}")

    for group, expected_count in EXPECTED_COUNTS.items():
        if group_counts[group] != expected_count:
            fail(f"{group} contains {group_counts[group]} reviewed image(s), expected {expected_count}", failures)

    if not REVIEW.is_file():
        fail(f"human-readable review ledger is missing: {REVIEW}", failures)
    else:
        review_text = REVIEW.read_text(encoding="utf-8")
        for relative in sorted(expected):
            if f"`{relative}`" not in review_text:
                fail(f"asset is absent from the named review ledger: {relative}", failures)
        if args.release and "RIGHTS STATUS: PENDING AUTHOR CONFIRMATION" in review_text:
            fail("per-image photographer, venue, and product-photo rights remain pending", failures)

    photo_paths = [PROJECT / path for path in sorted(expected) if path.startswith("assets/photos/")]
    audit_metadata(photo_paths, failures)
    if args.ocr:
        ocr_paths = photo_paths + [
            PROJECT / path for path in sorted(expected) if path.startswith("assets/slides/")
        ]
        audit_ocr(ocr_paths, failures)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "asset-inventory.tsv").write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")

    print(
        "Reviewed asset set: "
        f"{group_counts['photos']} real photos, {group_counts['slides']} historical slides, "
        f"{group_counts['generated']} book illustrations, and "
        f"{group_counts['posters/book-covers'] + group_counts['posters'] + group_counts['root']} "
        "derived/brand assets."
    )
    print(f"Reports: {REPORT_DIR}")
    if failures:
        print(f"Asset audit failed with {len(failures)} issue(s).")
        return 1
    print("Asset integrity, geometry, color-space, metadata, and recorded visual-review checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
