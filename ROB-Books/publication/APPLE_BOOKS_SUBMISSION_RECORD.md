# Building R.O.B. — Apple Books submission record

**Prepared:** 2026-08-29

**Portal status:** Not submitted; the signed-in browser has not yet been attached to this Codex session.
**Catalog:** `publication/apple-books-catalog.json`

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
| ISBN | **Publisher choice pending before initial upload** |
| Apple DRM | **Publisher choice pending before Rights and Pricing is finalized** |

The ISBN decision is intentionally open because it is irreversible for an Apple Books record. The fastest Apple-only digital launch is to omit ebook ISBNs and retain the ten permanent UUID Vendor IDs already embedded in the EPUBs. Supplying ISBNs instead requires ten unique ebook ISBN-13 values before any initial upload; later print editions need their own format-specific ISBNs.

## Upload inventory

| Title | Vendor ID | Price | EPUB/cover preflight | Apple status / ID |
|---|---|---:|---|---|
| ROB and the Lost Yellow Ball | `0ef3f5ab-e49d-5f6c-a22e-ad2c70a07f4b` | $2.99 | Ready | Not submitted |
| Meet ROB | `aaffc931-e02b-53a3-812d-0ef80c58abdb` | $4.99 | Ready | Not submitted |
| Circuits & Signals | `6827d07c-737e-5752-afaa-e807bac2b73b` | $4.99 | Ready | Not submitted |
| Motion Workshop | `9c8af395-77e4-5895-b86b-59028603a3cd` | $4.99 | Ready | Not submitted |
| Mission Control | `3fd86b5a-d5ee-5fe1-a628-94ea968acdea` | $4.99 | Ready | Not submitted |
| AI, Robotics, and Codex | `3183db78-228b-5df2-bc63-f2e5d4ff8c49` | $8.99 | Ready | Not submitted |
| Dual-Arm Robotics | `e29b1978-9972-5f0d-96ba-fd84ea53716a` | $8.99 | Ready | Not submitted |
| Engineering ROBControllerVision | `d08790c7-7646-56b7-914a-498d30a77128` | $8.99 | Ready | Not submitted |
| Engineering Cerebro | `2d2c834f-9340-50f7-8a38-5b06c8379705` | $8.99 | Ready | Not submitted |
| Complete Builder's Field Manual | `454776a4-d151-539c-9ae4-7e7ccb9a3eda` | $24.99 | Ready | Not submitted |

Each title has a detailed UTF-8 store description, two current BISAC subjects, the approved audience/interest-age values, series metadata where applicable, a stable Vendor ID that matches the EPUB identifier, and explicit submission-status fields in the catalog. The complete collection is intentionally not numbered as Volume 9, and the children's story is intentionally a companion rather than a numbered engineering volume.

## File evidence

- All ten EPUB 3 files pass EPUBCheck 5.3.0 and the repository's structural accessibility audit.
- Every embedded JPEG/PNG is sRGB and at or below 4,000,000 pixels. External store covers remain 2,550 × 3,300 sRGB JPEGs so their shortest edge exceeds Apple's 1,400-pixel minimum.
- The 89 interior images resized to satisfy the four-million-pixel guidance were compared with source images resampled to the same dimensions. The ten lowest-ranked pairs received a side-by-side visual check at original contact-sheet detail; no visible crop, rotation, color, sharpness, or compression defect was found.
- Every EPUB is below Apple's 2 GB maximum; the largest is the complete manual at well under 100 MB.
- All ten UUID identifiers are stable and matched against the catalog.
- The ten print-layout PDFs remain a separate, byte-reviewed 573-page set; PDFs are not the Apple Books upload assets.

## Portal completion procedure

1. Confirm the Books agreement is active and that banking/tax tasks have no pending action.
2. Resolve ISBN and DRM choices in this record and the JSON catalog.
3. For each title, choose **Submit a New Book**, upload the catalog EPUB and cover, and leave the custom sample empty.
4. Enter the exact catalog title, subtitle, primary author, description, subject categories, interest age, language, publisher, original publication date, and Vendor ID/ISBN fields. Confirm explicit content is No.
5. Use **Upload Book to iTunes Connect** only after reviewing the summary. Record the returned import confirmation and do not claim an Apple ID until it appears in My Books or a catalog report.
6. In My Books, set worldwide Rights and Pricing, the catalog price in USD, effective immediately with no end date, Digital Only release type, the approved DRM choice, Cleared for Sale, and Volume Content Service enabled.
7. Record every Apple Books ID, public URL, import/review status, ticket, and pricing/territory result in `apple-books-catalog.json`.
8. Open the delivered edition in Apple Books on representative Mac, iPhone, and iPad devices. Check cover announcement, reading order, headings, lists, tables, links, image alternatives, theme/contrast, text resizing, navigation, and the automatically generated sample before clearing the digital-proof gate.
