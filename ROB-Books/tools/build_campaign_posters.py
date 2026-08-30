#!/usr/bin/env python3
"""Build the three 36 x 60 inch Orbitus Robotics campaign posters."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


FINISHED_SIZE = portrait((36 * inch, 60 * inch))
SAFE = 1.25 * inch

NAVY = HexColor("#071020")
INK = HexColor("#050811")
INDIGO = HexColor("#4F46E5")
CYAN = HexColor("#22D3EE")
LIME = HexColor("#A3E635")
GOLD = HexColor("#FBBF24")
SOFT = HexColor("#DDE7FF")
MUTED = HexColor("#A8B6D8")

FONT_REGULAR = "OrbitusArial"
FONT_BOLD = "OrbitusDIN"
FONT_HEAVY = "OrbitusArialBlack"


def register_fonts() -> None:
    pdfmetrics.registerFont(
        TTFont(FONT_REGULAR, "/System/Library/Fonts/Supplemental/Arial.ttf")
    )
    pdfmetrics.registerFont(
        TTFont(FONT_BOLD, "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont(FONT_HEAVY, "/System/Library/Fonts/Supplemental/Arial Black.ttf")
    )


def image_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def draw_cover_image(
    canvas: Canvas,
    path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    opacity: float = 1.0,
) -> None:
    """Cover a rectangle with an image, preserving aspect ratio and cropping."""
    source_width, source_height = image_dimensions(path)
    scale = max(width / source_width, height / source_height)
    draw_width = source_width * scale
    draw_height = source_height * scale
    canvas.saveState()
    canvas.rect(x, y, width, height, stroke=0, fill=0)
    canvas.clipPath(canvas.beginPath())
    if opacity < 1:
        canvas.setFillAlpha(opacity)
    canvas.drawImage(
        str(path),
        x + (width - draw_width) / 2,
        y + (height - draw_height) / 2,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.restoreState()


def clip_and_draw_cover(
    canvas: Canvas,
    path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    opacity: float = 1.0,
) -> None:
    source_width, source_height = image_dimensions(path)
    scale = max(width / source_width, height / source_height)
    draw_width = source_width * scale
    draw_height = source_height * scale
    clip = canvas.beginPath()
    clip.rect(x, y, width, height)
    canvas.saveState()
    canvas.clipPath(clip, stroke=0, fill=0)
    canvas.setFillAlpha(opacity)
    canvas.drawImage(
        str(path),
        x + (width - draw_width) / 2,
        y + (height - draw_height) / 2,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.restoreState()


def draw_vertical_gradient(
    canvas: Canvas,
    top: Color,
    bottom: Color,
    *,
    x: float = 0,
    y: float = 0,
    width: float = FINISHED_SIZE[0],
    height: float = FINISHED_SIZE[1],
    steps: int = 160,
) -> None:
    for index in range(steps):
        ratio = index / max(steps - 1, 1)
        color = Color(
            bottom.red + (top.red - bottom.red) * ratio,
            bottom.green + (top.green - bottom.green) * ratio,
            bottom.blue + (top.blue - bottom.blue) * ratio,
        )
        canvas.setFillColor(color)
        canvas.rect(
            x,
            y + height * index / steps,
            width,
            height / steps + 1,
            stroke=0,
            fill=1,
        )


def draw_readability_scrims(canvas: Canvas, *, strong_top: bool = True) -> None:
    width, height = FINISHED_SIZE
    bands = 42
    for index in range(bands):
        ratio = index / max(bands - 1, 1)
        alpha = (0.74 if strong_top else 0.56) * (1 - ratio) ** 1.4
        canvas.saveState()
        canvas.setFillColor(INK)
        canvas.setFillAlpha(alpha)
        canvas.rect(0, height * (0.59 + ratio * 0.41), width, height * 0.41 / bands + 2, 0, 1)
        canvas.restoreState()
    for index in range(bands):
        ratio = index / max(bands - 1, 1)
        alpha = 0.85 * (1 - ratio) ** 1.6
        canvas.saveState()
        canvas.setFillColor(INK)
        canvas.setFillAlpha(alpha)
        canvas.rect(0, height * ratio * 0.32, width, height * 0.32 / bands + 2, 0, 1)
        canvas.restoreState()


def draw_brand(canvas: Canvas, logo_path: Path, *, dark_chip: bool = True) -> None:
    x = SAFE
    y = FINISHED_SIZE[1] - SAFE - 1.7 * inch
    if dark_chip:
        canvas.saveState()
        canvas.setFillColor(INK)
        canvas.setFillAlpha(0.64)
        canvas.roundRect(x - 0.35 * inch, y - 0.3 * inch, 15.8 * inch, 2.25 * inch, 0.45 * inch, 0, 1)
        canvas.restoreState()
    canvas.drawImage(
        str(logo_path),
        x,
        y,
        width=14.5 * inch,
        height=1.55 * inch,
        preserveAspectRatio=True,
        anchor="w",
        mask="auto",
    )


def draw_pill(canvas: Canvas, x: float, y: float, text: str, color: Color) -> float:
    canvas.setFont(FONT_HEAVY, 0.52 * inch)
    pad_x = 0.42 * inch
    width = canvas.stringWidth(text, FONT_HEAVY, 0.52 * inch) + 2 * pad_x
    height = 1.12 * inch
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.setFillAlpha(0.78)
    canvas.roundRect(x, y, width, height, height / 2, 0, 1)
    canvas.setStrokeColor(color)
    canvas.setStrokeAlpha(0.95)
    canvas.setLineWidth(0.06 * inch)
    canvas.roundRect(x, y, width, height, height / 2, 1, 0)
    canvas.setFillAlpha(1)
    canvas.setFillColor(white)
    canvas.drawString(x + pad_x, y + 0.31 * inch, text)
    canvas.restoreState()
    return width


def draw_headline(
    canvas: Canvas,
    lines: list[str],
    *,
    top: float,
    font_size: float,
    leading: float,
    accent_line: int | None = None,
    accent_color: Color = CYAN,
) -> float:
    y = top
    for index, line in enumerate(lines):
        canvas.setFont(FONT_BOLD, font_size)
        canvas.setFillColor(accent_color if index == accent_line else white)
        canvas.drawString(SAFE, y - font_size, line)
        y -= leading
    return y


def draw_wrapped_text(
    canvas: Canvas,
    text: str,
    *,
    x: float,
    top: float,
    max_width: float,
    font: str,
    size: float,
    leading: float,
    color: Color,
    max_lines: int | None = None,
) -> float:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and canvas.stringWidth(candidate, font, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if max_lines is not None:
        lines = lines[:max_lines]
    canvas.setFont(font, size)
    canvas.setFillColor(color)
    y = top
    for line in lines:
        canvas.drawString(x, y - size, line)
        y -= leading
    return y


def draw_qr(canvas: Canvas, url: str, *, x: float, y: float, size: float) -> None:
    quiet = size * 0.07
    canvas.setFillColor(white)
    canvas.roundRect(x, y, size, size, 0.42 * inch, 0, 1)
    code = qr.QrCodeWidget(url, barLevel="H")
    bounds = code.getBounds()
    code_width = bounds[2] - bounds[0]
    code_height = bounds[3] - bounds[1]
    usable = size - 2 * quiet
    drawing = Drawing(
        usable,
        usable,
        transform=[usable / code_width, 0, 0, usable / code_height, 0, 0],
    )
    drawing.add(code)
    renderPDF.draw(drawing, canvas, x + quiet, y + quiet)


def draw_cta_panel(
    canvas: Canvas,
    *,
    url: str,
    eyebrow: str,
    action: str,
    detail: str,
    accent: Color,
) -> None:
    panel_x = SAFE
    panel_y = SAFE
    panel_width = FINISHED_SIZE[0] - 2 * SAFE
    panel_height = 10.25 * inch
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.setFillAlpha(0.92)
    canvas.roundRect(panel_x, panel_y, panel_width, panel_height, 0.65 * inch, 0, 1)
    canvas.setStrokeColor(accent)
    canvas.setStrokeAlpha(0.8)
    canvas.setLineWidth(0.08 * inch)
    canvas.roundRect(panel_x, panel_y, panel_width, panel_height, 0.65 * inch, 1, 0)
    canvas.restoreState()

    qr_size = 8.05 * inch
    qr_x = panel_x + panel_width - qr_size - 1.05 * inch
    qr_y = panel_y + 1.1 * inch
    draw_qr(canvas, url, x=qr_x, y=qr_y, size=qr_size)

    copy_x = panel_x + 1.1 * inch
    copy_width = qr_x - copy_x - 0.9 * inch
    canvas.setFillColor(accent)
    canvas.setFont(FONT_HEAVY, 0.54 * inch)
    canvas.drawString(copy_x, panel_y + 8.45 * inch, eyebrow.upper())
    y = draw_wrapped_text(
        canvas,
        action,
        x=copy_x,
        top=panel_y + 7.9 * inch,
        max_width=copy_width,
        font=FONT_BOLD,
        size=1.45 * inch,
        leading=1.45 * inch,
        color=white,
        max_lines=3,
    )
    draw_wrapped_text(
        canvas,
        detail,
        x=copy_x,
        top=y - 0.1 * inch,
        max_width=copy_width,
        font=FONT_REGULAR,
        size=0.52 * inch,
        leading=0.72 * inch,
        color=SOFT,
        max_lines=2,
    )
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_HEAVY, 0.36 * inch)
    canvas.drawString(copy_x, panel_y + 0.74 * inch, url.replace("https://", ""))


def draw_classroom_poster(root: Path, output: Path) -> None:
    canvas = Canvas(str(output), pagesize=FINISHED_SIZE, pageCompression=1)
    canvas.setTitle("Orbitus Robotics Learning Classroom - 36 x 60 inch poster")
    canvas.setAuthor("Orbitus Robotics")
    clip_and_draw_cover(
        canvas,
        root / "assets/posters/rob-learning-classroom-hero.png",
        0,
        0,
        FINISHED_SIZE[0],
        FINISHED_SIZE[1],
    )
    draw_readability_scrims(canvas, strong_top=True)
    draw_brand(canvas, root / "assets/orbitus-horizontal-logo.png")
    y = draw_headline(
        canvas,
        ["BUILD.", "CODE.", "MAKE ROB MOVE."],
        top=FINISHED_SIZE[1] - 5.25 * inch,
        font_size=3.8 * inch,
        leading=3.6 * inch,
        accent_line=2,
        accent_color=LIME,
    )
    y = draw_wrapped_text(
        canvas,
        "A free learning classroom - from your first circuit to the systems behind a real robot.",
        x=SAFE,
        top=y - 1.05 * inch,
        max_width=30 * inch,
        font=FONT_REGULAR,
        size=0.93 * inch,
        leading=1.18 * inch,
        color=SOFT,
        max_lines=3,
    )
    pill_y = 38.3 * inch
    x = SAFE
    for text_value, color in [
        ("80 INTERACTIVE MISSIONS", LIME),
        ("AGES 8-16", CYAN),
        ("100% VIRTUAL", GOLD),
    ]:
        x += draw_pill(canvas, x, pill_y, text_value, color) + 0.28 * inch
    draw_cta_panel(
        canvas,
        url="https://www.orbitusrobotics.com/learn/",
        eyebrow="Start here",
        action="SCAN TO BEGIN YOUR LEARNING JOURNEY",
        detail="Circuit Quest, ROB Training, books, and open-source projects.",
        accent=LIME,
    )
    canvas.showPage()
    canvas.save()


def draw_game_poster(root: Path, output: Path, game_art: Path) -> None:
    canvas = Canvas(str(output), pagesize=FINISHED_SIZE, pageCompression=1)
    canvas.setTitle("ROB Training Games - 36 x 60 inch poster")
    canvas.setAuthor("Orbitus Robotics")
    clip_and_draw_cover(canvas, game_art, 0, 0, FINISHED_SIZE[0], FINISHED_SIZE[1])
    draw_readability_scrims(canvas, strong_top=True)
    draw_brand(canvas, root / "assets/orbitus-horizontal-logo.png")
    y = draw_headline(
        canvas,
        ["TRAIN ROB.", "WIN BATTLES.", "UPGRADE EVERYTHING."],
        top=FINISHED_SIZE[1] - 5.2 * inch,
        font_size=3.45 * inch,
        leading=3.35 * inch,
        accent_line=2,
        accent_color=CYAN,
    )
    y = draw_wrapped_text(
        canvas,
        "Drive, battle, earn points, and engineer your way through every mission.",
        x=SAFE,
        top=y - 1.25 * inch,
        max_width=31 * inch,
        font=FONT_REGULAR,
        size=0.92 * inch,
        leading=1.15 * inch,
        color=SOFT,
        max_lines=2,
    )
    pill_y = 39.1 * inch
    x = SAFE
    for text_value, color in [
        ("WEB", LIME),
        ("IPHONE + IPAD", CYAN),
        ("APPLE VISION PRO", GOLD),
    ]:
        x += draw_pill(canvas, x, pill_y, text_value, color) + 0.28 * inch
    draw_cta_panel(
        canvas,
        url="https://www.orbitusrobotics.com/rob-training-apps/",
        eyebrow="Choose your platform",
        action="SCAN TO PLAY AND GET THE APPS",
        detail="One ROB Training campaign across mobile, web, and spatial computing.",
        accent=CYAN,
    )
    canvas.showPage()
    canvas.save()


def draw_book_card(
    canvas: Canvas,
    image_path: Path,
    *,
    x: float,
    y: float,
    width: float,
    angle: float,
    shadow: bool = True,
) -> None:
    source_width, source_height = image_dimensions(image_path)
    height = width * source_height / source_width
    canvas.saveState()
    canvas.translate(x + width / 2, y + height / 2)
    canvas.rotate(angle)
    if shadow:
        canvas.setFillColor(INK)
        canvas.setFillAlpha(0.62)
        canvas.roundRect(-width / 2 + 0.2 * inch, -height / 2 - 0.2 * inch, width, height, 0.25 * inch, 0, 1)
    canvas.setFillAlpha(1)
    canvas.drawImage(
        str(image_path),
        -width / 2,
        -height / 2,
        width=width,
        height=height,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.setStrokeColor(white)
    canvas.setStrokeAlpha(0.86)
    canvas.setLineWidth(0.07 * inch)
    canvas.rect(-width / 2, -height / 2, width, height, 1, 0)
    canvas.restoreState()


def draw_books_poster(root: Path, output: Path) -> None:
    canvas = Canvas(str(output), pagesize=FINISHED_SIZE, pageCompression=1)
    canvas.setTitle("Building R.O.B. Books - 36 x 60 inch poster")
    canvas.setAuthor("Orbitus Robotics")
    draw_vertical_gradient(canvas, HexColor("#16275E"), INK)

    canvas.saveState()
    canvas.setFillColor(CYAN)
    canvas.setFillAlpha(0.11)
    for radius in [7, 10, 13, 16, 19, 22]:
        canvas.setLineWidth(0.05 * inch)
        canvas.circle(28 * inch, 33 * inch, radius * inch, 1, 0)
    canvas.restoreState()

    draw_brand(canvas, root / "assets/orbitus-horizontal-logo.png", dark_chip=False)
    y = draw_headline(
        canvas,
        ["THE STORY.", "THE SCIENCE.", "THE WHOLE BUILD."],
        top=FINISHED_SIZE[1] - 5.25 * inch,
        font_size=3.45 * inch,
        leading=3.25 * inch,
        accent_line=2,
        accent_color=GOLD,
    )
    y = draw_wrapped_text(
        canvas,
        "Picture-book wonder, hands-on maker lessons, and the complete engineering record of R.O.B.",
        x=SAFE,
        top=y - 1.15 * inch,
        max_width=31 * inch,
        font=FONT_REGULAR,
        size=0.86 * inch,
        leading=1.1 * inch,
        color=SOFT,
        max_lines=3,
    )

    covers = root / "assets/posters/book-covers"
    cards = [
        ("volume-1-meet-rob.jpg", 1.7, 16.6, 7.1, -7),
        ("volume-2-circuits-and-signals.jpg", 7.4, 17.0, 7.1, -3),
        ("volume-3-motion-workshop.jpg", 13.1, 17.2, 7.1, 1),
        ("volume-4-mission-control.jpg", 18.8, 16.8, 7.1, 5),
        ("complete-builders-field-manual.jpg", 24.8, 17.1, 7.1, 8),
    ]
    for filename, x, card_y, width, angle in cards:
        draw_book_card(
            canvas,
            covers / filename,
            x=x * inch,
            y=card_y * inch,
            width=width * inch,
            angle=angle,
        )
    draw_book_card(
        canvas,
        covers / "rob-and-the-lost-yellow-ball.jpg",
        x=12.7 * inch,
        y=15.4 * inch,
        width=10.6 * inch,
        angle=0,
    )

    draw_cta_panel(
        canvas,
        url="https://www.orbitusrobotics.com/books/",
        eyebrow="Read with ROB",
        action="SCAN TO EXPLORE THE ROB LIBRARY",
        detail="Meet every volume, preview the series, and find Apple Books editions.",
        accent=GOLD,
    )
    canvas.showPage()
    canvas.save()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-art",
        type=Path,
        default=Path("../ORobotics/static/images/rob-simulator/rob-training-key-art.png"),
        help="Path to the ROB Training key art.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = root / "output/posters"
    output.mkdir(parents=True, exist_ok=True)
    game_art = args.game_art.expanduser().resolve()
    if not game_art.exists():
        raise SystemExit(f"ROB Training key art not found: {game_art}")

    register_fonts()
    draw_classroom_poster(root, output / "orbitus-learning-classroom-36x60.pdf")
    draw_game_poster(root, output / "rob-training-games-36x60.pdf", game_art)
    draw_books_poster(root, output / "building-rob-books-36x60.pdf")
    print(f"Built 3 posters in {output}")


if __name__ == "__main__":
    main()
