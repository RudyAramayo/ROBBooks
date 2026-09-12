#!/usr/bin/env python3
"""Audit the preschool sources and generated Apple Books assets."""

from __future__ import annotations

import json
import posixpath
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "preschool-apple-books-catalog.json"
IMAGE_PATTERN = re.compile(r"!\[[^\]]+\]\((images/[^)]+)\)")
PLACEHOLDERS = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b", re.IGNORECASE)


def identify(path: Path) -> tuple[int, int, str]:
    result = subprocess.run(
        ["magick", "identify", "-quiet", "-format", "%w\t%h\t%[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, colorspace = result.stdout.split("\t")
    return int(width), int(height), colorspace


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    books = catalog.get("books", [])
    expected = int(catalog.get("series", {}).get("expected_title_count", 10))
    errors: list[str] = []
    expected_authors = [str(author) for author in catalog.get("series", {}).get("authors", [])]
    if expected_authors != ["Rodolfo Aramayo", "Kierie Aramayo"]:
        errors.append(f"catalog co-author list is incorrect: {expected_authors!r}")

    if len(books) != expected:
        errors.append(f"catalog contains {len(books)} books; expected {expected}")

    slugs = [str(book.get("slug", "")) for book in books]
    if len(set(slugs)) != len(slugs):
        errors.append("catalog contains duplicate slugs")

    vendor_ids = [str(book.get("vendor_id", "")) for book in books]
    if any(not value for value in vendor_ids) or len(set(vendor_ids)) != len(vendor_ids):
        errors.append("catalog Vendor IDs must be present and unique")

    for book in books:
        slug = book["slug"]
        source = PROJECT / book["source"]
        cover = PROJECT / book["cover"]
        epub = PROJECT / book["epub"]
        pdf = PROJECT / "output" / "pdf" / "preschool" / f"{slug}.pdf"

        if not source.is_file():
            errors.append(f"{slug}: missing source {book['source']}")
            continue

        markdown = source.read_text(encoding="utf-8")
        if PLACEHOLDERS.search(markdown):
            errors.append(f"{slug}: source contains unfinished placeholder text")
        image_refs = IMAGE_PATTERN.findall(markdown)
        if len(image_refs) != 4:
            errors.append(f"{slug}: expected four illustrated scenes, found {len(image_refs)}")
        for reference in image_refs:
            image = source.parent / reference
            if not image.is_file():
                errors.append(f"{slug}: missing story image {reference}")
                continue
            width, height, colorspace = identify(image)
            if width * height > 4_000_000:
                errors.append(f"{slug}: {reference} exceeds 4,000,000 pixels")
            if colorspace.casefold() != "srgb":
                errors.append(f"{slug}: {reference} is {colorspace}, expected sRGB")

        if not cover.is_file():
            errors.append(f"{slug}: missing store cover")
        else:
            width, height, colorspace = identify(cover)
            if (width, height) != (2550, 3300):
                errors.append(f"{slug}: cover is {width}x{height}, expected 2550x3300")
            if colorspace.casefold() != "srgb":
                errors.append(f"{slug}: cover is {colorspace}, expected sRGB")

        if not epub.is_file():
            errors.append(f"{slug}: missing EPUB")
        else:
            try:
                with zipfile.ZipFile(epub) as archive:
                    bad_member = archive.testzip()
                    if bad_member:
                        errors.append(f"{slug}: corrupt EPUB member {bad_member}")
                    names = set(archive.namelist())
                    package = ET.fromstring(archive.read("EPUB/content.opf"))
                    creators = [
                        " ".join((element.text or "").split())
                        for element in package.findall(".//{http://purl.org/dc/elements/1.1/}creator")
                    ]
                    if creators != expected_authors:
                        errors.append(f"{slug}: EPUB creators are {creators!r}, expected {expected_authors!r}")
                    story_sources: set[str] = set()
                    for name in names:
                        if not name.endswith(".xhtml") or name.endswith("cover.xhtml"):
                            continue
                        markup = archive.read(name).decode("utf-8")
                        for reference in re.findall(r'<img[^>]+src="([^"]+)"', markup):
                            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), reference))
                            story_sources.add(target)
                            if target not in names:
                                errors.append(f"{slug}: EPUB references missing image {reference}")
                    rasters = {
                        name for name in names if Path(name).suffix.lower() in {".jpg", ".jpeg", ".png"}
                    }
                    if len(story_sources) != 4:
                        errors.append(f"{slug}: EPUB contains {len(story_sources)} distinct story image references, expected four")
                    if len(rasters) != 5:
                        errors.append(f"{slug}: EPUB contains {len(rasters)} rasters, expected one cover and four story images")
            except zipfile.BadZipFile:
                errors.append(f"{slug}: EPUB is not a valid ZIP archive")

        if not pdf.is_file():
            errors.append(f"{slug}: missing image-rich PDF")
        else:
            info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
            page_match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
            if not page_match or int(page_match.group(1)) != 9:
                errors.append(f"{slug}: PDF should contain nine pages")
            images = subprocess.run(["pdfimages", "-list", str(pdf)], check=True, capture_output=True, text=True).stdout
            image_rows = [line for line in images.splitlines() if re.match(r"^\s*\d+\s+\d+\s+image\s+", line)]
            if len(image_rows) < 7:
                errors.append(f"{slug}: PDF contains {len(image_rows)} image placements, expected at least seven")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Preschool publication audit failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        f"Preschool publication audit passed: {len(books)} books, "
        f"{len(books) * 4} story images, {len(books)} covers, {len(books)} EPUBs, "
        f"and {len(books)} image-rich PDFs."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
