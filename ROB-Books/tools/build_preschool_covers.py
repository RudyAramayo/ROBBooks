#!/usr/bin/env python3
"""Build deterministic Apple Books covers for ROB's Little Helper Library."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


def build_cover(book: dict[str, object], series_title: str) -> Path:
    art_path = PROJECT / str(book["cover_art"])
    output_path = PROJECT / str(book["cover"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(art_path) as source:
        art = source.convert("RGB")
    scale = max(COVER_SIZE[0] / art.width, COVER_SIZE[1] / art.height)
    resized = art.resize((round(art.width * scale), round(art.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - COVER_SIZE[0]) // 2
    top = (resized.height - COVER_SIZE[1]) // 2
    cover = resized.crop((left, top, left + COVER_SIZE[0], top + COVER_SIZE[1])).convert("RGBA")

    overlay = Image.new("RGBA", COVER_SIZE, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 0, COVER_SIZE[0], 1260), fill=(8, 20, 32, 222))
    overlay_draw.rectangle((0, 2910, COVER_SIZE[0], COVER_SIZE[1]), fill=(8, 20, 32, 232))
    accent = cover_accent(str(book["slug"]))
    overlay_draw.rectangle((150, 150, 2400, 166), fill=accent)
    overlay_draw.rectangle((150, 2895, 2400, 2911), fill=accent)
    cover = Image.alpha_composite(cover, overlay)

    draw = ImageDraw.Draw(cover)
    draw.text(
        (170, 215),
        f"{series_title.upper()}  •  BOOK {book['series_number']}",
        font=font(BODY_FONT, 66),
        fill=accent,
    )
    title = wrapped_title(str(book["title"]))
    draw.multiline_text(
        (165, 350),
        title,
        font=font(TITLE_FONT, 174),
        fill="#ffffff",
        spacing=12,
    )
    title_box = draw.multiline_textbbox((165, 350), title, font=font(TITLE_FONT, 174), spacing=12)
    subtitle_y = min(title_box[3] + 48, 1090)
    draw.text((170, subtitle_y), str(book["subtitle"]), font=font(BODY_FONT, 72), fill="#f8fafc")
    draw.text((170, 3000), "AGES 2–5  •  READ ALOUD TOGETHER", font=font(BODY_FONT, 64), fill=accent)
    draw.text(
        (170, 3110),
        "Rodolfo Aramayo  /  OrbitusRobotics LLC",
        font=font(BODY_FONT, 52),
        fill="#f8fafc",
    )

    cover.convert("RGB").save(output_path, "JPEG", quality=94, subsampling=0, dpi=(300, 300), optimize=True)
    return output_path


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    for book in catalog["books"]:
        path = build_cover(book, str(catalog["series"]["title"]))
        print(f"built {path.relative_to(PROJECT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
