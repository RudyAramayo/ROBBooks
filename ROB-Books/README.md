# Building R.O.B. — Maker Faire book set

This folder contains the editable sources, selected print-safe photographs, and PDF layout proofs for a picture-heavy ROB learning series. The set follows one real robot from early prototypes through mechanics, circuits, firmware, macOS software, controllers, sensing, autonomy, and public operation.

## The six books

| Book | Audience | Pages | Main idea | PDF |
|---|---|---:|---|---|
| Volume 1 — *Meet ROB* | Ages 8–12 | 30 | Systems thinking, structure, energy, sensors, iteration, and engineering logs | [`output/pdf/volume-1-meet-rob.pdf`](output/pdf/volume-1-meet-rob.pdf) |
| Volume 2 — *Circuits & Signals* | Ages 10–14 | 25 | Circuits, digital/analog/PWM signals, Arduino pins, serial messages, sensors, and watchdogs | [`output/pdf/volume-2-circuits-and-signals.pdf`](output/pdf/volume-2-circuits-and-signals.pdf) |
| Volume 3 — *Motion Workshop* | Ages 10–15 | 32 | Loads, differential drive, gearing, actuators, materials, fabrication, assembly, and testing | [`output/pdf/volume-3-motion-workshop.pdf`](output/pdf/volume-3-motion-workshop.pdf) |
| Volume 4 — *Mission Control* | Ages 12–16 | 30 | Mac/Arduino responsibilities, state, secure controllers, camera/depth/lidar data, AI boundaries, and simulation | [`output/pdf/volume-4-mission-control.pdf`](output/pdf/volume-4-mission-control.pdf) |
| *Complete Builder's Field Manual* | Advanced makers and mentors | 67 | Evidence-based full-build record, architecture, fabrication, power, firmware, software, verification, show operations, maintenance, and worksheets | [`output/pdf/complete-builders-field-manual.pdf`](output/pdf/complete-builders-field-manual.pdf) |
| Volume 5 — *AI, Robotics, and the Codex-Accelerated Evolution of ROBController and Cerebro* | Advanced makers and software builders | Printable edition | Source-based software history and a practical guide to using Codex and OpenAI while preserving robot safety, evidence, review, and human responsibility | [`output/pdf/volume-5-ai-robotics-with-codex.pdf`](output/pdf/volume-5-ai-robotics-with-codex.pdf) |

Volume 5's factual commit-by-commit appendix is maintained separately as the
[`Volume 5 Change Atlas`](source/volume-5-change-atlas.md). The manuscript was
reconstructed from the local ROBController and Cerebro Git histories on
August 10, 2026. Statements about the Codex-accelerated era are explicitly
presented as interpretation rather than Git authorship evidence. Product
guidance should be checked against the current
[official OpenAI documentation](https://learn.chatgpt.com/docs/) before publication.

The four youth volumes are designed to work independently or as a sequence. Their activities emphasize paper models, observation, low-energy educational circuits, simulations, and adult-supervised experiments. The expanded deep-learning labs use one repeated engineering cycle---observe, model, predict, test, explain, and revise---to develop systems reasoning, measurement, signal literacy, mechanics, networking, and bounded autonomy rather than vocabulary recall alone. The complete manual preserves the difficult questions and missing evidence that an experienced builder must resolve, adds a mentor curriculum, and records a structured workflow for the builder's future oral history.

The 2026 cover edition gives all four youth volumes a coordinated set of real
R.O.B. portraits with one green and one blue lightsaber. Each volume uses a
different front, portrait, side, or overhead view; the advanced field manual
keeps its more technical workshop cover.

The matching static web lesson lives in the ORobotics Hugo project at `/robot-lab/`. It is a four-mission, browser-only diagnostic game covering feedback, PWM, differential drive, and command freshness. It never connects to ROB or stores learner data.

## Edition status

These files are **layout proofs and an editorial first edition**, not certified build plans. ROB contains high-energy batteries, powerful motors, chains, treads, pinch and crush points, machine-made metal parts, networked control, cameras, microphones, and software-controlled motion. A qualified adult must own the electrical and mechanical design, guarding, emergency-stop system, hazard analysis, test perimeter, and public-show procedure.

Facts supported by the inspected archive are separated from proposals, historical revisions, commanded-but-unmeasured behavior, and unknowns. Search the TeX sources for `ROBPlaceholder` to find every question that still needs the builder's measurements or narrative. Work through [`EDITORIAL_GAPS.md`](EDITORIAL_GAPS.md) before calling the manual complete, then use [`PRINT_AND_SAFETY_REVIEW.md`](PRINT_AND_SAFETY_REVIEW.md) as the release gate.

## Evidence used

- `../Presentation/ROB_v3.pdf` — 95-page design-history presentation.
- `../ORobotics/media/gallery-originals/` and its gallery metadata — construction photographs from 2019–2025.
- `../ROBOT Build/ROBOT_CEREBELLULAR_BASE_APP.ino` — historical Arduino base firmware for treads, flipper, linear actuator, IR sensors, and heartbeat behavior.
- `../Cerebro/` — central macOS application and its current experimental branches.
- `../ROBController/` — iPhone and Watch control paths.
- `../ROBControllerVision/` — Vision Pro controller and simulator.
- `../M2M1-RPLIDAR-iOS-MacOS-Catalyst-/` — lidar telemetry implementation and fixtures.

The exact inspection snapshot is recorded in [`SOURCE_SNAPSHOT.md`](SOURCE_SNAPSHOT.md). Restricted vendor PDFs were not reproduced or paraphrased for publication; only visible component identity is mentioned, with a request for authorized public documentation.

## Project map

```text
ROB-Books/
├── source/                 editable XeLaTeX manuscripts, Volume 5 Markdown, and shared style
├── assets/photos/          selected, resized, metadata-stripped build photos
├── assets/slides/          selected presentation-page images
├── assets/generated/       original illustrative artwork, not engineering evidence
├── tools/                  asset, build, validation, preview, and learning tools
├── output/pdf/             the six printable PDF layout proofs
├── output/previews/        contact sheets for quick visual review
└── tmp/                    generated build files and excluded private-review images
```

[`ASSET_CREDITS.md`](ASSET_CREDITS.md) records image provenance, exclusions, and the illustration prompts. The preparation script is the authoritative mapping between gallery originals and public book filenames.

## Continuation handoff

Durable development notes are centralized outside this plain project folder at
[`../codex-notes/ROB-Books/README.md`](../codex-notes/ROB-Books/README.md).
They record the delivered edition, evidence boundaries, hardware and software
caveats, exact restart sequence, validation baseline, and prioritized next
work. Read the central
[`../codex-notes/README.md`](../codex-notes/README.md) first. Append future
checkpoints there rather than creating another project-local `codex-notes`
directory.

## Build and inspect

The scripts expect XeLaTeX/`latexmk`, Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`), ImageMagick 7 at the path used in the scripts, `exiv2`, `rg`, and the macOS fonts Avenir Next, Avenir Next Condensed, Futura, and Menlo.

From this directory:

```bash
bash tools/prepare_assets.sh
bash tools/build_books.sh
bash tools/validate_books.sh
bash tools/render_previews.sh
```

`prepare_assets.sh` rebuilds a conservative publication allowlist and strips image metadata. It fails if either publishable asset directory contains any unlisted entry, without deleting that entry automatically. `validate_books.sh` checks PDF freshness against each manuscript, the shared style, and referenced assets; rejects retired image names from publishable sources and outputs; and checks page geometry, text extraction, serious LaTeX warnings, and prepared-photo metadata. Validation does not replace engineering, privacy, legal, color, or press-preflight review.

## Safe companion lab

Volume 4 includes an offline Mac/Arduino serial-frame exercise. The companion script builds and validates the historical 42-byte text frame but never opens a serial port or moves hardware:

```bash
python3 tools/mac_serial_frame_lab.py
python3 tools/mac_serial_frame_lab.py --left-speed 120 --right-speed -120
```

Run `python3 tools/mac_serial_frame_lab.py --help` for all options. Do not repurpose the learning script as a live robot controller.

## Visual direction and rights

The books use an original weathered, optimistic retro-space workshop language: charcoal metal, warm cream, amber and cyan indicators, technical linework, and familiar system fonts. The project does not copy protected franchise logos, characters, typography, layouts, props, or story elements and is not affiliated with or endorsed by any film studio, franchise owner, component vendor, or platform company.

Before distribution, verify photo ownership and releases, component-image and documentation permissions, trademark wording, printer requirements, and all safety statements. Keep the generated illustrations labeled as storytelling rather than engineering evidence.
