# Building R.O.B. — historical-edition publication release gate

This checklist releases books, not the physical robot. The edition documents one maker's hand-built history and teaches from the surviving evidence. It does not provide certified construction plans or authorize energized construction, testing, movement, or public operation.

## Scope and evidence

- [x] The publisher selected a historical engineering reference and educational field-manual posture.
- [x] The manuscripts state that as-built CAD, complete schematics, measurements, and qualified engineering approvals do not exist for this edition.
- [x] Missing technical facts are presented as evidence limits or future measured-edition work rather than invented values.
- [x] No electrical, mechanical, educator, accessibility, privacy, or legal approval is claimed.
- [x] Controlled vendor drawings are excluded as public technical sources; no restricted drawing, table, connector assignment, ratio, rating, or performance curve is reproduced or paraphrased.
- [x] Q01 and Q03–Q05 in `publication/AUTHOR_INTERVIEW_RECORD.md` are answered and reconciled into the manuscripts, metadata, and rights ledger.
- [x] The final source snapshot, factual claims, revision labels, captions, credits, cross-references, spelling, and accessibility language received a complete Codex-assisted publisher copyedit against the dated evidence and author answers.

## Youth, safety, and privacy language

- [x] Youth activities are limited to paper, simulation, observation, or explicitly supervised low-energy educational work.
- [x] The books do not invite youth access to ROB's traction batteries, inverter/mains circuits, drivetrain, chains, machine tools, actuators, live controllers, or unrestricted network commands.
- [x] Fabrication and hardware photographs are described as historical evidence rather than complete safety instruction.
- [x] Every statement about cameras, microphones, face identity, Messages, recording, cloud services, retention, consent, authorization, and emergency behavior was checked against the dated publication snapshot; evidence, corrections, and limits are recorded in `publication/FACTUAL_CLAIM_AUDIT.md`.
- [ ] Final publisher review accepts the residual trademark, privacy, safety-language, and legal risk without implying review by an outside professional.

## Photographs and artwork

- [x] The author confirms that he took every selected real photograph with his iPhone, owns ROB and the visible components, and permits commercial publication. Venue terms are not applicable because the closed allowlist contains no event or venue photograph.
- [x] Every selected photograph was inspected at full resolution for people, labels, addresses, account UI, credentials, network identifiers, locations, reflections, screens, and private notes; the named findings and exact reviewed bytes are recorded in `publication/ASSET_REVIEW_RECORD.md` and `publication/reviewed-assets.sha256`.
- [x] The exact 77-file image allowlist is checksum-verified; prepared photographs are metadata-stripped; automated validation rejects excluded names, changed reviewed bytes, missing files, and unreviewed image additions.
- [x] The 15 book illustrations, six derived cover JPEGs, campaign hero, and logo were visually reviewed at source resolution; the shared imprint now labels generated book imagery as illustration rather than documentary or engineering evidence. Printer-specific effective-resolution and physical-proof acceptance remain in the printer gate below.

## PDF and EPUB preflight

- [x] All ten PDFs build from the current sources and pass `bash tools/validate_books.sh`; rerun after the final author-answer reconciliation.
- [x] Every rendered PDF page receives a readable visual review for clipping, overflow, blank pages, missing images, caption placement, contrast, and navigation; the byte-bound result is recorded in publication/PDF_VISUAL_REVIEW_RECORD.md.
- [x] All ten EPUBs rebuild from the current sources and pass EPUBCheck plus the structural content/accessibility audit; rerun after the final author-answer reconciliation.
- [ ] A human checks EPUB reading order, headings, lists, tables, links, alt text, cover announcement, contrast, text resizing, VoiceOver, and Apple Books behavior on representative iPhone, iPad, and Mac devices.

## Printer and distribution proof

- [ ] The selected printer confirms trim, binding, safe margins/gutter, bleed, raster resolution, color space/profile, ink limits, transparency, embedded fonts, cover/spine specification, paper, and barcode requirements.
- [ ] Printer-specific interiors and covers pass the vendor's file review without press-side scaling or silent substitution.
- [ ] Full-page photographs, darkest pages, small captions, tables, and generated illustrations are checked in a physical proof.
- [ ] A complete bound proof is approved under representative event lighting before the production quantity is ordered.

## Apple Books and final approval

- [ ] Final title/subtitle, descriptions, categories, age/grade ranges, pricing, samples, territories, tax/banking status, ISBN strategy, and series metadata are approved.
- [ ] Apple Books submissions pass account-side validation and device review; each resulting book ID and URL is recorded in `publication/apple-books-catalog.json`.
- [ ] Rodolfo Aramayo records final publisher approval after rights, digital, and physical proofs are complete.

## Explicitly outside this book-release gate

Live ROB operation requires a separate machine/event release: qualified electrical and mechanical review, current schematics, guarding, E-stop and failure testing, measured stopping behavior, battery/charging controls, public barriers, trained operators and spotters, privacy signage, fire response, insurance, and venue approval. Printing these books does not satisfy or waive those duties.

## Release record

| Item | Reviewer | Evidence/revision | Date | Result |
|---|---|---|---|---|
| Dated camera/privacy claim audit | Codex-assisted source inspection | `publication/FACTUAL_CLAIM_AUDIT.md`; Cerebro `e76d515a56e8018c96d07efb251470a40f9de174` | 2026-08-29 | Pass against dated snapshot; publisher residual-risk acceptance remains open |
| Publisher factual/copyedit | Codex-assisted source and manuscript review | `publication/FACTUAL_CLAIM_AUDIT.md`; reconciled author answers; rebuilt and validated ten-title set | 2026-08-29 | Pass against dated evidence; final publisher legal-risk acceptance remains open |
| Photo/privacy rights | Rodolfo Aramayo author confirmation; Codex-assisted asset review | `publication/AUTHOR_INTERVIEW_RECORD.md`; `publication/ASSET_REVIEW_RECORD.md`; `publication/reviewed-assets.sha256` | 2026-08-29 | Pass for the closed 77-file allowlist |
| PDF visual proof | Codex-assisted page review | `publication/PDF_VISUAL_REVIEW_RECORD.md`; `publication/reviewed-pdfs.sha256` | 2026-08-29 | Pass — 573 byte-matched pages; later factual rebuild scoped and re-reviewed |
| EPUB accessibility/device proof |  |  |  |  |
| Printer file/physical proof |  |  |  |  |
| Apple Books account review |  |  |  |  |
| Final publisher approval | Rodolfo Aramayo |  |  |  |
