#!/usr/bin/env python3
"""Validate the reproducible IngramSpark interior build outputs."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops
from pypdf import PdfReader

from build_ingramspark_interiors import (
    BLEED,
    BOOKS,
    OUTPUT_DIR,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    ROOT,
    SOURCE_DIR,
    TRIM_HEIGHT,
    TRIM_WIDTH,
    WORK_DIR,
)


def capture(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def nearly(actual: float, expected: float) -> bool:
    return abs(actual - expected) < 0.02


def check_pdf_structure(book: str) -> tuple[int, int]:
    source = PdfReader(SOURCE_DIR / f"{book}.pdf")
    output_path = OUTPUT_DIR / f"{book}-interior.pdf"
    output = PdfReader(output_path)
    expected_pages = len(source.pages) + (len(source.pages) % 2)
    if len(output.pages) != expected_pages or len(output.pages) % 2:
        raise ValueError(f"{book}: unexpected page count {len(output.pages)}")
    for number, page in enumerate(output.pages, start=1):
        if not nearly(float(page.mediabox.width), PAGE_WIDTH) or not nearly(
            float(page.mediabox.height), PAGE_HEIGHT
        ):
            raise ValueError(f"{book}: page {number} has incorrect dimensions")
    if output.is_encrypted:
        raise ValueError(f"{book}: output is encrypted")

    info = capture(["pdfinfo", str(output_path)])
    if "PDF subtype:    PDF/X-1a:2001" not in info:
        raise ValueError(f"{book}: PDF/X-1a subtype not reported")

    fonts = capture(["pdffonts", str(output_path)]).splitlines()[2:]
    for font in fonts:
        match = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", font)
        if not match or match.group(1) != "yes":
            raise ValueError(f"{book}: unembedded or unparseable font record: {font}")

    images = capture(["pdfimages", "-list", str(output_path)]).splitlines()[2:]
    for image in images:
        fields = image.split()
        if len(fields) < 14:
            continue
        color = fields[5].lower()
        x_ppi = int(fields[12])
        y_ppi = int(fields[13])
        if color not in {"cmyk", "gray"}:
            raise ValueError(f"{book}: non-CMYK image record: {image}")
        # IngramSpark recommends 300 ppi and rejects interior images below
        # 72 ppi. Use 200 ppi as a deliberately stricter production floor;
        # upsampling a lower source would not create real detail.
        if x_ppi < 200 or y_ppi < 200:
            raise ValueError(f"{book}: image below 200 ppi: {image}")

    subprocess.run(
        ["gs", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=nullpage", str(output_path)],
        check=True,
    )
    return len(source.pages), len(output.pages)


def render_page(pdf: Path, page_number: int, output: Path) -> Path:
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            str(page_number),
            "-l",
            str(page_number),
            "-r",
            "72",
            "-singlefile",
            "-png",
            str(pdf),
            str(output.with_suffix("")),
        ],
        check=True,
        capture_output=True,
    )
    return output


def check_trim_placement(book: str) -> None:
    source_path = SOURCE_DIR / f"{book}.pdf"
    work_path = WORK_DIR / f"{book}-interior-bleed-rgb.pdf"
    count = len(PdfReader(source_path).pages)
    samples = sorted({1, min(2, count), max(1, count // 2), count})
    with tempfile.TemporaryDirectory(prefix="ingram-trim-check-") as directory:
        root = Path(directory)
        for page_number in samples:
            source_png = render_page(source_path, page_number, root / "source.png")
            bleed_png = render_page(work_path, page_number, root / "bleed.png")
            source_image = Image.open(source_png).convert("RGB")
            bleed_image = Image.open(bleed_png).convert("RGB")
            x_offset = 0 if page_number % 2 else round(BLEED)
            trim = bleed_image.crop(
                (
                    x_offset,
                    round(BLEED),
                    x_offset + round(TRIM_WIDTH),
                    round(BLEED + TRIM_HEIGHT),
                )
            )
            if ImageChops.difference(source_image, trim).getbbox() is not None:
                raise ValueError(f"{book}: trim-region mismatch on page {page_number}")


def main() -> None:
    total_source = 0
    total_output = 0
    for book in BOOKS:
        source_pages, output_pages = check_pdf_structure(book)
        check_trim_placement(book)
        total_source += source_pages
        total_output += output_pages
        size_mb = (OUTPUT_DIR / f"{book}-interior.pdf").stat().st_size / 1_000_000
        print(f"PASS {book}: {source_pages} -> {output_pages} pages, {size_mb:.1f} MB")
    print(f"PASS all interiors: {total_source} source pages -> {total_output} print pages")


if __name__ == "__main__":
    main()
