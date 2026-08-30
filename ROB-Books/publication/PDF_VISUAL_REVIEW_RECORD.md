# Building R.O.B. — PDF visual review record

**Review date:** 2026-08-29
**STATUS: COMPLETE**

**Scope:** All 573 physical pages in the ten print-layout PDFs.

**Method:** Codex-assisted page-by-page publication preflight. Every page was rendered with Poppler at 120 dpi and inspected on labeled, readable 3 × 2 review sheets for clipping, overflow, unintended blank pages, missing or distorted images, caption placement, contrast, navigation continuity, and obvious typographic defects. Suspect pages and every corrected page were rendered again at 144 dpi for focused inspection. PDF text extraction and pdfinfo supplied independent page-count, page-size, encryption, and text-presence checks.

This is a screen-rendering and editorial layout review. It is not a human accessibility/device review, a physical printer proof, a color-managed press approval, or an electrical, mechanical, legal, or safety certification. A changed PDF byte invalidates this record until the affected artifact is rebuilt and reviewed again.

## Reviewed artifacts

| PDF | Pages | SHA-256 |
|---|---:|---|
| complete-builders-field-manual.pdf | 236 | 50033ccb1ffb518f57b227b6c9b20566750f805fcb3a99710ad89d274d1589be |
| rob-and-the-lost-yellow-ball.pdf | 23 | 1f3229280052cf8ca5577318190a7a9159c8822f39e727cd75accc938df01517 |
| volume-1-meet-rob.pdf | 37 | c000662720bc4f9fc205293e31132718fa34536fb4afc65bc99462aa46f401a8 |
| volume-2-circuits-and-signals.pdf | 36 | f855566efffc37b1071b3c43cc34d231eff1294a5c74cfe207962b1dc3ee94a9 |
| volume-3-motion-workshop.pdf | 36 | 969c64d5e5a71486eebc40634def59e5ea3a8b322afeaa4c66531e6ee296723e |
| volume-4-mission-control.pdf | 40 | e7c9916458471893625f26ea6d604452adf471e6fa75ff99287749cb2dd515a6 |
| volume-5-ai-robotics-with-codex.pdf | 43 | 9e026dcd59ca50f0e66ba104e601558e05a190f2a311e5f38aee643da33512fd |
| volume-6-amber-dual-arm-robotics.pdf | 34 | 415b4a2255e56b151cb9791808a6b893eb41977a4ff64361db42466364041efa |
| volume-7-engineering-robcontrollervision.pdf | 38 | 53d7d69004ceff66c3328afc0cfae814bdf7b504dbcc4eeeca7234d8b81eeefc |
| volume-8-engineering-cerebro.pdf | 50 | ee0c264916928f9ee7d8775afc43eb2323061e78566f0a81a8cd21660450ae98 |

All ten are unencrypted US Letter PDFs with extractable text. Their physical page total is 573.

## Findings and corrections

- The complete 236-page field manual, the 23-page story, and Volumes 5, 6, and 8 passed the first visual pass without clipping, overflow, missing images, unintended blanks, or page-continuity defects.
- Volume 7 body pages passed, but its cover initially allowed the long ROBControllerVision product name to hyphenate. The cover now uses an intentional two-line title and preserves the product name without a forced hyphen.
- The shared full-bleed opener macro used by Volumes 1–4 initially produced compressed word spacing and automatic hyphenation in some display titles. The macro now uses explicit readable interword spacing, ragged wrapping, and disabled title hyphenation.
- All 32 corrected mission/deep-lab openers in Volumes 1–4 and all ten rebuilt covers received a second 144 dpi visual pass. Titles fit their bands, preserve complete words, retain contrast, and do not clip.
- Sparse part-title pages, chapter-closing pages, and continuation pages were checked against adjacent pages and accepted as intentional design.
- The complete manual footer ends at “/ 220” because its internal main-matter pagination excludes front matter; the physical PDF contains 236 pages. This was reviewed as intentional, not a missing-page condition.

No unresolved visual-layout defect remains in the byte-matched PDFs listed above.

## Recheck

- publication/reviewed-pdfs.sha256 binds this review to the exact ten PDF files.
- python3 tools/audit_pdf_review.py verifies the closed PDF set, checksums, per-book page counts, US Letter geometry, unencrypted state, 573-page total, and completed review marker.
- bash tools/validate_books.sh runs that audit with the other publication checks.
- Any source, asset, font, TeX toolchain, or build change requires rebuilding the affected PDFs, repeating readable visual inspection, and deliberately replacing the checksums and this record.
