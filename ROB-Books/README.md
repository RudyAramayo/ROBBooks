# Building R.O.B. — Maker Faire book set

This folder contains the editable sources, selected print-safe photographs, and PDF layout proofs for a picture-heavy ROB learning series. The set follows one real robot from early prototypes through mechanics, circuits, firmware, macOS software, controllers, sensing, autonomy, and public operation.

## The nine books

| Book | Audience | Pages | Main idea | PDF |
|---|---|---:|---|---|
| Volume 1 — *Meet ROB* | Ages 8–12 | 37 | Systems thinking, structure, energy, sensors, iteration, and engineering logs | [`output/pdf/volume-1-meet-rob.pdf`](output/pdf/volume-1-meet-rob.pdf) |
| Volume 2 — *Circuits & Signals* | Ages 10–14 | 36 | Circuits, a supervised USB-to-5 V toy lab, digital/analog/PWM signals, Arduino pins, serial messages, sensors, and watchdogs | [`output/pdf/volume-2-circuits-and-signals.pdf`](output/pdf/volume-2-circuits-and-signals.pdf) |
| Volume 3 — *Motion Workshop* | Ages 10–15 | 36 | Loads, differential drive, gearing, actuators, materials, fabrication, assembly, and testing | [`output/pdf/volume-3-motion-workshop.pdf`](output/pdf/volume-3-motion-workshop.pdf) |
| Volume 4 — *Mission Control* | Ages 12–16 | 40 | Mac/Arduino responsibilities, Cerebro's recovered roots, controller ownership, three camera feeds, depth/lidar maps, consent-based face context, private messaging, AI boundaries, and simulation | [`output/pdf/volume-4-mission-control.pdf`](output/pdf/volume-4-mission-control.pdf) |
| Volume 5 — *AI, Robotics, and the Codex-Accelerated Evolution of ROBController and Cerebro* | Advanced makers and software builders | 43 | Source-based history from Cerebro's 2017-2018 seed through the 2025 repository migration, plus practical Swift/MLX, recording, identity, Messages, perception, shows, and Vision Pro lessons | [`output/pdf/volume-5-ai-robotics-with-codex.pdf`](output/pdf/volume-5-ai-robotics-with-codex.pdf) |
| Volume 6 — *Dual-Arm Robotics: AMBER B1, URDF, CAN, and Ubuntu* | Advanced makers and robot integrators | 34 | Two seven-joint AMBER arms, URDF and frame calibration, stable CAN identity, UDP/LCM protocols, clean Ubuntu reproduction, diagnostics, and staged commissioning | [`output/pdf/volume-6-amber-dual-arm-robotics.pdf`](output/pdf/volume-6-amber-dual-arm-robotics.pdf) |
| Volume 7 — *Engineering ROBControllerVision* | Swift and visionOS developers | 38 | Swift 6 architecture, explicit control ownership, PSVR Sense dual-arm jogging, three authenticated video feeds, immersive 360 presentation, speech, testing, and production review | [`output/pdf/volume-7-engineering-robcontrollervision.pdf`](output/pdf/volume-7-engineering-robcontrollervision.pdf) |
| Volume 8 — *Engineering Cerebro* | Swift and Objective-C developers | 50 | Recovered pre-v5 lineage, mixed-language coordination, RGB-D and panoramic perception, MLX/Gemini, encrypted face identity, private Messages, training capture, H.264, and bounded autonomy | [`output/pdf/volume-8-engineering-cerebro.pdf`](output/pdf/volume-8-engineering-cerebro.pdf) |
| *Complete Builder's Field Manual* | Advanced makers and developers | 236 | Unified historical engineering record with Cerebro's recovered lineage, current control, mapping, perception, privacy, recording, arms, AI boundaries, verification, operations, and maintenance | [`output/pdf/complete-builders-field-manual.pdf`](output/pdf/complete-builders-field-manual.pdf) |

## Standalone picture story

*ROB and the Lost Yellow Ball* is a separate 23-page read-aloud picture book for ages 5–6; it is not a numbered technical-series volume. Its gentle story introduces sensing, stopping, planning, checking, counting, kindness, and feedback through large illustrations and simple diagrams. It contains no robot-building instructions. PDF: [`output/pdf/rob-and-the-lost-yellow-ball.pdf`](output/pdf/rob-and-the-lost-yellow-ball.pdf).

Volume 5's factual commit-by-commit appendix is maintained separately as the
[`Volume 5 Change Atlas`](source/volume-5-change-atlas.md). The manuscript was
reconstructed from the local ROB repositories and the preserved Cerebro v1-v5
workshop folders through August 23, 2026. The recovered chronology and its
evidence boundaries are maintained in
[`CEREBRO_ARCHIVE_HISTORY.md`](CEREBRO_ARCHIVE_HISTORY.md). The 2025 v5 root is
documented as a fresh-repository migration, not Cerebro's inception.
Statements about the Codex-accelerated era are explicitly
presented as interpretation rather than Git authorship evidence. Product
guidance should be checked against the current
[official OpenAI documentation](https://learn.chatgpt.com/docs/) before publication.

The four youth volumes are designed to work independently or as a sequence. Their activities emphasize paper models, observation, low-energy educational circuits, simulations, and adult-supervised experiments. The expanded deep-learning labs use one repeated engineering cycle---observe, model, predict, test, explain, and revise---to develop systems reasoning, measurement, signal literacy, mechanics, networking, and bounded autonomy rather than vocabulary recall alone. The complete manual preserves ROB's hand-built history, teaches from revision evidence, adds a mentor curriculum, and keeps missing as-built measurements in a clearly scoped future-edition ledger.

The 2026 cover edition gives all four youth volumes a coordinated set of real
R.O.B. portraits with one green and one blue lightsaber. Each volume uses a
different front, portrait, side, or overhead view; the advanced field manual
keeps its more technical workshop cover.

The matching Circuit Quest lesson lives in the ORobotics Hugo project at
`/robot-lab/`. It is a 90-build, browser-only learning lab that grows from
closed DC loops and Ohm's law through AC, RLC behavior, Arduino programming,
timer and op-amp circuits, and a sectional virtual ROB build. Builds 81–90 are
the Book Bridge: base-flipper recovery, speaker and custom-techno signal paths,
far-field conference-microphone reasoning, and a bounded integrated show. The
first 80 builds remain the Maker Faire passport curriculum; the Book Bridge is
additional advanced practice. The simulation never connects to physical ROB,
and microphone lessons model signal levels without recording microphone audio.

The companion ROB Training campaign now spans the Three.js website game and the
native iOS/visionOS project in `../ROBTrainingGames/`. A completed sectional
droid profile carries color and unlocked systems into training. The simulated
ROB includes a tread-base lift flipper, visible stereo speakers for the game's
procedural techno, and a conference microphone with explicit listening and
privacy boundaries. The shared mission, component, scoring, and safety
vocabulary is maintained in
[`ROBOT_GAME_CURRICULUM.md`](ROBOT_GAME_CURRICULUM.md).

## Edition status

These files are **layout proofs of a historical engineering and educational edition**, not certified build plans. ROB contains high-energy batteries, powerful motors, chains, treads, pinch and crush points, machine-made metal parts, networked control, cameras, microphones, and software-controlled motion. Nothing in the books approves construction or live operation. A qualified adult must own any electrical and mechanical design, guarding, emergency-stop system, hazard analysis, test perimeter, and public-show procedure.

Facts supported by the inspected archive are separated from the author's recollection, proposals, historical revisions, commanded-but-unmeasured behavior, and unknowns. The manuscripts use evidence-limit callouts instead of blank technical placeholders. [`publication/AUTHOR_INTERVIEW_RECORD.md`](publication/AUTHOR_INTERVIEW_RECORD.md) tracks the few remaining author confirmations; [`EDITORIAL_GAPS.md`](EDITORIAL_GAPS.md) separates publication blockers from future as-built engineering work; [`publication/PDF_VISUAL_REVIEW_RECORD.md`](publication/PDF_VISUAL_REVIEW_RECORD.md) binds the complete 573-page visual review to exact PDF checksums; and [`PRINT_AND_SAFETY_REVIEW.md`](PRINT_AND_SAFETY_REVIEW.md) is the scoped publication release gate.

## Evidence used

- `../Presentation/ROB_v3.pdf` — 95-page design-history presentation.
- `../ORobotics/media/gallery-originals/` and its gallery metadata — construction photographs from 2019–2025.
- `../ROBArduino/` — Base, Torso, and Head firmware from the earlier three-Arduino architecture. The builder reports that only Base is presently used; see [`ARDUINO_FIRMWARE_HISTORY.md`](ARDUINO_FIRMWARE_HISTORY.md) for hashes, roles, protocols, and cautions.
- `../Cerebro/` — central macOS application and its current experimental branches.
- preserved `Cerebro v1` through `Cerebro v5` workshop folders — historical Mac software from the pre-Git serial-control seed through the 2018-2025 Git lineages and the fresh v5 repository migration. These are read-only local evidence, not public clone targets; see [`CEREBRO_ARCHIVE_HISTORY.md`](CEREBRO_ARCHIVE_HISTORY.md).
- `../ROBController/` — iPhone and Watch control paths.
- `../ROBControllerVision/` — Vision Pro controller and simulator.
- `../AmberHomeFolder/` — captured Ubuntu AMBER runtime evidence: separate left/right cores, launch configuration, CAN initialization, LCM schemas, URDFs, and historical install scripts. It is not a deployable image; credentials, histories, logs, caches, virtual environments, and machine identifiers are excluded from publication instructions.
- `../Amber URDF/amber_b1.urdf` — independent seven-joint AMBER B1 robot description used to cross-check geometry and model limits.
- `../Cerebro/Amber-PythonAPI/` — V1 examples and the V2 packed-UDP client used to document the observed network protocol.
- `../M2M1-RPLIDAR-iOS-MacOS-Catalyst-/` — lidar telemetry implementation and fixtures.

The exact inspection snapshot is recorded in [`SOURCE_SNAPSHOT.md`](SOURCE_SNAPSHOT.md). Restricted vendor PDFs were not reproduced or paraphrased for publication; only visible component identity is mentioned, with a request for authorized public documentation.

Readers can move from every book lesson to the implementation through [`OPEN-SOURCE-CODE-MAP.md`](OPEN-SOURCE-CODE-MAP.md). Each volume now prints the workspace-root convention and “SOURCE TRAIL — ANALYZING NOW” boxes at code-backed chapters. The map also distinguishes explicitly licensed open source, locally readable source without a discovered license grant, captured configuration, and binary-only AMBER components.

[`IMAGE_USAGE_POLICY.md`](IMAGE_USAGE_POLICY.md) gives every numbered volume its own visual territory and documents the single intentional cross-volume photograph. `tools/audit_image_reuse.sh` enforces that allowlist during validation and reports the complete field manual's deliberate evidence-photo overlap separately. [`publication/ASSET_REVIEW_RECORD.md`](publication/ASSET_REVIEW_RECORD.md) names the full-resolution visual and privacy review for all 77 current image assets; its SHA-256 manifest prevents a changed or newly added image from silently inheriting that review.

## Project map

```text
ROB-Books/
├── source/                 editable XeLaTeX manuscripts, advanced-volume Markdown, and shared style
├── assets/photos/          selected, resized, metadata-stripped build photos
├── assets/slides/          selected presentation-page images
├── assets/generated/       original illustrative artwork, not engineering evidence
├── tools/                  asset, build, validation, preview, and learning tools
├── output/pdf/             the ten printable PDF layout proofs
├── output/previews/        contact sheets for quick visual review
├── output/posters/         three 36×60-inch campaign PDFs
├── output/apple-books/     store covers and ten validated reflowable EPUB 3 editions
├── publication/            machine-readable store catalog and planned prices
└── tmp/                    generated build files and excluded private-review images
```

## Learning campaign and publication preparation

Three finished-size 36×60-inch campaign posters live in [`output/posters/`](output/posters/). Install `requirements-posters.txt`, rebuild them with `python3 tools/build_campaign_posters.py`, and verify finished geometry plus the rendered QR destinations with `python3 tools/validate_campaign_posters.py`. Their QR codes point to stable learning, game, and book routes on orbitusrobotics.com.

[`APPLE_BOOKS_PUBLICATION_PLAN.md`](APPLE_BOOKS_PUBLICATION_PLAN.md) records planned Apple Books pricing, accessible EPUB requirements, metadata, and the account-side release sequence. [`PRINT_DISTRIBUTION_PLAN.md`](PRINT_DISTRIBUTION_PLAN.md) covers local proofs, Lulu, and IngramSpark. Both routes remain behind the existing editorial, safety, privacy, rights, and printer release gate.

Run `python3 tools/audit_publication_readiness.py` for the complete machine-detectable blocker ledger. Publisher answers are recorded in `publication/publisher-answers.json`; empty values are intentional until the author supplies them. `python3 tools/audit_publication_readiness.py --release` must remain failing until all author questions, scoped review gates, EPUBs, publisher answers, and final store records are resolved.

Build the ten EPUB editions with `python3 tools/build_accessible_epubs.py`. The build converts the print-specific LaTeX semantics without dropping chapter photographs, captions, callouts, diagrams, or included deep labs; it also assembles the complete manual's embedded advanced Markdown volumes. Every output must pass EPUBCheck and the structural accessibility/content audit.

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

`prepare_assets.sh` rebuilds a conservative publication allowlist and strips image metadata. It fails if either publishable asset directory contains any unlisted entry, without deleting that entry automatically. `validate_books.sh` checks PDF freshness against each manuscript, the shared style, and referenced assets; rejects retired image names from publishable sources and outputs; verifies the reviewed asset checksums, dimensions, color space, metadata, ledger coverage, and OCR privacy patterns; and checks page geometry, text extraction, and serious LaTeX warnings. Validation does not replace engineering, privacy, legal, color, or press-preflight review.

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
