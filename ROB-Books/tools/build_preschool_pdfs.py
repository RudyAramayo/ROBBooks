#!/usr/bin/env python3
"""Build image-rich PDF editions of ROB's Little Helper Library."""

from __future__ import annotations

import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "preschool-apple-books-catalog.json"
OUTPUT = PROJECT / "output" / "pdf" / "preschool"
PAGE_W, PAGE_H = letter
MARGIN = 52

CREAM = colors.HexColor("#FFF8E8")
INK = colors.HexColor("#263238")
TEAL = colors.HexColor("#168C8C")
AMBER = colors.HexColor("#F2A52B")
CORAL = colors.HexColor("#E96F55")
PALE_TEAL = colors.HexColor("#DFF4F1")
PALE_AMBER = colors.HexColor("#FFF0C9")

IMAGE_RE = re.compile(r"!\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)


def clean_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    lines: list[str] = []
    for raw in text.strip().splitlines():
        line = raw.strip()
        if not line:
            lines.append("")
        elif re.match(r"^\d+\.\s", line):
            lines.append(line)
        else:
            lines.append(line)
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if re.match(r"^\d+\.\s", line):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append(line)
        elif line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "<br/><br/>".join(paragraphs)


def parse_source(source: Path) -> tuple[str, list[tuple[str, str, Path | None]]]:
    markdown = source.read_text(encoding="utf-8")
    title = markdown.splitlines()[0].removeprefix("# ").strip()
    matches = list(HEADING_RE.finditer(markdown))
    sections: list[tuple[str, str, Path | None]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        image_match = IMAGE_RE.search(body)
        image = source.parent / image_match.group(2) if image_match else None
        sections.append((match.group(1).strip(), clean_markdown(body), image))
    return title, sections


def draw_page_background(pdf: canvas.Canvas, accent: colors.Color = TEAL) -> None:
    pdf.setFillColor(CREAM)
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf.setFillColor(accent)
    pdf.roundRect(30, PAGE_H - 34, PAGE_W - 60, 9, 4.5, fill=1, stroke=0)
    pdf.setFillColor(AMBER)
    pdf.circle(PAGE_W - 42, 25, 7, fill=1, stroke=0)


def draw_footer(pdf: canvas.Canvas, title: str, page_number: int) -> None:
    pdf.setFillColor(colors.HexColor("#607D7D"))
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(MARGIN, 24, "ROB's Little Helper Library")
    number = str(page_number)
    pdf.drawString(PAGE_W - MARGIN - stringWidth(number, "Helvetica", 8.5), 24, number)
    pdf.setTitle(title)
    pdf.setAuthor("Rodolfo Aramayo")
    pdf.setCreator("OrbitusRobotics LLC")


def draw_paragraph(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    width: float,
    height: float,
    *,
    size: float = 17,
    leading: float = 24,
    align: int = TA_LEFT,
    color: colors.Color = INK,
) -> float:
    style = ParagraphStyle(
        "book",
        fontName="Helvetica",
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align,
        spaceAfter=0,
    )
    paragraph = Paragraph(text, style)
    used_w, used_h = paragraph.wrap(width, height)
    paragraph.drawOn(pdf, x, y_top - used_h)
    return used_h


def draw_contained_image(pdf: canvas.Canvas, path: Path, x: float, y: float, width: float, height: float) -> None:
    image = ImageReader(path)
    image_w, image_h = image.getSize()
    scale = min(width / image_w, height / image_h)
    draw_w, draw_h = image_w * scale, image_h * scale
    draw_x = x + (width - draw_w) / 2
    draw_y = y + (height - draw_h) / 2
    pdf.setFillColor(colors.white)
    pdf.roundRect(x - 8, y - 8, width + 16, height + 16, 18, fill=1, stroke=0)
    pdf.drawImage(image, draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")


def build_book(book: dict) -> Path:
    source = PROJECT / book["source"]
    title, sections = parse_source(source)
    note = sections[0]
    story_sections = sections[1:5]
    activity_sections = sections[5:]
    output = OUTPUT / f"{book['slug']}.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(output), pagesize=letter, pageCompression=1)

    cover = PROJECT / book["cover"]
    pdf.drawImage(ImageReader(cover), 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=False, mask="auto")
    draw_footer(pdf, title, 1)
    pdf.showPage()

    draw_page_background(pdf, TEAL)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_W / 2, PAGE_H - 100, "ROB'S LITTLE HELPER LIBRARY")
    draw_paragraph(pdf, title, MARGIN, PAGE_H - 158, PAGE_W - 2 * MARGIN, 130, size=31, leading=36, align=TA_CENTER)
    draw_paragraph(pdf, book["subtitle"], MARGIN + 30, PAGE_H - 278, PAGE_W - 2 * MARGIN - 60, 90, size=18, leading=24, align=TA_CENTER, color=CORAL)
    pdf.setFillColor(PALE_TEAL)
    pdf.roundRect(120, 210, PAGE_W - 240, 120, 28, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(PAGE_W / 2, 278, "Written by Rodolfo Aramayo")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(PAGE_W / 2, 246, "Ages 2-5  |  Read aloud together")
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_W / 2, 96, "Copyright © 2026 OrbitusRobotics LLC. All rights reserved.")
    draw_footer(pdf, title, 2)
    pdf.showPage()

    draw_page_background(pdf, AMBER)
    pdf.setFillColor(AMBER)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(MARGIN, PAGE_H - 94, note[0])
    illustration = story_sections[0][2]
    if illustration:
        draw_contained_image(pdf, illustration, PAGE_W - 222, PAGE_H - 360, 150, 226)
    draw_paragraph(pdf, note[1], MARGIN, PAGE_H - 145, PAGE_W - 300, 320, size=17, leading=25)
    pdf.setFillColor(PALE_AMBER)
    pdf.roundRect(MARGIN, 135, PAGE_W - 2 * MARGIN, 118, 22, fill=1, stroke=0)
    draw_paragraph(
        pdf,
        "Read slowly. Pause for pointing, counting, sounds, and wiggles. It is always okay for a little listener to turn the page.",
        MARGIN + 24,
        226,
        PAGE_W - 2 * MARGIN - 48,
        80,
        size=15,
        leading=22,
        align=TA_CENTER,
    )
    draw_footer(pdf, title, 3)
    pdf.showPage()

    page_number = 4
    accents = (TEAL, CORAL, AMBER, TEAL)
    for (heading, body, image_path), accent in zip(story_sections, accents):
        draw_page_background(pdf, accent)
        pdf.setFillColor(accent)
        pdf.setFont("Helvetica-Bold", 23)
        pdf.drawString(MARGIN, PAGE_H - 70, heading)
        if image_path:
            draw_contained_image(pdf, image_path, 105, 326, PAGE_W - 210, 354)
        draw_paragraph(pdf, body, MARGIN + 8, 300, PAGE_W - 2 * MARGIN - 16, 250, size=15.5, leading=20.5, align=TA_CENTER)
        draw_footer(pdf, title, page_number)
        pdf.showPage()
        page_number += 1

    for index, (heading, body, image_path) in enumerate(activity_sections):
        accent = AMBER if index == 0 else TEAL
        draw_page_background(pdf, accent)
        pdf.setFillColor(accent)
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawCentredString(PAGE_W / 2, PAGE_H - 105, heading)
        pdf.setFillColor(colors.white)
        pdf.roundRect(MARGIN, 198, PAGE_W - 2 * MARGIN, 425, 28, fill=1, stroke=0)
        draw_paragraph(pdf, body, MARGIN + 35, 565, PAGE_W - 2 * MARGIN - 70, 310, size=18, leading=28, align=TA_CENTER)
        if index == len(activity_sections) - 1 and story_sections[-1][2]:
            draw_contained_image(pdf, story_sections[-1][2], PAGE_W / 2 - 66, 75, 132, 100)
        draw_footer(pdf, title, page_number)
        pdf.showPage()
        page_number += 1

    pdf.save()
    print(f"built {output.relative_to(PROJECT)} ({page_number - 1} pages)")
    return output


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    outputs = [build_book(book) for book in catalog["books"]]
    print(f"Built {len(outputs)} image-rich preschool PDFs in {OUTPUT.relative_to(PROJECT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
