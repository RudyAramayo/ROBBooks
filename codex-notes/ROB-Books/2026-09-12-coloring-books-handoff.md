# Illustrated coloring collection — 2026-09-12

The author rejected the first procedural coloring draft for repetitive artwork.
That draft was moved to ignored `ROB-Books/tmp/superseded-procedural-coloring/`;
it is superseded and is not a final deliverable.

The replacement uses 350 individually generated interior illustrations:
five children's books with 30 pages each, and five adult books with 40 each.
Ten separately generated color front-cover illustrations accompany matching
back-cover layouts. Children: Good Morning, Fireflies, Rainbow Lights, Little
Sound, Shiny Star. Adults: Halloween, Thanksgiving, Christmas, Clockwork Gardens,
and the clearly labeled 18+ After Hours edition, including cannabis smoking,
tobacco, alcohol, and non-explicit adult robot companionship.

Source briefs and catalog: `ROB-Books/source/coloring-v2/`.
Art and prompt provenance: `ROB-Books/assets/coloring-v2/`.
Builder: `ROB-Books/tools/build_illustrated_coloring_books.py`.
Verifier: `ROB-Books/tools/verify_illustrated_coloring_books.py`.
Final destination: `ROB-Books/output/pdf/coloring-v2/{children,adult}/`.

Print US Letter, actual size, long-edge duplex. Children's coloring art is PDF
pages 3–32 (15 duplex sheets); adult coloring art is pages 3–42 (20 duplex
sheets). With covers, introduction, and palette page, total PDF lengths are
34 and 44 respectively. These are reader PDFs for ordinary printing.

Production environment: `/tmp/rob-cover-venv/bin/python`, ReportLab 5.0.1,
pypdf 6.18.1, PyMuPDF 1.26.5, Pillow 11.3.0. Poppler is unavailable;
PyMuPDF renders all pages for review. macOS Arial, Arial Rounded Bold,
and Georgia Bold fonts are embedded by the builder.

Generation, assembly, and final validation are complete. All ten PDFs passed
the builder and verifier with 350 unique interior source hashes and 390 total
rendered PDF pages. All 35 final contact sheets and both cover-pair sheets were
visually reviewed, with larger page samples also inspected. The 30 firefly
illustrations were individually checked for the intended zero-to-five counts;
the cover was revised to show five fireflies.

Minimum effective interior resolution is 162.2 DPI. These are ordinary-print
reader PDFs, not 300-DPI press files. All PDFs are below GitHub's 100-MiB
individual-file limit. The original generated PNGs are retained without resizing.
Built-in image generation produced all artwork. All 350 image/JSON pairs match
the catalog; 348 interior prompts and all ten cover prompts are preserved.
Morning 01 and Halloween 01 are documented trial-image provenance exceptions.

Validation commands, run successfully from `ROB-Books/`:

```sh
/tmp/rob-cover-venv/bin/python tools/build_illustrated_coloring_books.py
/tmp/rob-cover-venv/bin/python tools/verify_illustrated_coloring_books.py
```

Final automated results: `ROB-Books/output/previews/coloring-v2/validation.json`.
