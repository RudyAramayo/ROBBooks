#!/usr/bin/env python3
"""Build the source-native advanced Building R.O.B. EPUB 3 editions."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from prepare_semantic_latex import prepare_latex, prepare_manual_markdown


PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "publication" / "apple-books-catalog.json"
CSS = PROJECT / "publication" / "epub.css"
OUTPUT = PROJECT / "output" / "apple-books" / "epub"
SUPPORTED = {
    "rob-and-the-lost-yellow-ball": ("markdown", "source/epub/rob-and-the-lost-yellow-ball.md"),
    "volume-1-meet-rob": ("latex", "source/volume-1-meet-rob.tex"),
    "volume-2-circuits-and-signals": ("latex", "source/volume-2-circuits-and-signals.tex"),
    "volume-3-motion-workshop": ("latex", "source/volume-3-motion-workshop.tex"),
    "volume-4-mission-control": ("latex", "source/volume-4-mission-control.tex"),
    "volume-5-ai-robotics-with-codex": ("markdown", "source/volume-5-ai-robotics-with-codex.md"),
    "volume-6-amber-dual-arm-robotics": ("markdown", "source/volume-6-amber-dual-arm-robotics.md"),
    "volume-7-engineering-robcontrollervision": ("markdown", "source/volume-7-engineering-robcontrollervision.md"),
    "volume-8-engineering-cerebro": ("markdown", "source/volume-8-engineering-cerebro.md"),
    "complete-builders-field-manual": ("manual", "source/complete-builders-field-manual.tex"),
}
IDENTIFIER_NAMESPACE = uuid.UUID("52f9dc75-d997-48bc-80a0-8f06baee89ca")
MAX_INTERIOR_IMAGE_PIXELS = 4_000_000
EPUB_IMAGE_DISCLOSURE = (
    "> **Image note:** Photographs are from the private ROB build archive unless otherwise noted. "
    "Generated covers, frontispieces, story scenes, and conceptual teaching plates are original "
    "project illustrations derived from or inspired by ROB reference photographs. They are "
    "illustrations, not documentary photographs, technical drawings, or evidence of the as-built "
    "configuration.\n\n"
)


def command(*args: str) -> None:
    subprocess.run(args, check=True, cwd=PROJECT)


def accessible_xhtml(epub: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(epub) as archive:
        for name in archive.namelist():
            if not name.endswith(".xhtml"):
                continue
            root = ET.fromstring(archive.read(name))
            namespace = {"x": "http://www.w3.org/1999/xhtml"}
            if not (root.get("lang") or root.get("{http://www.w3.org/XML/1998/namespace}lang")):
                errors.append(f"{name}: root language is missing")
            if name.endswith("cover.xhtml"):
                continue
            for image in root.findall(".//x:img", namespace):
                if image.get("alt") is None:
                    errors.append(f"{name}: image {image.get('src', 'unknown')} has no alt attribute")
            for table in root.findall(".//x:table", namespace):
                if not table.findall(".//x:th", namespace):
                    errors.append(f"{name}: data table has no header cells")
            previous_heading_level: int | None = None
            for element in root.iter():
                match = re.fullmatch(rf"\{{{re.escape(namespace['x'])}\}}h([1-6])", element.tag)
                if not match:
                    continue
                level = int(match.group(1))
                if previous_heading_level is not None and level > previous_heading_level + 1:
                    errors.append(f"{name}: heading level jumps from h{previous_heading_level} to h{level}")
                previous_heading_level = level
            for region in root.findall(".//x:div", namespace):
                if "sourceCode" in set(region.get("class", "").split()) and region.get("tabindex") != "0":
                    errors.append(f"{name}: code region is not keyboard focusable")
            if name.endswith("nav.xhtml"):
                landmarks = root.find(".//x:nav[@epub:type='landmarks']", {
                    **namespace,
                    "epub": "http://www.idpf.org/2007/ops",
                })
                if landmarks is None or landmarks.find(
                    ".//x:a[@epub:type='bodymatter']",
                    {**namespace, "epub": "http://www.idpf.org/2007/ops"},
                ) is None:
                    errors.append(f"{name}: bodymatter landmark is missing")
    return errors


def accessibility_metadata_errors(epub: Path, expected_summary: str) -> list[str]:
    with zipfile.ZipFile(epub) as archive:
        opf_names = [name for name in archive.namelist() if name.lower().endswith(".opf")]
        if len(opf_names) != 1:
            return [f"expected one OPF package document, found {len(opf_names)}"]
        root = ET.fromstring(archive.read(opf_names[0]))
        namespace = {"opf": "http://www.idpf.org/2007/opf"}
        summaries = root.findall(".//opf:meta[@property='schema:accessibilitySummary']", namespace)
        if len(summaries) != 1:
            return [f"expected one schema:accessibilitySummary, found {len(summaries)}"]
        if " ".join((summaries[0].text or "").split()) != " ".join(expected_summary.split()):
            return ["schema:accessibilitySummary differs from the catalog"]
    return []


def epub_text(epub: Path) -> str:
    with zipfile.ZipFile(epub) as archive:
        return "\n".join(
            " ".join(ET.fromstring(archive.read(name)).itertext())
            for name in archive.namelist()
            if name.endswith(".xhtml")
        )


def image_properties(path: Path) -> tuple[int, int, str]:
    result = subprocess.run(
        ["magick", "identify", "-quiet", "-format", "%w\t%h\t%[colorspace]", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height, color_space = result.stdout.split("\t")
    return int(width), int(height), color_space


def normalize_epub(epub: Path, accessibility_summary: str) -> None:
    """Improve EPUB semantics and constrain in-book rasters for Apple Books."""
    namespace = "http://www.w3.org/1999/xhtml"
    opf_namespace = "http://www.idpf.org/2007/opf"
    ET.register_namespace("", namespace)
    ET.register_namespace("epub", "http://www.idpf.org/2007/ops")
    ET.register_namespace("opf", opf_namespace)
    with tempfile.TemporaryDirectory(prefix="rob-epub-table-fix-") as temporary:
        root_dir = Path(temporary)
        with zipfile.ZipFile(epub) as archive:
            archive.extractall(root_dir)
        for image in sorted(root_dir.rglob("*")):
            if not image.is_file() or image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            width, height, _ = image_properties(image)
            pixels = width * height
            if pixels <= MAX_INTERIOR_IMAGE_PIXELS:
                continue
            scale = math.sqrt(MAX_INTERIOR_IMAGE_PIXELS / pixels)
            target_width = max(1, math.floor(width * scale))
            target_height = max(1, math.floor(height * scale))
            while target_width * target_height > MAX_INTERIOR_IMAGE_PIXELS:
                target_height -= 1
            replacement_image = image.with_name(f"{image.stem}.normalized{image.suffix}")
            resize_args = [
                "magick",
                str(image),
                "-resize",
                f"{target_width}x{target_height}>",
                "-colorspace",
                "sRGB",
                "-strip",
            ]
            if image.suffix.lower() in {".jpg", ".jpeg"}:
                resize_args.extend(["-quality", "92"])
            resize_args.append(str(replacement_image))
            subprocess.run(resize_args, check=True)
            replacement_image.replace(image)
        for xhtml in root_dir.rglob("*.xhtml"):
            tree = ET.parse(xhtml)
            root = tree.getroot()
            changed = False
            for table in root.findall(f".//{{{namespace}}}table"):
                if table.findall(f".//{{{namespace}}}th"):
                    continue
                rows = table.findall(f".//{{{namespace}}}tr")
                cells = [row.findall(f"{{{namespace}}}td") for row in rows]
                if rows and cells[0] and all(cell.find(f"{{{namespace}}}strong") is not None for cell in cells[0]):
                    for cell in cells[0]:
                        cell.tag = f"{{{namespace}}}th"
                        cell.set("scope", "col")
                        changed = True
                elif rows and all(row_cells and row_cells[0].find(f"{{{namespace}}}strong") is not None for row_cells in cells):
                    for row_cells in cells:
                        row_cells[0].tag = f"{{{namespace}}}th"
                        row_cells[0].set("scope", "row")
                        changed = True
            previous_heading_level: int | None = None
            for element in root.iter():
                match = re.fullmatch(rf"\{{{re.escape(namespace)}\}}h([1-6])", element.tag)
                if not match:
                    continue
                level = int(match.group(1))
                if previous_heading_level is not None and level > previous_heading_level + 1:
                    level = previous_heading_level + 1
                    element.tag = f"{{{namespace}}}h{level}"
                    changed = True
                previous_heading_level = level
            for region in root.findall(f".//{{{namespace}}}div"):
                classes = set(region.get("class", "").split())
                if "sourceCode" in classes:
                    region.set("tabindex", "0")
                    region.set("aria-label", "Code example")
                    changed = True
            if changed:
                tree.write(xhtml, encoding="utf-8", xml_declaration=True)
        package = root_dir / "EPUB" / "content.opf"
        package_tree = ET.parse(package)
        package_root = package_tree.getroot()
        metadata = package_root.find(f"{{{opf_namespace}}}metadata")
        if metadata is None:
            raise RuntimeError("EPUB package metadata element is missing")
        summary_nodes = metadata.findall(f"{{{opf_namespace}}}meta[@property='schema:accessibilitySummary']")
        if summary_nodes:
            summary_nodes[0].text = accessibility_summary
            for duplicate in summary_nodes[1:]:
                metadata.remove(duplicate)
        else:
            summary = ET.SubElement(metadata, f"{{{opf_namespace}}}meta", {"property": "schema:accessibilitySummary"})
            summary.text = accessibility_summary
        package_tree.write(package, encoding="utf-8", xml_declaration=True)
        nav = root_dir / "EPUB" / "nav.xhtml"
        tree = ET.parse(nav)
        root = tree.getroot()
        epub_type = "{http://www.idpf.org/2007/ops}type"
        landmarks = next(
            (element for element in root.findall(f".//{{{namespace}}}nav") if element.get(epub_type) == "landmarks"),
            None,
        )
        if landmarks is not None and not any(
            element.get(epub_type) == "bodymatter" for element in landmarks.findall(f".//{{{namespace}}}a")
        ):
            ordered = landmarks.find(f"{{{namespace}}}ol")
            if ordered is not None:
                item = ET.SubElement(ordered, f"{{{namespace}}}li")
                anchor = ET.SubElement(item, f"{{{namespace}}}a", {"href": "text/ch001.xhtml", epub_type: "bodymatter"})
                anchor.text = "Beginning of book"
                tree.write(nav, encoding="utf-8", xml_declaration=True)
        replacement = epub.with_suffix(".normalized.epub")
        with zipfile.ZipFile(replacement, "w") as archive:
            mimetype = root_dir / "mimetype"
            archive.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
            for item in sorted(root_dir.rglob("*")):
                if not item.is_file() or item == mimetype:
                    continue
                archive.write(item, item.relative_to(root_dir).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
        replacement.replace(epub)


def embedded_image_errors(epub: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(epub) as archive:
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
                errors.append(
                    f"{name}: {width}x{height} exceeds the {MAX_INTERIOR_IMAGE_PIXELS:,}-pixel Apple interior-image ceiling"
                )
            if color_space.casefold() != "srgb":
                errors.append(f"{name}: color space is {color_space}, expected sRGB")
    return errors


def semantic_content_errors(epub: Path, slug: str) -> list[str]:
    required = {
        "volume-1-meet-rob": ["Deep Lab: See the loop, not just the parts", "Goal-directed feedback loop"],
        "volume-2-circuits-and-signals": ["Deep Lab: Energy moves; signals describe", "Signal shapes over time"],
        "volume-3-motion-workshop": ["Deep Lab: Forces leave clues", "Design for failure and service"],
        "volume-4-mission-control": ["Deep Lab: Trust, time, and authority", "Control-authority state machine"],
        "complete-builders-field-manual": [
            "AI-assisted robotics engineering",
            "The arm system we actually have",
            "Read this book with the repository open",
            "Read Cerebro as a living robot system",
            "H.264 media pipeline",
        ],
    }
    text = epub_text(epub)
    folded = text.casefold()
    required_phrases = [
        "not documentary photographs, technical drawings, or evidence of the as-built configuration",
        *required.get(slug, []),
    ]
    return [f"missing semantic content: {phrase}" for phrase in required_phrases if phrase.casefold() not in folded]


def build(book: dict[str, object], source: Path, from_format: str) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / f"{book['slug']}.epub"
    stable_id = f"urn:uuid:{uuid.uuid5(IDENTIFIER_NAMESPACE, str(book['slug']))}"
    title = str(book["title"])
    subtitle = str(book["subtitle"])
    cover = PROJECT / str(book["cover"])
    args = [
        shutil.which("pandoc") or "pandoc",
        str(source),
        f"--from={from_format}",
        "--to=epub3",
        "--standalone",
        "--toc",
        "--toc-depth=3",
        "--split-level=2",
        f"--css={CSS}",
        f"--epub-cover-image={cover}",
        "--resource-path=source:assets/photos:assets/generated:assets/slides",
        "--metadata",
        f"title={title}",
        "--metadata",
        f"subtitle={subtitle}",
        "--metadata",
        "creator=Rodolfo Aramayo",
        "--metadata",
        "publisher=OrbitusRobotics LLC",
        "--metadata",
        "language=en-US",
        "--metadata",
        "date=2026",
        "--metadata",
        f"identifier={stable_id}",
        "--metadata",
        "rights=Copyright © 2026 OrbitusRobotics LLC. All rights reserved.",
        "-o",
        str(destination),
    ]
    subprocess.run(args, check=True, cwd=PROJECT)
    normalize_epub(destination, str(book["accessibility_summary"]))
    command(shutil.which("epubcheck") or "epubcheck", str(destination))
    errors = accessible_xhtml(destination)
    errors.extend(accessibility_metadata_errors(destination, str(book["accessibility_summary"])))
    errors.extend(embedded_image_errors(destination))
    errors.extend(semantic_content_errors(destination, str(book["slug"])))
    if errors:
        raise RuntimeError("\n".join(errors))
    print(f"PASS {destination.relative_to(PROJECT)} — EPUBCheck 5.3.0 and structural accessibility audit")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slugs", nargs="*", help="advanced-edition slugs; defaults to all currently supported editions")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_slug = {book["slug"]: book for book in catalog["books"]}
    selected = args.slugs or list(SUPPORTED)
    unknown = [slug for slug in selected if slug not in SUPPORTED]
    if unknown:
        print(f"Unsupported until the LaTeX accessibility conversion is complete: {', '.join(unknown)}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="rob-epub-build-") as temporary:
        temporary_path = Path(temporary)
        for slug in selected:
            source_type, relative_source = SUPPORTED[slug]
            source = PROJECT / relative_source
            if source_type == "latex":
                semantic, markers = prepare_latex(source)
                if markers:
                    raise RuntimeError(f"unexpected Markdown inputs in {relative_source}")
                prepared = temporary_path / f"{slug}.tex"
                prepared.write_text(semantic, encoding="utf-8")
                build(by_slug[slug], prepared, "latex")
            elif source_type == "manual":
                prepared = temporary_path / f"{slug}.md"
                prepared.write_text(prepare_manual_markdown(source), encoding="utf-8")
                build(by_slug[slug], prepared, "gfm")
            else:
                prepared = temporary_path / f"{slug}.md"
                prepared.write_text(EPUB_IMAGE_DISCLOSURE + source.read_text(encoding="utf-8"), encoding="utf-8")
                build(by_slug[slug], prepared, "gfm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
