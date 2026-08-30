#!/usr/bin/env python3
"""Validate finished poster size, raster rendering, and QR destinations."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
import zxingcpp


PROJECT = Path(__file__).resolve().parents[1]
POSTERS = {
    "orbitus-learning-classroom-36x60.pdf": "https://www.orbitusrobotics.com/learn/",
    "rob-training-games-36x60.pdf": "https://www.orbitusrobotics.com/rob-training-apps/",
    "building-rob-books-36x60.pdf": "https://www.orbitusrobotics.com/books/",
}
EXPECTED_SIZE = (2592.0, 4320.0)


def run(*args: str) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=True)
    return result.stdout


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="orbitus-poster-validation-") as temporary:
        render_root = Path(temporary)
        for filename, expected_url in POSTERS.items():
            poster = PROJECT / "output" / "posters" / filename
            if not poster.exists():
                raise FileNotFoundError(poster)
            info = run("pdfinfo", str(poster))
            pages = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
            size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
            if not pages or pages.group(1) != "1":
                raise RuntimeError(f"{filename}: expected one PDF page")
            if not size or tuple(map(float, size.groups())) != EXPECTED_SIZE:
                raise RuntimeError(f"{filename}: expected 36×60 inches, found {size.group(0) if size else 'unknown'}")

            preview_base = render_root / poster.stem
            subprocess.run(
                ["pdftoppm", "-f", "1", "-l", "1", "-singlefile", "-r", "25", "-png", str(poster), str(preview_base)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            preview = preview_base.with_suffix(".png")
            with Image.open(preview) as image:
                if image.size != (900, 1500):
                    raise RuntimeError(f"{filename}: 25 dpi proof has unexpected dimensions {image.size}")
                decoded = {result.text for result in zxingcpp.read_barcodes(image)}
            if expected_url not in decoded:
                raise RuntimeError(f"{filename}: QR did not decode to {expected_url}; decoded {sorted(decoded)}")
            print(f"PASS {filename}: 36×60 inches; QR → {expected_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
