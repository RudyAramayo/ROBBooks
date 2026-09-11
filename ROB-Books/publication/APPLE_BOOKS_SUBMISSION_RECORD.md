# Building R.O.B. — Apple Books submission record

**Prepared:** 2026-08-29 · **Updated:** 2026-09-11

**Portal status:** The original ten ROB titles were imported on 2026-08-30 and are now live in the U.S. Apple Books catalog. All ten additional titles in **ROB's Little Helper Library** were uploaded, imported, assigned Apple IDs, and submitted with complete worldwide Rights and Pricing on 2026-09-11. Every new edition is currently **Waiting for Review**; public availability must not be claimed until Apple completes review and the product pages are verified live.
**Catalogs:** `publication/apple-books-catalog.json` and `publication/preschool-apple-books-catalog.json`

This record distinguishes file readiness from actions confirmed by Apple. It must not describe a title as uploaded, imported, in review, approved, cleared for sale, or live until the corresponding Apple Books page or catalog report supplies that evidence.

## Current Apple requirements used for preflight

- Apple requires an EPUB and appropriate metadata, recommends validation with the latest EPUBCheck, and routes web delivery through the Apple Books Publishing Portal: <https://itunespartner.apple.com/books/support/18-submit-your-book>.
- The current preparation guide limits books to 2 GB, recommends keeping each interior image at no more than four million pixels, asks for accessibility descriptions, and requires external JPEG/PNG RGB cover art with at least 1,400 pixels on the shortest side: <https://itunespartner.apple.com/books/support/9-prepare-book>.
- Required metadata includes title, primary author, a description of at least 50 characters, main and secondary subject categories, publisher, original publication date, language, and a unique permanent Vendor ID. Interest age is required for children and teen books. ISBN is optional, but Apple's publisher guide says it must be supplied with the initial submission and cannot be added later: <https://itunespartner.apple.com/books/support/12-metadata> and <https://help.apple.com/itc/bookspublisher/en.lproj/static.html>.
- Initial web upload sends the files and metadata to iTunes Connect. Pricing and availability are then configured in My Books; Apple warns that a newly imported title can take up to 24 hours to appear there: <https://itunespartner.apple.com/books/support/21-publish-from-web>.
- Rights and Pricing controls release timing, cleared-for-sale territory, DRM, Volume Content Service, release type, currency, price, and countries/regions: <https://itunespartner.apple.com/books/support/30-manage-book-rights-pricing>.

## Series-wide decisions already established

| Field | Prepared value |
|---|---|
| Author | Rodolfo Aramayo |
| Publisher / copyright owner | OrbitusRobotics LLC |
| Copyright | 2026; book text/art all rights reserved; repository source licenses remain separate |
| Language | en-US |
| Original publication date | 2026-08-29 |
| Release timing | As soon as Apple review is complete; no pre-order |
| Release type | Digital Only |
| Territory | Worldwide / all available countries and regions |
| Explicit content | No for every title |
| Sample | Apple-generated |
| Volume Content Service | Enabled |
| Accessibility claims | Alternative text, reading order, structural navigation, table of contents; no known accessibility hazard |
| ISBN | No ebook ISBNs; the ISBN field is blank on all ten Apple title records |
| Apple DRM | Disabled for every title; distribute the educational ebooks DRM-free |

On August 29, 2026, Rodolfo Aramayo directed the publisher to proceed without ebook ISBNs because none have been assigned and to disable DRM because the books are educational. No identifier was invented. The UUID values in the catalog remain the permanent identifiers embedded in the EPUB packages; iTunes Connect assigned separate numeric Vendor IDs during import, recorded below. Any later print edition requires a legitimate format-specific ISBN rather than a reused or fabricated number.

## Original ROB catalog inventory

| Title | EPUB UUID | Apple Vendor ID | Price | EPUB/cover preflight | Apple status / ID |
|---|---|---|---:|---|---|
| ROB and the Lost Yellow Ball | `0ef3f5ab-e49d-5f6c-a22e-ad2c70a07f4b` | `10084085996` | $2.99 | Passed and imported | On Store · [6806729418](https://books.apple.com/us/book/rob-and-the-lost-yellow-ball/id6806729418?ls=1) |
| Meet ROB | `aaffc931-e02b-53a3-812d-0ef80c58abdb` | `10084086331` | $4.99 | Passed and imported | On Store · [6806730228](https://books.apple.com/us/book/meet-rob/id6806730228?ls=1) |
| Circuits & Signals | `6827d07c-737e-5752-afaa-e807bac2b73b` | `10084086223` | $4.99 | Passed and imported | On Store · [6806730681](https://books.apple.com/us/book/circuits-signals/id6806730681?ls=1) |
| Motion Workshop | `9c8af395-77e4-5895-b86b-59028603a3cd` | `10084086370` | $4.99 | Passed and imported | On Store · [6806731300](https://books.apple.com/us/book/motion-workshop/id6806731300?ls=1) |
| Mission Control | `3fd86b5a-d5ee-5fe1-a628-94ea968acdea` | `10084086371` | $4.99 | Passed and imported | On Store · [6806731600](https://books.apple.com/us/book/mission-control/id6806731600?ls=1) |
| AI, Robotics, and Codex | `3183db78-228b-5df2-bc63-f2e5d4ff8c49` | `10084086394` | $8.99 | Passed and imported | On Store · [6806732016](https://books.apple.com/us/book/ai-robotics-and-codex/id6806732016?ls=1) |
| Dual-Arm Robotics | `e29b1978-9972-5f0d-96ba-fd84ea53716a` | `10084086449` | $8.99 | Passed and imported | On Store · [6806732519](https://books.apple.com/us/book/dual-arm-robotics/id6806732519?ls=1) |
| Engineering ROBControllerVision | `d08790c7-7646-56b7-914a-498d30a77128` | `10084086224` | $8.99 | Passed and imported | On Store · [6806732984](https://books.apple.com/us/book/engineering-robcontrollervision/id6806732984?ls=1) |
| Engineering Cerebro | `2d2c834f-9340-50f7-8a38-5b06c8379705` | `10084086583` | $8.99 | Passed and imported | On Store · [6806807905](https://books.apple.com/us/book/engineering-cerebro/id6806807905?ls=1) |
| Complete Builder's Field Manual | `454776a4-d151-539c-9ae4-7e7ccb9a3eda` | `10084086661` | $24.99 | Passed and imported | On Store · [6806809290](https://books.apple.com/us/book/complete-builders-field-manual/id6806809290?ls=1) |

Each title has a detailed UTF-8 store description, two current BISAC subjects, the approved audience/interest-age values, series metadata where applicable, a stable EPUB UUID, an Apple-assigned numeric Vendor ID, and explicit submission-status fields in the catalog. The complete collection is intentionally not numbered as Volume 9, and the children's story is intentionally a companion rather than a numbered engineering volume.

## ROB's Little Helper Library submission inventory

These ten new editions were submitted at $2.99 each for ages 2–5. The two Halloween titles and two Christmas titles use holiday-specific BISAC subjects; all titles include a second subject appropriate to their story.

| Title | EPUB UUID / initial Vendor ID | Price | EPUB/cover preflight | Apple status / ID |
|---|---|---:|---|---|
| Good Morning, ROB! | `b0f45c69-0c21-5121-8a01-5584bd6353b1` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6810959426](https://books.apple.com/us/book/id6810959426) |
| ROB Counts the Fireflies | `ff4bd173-4019-58da-a6c4-46e0a6a4b46b` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811118109](https://books.apple.com/us/book/id6811118109) |
| ROB's Rainbow Lights | `c07db8ca-cdc4-5d41-923b-ba6e6f2e2411` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811120320](https://books.apple.com/us/book/id6811120320) |
| ROB Hears a Little Sound | `5ceb6667-e969-59a9-ae2f-6d24046e8098` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811121042](https://books.apple.com/us/book/id6811121042) |
| ROB Shares the Shiny Star | `99001f04-05f8-5f58-a3b7-5cb090759d54` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811121106](https://books.apple.com/us/book/id6811121106) |
| ROB Waits for the Ducklings | `9a685d36-ba81-5eec-bd3a-9fc444fc5e71` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811124273](https://books.apple.com/us/book/id6811124273) |
| ROB and the Friendly Pumpkin | `7022a6c0-da87-5adc-89a0-9c57f1298761` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811125927](https://books.apple.com/us/book/id6811125927) |
| ROB's Costume Parade | `ff3639ef-f2b0-55df-9c35-328f08fd74e8` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811127353](https://books.apple.com/us/book/id6811127353) |
| ROB Lights the Little Tree | `5f1c5b72-14c3-5577-a571-9adbc8809dc8` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811128266](https://books.apple.com/us/book/id6811128266) |
| ROB's Quiet Christmas Eve | `aed789a8-f37f-5da2-9845-4e790c545b64` | $2.99 | Portal-validated and uploaded | Waiting for Review · [6811128916](https://books.apple.com/us/book/id6811128916) |

The cover and all four interior illustrations for every new title were visually inspected at source resolution on 2026-09-10. Covers are 2,550 × 3,300 sRGB JPEG files. Every story image is sRGB, includes editorially written alternative text in the manuscript, and stays below Apple's four-million-pixel interior-image guidance.

## ROB's Little Helper Library portal evidence recorded on 2026-09-11

- All ten uploads returned Apple's **You're almost done!** confirmation and appeared in My Books with their EPUB, Apple-generated sample, and cover art.
- Apple assigned a numeric Apple ID and direct Apple Books URL to every title; those identifiers are recorded in the inventory and preschool catalog.
- Rights and Pricing was confirmed for all 51 available countries or regions with a release date of Sep 11, 2026, Digital Only release type, a U.S. base price of $2.99, Cleared for Sale enabled, Volume Content Service enabled, and DRM disabled.
- Every title currently reports **Waiting for Review**. This is a completed submission, not an Apple approval or a verified live-store release.

## Store verification recorded on 2026-09-10

Apple's public U.S. Search API returned all ten original titles with the expected title, author, Apple Books URL, and U.S. price. Each linked product page returned HTTP 200. The original catalog records may now be reconciled from review-pending to live without relying only on the historical My Books snapshot below.

## Portal evidence recorded on 2026-08-30

- Every EPUB and cover import returned Apple's **You're almost done!** confirmation before the title appeared in My Books.
- Each My Books detail page shows a blank ISBN, the expected Apple ID and public URL, the original publication date of Aug 29, 2026, and **Waiting for Review**.
- Rights and Pricing was confirmed separately for every title with a release date of Aug 30, 2026, Digital Only release type, the catalog USD price, and all 51 available countries or regions selected.
- The saved Rights and Pricing table contains 51 rows for every title. All 51 rows are Cleared for Sale and VCS-Enabled, all 51 have a price tier and release date, and zero rows apply DRM.
- The final My Books refresh reports **Not on 51 Stores** for all ten titles. This is retained as the current store state while Apple review is pending; it is not treated as approval or a live-store confirmation.

## File evidence

- All ten EPUB 3 files pass EPUBCheck 5.3.0, the repository's structural accessibility audit, and DAISY Ace 1.4.5 with zero automated violations. The byte-bound evidence and browser visual review are recorded in `EPUB_ACCESSIBILITY_REVIEW_RECORD.md`; Apple Books and VoiceOver device review remains open.
- Every embedded JPEG/PNG is sRGB and at or below 4,000,000 pixels. External store covers remain 2,550 × 3,300 sRGB JPEGs so their shortest edge exceeds Apple's 1,400-pixel minimum.
- The 89 interior images resized to satisfy the four-million-pixel guidance were compared with source images resampled to the same dimensions. The ten lowest-ranked pairs received a side-by-side visual check at original contact-sheet detail; no visible crop, rotation, color, sharpness, or compression defect was found.
- Every EPUB is below Apple's 2 GB maximum; the largest is the complete manual at well under 100 MB.
- All ten UUID identifiers are stable and matched against the catalog.
- The ten print-layout PDFs remain a separate, byte-reviewed 573-page set; PDFs are not the Apple Books upload assets.

## Portal completion procedure

1. Confirm the Books agreement is active and that banking/tax tasks have no pending action.
2. Use no ISBN and retain the catalog Vendor ID for each title. Select DRM disabled in Rights and Pricing.
3. For each title, choose **Submit a New Book**, upload the catalog EPUB and cover, and leave the custom sample empty.
4. Enter the exact catalog title, subtitle, primary author, description, subject categories, interest age, language, publisher, original publication date, and Vendor ID/ISBN fields. Confirm explicit content is No.
5. Use **Upload Book to iTunes Connect** only after reviewing the summary. Record the returned import confirmation and do not claim an Apple ID until it appears in My Books or a catalog report.
6. In My Books, set worldwide Rights and Pricing, the catalog price in USD, effective immediately with no end date, Digital Only release type, the approved DRM choice, Cleared for Sale, and Volume Content Service enabled.
7. Record every Apple Books ID, public URL, import/review status, ticket, and pricing/territory result in `apple-books-catalog.json`.
8. Open the delivered edition in Apple Books on representative Mac, iPhone, and iPad devices. Check cover announcement, reading order, headings, lists, tables, links, image alternatives, theme/contrast, text resizing, navigation, and the automatically generated sample before clearing the digital-proof gate.
