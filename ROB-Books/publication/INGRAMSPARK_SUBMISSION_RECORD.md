# IngramSpark print submission record

## Current state

On September 5, 2026, Rodolfo Aramayo approved complimentary IngramSpark print ISBNs and final title submission for all ten titles. Each title was created as a **Print Book Only** record with the intended **Print, distribute, and sell book** workflow. All ten page-count-specific cover templates were obtained from IngramSpark, and all ten interiors and complete wrap covers were built and locally validated.

All ten titles have now been fully submitted and reached IngramSpark's **Congratulations** page after both metadata and content-file validation reported no errors. The title dashboard shows every record in **Processing**, **In Processing**, or **Creating Title Record** status. IngramSpark says their digital proofs should arrive in 3-5 days. No digital proof has been approved, no physical proof or production run has been ordered, and distribution has not been enabled.

The complimentary ISBN notice states that each ISBN is nontransferable, is owned by IngramSpark, uses the `Indy Pub` imprint, and requires participation in the wholesale program with retail pricing in at least one market. This is a print-format decision only. It does not replace or conflict with the existing Apple Books ebook identifiers, and no print ISBN has been reused for an ebook.

## Portal records

| # | Title | IngramSpark title ID | Complimentary print ISBN | Portal status |
|---:|---|---|---|---|
| 1 | *ROB and the Lost Yellow Ball* | `CSS9655730` | `979-8-2408-3421-9` | Processing; awaiting digital proof |
| 2 | *Meet ROB* | `CSS9655778` | `979-8-1827-4639-7` | Processing; awaiting digital proof |
| 3 | *Circuits & Signals* | `CSS9655786` | `979-8-1827-4640-3` | Processing; awaiting digital proof |
| 4 | *Motion Workshop* | `CSS9655791` | `979-8-1827-4641-0` | Processing; awaiting digital proof |
| 5 | *Mission Control* | `CSS9655796` | `979-8-1827-4642-7` | In Processing; awaiting digital proof |
| 6 | *AI, Robotics, and Codex* | `CSS9655797` | `979-8-1827-4643-4` | Processing; awaiting digital proof |
| 7 | *Dual-Arm Robotics* | `CSS9655798` | `979-8-1827-4644-1` | In Processing; awaiting digital proof |
| 8 | *Engineering ROBControllerVision* | `CSS9655800` | `979-8-1827-4645-8` | In Processing; awaiting digital proof |
| 9 | *Engineering Cerebro* | `CSS9655802` | `979-8-1827-4646-5` | Creating Title Record; awaiting digital proof |
| 10 | *Complete Builder's Field Manual* | `CSS9655803` | `979-8-1827-4647-2` | Creating Title Record; awaiting digital proof |

The status above was verified on the title dashboard immediately after the final submission. All ten records show a September 5, 2026 submit date and a September 25, 2026 publication date.

## Metadata entered

- English language, Rodolfo Aramayo as author, owned/necessary publishing rights, and nonfiction classification were entered for the technical titles. The story title remains classified as fiction.
- AI use was disclosed for text, images, and editorial function.
- Full and short descriptions, keywords, and two BISAC subjects were entered for every title.
- Volumes 1–8 use the `Building R.O.B.` series and their corresponding volume numbers. The complete manual has no print subtitle, avoiding the ebook-only phrase “The discounted complete digital collection.”
- The portal's Young Adult audience restricts interest ages to 13–18. Consequently, *Circuits & Signals* uses 13–14 instead of the source 10–14 range, *Motion Workshop* uses 13–15 instead of 10–15, and *Mission Control* uses 13–16 instead of 12–16. The manuscript audience guidance remains unchanged.
- The complete manual's draft had lost its subject assignments. Before submission it was corrected to `TECHNOLOGY & ENGINEERING / Robotics` and `COMPUTERS / Artificial Intelligence / General`.
- The portal accepted the existing `OrbitusRobotics LLC` imprint selector value for all ten titles. Because complimentary ISBN documentation still describes `Indy Pub` as IngramSpark's ISBN-owning imprint, the digital proofs and final retail metadata must be checked to confirm how the public imprint is rendered.

## Portal print terms

- All titles use an 8.5 x 11-inch matte perfect-bound paperback. The story uses Premium Color on 70 lb white paper; Volumes 1-8 and the complete manual use Color 70.
- The publication date is September 25, 2026. The story's U.S. retail price is $12; Volumes 1-4 are $15; Volumes 5-8 are $18; and the complete manual is $40.
- Configured U.S. terms use a 40% wholesale discount and non-returnable status. IngramSpark's converted international prices use a 55% discount and non-returnable status. The required discount, non-return, and currency-conversion acknowledgements were accepted.
- The complete manual's portal print cost is $15.40 per book. At the $40 U.S. retail price and 40% wholesale discount, the portal estimated $7.85 U.S. publisher compensation before taxes and future pricing or currency changes.
- Text and number values were applied through the form's native input and change events because the portal's reactive controls discarded ordinary automated typing. Each saved page was verified after submission, and any international term temporarily lost during a portal refresh was reapplied before continuing.

## Production interiors

The production files are under `output/pdf/ingramspark/interiors/`. They use the current IngramSpark color-interior requirements: single pages, CMYK PDF/X-1a:2001, 8.5 x 11-inch trim, 0.125-inch bleed on the top, bottom, and outside edge only, no crop marks or interactive annotations, and even page counts. The reviewed trim region is not scaled or reflowed. Edge artwork is mirrored into bleed, and an intentional blank final page is added to the three odd-page source books.

| Title | Print pages | File size | Minimum effective raster resolution |
|---|---:|---:|---:|
| *ROB and the Lost Yellow Ball* | 24 | 6.1 MB | 300 ppi |
| *Meet ROB* | 38 | 15.4 MB | 246 ppi |
| *Circuits & Signals* | 36 | 11.8 MB | 222 ppi |
| *Motion Workshop* | 36 | 21.9 MB | 226 ppi |
| *Mission Control* | 40 | 17.4 MB | 226 ppi |
| *AI, Robotics, and Codex* | 44 | 1.5 MB | 300 ppi |
| *Dual-Arm Robotics* | 34 | 1.5 MB | 300 ppi |
| *Engineering ROBControllerVision* | 38 | 1.9 MB | 300 ppi |
| *Engineering Cerebro* | 50 | 2.1 MB | 210 ppi |
| *Complete Builder's Field Manual* | 236 | 28.3 MB | 299 ppi |

The validator passed all 576 print pages. All listed fonts are embedded; all raster records are CMYK or gray and at least 200 ppi; Ghostscript rendered every PDF without an error; sampled odd/even trim regions matched the reviewed RGB source pixels exactly; and contact sheets plus representative 150-dpi detail renders showed no clipping, missing pages, broken photographs, or raster defects. The file hashes are byte-bound in `publication/ingramspark-interiors.sha256`.

IngramSpark recommends 300 ppi and states that color-interior images below 72 ppi may be rejected. Four photo-heavy volumes contain a small number of source images between 210 and 246 effective ppi; they exceed the rejection threshold and the project's stricter 200-ppi preflight floor, but must be examined in the physical proof. Requirements were checked against the current [IngramSpark File Creation Guide](https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf) and [print file requirements](https://www.ingramspark.com/blog/file-requirements-for-print-books).

## Production covers

The official templates are archived under `publication/ingramspark/templates/`, one per ISBN and exact page count. The complete wrap covers are under `output/pdf/ingramspark/covers/`. Each retains IngramSpark's exact template geometry and supplied barcode, uses the reviewed 8.5 x 11-inch front artwork with edge-extended bleed, and adds a CMYK vector back cover with OrbitusRobotics LLC identification. The 236-page manual has spine text; the thinner books intentionally do not.

All ten one-page covers are 21 x 12 inches, PDF/X-1a:2001, CMYK/gray only, with embedded fonts and 300 ppi raster components. Ghostscript and Poppler rendered every cover without errors, and contact-sheet plus individual visual review showed the trim, bleed, back copy, barcodes, and manual spine correctly placed. Exact output hashes are recorded in `publication/ingramspark-covers.sha256`.

## Remaining release gates

1. Inspect each digital proof when IngramSpark supplies it, paying particular attention to the public imprint, spine, barcodes, bleed, and the 210-246 ppi source photographs.
2. Confirm production timing and shipping before ordering. A balanced 50-copy event order means five copies of each title; no paid order may be placed until the portal shows the exact total and delivery estimate and Rodolfo confirms the purchase.
3. Approve proofs and enable distribution only after review. The September 25 event date creates schedule pressure but does not waive proof or checkout verification.
