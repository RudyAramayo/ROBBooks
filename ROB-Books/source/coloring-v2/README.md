# ROB illustrated coloring collection

Ten books built around 350 separately generated coloring illustrations, with
matching color front and back covers. This edition replaces the procedural
coloring draft after the author requested substantially more varied artwork.

## Children's adventures

Each book contains 30 coloring pages total, plus a front cover, name/instruction
page, palette page, and back cover: 34 PDF pages.

| Title | PDF |
| --- | --- |
| Good Morning, ROB! | [Download](../../output/pdf/coloring-v2/children/good-morning-rob-coloring.pdf) |
| ROB Counts the Fireflies | [Download](../../output/pdf/coloring-v2/children/rob-counts-the-fireflies-coloring.pdf) |
| ROB's Rainbow Lights | [Download](../../output/pdf/coloring-v2/children/robs-rainbow-lights-coloring.pdf) |
| ROB Hears a Little Sound | [Download](../../output/pdf/coloring-v2/children/rob-hears-a-little-sound-coloring.pdf) |
| ROB Shares the Shiny Star | [Download](../../output/pdf/coloring-v2/children/rob-shares-the-shiny-star-coloring.pdf) |

Bold outlines and spacious shapes accompany ROB, Puppy, familiar objects, garden
creatures, weather, and playful geometric designs. These are new coloring
adventures inspired by the preschool stories, with expanded scenes.

## Adult collection

Each book contains 40 coloring illustrations, plus a front cover, introductory
page, palette page, and back cover: 44 PDF pages.

| Title | Focus | PDF |
| --- | --- | --- |
| ROB's Clockwork Halloween | Gothic plants, ornamental skulls, costumes, pumpkins | [Download](../../output/pdf/coloring-v2/adult/rob-halloween-coloring.pdf) |
| ROB's Harvest and Thanksgiving | Orchards, wreaths, feasts, autumn still lifes | [Download](../../output/pdf/coloring-v2/adult/rob-thanksgiving-coloring.pdf) |
| ROB's Christmas Workshop | Snowy villages, ornaments, mechanical reindeer | [Download](../../output/pdf/coloring-v2/adult/rob-christmas-coloring.pdf) |
| ROB's Clockwork Gardens | Glasshouses, botanicals, mechanical pollinators | [Download](../../output/pdf/coloring-v2/adult/rob-clockwork-gardens-coloring.pdf) |
| ROB After Hours: Neon and Smoke — 18+ | Cannabis smoking, tobacco, cocktails, music, adult robot companionship | [Download](../../output/pdf/coloring-v2/adult/rob-after-hours-coloring.pdf) |

Adult illustrations have moderately finer detail, varied perspectives, botanical
textures, architecture, patterned objects, and decorative arrangements. After
Hours uses adult robot characters and non-explicit anime/noir settings. Cannabis,
tobacco, and alcohol themes are confined to that clearly labeled 18+ edition.

## Printing

- US Letter, portrait, actual size (100%).
- Children's art: PDF pages 3–32; 15 sheets when printed on both sides.
- Adult art: PDF pages 3–42; 20 sheets when printed on both sides.
- Duplex: flip on the long edge. Crayons and colored pencils suit duplex use.
- Markers: print one-sided and use a protective sheet beneath the page.
- Front covers: page 1. Back covers: page 34 (children) or 44 (adult).
- Complete PDFs: 17 duplex sheets per children's book; 22 per adult book.

These are printable reader PDFs, not printer-specific imposed booklets or
wraparound covers with spine and bleed. Source artwork is retained at its native
resolution and placed uncropped; the validation report records effective DPI.
The finished interiors have a minimum effective resolution of 162.2 DPI; these
are not 300-DPI press files.

Preview all matching covers: [children](../../output/previews/coloring-v2/children-cover-pairs.jpg)
and [adults](../../output/previews/coloring-v2/adult-cover-pairs.jpg).

## Source and provenance

- `children-scenes.txt`: 150 individually written page briefs and titles.
- `adult-scenes.txt`: 200 individually written page briefs and titles.
- `catalog.json`: ordered book/page data used by the builder.
- `assets/coloring-v2/<book>/<page>.png`: individual generated source illustrations.
- Adjacent JSON files retain the scene, generation prompt, and source image path.
  Two initial trial images (Morning 01 and Halloween 01) have provenance notes
  instead of a verbatim prompt; their original prompts remain in the session.
- Each `cover.png` is separately generated full-color art; the back cover uses
  three previews from that book in a matching typographic design.
- `publication-manifest.json`: PDF/page/image mapping, SHA-256 hashes, geometry.
- `output/previews/coloring-v2/`: all-page contact sheets and validation results.

The original preschool manuscripts and paintings remain unchanged. ROB's shared
character features are a rectangular head, round eyes, mechanical hands, and
tracked base; individual illustrations have natural AI-assisted drawing variation.
No interior artwork is repeated as another coloring page. Cover previews are
intentional reuse and do not count toward the 30/40-page totals.

The author's references informed broad art-direction criteria:
[Free Coloring Pages — Kids](https://www.freecoloringpages.net/category/kids/)
(simple objects, characters, and varied subjects) and
[Robin Colors — Adult Skulls](https://www.robincolors.com/skulls-coloring-pages-for-adults/)
(flora, ornamental motifs, and varied detail). Reference page descriptions were
reviewed; their downloadable illustrations were not copied into these books.

## Rebuild and verify

Python 3.9+, with the dependencies in `requirements-coloring.txt` and the macOS
Arial, Arial Rounded Bold, and Georgia Bold fonts used by the builder:

```sh
python3 tools/build_illustrated_coloring_books.py
python3 tools/verify_illustrated_coloring_books.py
```

The builder requires all 350 interiors and ten cover artworks. It embeds fonts
and preserves complete image bounds. The verifier checks totals, Letter geometry,
caption extraction, margins, unique source hashes across books, monochrome art,
nonblank interiors, effective resolution, and successful rendering of every page.
Rendered contact sheets and larger page samples complement automated checks;
image hash uniqueness alone does not establish visual variety.

For an incomplete production proof only:

```sh
python3 tools/build_illustrated_coloring_books.py --proof --book rob-after-hours
python3 tools/verify_illustrated_coloring_books.py --proof
python3 tools/verify_illustrated_coloring_books.py --art-sheets
```

Copyright 2026 OrbitusRobotics LLC. Stories and characters by Rodolfo Aramayo and
Kierie Aramayo. Original AI-assisted illustrations for this edition.
