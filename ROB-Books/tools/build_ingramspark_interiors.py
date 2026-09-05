#!/usr/bin/env python3
"""Build IngramSpark color interiors from the reviewed 8.5 x 11 PDFs.

The source PDFs are exact-trim RGB review artifacts. IngramSpark color interiors
with bleed use a 0.125-inch bleed on the top, bottom, and outside edge only. This
builder keeps the original trim region unchanged, mirrors only the edge pixels
into the bleed, adds an intentional final blank where needed, and converts the
result to CMYK PDF/X-1a:2001 with embedded fonts.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject, RectangleObject


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "output" / "pdf"
WORK_DIR = ROOT / "tmp" / "pdfs" / "ingramspark"
OUTPUT_DIR = ROOT / "output" / "pdf" / "ingramspark" / "interiors"

TRIM_WIDTH = 8.5 * 72
TRIM_HEIGHT = 11 * 72
BLEED = 0.125 * 72
PAGE_WIDTH = TRIM_WIDTH + BLEED
PAGE_HEIGHT = TRIM_HEIGHT + (2 * BLEED)

BOOKS = (
    "rob-and-the-lost-yellow-ball",
    "volume-1-meet-rob",
    "volume-2-circuits-and-signals",
    "volume-3-motion-workshop",
    "volume-4-mission-control",
    "volume-5-ai-robotics-with-codex",
    "volume-6-amber-dual-arm-robotics",
    "volume-7-engineering-robcontrollervision",
    "volume-8-engineering-cerebro",
    "complete-builders-field-manual",
)


def run(command: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def find_ghostscript_resource(name: str) -> Path:
    executable = shutil.which("gs")
    if executable is None:
        raise FileNotFoundError("Ghostscript executable not found")
    version_root = Path(executable).resolve().parents[1]
    candidate = version_root / "share" / "ghostscript" / name
    if candidate.is_file():
        return candidate
    matches = sorted(version_root.glob(f"share/ghostscript/**/{Path(name).name}"))
    if not matches:
        raise FileNotFoundError(f"Ghostscript resource not found: {name}")
    return matches[0]


def trim_box(page_number: int) -> RectangleObject:
    # Odd pages are recto (binding left); even pages are verso (binding right).
    x_offset = 0 if page_number % 2 else BLEED
    return RectangleObject((x_offset, BLEED, x_offset + TRIM_WIDTH, BLEED + TRIM_HEIGHT))


def remove_unused_transparency_resources(page) -> None:
    """Remove page-level transparency declarations that are unused or a no-op.

    XeLaTeX places every TikZ opacity state in every page resource dictionary,
    even when the page never invokes it. Ghostscript conservatively rasterizes a
    full PDF/X-1a page merely because those unused states are present. Removing
    them keeps ordinary text and diagrams as embedded vector content; pages that
    genuinely use transparency are still flattened correctly.
    """
    contents = page.get_contents()
    resources_reference = page.get("/Resources")
    if contents is None or resources_reference is None:
        return
    resources_source = resources_reference.get_object()
    ext_reference = resources_source.get("/ExtGState")
    if ext_reference is None:
        return

    data = contents.get_data()
    resources = DictionaryObject({key: value for key, value in resources_source.items()})
    ext_source = ext_reference.get_object()
    ext_states = DictionaryObject({key: value for key, value in ext_source.items()})

    for name, reference in list(ext_states.items()):
        token = re.compile(rb"/" + re.escape(str(name)[1:].encode("ascii")) + rb"\s+gs\b")
        matches = token.search(data) is not None
        state = reference.get_object()
        only_opacity = set(state.keys()).issubset({NameObject("/ca"), NameObject("/CA")})
        default_opacity = float(state.get("/ca", 1)) == 1 and float(state.get("/CA", 1)) == 1
        if not matches:
            del ext_states[name]
        elif only_opacity and default_opacity:
            data = token.sub(b"", data)
            del ext_states[name]

    if ext_states:
        resources[NameObject("/ExtGState")] = ext_states
    else:
        resources.pop(NameObject("/ExtGState"), None)
    page[NameObject("/Resources")] = resources
    replacement = DecodedStreamObject()
    replacement.set_data(data)
    page[NameObject("/Contents")] = replacement


def add_edge_bleed(destination, source, page_number: int) -> None:
    """Mirror source edges outside trim, then overlay the unchanged source page."""
    recto = page_number % 2 == 1
    main_x = 0 if recto else BLEED

    # Top and bottom mirrors. Only the portions outside trim remain visible once
    # the unchanged page is overlaid.
    destination.merge_transformed_page(
        source,
        Transformation(ctm=(1, 0, 0, -1, main_x, (2 * TRIM_HEIGHT) + BLEED)),
        expand=False,
    )
    destination.merge_transformed_page(
        source,
        Transformation(ctm=(1, 0, 0, -1, main_x, BLEED)),
        expand=False,
    )

    if recto:
        outside_transform = Transformation(ctm=(-1, 0, 0, 1, 2 * TRIM_WIDTH, BLEED))
        top_corner = Transformation(
            ctm=(-1, 0, 0, -1, 2 * TRIM_WIDTH, (2 * TRIM_HEIGHT) + BLEED)
        )
        bottom_corner = Transformation(ctm=(-1, 0, 0, -1, 2 * TRIM_WIDTH, BLEED))
    else:
        outside_transform = Transformation(ctm=(-1, 0, 0, 1, BLEED, BLEED))
        top_corner = Transformation(
            ctm=(-1, 0, 0, -1, BLEED, (2 * TRIM_HEIGHT) + BLEED)
        )
        bottom_corner = Transformation(ctm=(-1, 0, 0, -1, BLEED, BLEED))

    destination.merge_transformed_page(source, outside_transform, expand=False)
    destination.merge_transformed_page(source, top_corner, expand=False)
    destination.merge_transformed_page(source, bottom_corner, expand=False)
    destination.merge_transformed_page(
        source,
        Transformation().translate(main_x, BLEED),
        expand=False,
    )


def make_bleed_pdf(source_path: Path, output_path: Path) -> int:
    reader = PdfReader(source_path)
    writer = PdfWriter()

    for page_number, source_page in enumerate(reader.pages, start=1):
        width = float(source_page.mediabox.width)
        height = float(source_page.mediabox.height)
        if abs(width - TRIM_WIDTH) > 0.01 or abs(height - TRIM_HEIGHT) > 0.01:
            raise ValueError(
                f"{source_path.name} page {page_number} is {width} x {height} pt; "
                f"expected {TRIM_WIDTH} x {TRIM_HEIGHT} pt"
            )

        remove_unused_transparency_resources(source_page)
        destination = writer.add_blank_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        add_edge_bleed(destination, source_page, page_number)
        # Interactive link annotations are neither useful in print nor allowed
        # in PDF/X-1a. pypdf copies them during page merges, so remove them.
        destination.pop(NameObject("/Annots"), None)
        destination.cropbox = RectangleObject((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
        destination.bleedbox = RectangleObject((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
        destination.trimbox = trim_box(page_number)
        destination.compress_content_streams()

    if len(reader.pages) % 2:
        page_number = len(reader.pages) + 1
        destination = writer.add_blank_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        destination.cropbox = RectangleObject((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
        destination.bleedbox = RectangleObject((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
        destination.trimbox = trim_box(page_number)

    writer.add_metadata(
        {
            "/Title": f"{source_path.stem} - IngramSpark print interior",
            "/Author": "Rodolfo Aramayo",
            "/Producer": "ROB Books IngramSpark interior builder",
        }
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as stream:
        writer.write(stream)
    return len(writer.pages)


def make_pdfx_definition(title: str, output_path: Path) -> Path:
    sample = find_ghostscript_resource("PDFX_def.ps").read_text(encoding="utf-8")
    profile_source = find_ghostscript_resource("iccprofiles/default_cmyk.icc")
    profile_target = output_path.parent / "default_cmyk.icc"
    shutil.copyfile(profile_source, profile_target)

    safe_title = re.sub(r"[()\\]", "", title)
    profile_literal = str(profile_target).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    definition = sample.replace(
        "/ICCProfile (ISO Coated sb.icc)", f"/ICCProfile ({profile_literal})"
    )
    definition = definition.replace("/Title (Title)", f"/Title ({safe_title})")
    definition_path = output_path.parent / "PDFX_def.ps"
    definition_path.write_text(definition, encoding="utf-8")
    return definition_path


def convert_to_pdfx(source_path: Path, output_path: Path, title: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    staged_path = output_path.with_suffix(".staged.pdf")
    definition = make_pdfx_definition(title, source_path)
    command = [
        "gs",
        "-q",
        "-dBATCH",
        "-dNOPAUSE",
        "-dSAFER",
        f"--permit-file-read={source_path.parent}/*",
        "-dPDFX=1",
        "-dCompatibilityLevel=1.3",
        "-sDEVICE=pdfwrite",
        "-dPDFSETTINGS=/prepress",
        "-dAutoRotatePages=/None",
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        "-dCompressFonts=true",
        "-dDetectDuplicateImages=true",
        "-dAutoFilterColorImages=false",
        "-dColorImageFilter=/DCTEncode",
        "-dJPEGQ=95",
        "-dColorImageDownsampleType=/Bicubic",
        "-dColorImageResolution=300",
        "-dAutoFilterGrayImages=false",
        "-dGrayImageFilter=/DCTEncode",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dGrayImageResolution=300",
        "-dMonoImageDownsampleType=/Subsample",
        "-dMonoImageResolution=1200",
        "-sColorConversionStrategy=CMYK",
        "-sProcessColorModel=DeviceCMYK",
        "-dOverrideICC=true",
        f"-sOutputFile={staged_path}",
        str(definition),
        str(source_path),
    ]
    run(command, cwd=source_path.parent)
    staged_path.replace(output_path)


def build(book: str) -> Path:
    source_path = SOURCE_DIR / f"{book}.pdf"
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    work_path = WORK_DIR / f"{book}-interior-bleed-rgb.pdf"
    output_path = OUTPUT_DIR / f"{book}-interior.pdf"
    page_count = make_bleed_pdf(source_path, work_path)
    convert_to_pdfx(work_path, output_path, f"{book} IngramSpark interior")
    print(f"built {output_path.relative_to(ROOT)} ({page_count} pages)")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("books", nargs="*", help="Book stems; default is all ten")
    args = parser.parse_args()
    selected = args.books or BOOKS
    unknown = sorted(set(selected) - set(BOOKS))
    if unknown:
        parser.error(f"unknown book stem(s): {', '.join(unknown)}")
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    for book in selected:
        build(book)


if __name__ == "__main__":
    main()
