#!/usr/bin/env python3
"""Report every machine-detectable Building R.O.B. publication blocker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "source"
CATALOG = PROJECT / "publication" / "apple-books-catalog.json"
ANSWERS = PROJECT / "publication" / "publisher-answers.json"
GATE = PROJECT / "PRINT_AND_SAFETY_REVIEW.md"
GAPS = PROJECT / "EDITORIAL_GAPS.md"
AUTHOR_RECORD = PROJECT / "publication" / "AUTHOR_INTERVIEW_RECORD.md"


def extract_braced(text: str, start: int) -> tuple[str, int]:
    if start >= len(text) or text[start] != "{":
        raise ValueError("expected opening brace")
    depth = 0
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
    raise ValueError("unterminated brace group")


def placeholders() -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    marker = "\\ROBPlaceholder"
    for path in sorted(SOURCE.glob("*.tex")):
        text = path.read_text(encoding="utf-8")
        cursor = 0
        while True:
            offset = text.find(marker, cursor)
            if offset < 0:
                break
            brace = text.find("{", offset + len(marker))
            body, cursor = extract_braced(text, brace)
            found.append(
                {
                    "id": f"P{len(found) + 1:03d}",
                    "source": str(path.relative_to(PROJECT)),
                    "line": text.count("\n", 0, offset) + 1,
                    "question": re.sub(r"\s+", " ", body).strip(),
                }
            )
    return found


def missing_leaves(value: object, prefix: str = "") -> list[str]:
    missing: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "schema_version":
                continue
            missing.extend(missing_leaves(child, f"{prefix}.{key}".lstrip(".")))
    elif value is None or (isinstance(value, str) and not value.strip()):
        missing.append(prefix)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true", help="exit nonzero while any blocker remains")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    answers = json.loads(ANSWERS.read_text(encoding="utf-8"))
    unresolved_placeholders = placeholders()
    gate_text = GATE.read_text(encoding="utf-8")
    gap_text = GAPS.read_text(encoding="utf-8")
    author_record_text = AUTHOR_RECORD.read_text(encoding="utf-8")
    unchecked_gate_items = [
        {"line": index, "text": line[6:].strip()}
        for index, line in enumerate(gate_text.splitlines(), start=1)
        if line.startswith("- [ ] ")
    ]
    editorial_gap_items = [
        {"line": index, "text": line[2:].strip()}
        for index, line in enumerate(gap_text.splitlines(), start=1)
        if line.startswith("- ")
    ]
    unanswered_author_questions = [
        {"line": index, "text": line[6:].strip()}
        for index, line in enumerate(author_record_text.splitlines(), start=1)
        if line.startswith("- [ ] ")
    ]
    missing_answers = missing_leaves(answers)
    missing_epubs = [book["epub"] for book in catalog["books"] if not (PROJECT / book["epub"]).exists()]
    missing_store_records = [
        book["slug"]
        for book in catalog["books"]
        if not str(book.get("apple_books_id", "")).strip() or not str(book.get("apple_books_url", "")).strip()
    ]
    report = {
        "ready": not any((unresolved_placeholders, unchecked_gate_items, unanswered_author_questions, missing_answers, missing_epubs, missing_store_records)),
        "placeholder_count": len(unresolved_placeholders),
        "placeholders": unresolved_placeholders,
        "unchecked_release_gate_count": len(unchecked_gate_items),
        "unchecked_release_gate_items": unchecked_gate_items,
        "editorial_question_count": len(editorial_gap_items),
        "editorial_questions": editorial_gap_items,
        "unanswered_author_question_count": len(unanswered_author_questions),
        "unanswered_author_questions": unanswered_author_questions,
        "missing_publisher_answer_count": len(missing_answers),
        "missing_publisher_answers": missing_answers,
        "missing_epub_count": len(missing_epubs),
        "missing_epubs": missing_epubs,
        "missing_apple_store_record_count": len(missing_store_records),
        "missing_apple_store_records": missing_store_records,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Explicit manuscript placeholders: {report['placeholder_count']}")
        for item in unresolved_placeholders:
            print(f"  {item['id']} {item['source']}:{item['line']} — {item['question']}")
        print(f"Unchecked release-gate items: {report['unchecked_release_gate_count']}")
        print(f"Editorial question groups: {report['editorial_question_count']}")
        print(f"Unanswered author questions: {report['unanswered_author_question_count']}")
        for item in unanswered_author_questions:
            print(f"  AUTHOR {item['text']}")
        print(f"Missing publisher answers: {report['missing_publisher_answer_count']}")
        for key in missing_answers:
            print(f"  ANSWER {key}")
        print(f"Missing EPUBs: {report['missing_epub_count']}")
        for path in missing_epubs:
            print(f"  EPUB {path}")
        print(f"Missing Apple Books IDs or URLs: {report['missing_apple_store_record_count']}")
        print("READY" if report["ready"] else "NOT READY")

    if args.release and not report["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
