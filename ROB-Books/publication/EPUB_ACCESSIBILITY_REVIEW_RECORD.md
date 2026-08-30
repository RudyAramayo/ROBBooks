# Building R.O.B. — EPUB accessibility and visual preflight record

**Review date:** 2026-08-29

**AUTOMATED AND BROWSER VISUAL PREFLIGHT: COMPLETE**

**APPLE BOOKS AND ASSISTIVE-TECHNOLOGY DEVICE REVIEW: OPEN**

This record binds the completed automated accessibility checks and browser rendering review to the exact ten EPUB files listed in `reviewed-epubs.sha256`. It does not claim WCAG conformance, third-party accessibility certification, VoiceOver approval, or Apple Books device approval. DAISY explains that Ace covers only automatable checks and that manual evaluation remains necessary.

## Automated checks

- EPUBCheck 5.3.0: all ten EPUB 3.3 packages passed with zero errors and zero warnings.
- DAISY Ace 1.4.5: all ten packages passed with zero automated violations after a complete `python3 tools/audit_daisy_ace.py --ace /path/to/ace` run against the final bytes.
- The repository structural audit confirms root language, alternative text on every image, table header cells, heading progression without skipped levels, keyboard-focusable code regions, a body-matter landmark, a table of contents, and a catalog-matched accessibility summary.
- Every package declares `schema:accessMode`, `schema:accessModeSufficient`, `schema:accessibilityFeature`, `schema:accessibilityHazard`, and `schema:accessibilitySummary`. Certifier and `dcterms:conformsTo` metadata are deliberately absent because no outside certifier or complete manual conformance review exists.
- The corrected styles provide explicit high-contrast light and dark backgrounds, inherit foreground color inside syntax tokens, wrap long code, and retain keyboard access to code regions.

The initial Ace run exposed low-contrast links and syntax colors, skipped heading levels, missing accessibility summaries, and two code regions that were not keyboard focusable. Those findings were corrected in the build pipeline before this final zero-violation run.

## Browser visual and large-text review

Each title was unpacked and rendered with Chrome 148.0.7778.97 in two modes: a 390 × 844 light viewport at 150% body text and a 1,024 × 768 dark viewport. The targeted element was centered before capture. Both ten-title contact sheets were inspected at original detail.

| Title | Reviewed content |
|---|---|
| Complete Builder's Field Manual | `ch003.xhtml`; evidence-status table |
| ROB and the Lost Yellow Ball | `ch005.xhtml`; story illustration and surrounding text |
| Meet ROB | `ch001.xhtml`; cover image and front matter |
| Circuits & Signals | `ch012.xhtml`; photograph, caption, and callout |
| Motion Workshop | `ch001.xhtml`; cover image and front matter |
| Mission Control | `ch024.xhtml`; illustration, caption, and callout |
| AI, Robotics, and Codex | `ch012.xhtml`; code example and explanatory prose |
| Dual-Arm Robotics | `ch017.xhtml`; configuration example and prose |
| Engineering ROBControllerVision | `ch005.xhtml`; Swift example and prose |
| Engineering Cerebro | `ch029.xhtml`; Swift example and numbered explanation |

Result: text, tables, images, captions, callouts, and code remained visible; content reflowed without overlap, hidden horizontal content, broken image scaling, or unreadable light/dark contrast. Long identifiers wrap at the narrow large-text viewport, which preserves all characters and avoids a keyboard-inaccessible horizontal region.

## Work still required

The real EPUB files must still be opened in Apple Books on representative Mac, iPhone, and iPad devices. A human must check navigation, generated samples, typography and themes, maximum practical text size, VoiceOver reading order and announcements, link operation, table navigation, and image alternatives. Those checks remain open in `PRINT_AND_SAFETY_REVIEW.md`; this browser review does not clear them.

References: [Ace by DAISY](https://daisy.org/activities/software/ace/), [DAISY Ace guidance](https://kb.daisy.org/publishing/docs/epub/validation/ace.html), and [EPUB accessibility validation](https://kb.daisy.org/publishing/docs/conformance/epub.html).
