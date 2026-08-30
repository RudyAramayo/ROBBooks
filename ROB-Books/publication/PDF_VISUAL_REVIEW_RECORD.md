# Building R.O.B. — PDF visual review record

**Review date:** 2026-08-29
**STATUS: COMPLETE**

**Scope:** All 573 physical pages in the ten print-layout PDFs.

**Method:** Codex-assisted page-by-page publication preflight. Every page was rendered with Poppler at 120 dpi and inspected on labeled, readable 3 × 2 review sheets for clipping, overflow, unintended blank pages, missing or distorted images, caption placement, contrast, navigation continuity, and obvious typographic defects. Suspect pages and every corrected page were rendered again at 144 dpi for focused inspection. PDF text extraction and pdfinfo supplied independent page-count, page-size, encryption, and text-presence checks.

This is a screen-rendering and editorial layout review. It is not a human accessibility/device review, a physical printer proof, a color-managed press approval, or an electrical, mechanical, legal, or safety certification. A changed PDF byte invalidates this record until the affected artifact is rebuilt and reviewed again.

## Reviewed artifacts

| PDF | Pages | SHA-256 |
|---|---:|---|
| complete-builders-field-manual.pdf | 236 | 39a08b31a1e86a9441c4ff4da0b5e30830b6caa91d172c930f3a2fcd9b73b898 |
| rob-and-the-lost-yellow-ball.pdf | 23 | 8b4c6562440ee10736c539d4f40c8592b526e585085f57430e734bafca2ae652 |
| volume-1-meet-rob.pdf | 37 | 55d747297bc69ca9c053f7212682f10363a675be911ac2bc5451759b38376633 |
| volume-2-circuits-and-signals.pdf | 36 | 5138b906505f3af3f4f2a124fc5d68e2170b80e6a90c50ffa529f11c3f4fef53 |
| volume-3-motion-workshop.pdf | 36 | 9b512937eaffe757a249d5e00d4303e2eee375aa795125651f270c69144efd82 |
| volume-4-mission-control.pdf | 40 | c478c14df6701ef5b322b102e8d27f794d7a5a698a60acf98d1fa06fd6ef69be |
| volume-5-ai-robotics-with-codex.pdf | 43 | 15eb3344f4b3be89106f6fafd912db9670adf7eb1985c1401792848779306ba0 |
| volume-6-amber-dual-arm-robotics.pdf | 34 | 161aac3d1d57cc2e3b55e33efd4edb65c9fd4d4b0d64600bdc2940733343bbde |
| volume-7-engineering-robcontrollervision.pdf | 38 | 8ee7d23a8736a448057bbf02d67bc52568ccff6a90ab09989a1d9706a62f9bee |
| volume-8-engineering-cerebro.pdf | 50 | d10ee490243fabc70b1d9a65a508baad115d7a74a4acf0859457297f1a1660b4 |

All ten are unencrypted US Letter PDFs with extractable text. Their physical page total is 573.

## Findings and corrections

- The complete 236-page field manual, the 23-page story, and Volumes 5, 6, and 8 passed the first visual pass without clipping, overflow, missing images, unintended blanks, or page-continuity defects.
- Volume 7 body pages passed, but its cover initially allowed the long ROBControllerVision product name to hyphenate. The cover now uses an intentional two-line title and preserves the product name without a forced hyphen.
- The shared full-bleed opener macro used by Volumes 1–4 initially produced compressed word spacing and automatic hyphenation in some display titles. The macro now uses explicit readable interword spacing, ragged wrapping, and disabled title hyphenation.
- All 32 corrected mission/deep-lab openers in Volumes 1–4 and all ten rebuilt covers received a second 144 dpi visual pass. Titles fit their bands, preserve complete words, retain contrast, and do not clip.
- Sparse part-title pages, chapter-closing pages, and continuation pages were checked against adjacent pages and accepted as intentional design.
- The complete manual footer ends at “/ 220” because its internal main-matter pagination excludes front matter; the physical PDF contains 236 pages. This was reviewed as intentional, not a missing-page condition.

## Factual-correction rebuild review

The ten PDFs were rebuilt after the 0.6-second controller-freshness correction and the resolved Volume 4 camera caption. Rebuilding changed container bytes in all ten files. Extracted text and same-renderer page images established the visual scope before renewing this record:

- the story and Volumes 1, 2, 3, 6, and 7 retained byte-identical extracted text and pixel-identical 72 dpi page renders across every page;
- 120 dpi old/new render comparison isolated visual changes to Volume 4 page 25, Volume 5 pages 14–16, Volume 8 page 16, and complete-manual pages 95–99 and 191;
- all eleven changed pages were inspected at their 120 dpi render size. The corrected caption fits its two-image layout, timeout language remains complete and readable, page transitions remain continuous, and no clipping, collision, overflow, unintended blank, missing image, or broken heading was found;
- page counts, trim geometry, encryption state, and the 573-page set total did not change.

No unresolved visual-layout defect remains in the byte-matched PDFs listed above.

## Author-answer and copyright rebuild review

The ten PDFs were rebuilt after the final author answers established the College Station origin, approximate 2016 treaded-prototype date, photographer/product-photo rights, and OrbitusRobotics LLC copyright ownership. The shared title and front-matter imprint was also corrected. Same-renderer 72 dpi comparison against the preceding reviewed PDFs isolated visual changes to:

- pages 1–2 of Volumes 1–8;
- page 1 of *ROB and the Lost Yellow Ball*;
- pages 1–2, 19, 23, 229, and 236 of the complete field manual; and
- page 13 of Volume 1.

Every changed page was rendered at 144 dpi and inspected in four labeled focused review sheets. The revised cover bylines and front-matter copyright paragraphs remain legible and contained; the College Station/circa-2016 language fits the Volume 1 field note and manual history pages; the future-edition ledger and photo-credit revisions fit without collision or overflow. No clipping, broken wrapping, unintended blank page, missing image, navigation break, or page-count change was found. The set remains 573 US Letter pages.

## Recheck

- publication/reviewed-pdfs.sha256 binds this review to the exact ten PDF files.
- python3 tools/audit_pdf_review.py verifies the closed PDF set, checksums, per-book page counts, US Letter geometry, unencrypted state, 573-page total, and completed review marker.
- bash tools/validate_books.sh runs that audit with the other publication checks.
- Any source, asset, font, TeX toolchain, or build change requires rebuilding the affected PDFs, repeating readable visual inspection, and deliberately replacing the checksums and this record.
