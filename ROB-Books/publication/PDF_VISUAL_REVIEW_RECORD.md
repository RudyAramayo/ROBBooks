# Building R.O.B. — PDF visual review record

**Review date:** 2026-08-29
**STATUS: COMPLETE**

**Scope:** All 573 physical pages in the ten print-layout PDFs.

**Method:** Codex-assisted page-by-page publication preflight. Every page was rendered with Poppler at 120 dpi and inspected on labeled, readable 3 × 2 review sheets for clipping, overflow, unintended blank pages, missing or distorted images, caption placement, contrast, navigation continuity, and obvious typographic defects. Suspect pages and every corrected page were rendered again at 144 dpi for focused inspection. PDF text extraction and pdfinfo supplied independent page-count, page-size, encryption, and text-presence checks.

This is a screen-rendering and editorial layout review. It is not a human accessibility/device review, a physical printer proof, a color-managed press approval, or an electrical, mechanical, legal, or safety certification. A changed PDF byte invalidates this record until the affected artifact is rebuilt and reviewed again.

## Reviewed artifacts

| PDF | Pages | SHA-256 |
|---|---:|---|
| complete-builders-field-manual.pdf | 236 | 41711c2b4dea8adf579252b7a632d3f74d7af5213f41a9c9854ea0b560f65e51 |
| rob-and-the-lost-yellow-ball.pdf | 23 | 5c1bc81fa2914500f48af12c956e0a43ac0034d0ab81a2ab12afde4b3452e44b |
| volume-1-meet-rob.pdf | 37 | 2ebd65e3747d8e81b7a093a6e2e71ed35de886fb8d13cf1ba6bd0438c5694260 |
| volume-2-circuits-and-signals.pdf | 36 | 1f0292be95eebb72d0029eb93b97e3f7c6ba24565d547d7ac65ce98d518e7273 |
| volume-3-motion-workshop.pdf | 36 | 8fae0be4083b553e21426980e3aa61fb857a934c5bfd796316a527f04df641a7 |
| volume-4-mission-control.pdf | 40 | 20deadec70559c54d7f65e46a5608da43ef666b95d12362f4ff6e97f331e516c |
| volume-5-ai-robotics-with-codex.pdf | 43 | cd859d7754f8bf813ec96dbb461ee92f853ce5271c9404d472d4f17795569bfa |
| volume-6-amber-dual-arm-robotics.pdf | 34 | f1e82b277597633e55b43ba8dc6c3680593e459d183d50ef1133586c35e10797 |
| volume-7-engineering-robcontrollervision.pdf | 38 | 64dda584b14727ae91a0b9938a15661b6edf1daba38a6009e2454335686465ce |
| volume-8-engineering-cerebro.pdf | 50 | 44c1182f9acd89adf4d1dbefba8499f2118723f4744bd79544230c83cae585c7 |

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

## Recheck

- publication/reviewed-pdfs.sha256 binds this review to the exact ten PDF files.
- python3 tools/audit_pdf_review.py verifies the closed PDF set, checksums, per-book page counts, US Letter geometry, unencrypted state, 573-page total, and completed review marker.
- bash tools/validate_books.sh runs that audit with the other publication checks.
- Any source, asset, font, TeX toolchain, or build change requires rebuilding the affected PDFs, repeating readable visual inspection, and deliberately replacing the checksums and this record.
