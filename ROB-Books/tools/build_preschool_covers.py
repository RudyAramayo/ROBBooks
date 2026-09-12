#!/usr/bin/env python3
"""Build deterministic Apple Books covers for ROB's Little Helper Library."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "preschool-apple-books-catalog.json"
TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf")
BODY_FONT = Path("/System/Library/Fonts/Avenir Next.ttc")
COVER_SIZE = (2550, 3300)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise FileNotFoundError(f"Required cover font is missing: {path}")
    return ImageFont.truetype(str(path), size=size)


def cover_accent(slug: str) -> str:
    if "pumpkin" in slug or "costume" in slug:
        return "#fb923c"
    if "christmas" in slug or "little-tree" in slug:
        return "#fbbf24"
    if "fireflies" in slug:
        return "#fde047"
    return "#34d399"


def wrapped_title(title: str) -> str:
    return "\n".join(textwrap.wrap(title.upper(), width=20, break_long_words=False))


def build_cover(book: dict[str, object], series_title: str, authors: list[str]) -> Path:
    art_path = PROJECT / str(book["cover_art"])
    output_path = PROJECT / str(book["cover"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(art_path) as source:
        art = source.convert("RGB")
    # Reserve separate title, illustration, and credit areas. Contain the
    # complete scene so neither a crop nor a text panel can hide ROB.
    cover = Image.new("RGB", COVER_SIZE, "#fff8e8")
    art_top, art_bottom = 650, 3020
    resized = ImageOps.contain(art, (2250, art_bottom - art_top), Image.Resampling.LANCZOS)
    left = (COVER_SIZE[0] - resized.width) // 2
    top = art_top + (art_bottom - art_top - resized.height) // 2
    accent = cover_accent(str(book["slug"]))
    draw = ImageDraw.Draw(cover)
    draw.rounded_rectangle(
        (left - 20, top - 20, left + resized.width + 20, top + resized.height + 20),
        radius=20, fill=accent,
    )
    cover.paste(resized, (left, top))
    draw.text(
        (1275, 85),
        f"{series_title.upper()}  •  BOOK {book['series_number']}",
        font=font(BODY_FONT, 62), anchor="mt",
        fill="#176967",
    )
    title = wrapped_title(str(book["title"]))
    draw.multiline_text(
        (1275, 200),
        title,
        font=font(TITLE_FONT, 144), anchor="ma", align="center",
        fill="#183b48",
        spacing=10,
    )
    title_box = draw.multiline_textbbox((1275, 200), title, font=font(TITLE_FONT, 144), spacing=10, anchor="ma", align="center")
    if title_box[0] < 150 or title_box[2] > 2400 or title_box[3] > 490:
        raise ValueError(f"Title does not fit the reserved header: {book['title']}")
    draw.text((1275, 535), str(book["subtitle"]), font=font(BODY_FONT, 64), anchor="mt", fill="#176967")
    draw.text((1275, 3090), "AGES 2–5  •  READ ALOUD TOGETHER", font=font(BODY_FONT, 58), anchor="mt", fill="#176967")
    credit = f"{' & '.join(authors)}  /  OrbitusRobotics LLC"
    credit_size = 52
    while draw.textlength(credit, font=font(BODY_FONT, credit_size)) > 2210 and credit_size > 38:
        credit_size -= 1
    draw.text((1275, 3190), credit, font=font(BODY_FONT, credit_size), anchor="mt", fill="#183b48")

    cover.convert("RGB").save(output_path, "JPEG", quality=94, subsampling=0, dpi=(300, 300), optimize=True)
    return output_path


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    authors = [str(author) for author in catalog["series"]["authors"]]
    for book in catalog["books"]:
        path = build_cover(book, str(catalog["series"]["title"]), authors)
        print(f"built {path.relative_to(PROJECT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
