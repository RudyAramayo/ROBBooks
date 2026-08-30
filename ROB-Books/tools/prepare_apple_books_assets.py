#!/usr/bin/env python3
"""Build and validate Apple Books cover and metadata preparation assets.

This does not upload books. Release validation deliberately fails until every
EPUB and store identifier exists and the human release checklist is complete.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "apple-books-catalog.json"
SHORT_AXIS_MIN = 1400


def run(*args: str) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=True)
    return result.stdout


def pdf_pages(path: Path) -> int:
    info = run("pdfinfo", str(path))
    match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not read page count from {path}")
    return int(match.group(1))


def image_properties(path: Path) -> tuple[int, int, str]:
    details = run("sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "space", str(path))
    width = re.search(r"pixelWidth:\s+(\d+)", details)
    height = re.search(r"pixelHeight:\s+(\d+)", details)
    space = re.search(r"space:\s+(.+)", details)
    if not (width and height and space):
        raise RuntimeError(f"Could not inspect cover {path}")
    return int(width.group(1)), int(height.group(1)), space.group(1).strip()


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def prepare_covers(catalog: dict) -> None:
    for book in catalog["books"]:
        pdf = PROJECT / book["pdf"]
        cover = PROJECT / book["cover"]
        cover.parent.mkdir(parents=True, exist_ok=True)
        if not pdf.exists():
            raise FileNotFoundError(pdf)
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                "1",
                "-l",
                "1",
                "-singlefile",
                "-r",
                "300",
                "-jpeg",
                "-jpegopt",
                "quality=94,progressive=y,optimize=y",
                str(pdf),
                str(cover.with_suffix("")),
            ],
            check=True,
        )
        print(f"prepared {cover.relative_to(PROJECT)}")


def validate(catalog: dict, release: bool) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    books = catalog.get("books", [])
    if len(books) != 10:
        errors.append(f"catalog should contain 10 books, found {len(books)}")

    numbered_total = sum(float(book["price_usd"]) for book in books if 1 <= int(book["position"]) <= 8)
    expected_total = float(catalog["series"]["individual_volume_total_usd"])
    if abs(numbered_total - expected_total) > 0.001:
        errors.append(f"numbered-volume prices total ${numbered_total:.2f}, expected ${expected_total:.2f}")

    collection = next((book for book in books if book["slug"] == "complete-builders-field-manual"), None)
    if not collection or float(collection["price_usd"]) != float(catalog["series"]["collection_price_usd"]):
        errors.append("collection price does not match the Complete Builder's Field Manual")

    for book in books:
        label = book.get("slug", "unknown")
        for field in ("title", "subtitle", "description", "audience", "category_recommendation"):
            if not str(book.get(field, "")).strip():
                errors.append(f"{label}: missing {field}")
        pdf = PROJECT / book["pdf"]
        cover = PROJECT / book["cover"]
        epub = PROJECT / book["epub"]
        if not pdf.exists():
            errors.append(f"{label}: missing PDF {book['pdf']}")
        elif pdf_pages(pdf) != int(book["pages"]):
            errors.append(f"{label}: PDF page count differs from catalog")
        if not cover.exists():
            errors.append(f"{label}: missing cover {book['cover']}")
        else:
            width, height, color_space = image_properties(cover)
            if min(width, height) < SHORT_AXIS_MIN:
                errors.append(f"{label}: cover short axis is {min(width, height)}px; minimum is {SHORT_AXIS_MIN}px")
            if "RGB" not in color_space:
                errors.append(f"{label}: cover color space is {color_space}, expected RGB")
        if not epub.exists():
            message = f"{label}: accessible EPUB 3 conversion is pending"
            (errors if release else warnings).append(message)
        if release:
            if not str(book.get("apple_books_id", "")).strip():
                errors.append(f"{label}: Apple Books ID is missing")
            if not str(book.get("apple_books_url", "")).strip():
                errors.append(f"{label}: Apple Books URL is missing")

    for warning in warnings:
        print(f"PENDING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Apple Books {'release' if release else 'preparation'} validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Apple Books {'release' if release else 'preparation'} validation passed for {len(books)} books.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-covers", action="store_true", help="render 300 dpi RGB JPEG covers from the approved PDF first pages")
    parser.add_argument("--release", action="store_true", help="require final EPUBs and Apple Books identifiers")
    args = parser.parse_args()
    catalog = load_catalog()
    if args.prepare_covers:
        prepare_covers(catalog)
    return validate(catalog, args.release)


if __name__ == "__main__":
    raise SystemExit(main())
