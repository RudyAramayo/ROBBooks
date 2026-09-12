#!/usr/bin/env python3
"""Build print-ready IngramSpark wrap covers from official templates."""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import CMYKColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from build_ingramspark_interiors import convert_to_pdfx


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "publication" / "apple-books-catalog.json"
TEMPLATE_DIR = ROOT / "publication" / "ingramspark" / "templates"
FRONT_DIR = ROOT / "output" / "apple-books" / "covers"
OUTPUT_DIR = ROOT / "output" / "pdf" / "ingramspark" / "covers"
TMP_DIR = ROOT / "tmp" / "pdfs" / "covers"

PAGE_W = 1512.0
PAGE_H = 864.0
COVER_BOTTOM = 54.0
TRIM_INSET = 9.0
FRONT_TRIM_X = 891.0
TRIM_W = 612.0
TRIM_H = 792.0

WHITE = CMYKColor(0, 0, 0, 0)
INK = CMYKColor(80, 55, 35, 83)
INK_2 = CMYKColor(72, 48, 31, 72)
MUTED = CMYKColor(10, 5, 0, 12)

REGULAR_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD_FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ITALIC_FONT = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"


BOOKS = {
    "rob-and-the-lost-yellow-ball": {
        "isbn": "9798240834219",
        "template": "9798240834219-ColorPF.pdf",
        "print_pages": 24,
        "series_label": "A ROB STORY",
        "accent": (70, 0, 45, 0),
        "topics": ["Stop, observe, plan, and check", "Kindness and careful problem-solving", "A warm read-aloud for ages 5-6"],
    },
    "volume-1-meet-rob": {
        "isbn": "9798182746397",
        "template": "9798182746397-Perfect.pdf",
        "print_pages": 38,
        "series_label": "BUILDING R.O.B. - VOLUME 1",
        "accent": (72, 8, 0, 0),
        "topics": ["Structure, energy, and sensors", "Feedback, iteration, and engineering logs", "Evidence from a real hand-built robot"],
    },
    "volume-2-circuits-and-signals": {
        "isbn": "9798182746403",
        "template": "9798182746403-Perfect.pdf",
        "print_pages": 36,
        "series_label": "BUILDING R.O.B. - VOLUME 2",
        "accent": (0, 28, 94, 2),
        "topics": ["Low-voltage circuits and signal paths", "PWM, serial messages, and sensors", "Commands, measurements, and safety claims"],
    },
    "volume-3-motion-workshop": {
        "isbn": "9798182746410",
        "template": "9798182746410-Perfect.pdf",
        "print_pages": 36,
        "series_label": "BUILDING R.O.B. - VOLUME 3",
        "accent": (76, 0, 38, 4),
        "topics": ["Tracked drive, gearing, and loads", "Fabrication, assembly, and service access", "Tests that reveal what a prototype proves"],
    },
    "volume-4-mission-control": {
        "isbn": "9798182746427",
        "template": "9798182746427-Perfect.pdf",
        "print_pages": 40,
        "series_label": "BUILDING R.O.B. - VOLUME 4",
        "accent": (54, 70, 0, 4),
        "topics": ["Computers, cameras, maps, and networks", "Privacy choices and bounded commands", "Verified behavior over impressive demos"],
    },
    "volume-5-ai-robotics-with-codex": {
        "isbn": "9798182746434",
        "template": "9798182746434-Perfect.pdf",
        "print_pages": 44,
        "series_label": "BUILDING R.O.B. - VOLUME 5",
        "accent": (67, 0, 72, 7),
        "topics": ["Swift, MLX, perception, and recording", "Identity, stage shows, and spatial interfaces", "Generative systems outside motor authority"],
    },
    "volume-6-amber-dual-arm-robotics": {
        "isbn": "9798182746441",
        "template": "9798182746441-Perfect.pdf",
        "print_pages": 34,
        "series_label": "BUILDING R.O.B. - VOLUME 6",
        "accent": (0, 48, 96, 0),
        "topics": ["Two seven-joint AMBER B1 arms", "URDF, CAN identity, UDP, and LCM", "Measured transforms and fail-closed tests"],
    },
    "volume-7-engineering-robcontrollervision": {
        "isbn": "9798182746458",
        "template": "9798182746458-Perfect.pdf",
        "print_pages": 38,
        "series_label": "BUILDING R.O.B. - VOLUME 7",
        "accent": (77, 8, 0, 0),
        "topics": ["Swift 6 and authenticated sessions", "Spatial input and independent arm leases", "Bounded video, speech, and immersive 360"],
    },
    "volume-8-engineering-cerebro": {
        "isbn": "9798182746465",
        "template": "9798182746465-Perfect.pdf",
        "print_pages": 50,
        "series_label": "BUILDING R.O.B. - VOLUME 8",
        "accent": (0, 30, 96, 0),
        "topics": ["RGB-D and panoramic perception", "Local and cloud AI with private context", "Control arbitration and bounded autonomy"],
    },
    "complete-builders-field-manual": {
        "isbn": "9798182746472",
        "template": "9798182746472-Perfect.pdf",
        "print_pages": 236,
        "series_label": "THE COMPLETE BUILDING R.O.B. COLLECTION",
        "accent": (8, 91, 75, 8),
        "topics": ["Volumes 1-8 in one field reference", "Mechanics, electronics, software, and AI", "Evidence-led verification and safe operations"],
    },
}


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("ROB-Regular", REGULAR_FONT))
    pdfmetrics.registerFont(TTFont("ROB-Bold", BOLD_FONT))
    pdfmetrics.registerFont(TTFont("ROB-Italic", ITALIC_FONT))


def render_template(template: Path, dpi: int, output_prefix: Path) -> Path:
    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "1",
            "-singlefile",
            "-png",
            "-r",
            str(dpi),
            str(template),
            str(output_prefix),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return output_prefix.with_suffix(".png")


def detect_bleed_x(template: Path, work_dir: Path) -> float:
    preview = render_template(template, 72, work_dir / f"{template.stem}-72")
    pixels = np.asarray(Image.open(preview).convert("RGB"))
    cyan = np.all(pixels == (179, 230, 250), axis=2)
    _, xs = np.where(cyan)
    if not len(xs):
        raise RuntimeError(f"Could not detect cover bleed region in {template}")
    return float(xs.min())


def extract_barcode(template: Path, bleed_x: float, work_dir: Path) -> tuple[Path, tuple[float, float, float, float]]:
    dpi = 300
    scale = dpi / 72.0
    rendered = render_template(template, dpi, work_dir / f"{template.stem}-300")
    image = Image.open(rendered).convert("RGB")
    pixels = np.asarray(image)

    # The template places a 1.25 x 1 inch white barcode panel at a fixed
    # offset from the left edge of the cover bleed region.
    search_left = round((bleed_x + 460) * scale)
    search_right = round((bleed_x + 575) * scale)
    search_top = round(695 * scale)
    search_bottom = round(790 * scale)
    region = pixels[search_top:search_bottom, search_left:search_right]
    white = np.all(region >= 250, axis=2)

    # Flood-fill white components and take the large rectangular background
    # surrounding the barcode. Other white islands are individual glyphs.
    height, width = white.shape
    seen = np.zeros_like(white, dtype=bool)
    components: list[tuple[int, int, int, int, int]] = []
    for y, x in zip(*np.where(white)):
        if seen[y, x]:
            continue
        stack = [(int(y), int(x))]
        seen[y, x] = True
        count = 0
        min_x = max_x = int(x)
        min_y = max_y = int(y)
        while stack:
            cy, cx = stack.pop()
            count += 1
            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < height and 0 <= nx < width and white[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if count > 100:
            components.append((count, min_x, min_y, max_x, max_y))

    if not components:
        raise RuntimeError(f"Could not isolate barcode in {template}")
    _, min_x, min_y, max_x, max_y = max(components)
    x0 = search_left + min_x
    y0 = search_top + min_y
    x1 = search_left + max_x + 1
    y1 = search_top + max_y + 1
    crop = image.crop((x0, y0, x1, y1)).convert("L")
    barcode_path = work_dir / f"{template.stem}-barcode.png"
    crop.save(barcode_path, dpi=(dpi, dpi))

    pdf_x = x0 / scale
    pdf_y = PAGE_H - y1 / scale
    pdf_w = (x1 - x0) / scale
    pdf_h = (y1 - y0) / scale
    return barcode_path, (pdf_x, pdf_y, pdf_w, pdf_h)


def edge_extend_front(front: Path, work_dir: Path) -> Path:
    image = Image.open(front).convert("CMYK")
    if image.size != (2550, 3300):
        raise RuntimeError(f"Unexpected cover dimensions for {front}: {image.size}")
    array = np.asarray(image)
    padded = np.pad(array, ((38, 38), (38, 38), (0, 0)), mode="edge")
    extended = Image.frombytes(
        "CMYK", (padded.shape[1], padded.shape[0]), padded.tobytes()
    ).resize((2625, 3375), Image.Resampling.LANCZOS)
    result = work_dir / f"{front.stem}-with-bleed.jpg"
    extended.save(result, quality=96, subsampling=0, dpi=(300, 300))
    return result


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.replace("\u2013", "-").replace("\u2014", "-").split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(c: canvas.Canvas, lines: list[str], x: float, y: float, font: str, size: float, leading: float, color=WHITE) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def create_overlay(
    book: dict,
    spec: dict,
    front: Path,
    bleed_x: float,
    barcode: Path,
    barcode_rect: tuple[float, float, float, float],
    work_dir: Path,
) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    accent = CMYKColor(*spec["accent"])
    back_trim_x = bleed_x + TRIM_INSET
    spine_left = bleed_x + TRIM_INSET + TRIM_W
    spine_width = FRONT_TRIM_X - spine_left

    # Paint the entire production cover area, including the bleed.
    c.setFillColor(INK)
    c.rect(
        bleed_x - 2,
        COVER_BOTTOM - 2,
        PAGE_W - bleed_x + 2,
        PAGE_H - COVER_BOTTOM + 2,
        stroke=0,
        fill=1,
    )

    # Front cover: exact 8.5 x 11 artwork within trim, with edge pixels
    # extended into the 0.125 inch bleed.
    extended_front = edge_extend_front(front, work_dir)
    c.drawImage(ImageReader(str(extended_front)), FRONT_TRIM_X - 9, COVER_BOTTOM, 630, 810, preserveAspectRatio=False, mask=None)

    # Re-establish a clean back and spine over the extended front's inner edge.
    c.setFillColor(INK)
    c.rect(
        bleed_x - 2,
        COVER_BOTTOM - 2,
        spine_left - bleed_x + 2,
        PAGE_H - COVER_BOTTOM + 2,
        stroke=0,
        fill=1,
    )
    c.setFillColor(INK_2)
    c.rect(spine_left, COVER_BOTTOM, max(spine_width, 0), PAGE_H - COVER_BOTTOM, stroke=0, fill=1)

    # Subtle technical grid and circuit nodes.
    c.saveState()
    c.setStrokeColor(CMYKColor(54, 32, 18, 63))
    c.setLineWidth(0.35)
    for gx in range(int(back_trim_x + 18), int(back_trim_x + TRIM_W - 18), 36):
        c.line(gx, 78, gx, 840)
    for gy in range(90, 841, 36):
        c.line(back_trim_x + 18, gy, back_trim_x + TRIM_W - 18, gy)
    c.restoreState()

    safe_x = back_trim_x + 36
    safe_w = TRIM_W - 72
    top_y = 815

    # Orbitus wordmark treatment rendered as vectors.
    c.setFillColor(WHITE)
    c.setLineWidth(1.5)
    c.circle(safe_x + 17, top_y + 3, 15, stroke=1, fill=0)
    c.setStrokeColor(accent)
    c.arc(safe_x + 2, top_y - 5, safe_x + 37, top_y + 8, 200, 165)
    c.setFont("ROB-Bold", 12)
    c.drawString(safe_x + 45, top_y - 1, "ORBITUS ROBOTICS")
    c.setFillColor(accent)
    c.rect(safe_x, top_y - 23, safe_w, 2.5, stroke=0, fill=1)

    y = top_y - 54
    c.setFillColor(accent)
    c.setFont("ROB-Bold", 9.5)
    c.drawString(safe_x, y, spec["series_label"])
    y -= 30
    title_lines = wrap_text(book["title"].upper(), "ROB-Bold", 25, safe_w)
    y = draw_lines(c, title_lines, safe_x, y, "ROB-Bold", 25, 27, WHITE)
    y -= 7
    c.setFillColor(MUTED)
    c.setFont("ROB-Italic", 10.5)
    c.drawString(safe_x, y, book["audience"].replace("\u2013", "-"))
    y -= 32

    description_lines = wrap_text(book["description"], "ROB-Regular", 11.2, safe_w)
    y = draw_lines(c, description_lines, safe_x, y, "ROB-Regular", 11.2, 15.2, WHITE)
    y -= 22

    c.setFillColor(accent)
    c.setFont("ROB-Bold", 10)
    c.drawString(safe_x, y, "INSIDE THIS BOOK")
    y -= 21
    for topic in spec["topics"]:
        c.setFillColor(accent)
        c.circle(safe_x + 4, y + 3, 2.4, stroke=0, fill=1)
        topic_lines = wrap_text(topic, "ROB-Regular", 10.5, safe_w - 20)
        y = draw_lines(c, topic_lines, safe_x + 16, y, "ROB-Regular", 10.5, 14, WHITE)
        y -= 7

    # Bottom-left information stays clear of the supplied barcode.
    c.setFillColor(accent)
    c.rect(safe_x, 139, 282, 2, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("ROB-Bold", 9)
    c.drawString(safe_x, 121, "RODOLFO ARAMAYO")
    c.setFont("ROB-Regular", 8.2)
    c.setFillColor(MUTED)
    c.drawString(safe_x, 106, "OrbitusRobotics LLC")
    c.drawString(safe_x, 92, f"ISBN {spec['isbn']}  |  {spec['print_pages']} pages")

    # Spine text is intentionally omitted below 48 pages. The 50-page spine
    # is too narrow for dependable legibility, so only the substantial manual
    # receives type on its spine.
    if spec["print_pages"] >= 200 and spine_width >= 36:
        c.saveState()
        c.translate(spine_left + spine_width / 2, COVER_BOTTOM + 405)
        c.rotate(90)
        c.setFillColor(WHITE)
        c.setFont("ROB-Bold", 11)
        spine_title = "COMPLETE BUILDER'S FIELD MANUAL"
        c.drawCentredString(0, 3, spine_title)
        c.setFont("ROB-Regular", 7.5)
        c.setFillColor(accent)
        c.drawCentredString(0, -10, "RODOLFO ARAMAYO")
        c.restoreState()

    # Restore the exact ISBN barcode supplied in the title-specific template.
    bx, by, bw, bh = barcode_rect
    c.setFillColor(WHITE)
    c.rect(bx - 1, by - 1, bw + 2, bh + 2, stroke=0, fill=1)
    c.drawImage(ImageReader(str(barcode)), bx, by, bw, bh, preserveAspectRatio=False, mask=None)

    c.showPage()
    c.save()
    return buffer.getvalue()


def build_cover(book: dict, spec: dict, work_dir: Path) -> Path:
    template = TEMPLATE_DIR / spec["template"]
    front = FRONT_DIR / f"{book['slug']}.jpg"
    if not template.exists():
        raise FileNotFoundError(template)
    if not front.exists():
        raise FileNotFoundError(front)

    bleed_x = detect_bleed_x(template, work_dir)
    barcode, barcode_rect = extract_barcode(template, bleed_x, work_dir)
    overlay = create_overlay(book, spec, front, bleed_x, barcode, barcode_rect, work_dir)

    template_reader = PdfReader(str(template))
    overlay_reader = PdfReader(io.BytesIO(overlay))
    template_reader.pages[0].merge_page(overlay_reader.pages[0], over=True)

    merged = work_dir / f"{book['slug']}-merged.pdf"
    writer = PdfWriter()
    writer.add_page(template_reader.pages[0])
    writer.add_metadata(
        {
            "/Title": f"{book['title']} - IngramSpark print cover",
            "/Author": (
                "Rodolfo Aramayo and Kierie Aramayo"
                if book["slug"] == "rob-and-the-lost-yellow-ball"
                else "Rodolfo Aramayo"
            ),
            "/Producer": "ROB Books IngramSpark cover builder",
        }
    )
    with merged.open("wb") as stream:
        writer.write(stream)
    output = OUTPUT_DIR / f"{book['slug']}-cover.pdf"
    convert_to_pdfx(merged, output, f"{book['title']} IngramSpark cover")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("books", nargs="*", help="Book stems; default is all ten")
    args = parser.parse_args()
    selected = args.books or list(BOOKS)
    unknown = sorted(set(selected) - set(BOOKS))
    if unknown:
        parser.error(f"unknown book stem(s): {', '.join(unknown)}")
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    catalog = json.loads(CATALOG_PATH.read_text())
    books = {book["slug"]: book for book in catalog["books"]}

    built: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="ingram-covers-", dir=TMP_DIR) as temp:
        work_dir = Path(temp)
        for slug in selected:
            spec = BOOKS[slug]
            built.append(build_cover(books[slug], spec, work_dir))

    for path in built:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
