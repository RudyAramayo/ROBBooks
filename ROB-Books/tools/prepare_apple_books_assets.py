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
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "apple-books-catalog.json"
SUBMISSION_RECORD = PROJECT / "publication" / "APPLE_BOOKS_SUBMISSION_RECORD.md"
SHORT_AXIS_MIN = 1400
MAX_INTERIOR_IMAGE_PIXELS = 4_000_000
REQUIRED_ACCESSIBILITY_FEATURES = {
    "alternativeText",
    "readingOrder",
    "structuralNavigation",
    "tableOfContents",
}


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


def epub_metadata_and_image_errors(path: Path, expected_vendor_id: str) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        opf_names = [name for name in archive.namelist() if name.lower().endswith(".opf")]
        if len(opf_names) != 1:
            return [f"expected one OPF package document, found {len(opf_names)}"]
        root = ET.fromstring(archive.read(opf_names[0]))
        namespaces = {
            "opf": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        identifiers = [element.text or "" for element in root.findall(".//dc:identifier", namespaces)]
        if f"urn:uuid:{expected_vendor_id}" not in identifiers:
            errors.append("EPUB identifier does not match the catalog vendor_id")
        features = {
            element.text or ""
            for element in root.findall(".//opf:meta[@property='schema:accessibilityFeature']", namespaces)
        }
        missing_features = REQUIRED_ACCESSIBILITY_FEATURES - features
        if missing_features:
            errors.append(f"EPUB is missing accessibility features: {', '.join(sorted(missing_features))}")
        for name in archive.namelist():
            if Path(name).suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            result = subprocess.run(
                ["magick", "identify", "-quiet", "-format", "%w\t%h\t%[colorspace]", "-"],
                input=archive.read(name),
                capture_output=True,
                check=True,
            )
            width_text, height_text, color_space = result.stdout.decode("utf-8").split("\t")
            width, height = int(width_text), int(height_text)
            if width * height > MAX_INTERIOR_IMAGE_PIXELS:
                errors.append(f"{name} is {width}x{height}, above Apple's {MAX_INTERIOR_IMAGE_PIXELS:,}-pixel guidance")
            if color_space.casefold() != "srgb":
                errors.append(f"{name} is {color_space}, expected sRGB")
    return errors


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

    vendor_ids: set[str] = set()
    submission_record = SUBMISSION_RECORD.read_text(encoding="utf-8") if SUBMISSION_RECORD.exists() else ""
    isbn_strategy = str(catalog.get("series", {}).get("isbn_strategy", "")).strip()
    if not isbn_strategy or isbn_strategy.casefold().startswith("pending"):
        (errors if release else warnings).append(
            "publisher must choose whether to supply ebook ISBNs before initial upload; Apple does not allow adding an ISBN later"
        )
    drm_strategy = str(catalog.get("series", {}).get("drm_strategy", "")).strip()
    if not drm_strategy or drm_strategy.casefold().startswith("pending"):
        (errors if release else warnings).append(
            "publisher must choose whether Apple DRM applies before Rights and Pricing is finalized"
        )

    for book in books:
        label = book.get("slug", "unknown")
        for field in ("title", "subtitle", "description", "audience", "category_recommendation"):
            if not str(book.get(field, "")).strip():
                errors.append(f"{label}: missing {field}")
        if len(str(book.get("description", "")).strip()) < 50:
            errors.append(f"{label}: description is shorter than Apple's 50-character minimum")
        categories = book.get("subject_categories", [])
        if len(categories) < 2:
            errors.append(f"{label}: Apple requires a main and secondary subject category")
        for category in categories:
            if not re.fullmatch(r"[A-Z]{3}\d{6}", str(category.get("code", ""))):
                errors.append(f"{label}: invalid BISAC code {category.get('code', '')}")
            if not str(category.get("label", "")).strip():
                errors.append(f"{label}: subject category label is missing")
        vendor_id = str(book.get("vendor_id", "")).strip()
        if not vendor_id:
            errors.append(f"{label}: vendor_id is missing")
        elif vendor_id in vendor_ids:
            errors.append(f"{label}: duplicate vendor_id {vendor_id}")
        else:
            vendor_ids.add(vendor_id)
            expected_submission_row = f"| {book['title']} | `{vendor_id}` |"
            if expected_submission_row not in submission_record:
                errors.append(f"{label}: title/vendor_id mapping differs from the Apple Books submission record")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(book.get("original_publication_date", ""))):
            errors.append(f"{label}: original publication date must use YYYY-MM-DD")
        isbn = re.sub(r"[- ]", "", str(book.get("isbn", "")))
        if isbn and not re.fullmatch(r"97[89]\d{10}", isbn):
            errors.append(f"{label}: ISBN must be a valid-looking 13-digit value")
        if any(value is not None for value in (book.get("interest_age_min"), book.get("interest_age_max"))):
            minimum, maximum = book.get("interest_age_min"), book.get("interest_age_max")
            if not isinstance(minimum, int) or not isinstance(maximum, int) or minimum > maximum:
                errors.append(f"{label}: invalid interest age range")
        if book.get("contains_explicit_content") is not False:
            errors.append(f"{label}: explicit-content answer must be the reviewed boolean false")
        if book.get("apply_drm") not in {None, True, False}:
            errors.append(f"{label}: apply_drm must be true, false, or null while awaiting the publisher decision")
        if book.get("volume_content_service_enabled") is not True:
            errors.append(f"{label}: Volume Content Service selection differs from the approved series default")
        if set(book.get("accessibility_features", [])) != REQUIRED_ACCESSIBILITY_FEATURES:
            errors.append(f"{label}: accessibility feature claims differ from the reviewed EPUB feature set")
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
        else:
            try:
                for problem in epub_metadata_and_image_errors(epub, vendor_id):
                    errors.append(f"{label}: {problem}")
            except (subprocess.CalledProcessError, ValueError, zipfile.BadZipFile, ET.ParseError) as error:
                errors.append(f"{label}: could not inspect EPUB: {error}")
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
