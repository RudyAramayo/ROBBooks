# IngramSpark print submission record

## Current state

On September 5, 2026, Rodolfo Aramayo approved complimentary IngramSpark print ISBNs for all ten titles. Each title was created as a **Print Book Only** record with files deferred and the intended **Print, distribute, and sell book** workflow. All ten records are saved as **Setup Incomplete**. Ten vendor-specific interior files have now been built and locally validated, but none has been uploaded. No cover file, retail price, or wholesale terms have been entered, no proof has been ordered, and distribution has not been enabled.

The complimentary ISBN notice states that each ISBN is nontransferable, is owned by IngramSpark, uses the `Indy Pub` imprint, and requires participation in the wholesale program with retail pricing in at least one market. This is a print-format decision only. It does not replace or conflict with the existing Apple Books ebook identifiers, and no print ISBN has been reused for an ebook.

## Portal records

| # | Title | IngramSpark title ID | Complimentary print ISBN | Portal status |
|---:|---|---|---|---|
| 1 | *ROB and the Lost Yellow Ball* | `CSS9655730` | `979-8-2408-3421-9` | Setup Incomplete |
| 2 | *Meet ROB* | `CSS9655778` | `979-8-1827-4639-7` | Setup Incomplete |
| 3 | *Circuits & Signals* | `CSS9655786` | `979-8-1827-4640-3` | Setup Incomplete |
| 4 | *Motion Workshop* | `CSS9655791` | `979-8-1827-4641-0` | Setup Incomplete |
| 5 | *Mission Control* | `CSS9655796` | `979-8-1827-4642-7` | Setup Incomplete |
| 6 | *AI, Robotics, and Codex* | `CSS9655797` | `979-8-1827-4643-4` | Setup Incomplete |
| 7 | *Dual-Arm Robotics* | `CSS9655798` | `979-8-1827-4644-1` | Setup Incomplete |
| 8 | *Engineering ROBControllerVision* | `CSS9655800` | `979-8-1827-4645-8` | Setup Incomplete |
| 9 | *Engineering Cerebro* | `CSS9655802` | `979-8-1827-4646-5` | Setup Incomplete |
| 10 | *Complete Builder's Field Manual* | `CSS9655803` | `979-8-1827-4647-2` | Setup Incomplete |

The title dashboard was refreshed after entry and showed all ten records with the status above.

## Metadata entered

- English language, Rodolfo Aramayo as author, owned/necessary publishing rights, and nonfiction classification were entered for the technical titles. The story title remains classified as fiction.
- AI use was disclosed for text, images, and editorial function.
- Full and short descriptions, keywords, and two BISAC subjects were entered for every title.
- Volumes 1–8 use the `Building R.O.B.` series and their corresponding volume numbers. The complete manual has no print subtitle, avoiding the ebook-only phrase “The discounted complete digital collection.”
- The portal's Young Adult audience restricts interest ages to 13–18. Consequently, *Circuits & Signals* uses 13–14 instead of the source 10–14 range, *Motion Workshop* uses 13–15 instead of 10–15, and *Mission Control* uses 13–16 instead of 12–16. The manuscript audience guidance remains unchanged.
- The account imprint selector was empty. A prior attempt to create `Indy Pub` returned “Imprint Name is restricted,” consistent with it being IngramSpark's protected complimentary-ISBN imprint. No substitute custom imprint was created.

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

## Remaining release gates

1. Complete the editorial, safety, privacy, rights, and accessibility release gates.
2. Obtain ISBN- and page-count-specific IngramSpark templates and build the ten complete wrap covers with the supplied barcodes.
3. Confirm the planned 8.5 x 11-inch matte perfect-bound paperbacks, premium color for the story, and standard color on 70 lb white paper for the nine technical books in each portal record.
4. Resolve the portal's blank imprint selector without attempting to register the protected `Indy Pub` name manually.
5. Obtain explicit publisher approval for retail prices, wholesale discounts, return settings, market selections, and any final distribution submission.
6. Upload and validate files, order physical proofs, record proof approval, and only then enable distribution or place the balanced 50-copy event order.
