# Building R.O.B. — Apple Books publication plan

The ten current PDFs are editorial layout proofs. They are not uploaded store editions. Publication is gated by [`PRINT_AND_SAFETY_REVIEW.md`](PRINT_AND_SAFETY_REVIEW.md), the unresolved items in [`EDITORIAL_GAPS.md`](EDITORIAL_GAPS.md), an accessible EPUB conversion, and review in the signed-in Apple Books publishing account.

## Prepared launch catalog

| Edition | Planned US price |
|---|---:|
| *ROB and the Lost Yellow Ball* | $2.99 |
| Volumes 1–4 | $4.99 each |
| Volumes 5–8 | $8.99 each |
| *Complete Builder's Field Manual* | $24.99 |

The eight numbered volumes total $55.92. The $24.99 Complete Builder's Field Manual is the discounted digital collection, a 55% saving. This avoids promising a store-level series bundle that Apple may not offer in the publisher account. The standalone picture story is not part of that comparison.

The machine-readable title, description, audience, page-count, price, category recommendation, cover, EPUB destination, and future Apple Books identifiers live in [`publication/apple-books-catalog.json`](publication/apple-books-catalog.json). Category wording is a recommendation and must be matched to the choices currently presented by the publishing portal.

## Asset preparation

Run:

```bash
python3 tools/prepare_apple_books_assets.py --prepare-covers
python3 tools/prepare_apple_books_assets.py
```

The cover command renders each approved first page as a 2550×3300-pixel RGB JPEG. The validator checks catalog totals, PDF page counts, cover size and color space, and reports EPUBs that are still pending.

Build all ten reflowable EPUB 3 editions with:

```bash
python3 tools/build_accessible_epubs.py
```

The builder uses Pandoc, applies the accessible publication stylesheet, assigns stable identifiers, runs EPUBCheck 5.3.0, and audits language declarations, image alternatives, table headers, and required deep-lab/compendium content. A semantic conversion layer preserves Volumes 1–4 and the complete manual's custom photographs, captions, callouts, diagrams, included deep labs, and embedded Markdown volumes. The picture story has its own source-native accessible Markdown edition. A superficially valid EPUB that silently drops custom material is not accepted by the build.

Apple Books can automatically create samples for these non-interactive, reflowable editions. The full EPUB navigation must therefore identify body matter correctly, and the automatically generated sample must be inspected in the publishing portal before release. A custom preview EPUB is optional for this set; it becomes mandatory only if an edition gains read-aloud behavior or other features for which Apple's current asset guide requires one.

Do not make an EPUB by turning every PDF page into an image. Apple requires searchable, accessible content and rejects interior images that contain embedded body text. The source needs a deliberate EPUB 3 conversion that keeps headings, paragraphs, lists, tables, links, alternative text, and reading order live. Page-dependent workshop diagrams may remain images when they have appropriate descriptions.

Each final EPUB must:

1. preserve real text and a logical table of contents;
2. include useful image descriptions and no private-review media;
3. pass the current production release of EPUBCheck with no errors;
4. be inspected in Apple Books on iPhone, iPad, and Mac at multiple text sizes;
5. have a representative sample whose links, image descriptions, and navigation are reviewed;
6. match the approved title, author, publisher, audience, description, rights, territories, and price.

`python3 tools/prepare_apple_books_assets.py --release` is intentionally strict. It fails until every EPUB, Apple Books ID, and Apple Books URL is present. Human sign-off in the release gate remains mandatory even after the script passes.

Before device review, run EPUBCheck and DAISY Ace against every final package. After installing the official `@daisy/ace` CLI, use `python3 tools/audit_daisy_ace.py`; pass `--ace /path/to/ace` when it is not on `PATH`. The byte-bound automated and browser-rendering evidence belongs in `publication/EPUB_ACCESSIBILITY_REVIEW_RECORD.md` and `publication/reviewed-epubs.sha256`. A zero-violation Ace report is useful evidence, but it does not replace the Apple Books, VoiceOver, and manual accessibility checks.

## Account-side release

After publisher approval:

1. sign in to the Apple Books publishing portal using the OrbitusRobotics account;
2. confirm agreements, tax, banking, rights, territories, and release dates;
3. upload the validated EPUB, cover, sample, and metadata for each edition;
4. set the prices above or select the closest permitted tier shown for each territory;
5. group Volumes 1–8 as the *Building R.O.B.* series and publish the manual as the discounted complete collection;
6. wait for Apple review, record each final ID and URL in the catalog, and run the release validator;
7. copy the approved links into the website catalog so the pending labels become purchase buttons.

The existing OrbitusRobotics title is [*Dark Vapor4* on Apple Books](https://books.apple.com/us/book/dark-vapor4/id1538369440/). It is linked from the website as proof of the current publisher identity; it is not part of the Building R.O.B. series.

## Official references

- [Publish a book from the web](https://authors.apple.com/support/4574-publish-book-from-web)
- [Apple Books Asset Guide: EPUB](https://help.apple.com/itc/booksassetguide/en.lproj/static.html)
- [Apple Books Asset Guide: interior images](https://help.apple.com/itc/booksassetguide/en.lproj/itca71ad3c33.html)
- [Apple Books Asset Guide: cover art](https://help.apple.com/itc/booksassetguide/en.lproj/itc1bda991ba.html)
- [W3C EPUBCheck](https://github.com/w3c/epubcheck)
