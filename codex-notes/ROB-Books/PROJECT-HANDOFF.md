# Building R.O.B. project handoff

Recorded: **2026-08-03**

Project: /Users/raramayo/dev/ROB-Books

## Outcome at this checkpoint

The first Maker Faire edition contains four youth volumes, one advanced AI and
software volume, and one advanced field manual. All six use US Letter pages
and share one XeLaTeX design system.

| Deliverable | Audience | Source | PDF pages |
|---|---|---|---:|
| Volume 1 — Meet ROB | Ages 8–12 | source/volume-1-meet-rob.tex | 30 |
| Volume 2 — Circuits & Signals | Ages 10–14 | source/volume-2-circuits-and-signals.tex | 29 |
| Volume 3 — Motion Workshop | Ages 10–15 | source/volume-3-motion-workshop.tex | 32 |
| Volume 4 — Mission Control | Ages 12–16 | source/volume-4-mission-control.tex | 30 |
| Volume 5 — AI, Robotics, and Codex | Advanced makers and software builders | source/volume-5-ai-robotics-with-codex.md plus .tex wrapper | 30 |
| Complete Builder's Field Manual | Advanced makers and mentors | source/complete-builders-field-manual.tex | 67 |

Total for these six books: **218 pages**.

The editable source, output PDFs, rendered pages, contact sheets, selected
assets, provenance, release gate, and helper scripts all live under ROB-Books.
The six PDF files are in output/pdf.

## Project structure

- source/robbook.sty — shared page geometry, typography, colors, boxes,
  diagrams, cover, and chapter-photo helpers.
- source/*.tex and source/volume-5-ai-robotics-with-codex.md — the six manuscripts.
- assets/photos/ — 42 selected, resized, sRGB, metadata-stripped photographs.
- assets/slides/ — eight selected rendered presentation pages.
- assets/generated/ — two original illustrations made with gpt-image-2.
- tools/prepare_assets.sh — exact publication allowlists and metadata removal.
- tools/build_books.sh — builds all six XeLaTeX PDFs, converting the Volume 5 Markdown through its XeLaTeX wrapper.
- tools/validate_books.sh — freshness, retired-image, PDF, LaTeX, text, and
  metadata checks.
- tools/render_previews.sh — renders every PDF page and creates contact sheets.
- tools/mac_serial_frame_lab.py — offline 42-character frame teaching tool; it
  never opens a serial device.
- tmp/private-review-do-not-publish/ — quarantined image derivatives.

## Evidence inspected

The edition synthesized:

- Presentation/ROB_v3.pdf, a 95-page design-history presentation.
- ORobotics/media/gallery-originals and its metadata.
- ROBOT Build/ROBOT_CEREBELLULAR_BASE_APP.ino.
- Cerebro, ROBController, ROBControllerVision, and the RPLidar project.

Exact commits and hashes are in
[SOURCE_SNAPSHOT.md](../../ROB-Books/SOURCE_SNAPSHOT.md). That snapshot is dated
2026-08-02. Relevant Cerebro work and ORobotics site work were uncommitted at
inspection, so a future agent must select intentional publication revisions
rather than treating one commit alone as the complete state.

## Evidence language to preserve

The books deliberately distinguish:

- current versus historical hardware;
- implemented versus proposed software;
- schema-declared versus executable AI actions;
- commanded versus physically measured behavior;
- software freshness/watchdog behavior versus an independent physical stop;
- storytelling illustration versus engineering evidence.

Never close a placeholder by inference. Ask the builder for measurements,
drawings, photographs, test records, or a first-person account. When revisions
differ, label both by date.

## Builder-input placeholders

There are **26** source placeholders:

- Volume 1: 1
- Volume 2: 3
- Volume 3: 6
- Volume 4: 2
- Advanced manual: 14

The complete question set is in
[EDITORIAL_GAPS.md](../../ROB-Books/EDITORIAL_GAPS.md). Major missing evidence
includes the project origin story, current dimensions and mass, center of mass,
dimensioned drawings, final materials and fasteners, fabrication sequence and
machine parameters, as-built power schematic, battery and protection details,
current bill of materials, calibration, current software release identifiers,
measured stopping/thermal/current results, maintenance limits, photo releases,
credits, and publication decisions.

## Hardware and firmware facts and cautions

The inspected historical Arduino sketch assigns:

- right tread direction/PWM/brake to D2/D3/D25;
- left tread direction/PWM/brake to D4/D5/D27;
- flipper direction/PWM/brake to D6/D7/D29;
- linear-actuator SoftwareSerial RX/TX to D22/D23 at 19,200 baud, with RX
  declared but not used by the sketch;
- six IR channels across A5 through A0;
- USB serial at 250,000 baud.

The command is a 42-character ASCII frame: a leading tilde plus seven signed
five-character fields separated by commas. The books document it as historical,
not safe live-control guidance.

Preserve these caveats:

- Exact Arduino-compatible board is unresolved; historical logs call it a Mega.
- Parser validation is incomplete and can consume or mis-handle malformed
  input.
- Any received byte refreshes the loop-count deadman before complete validation.
- Timeout zeros speed fields while brake-zero is interpreted as released;
  actual coast/hold behavior is unmeasured.
- PWM is active-low and values are not fully bounded.
- D6 can boot LOW, the maximum-command level under the active-low mapping,
  relying on an unverified flipper-brake path.
- Encoder proposals conflict at D18/D19, and a D20 proposal conflicts with Mega
  I2C SDA.
- Actuator values are nominally bounded at plus or minus 3200; plus or minus
  3201 clear safe start before substitution. The sketch exposes no verified
  position, end stop, or motion timeout.
- Only front/rear IR pairs participate in warning telemetry. Movement inhibit
  is disabled, side sensors are unused, and grass/floor reflection behavior is
  documented. IR is not safety-rated.
- Battery topology, branch protection, brake electronics, E-stop behavior, and
  physical stopping performance remain unverified.

Do not rewrite the historical sketch as a certified controller without a
separate reviewed implementation and restrained hardware test program.

## Software architecture cautions

- Cerebro on the Mac coordinates body subsystems; controller clients do not all
  represent motion intent identically.
- ROBControl security/pairing, application-payload validation, freshness, and
  physical command bounds are separate layers.
- A certificate fingerprint is public identity material, not a secret.
- The current iPhone controller's Always-location/live-coordinate behavior is a
  documented privacy debt that must be rechecked against the publication
  release.
- Current lidar use is a filtered near-field front/back subset, not proof of
  complete 360-degree obstacle protection. Stale lidar enters a waiting state
  without proving motion stopped.
- Gemini integration and action-tool exposure have independent runtime controls.
- At the inspected state, stop_motion had only a partial local executor;
  look_at, play_gesture, and navigate_relative were schema-only, request_pick
  was unavailable, and the approval console did not actuate ROB.
- Local Apple speech and optional external Gemini media are separate privacy
  paths.

Reinspect live source before retaining any of these statements in a later
edition.

## Images, privacy, and rights

The preparation script enforces exact allowlists. Eight derivatives remain
quarantined because of private console/network data, account UI, a shipping
label, identifiable people or minors without confirmed releases, or
quality/ambiguity:

- 2022-coding-workstation.jpg
- 2024-ethernet-controller-board.jpg
- 2024-maker-faire-demonstration.jpg
- 2025-code-logs-and-status.jpg
- 2025-rob-and-chessboard.jpg
- 2025-rob-camera-head-front.jpg
- 2025-rob-full-front.jpg
- 2025-vision-software-monitor.jpg

Do not copy them into a public asset or print package. Make a new deliberate
photograph or screenshot with permission and redaction if the subject is still
needed.

The two generated illustrations and their exact prompts are documented in
[ASSET_CREDITS.md](../../ROB-Books/ASSET_CREDITS.md). They are atmospheric
storytelling images, not proof of geometry, wiring, components, or safe
practice.

The design uses an original weathered, optimistic retro-space technical-manual
language with Avenir Next, Avenir Next Condensed, Futura, and Menlo. Preserve
the absence of protected franchise logos, exact typography, characters, props,
or layouts.

## Validation baseline

The final 2026-08-03 pass completed after correcting an orphaned 2025 timeline
heading in Volume 1. Results:

- all five PDFs in the original 2026-08-03 collection built successfully;
- 168 PDF pages and 168 rendered-page images matched;
- every PDF is 612 by 792 points, US Letter, unencrypted;
- all listed fonts are embedded and subset;
- no serious LaTeX error, undefined-reference, missing-character, or overfull
  box was accepted by the validation script;
- prepared photographs contained no GPS or camera make/model metadata;
- retired image basenames were absent from publishable sources and outputs;
- every contact sheet and affected page received visual inspection;
- the offline serial-frame lab built and decoded valid 42-character frames and
  rejected malformed input.

From /Users/raramayo/dev/ROB-Books:

~~~sh
bash tools/prepare_assets.sh
bash tools/build_books.sh
bash tools/render_previews.sh
bash tools/validate_books.sh
~~~

Run prepare_assets only when regenerating or changing the publication image
set. It intentionally fails rather than deleting an unexpected file.

## Remaining work in priority order

1. Interview the builder and fill the editorial gaps with dated evidence.
2. Select and record intentional software and hardware publication revisions.
3. Add as-built drawings, wiring schematic, power tree, connector/pin table,
   bill of materials, fabrication records, calibration, and measured tests.
4. Obtain photo ownership/release decisions and approved public component
   documentation.
5. Complete electrical, mechanical, youth-safety, firmware/software, privacy,
   rights, and copyediting review.
6. Perform printer-specific preflight and create separate bleed, cover/spine,
   CMYK, or imposed exports only if the selected printer requires them.
7. Review a physical bound proof under Maker Faire lighting before approving a
   production run.

The accountable checklist is
[PRINT_AND_SAFETY_REVIEW.md](../../ROB-Books/PRINT_AND_SAFETY_REVIEW.md).

## Change and handoff rule

ROB-Books is not currently a Git repository. Do not assume rollback or history
exists. Before a large edit, preserve the current source and document exactly
what changed. At the end of a future task, append a dated section here or add a
new dated topical handoff in this directory and update README.md. Do not erase
earlier evidence or validation history.

## 2026-08-10 deeper-learning expansion

Four new youth deep-dive inserts were added before each volume's field-word review. They teach systems boundaries and feedback, uncertainty and fair tests, waveform reasoning and parser state machines, forces and operating envelopes, tolerances and service design, identity/role/freshness gates, latency budgets, and bounded-autonomy state machines. Activities remain paper, simulation, or explicitly current-limited classroom work.

The adult manual gained chapters on spiral curriculum and facilitation, end-to-end secure-control commissioning, the 2026-08-10 Bonjour/QUIC pairing lessons, whole stop-chain measurement, release artifacts, and a staged oral-history workflow for the builder's future dictation. No historical placeholder was filled from inference.

Four project-local scientific-educational illustrations were generated with the built-in image tool and recorded in `ASSET_CREDITS.md`. They are conceptual art rather than as-built evidence. The final Mission Control plate was edited to remove a person and readable labels.

The ORobotics Hugo project gained `/robot-lab/`, a static four-mission game sharing the books' feedback, PWM, differential-drive, and command-freshness lessons. It has no backend, account, analytics, robot connection, or persistent learner data.

The Homebrew toolchain was restored on 2026-08-10 (`node@22`, Hugo, Poppler, TeX Live, ImageMagick, and Exiv2). The original five-book edition was rebuilt and every PDF passed `tools/validate_books.sh`; all contact sheets were regenerated. The ORobotics production build and its gallery and subpath validators also passed through `npm test`.

Later on 2026-08-10, Volume 2 gained a four-page, mentor-led Maker Faire lab that opens a sacrificial, unplugged USB-A cable and uses the verified 5 V and GND conductors to power an approved low-current toy. The lesson includes a new generated cutaway illustration, conductor-role table, source/load matching, a bounded procedure, measurement prompts, and explicit controls for tools, shorts, polarity, startup current, USB-C, and installed batteries. The rebuilt Volume 2 is 29 pages.

Volume 5 was then integrated as a full 30-page member of the series. It covers the source-based evolution of ROBController and Cerebro, AI development systems, communicating goals/context/output/boundaries, context engineering, evals, verification, deterministic robotics authority, a 30-day developer practice, and an AI change-contract worksheet. The complete six-book collection is 218 US-Letter pages.
