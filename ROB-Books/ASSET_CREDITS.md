# Building R.O.B. — image provenance and publication notes

## Real build photographs

The selected photographs come from the builder's local `ORobotics/media/gallery-originals/` archive (2019–2025) and the 2026 `BlueGreen Lightsaber Pics ROB/` portrait set. [`tools/prepare_assets.sh`](tools/prepare_assets.sh) is the authoritative mapping from original filenames to descriptive book filenames. It applies orientation, limits the longest edge to 3200 pixels, converts to sRGB JPEG, and strips metadata. A successful run requires `assets/photos/` and `assets/slides/` to match explicit allowlists exactly; the script reports unlisted entries for deliberate review and never deletes them automatically.

The photographs document different ROB revisions. Captions identify what can be seen and avoid treating a photograph as proof of hidden wiring, ratings, dimensions, current installation, or safe practice.

### 2026 youth-volume covers

The four youth books use distinct photographs from the new blue-and-green
lightsaber portrait session. They preserve the real robot and make the series
feel connected while giving every volume its own view:

- Volume 1: `IMG_6296.HEIC` → `2026-rob-lightsabers-front.jpg`
- Volume 2: `IMG_6318.HEIC` → `2026-rob-lightsabers-portrait.jpg`
- Volume 3: `IMG_6303.HEIC` → `2026-rob-lightsabers-side.jpg`
- Volume 4: `IMG_6325.HEIC` → `2026-rob-lightsabers-overhead.jpg`

These are metadata-stripped photographic conversions, not generated or
composited images. The complete advanced field manual retains its technical
2025 cover so the youth series receives the more playful visual treatment.

Selected pages from the builder's 95-page `Presentation/ROB_v3.pdf` are rendered into `assets/slides/`. They remain historical design evidence and must be captioned as proposals or dated concepts when that is what the slide shows.

## Excluded from publication

The following derivatives are held under `tmp/private-review-do-not-publish/` and are intentionally rejected by the preparation script because visual review found sensitive data, identifiable bystanders/minors without confirmed releases, legibility/quality problems, or ambiguous publication value:

- `2022-coding-workstation.jpg`
- `2024-ethernet-controller-board.jpg`
- `2024-maker-faire-demonstration.jpg`
- `2025-code-logs-and-status.jpg`
- `2025-rob-and-chessboard.jpg`
- `2025-rob-camera-head-front.jpg`
- `2025-rob-full-front.jpg`
- `2025-vision-software-monitor.jpg`

Do not copy these files into a print package. If the builder wants their subject matter, make a new tightly framed photograph or screenshot with releases and deliberate redaction, then review the full-resolution result rather than trying to conceal private details with a caption.

## Original generated illustrations

Six bitmap illustrations were generated with OpenAI's image-generation tooling. The first two were created on 2026-08-02; four educational plates were created on 2026-08-10. They are captioned as conceptual storytelling, not engineering evidence.

### `assets/generated/rob-used-future-frontispiece.png`

Final prompt:

> Use case: illustration-story. Asset type: portrait cover and frontispiece for a printed robotics book series. Transform the reference photograph into a richly detailed, optimistic illustrated portrait of the same real homemade robot ROB, standing ready in an original retro space-opera maker workshop. Preserve ROB's distinctive rectangular weathered metal torso, twin circular blue-ring speaker eyes, central depth camera, tall head/neck structure, exposed wiring, tracked base, and front linear actuator. Use an original well-lit spacecraft maintenance bay blended with a friendly community makerspace; subtle tools, workbench, and stars through a small window; no recognizable franchise locations or props. Premium children's science picture-book illustration with realistic mechanical detail, painterly gouache and crisp technical linework, vertical 2:3 full-body hero view, warm amber work lights, cool cyan accents, charcoal metal, warm cream, restrained red safety accents, scuffed metal, braided cables, rubber treads, and subtle paper grain. No people, text, logos, watermark, trademarked symbols, characters, helmets, spacecraft, or exact franchise visual assets. Avoid weapons, combat, horror, a glossy generic humanoid robot, duplicate limbs, extra eyes, and illegible text.

### `assets/generated/rob-software-control-room.png`

Final prompt:

> Use case: illustration-story. Asset type: landscape chapter-opener illustration for a printed robotics education book. Create a richly detailed original illustration of the same real homemade ROB, with Mac-computer software and control architecture represented through abstract luminous pathways, packet shapes, camera-depth rays, lidar arcs, and simple geometric state nodes around the robot. Preserve the rectangular weathered metal torso, twin circular blue-ring speaker eyes, central camera, spherical camera head, exposed wiring, articulated arms, tracked base, and front linear actuator. Set it in a friendly original retro space-workshop control room with a clean unbranded computer silhouette; screens contain only abstract blocks and diagrams, never readable text, code, credentials, addresses, usernames, or logos. Premium children's science picture-book illustration with realistic mechanical detail, painterly gouache and crisp technical linework, horizontal 4:3 composition, warm amber light, cool cyan/violet data accents, and subtle paper grain. No people, text, logos, watermark, trademarked characters, symbols, spacecraft, props, or exact franchise visual assets. Avoid weapons, combat, horror, duplicate limbs, extra eyes, legible UI, terminal text, network addresses, and brand marks.

The images are reinterpretations for atmosphere. Real photographs, measured drawings, schematics, code, and test evidence control every engineering claim.

### 2026-08-10 educational plates

- `rob-systems-feedback-lab.png` — ROB as connected structure, energy, sensing, computing, motion, and feedback systems.
- `rob-circuits-signals-lab.png` — conceptual low-voltage energy loop, digital/analog/PWM traces, framed messages, and watchdog behavior.
- `rob-motion-mechanics-lab.png` — differential drive, gear tradeoffs, lever arms, ramp forces, and a progressive evidence cycle.
- `rob-safe-autonomy-lab.png` — perception, planning, authority, separate data paths, freshness, watchdogs, and physical stop layers.

All four use a scientific-educational prompt derived from the established visual direction and reference ROB's real appearance. Shared constraints required painterly gouache with crisp technical linework, a warm cream retro workshop, charcoal/amber/cyan/violet/green safety palette, no brands or franchise elements, no credentials or as-built wiring claims, and explicit symbolic rather than evidentiary pathways. The Mission Control plate received a targeted edit to remove a generated person and readable labels, replacing them with an unoccupied console and nonverbal icons. Built-in image generation was used; final project assets are the files listed above.

## Visual identity

The shared style uses the local system fonts Avenir Next, Avenir Next Condensed, Futura, and Menlo with an original charcoal/cream/amber/cyan/red technical palette. The intended mood is a weathered, optimistic retro-space field manual. It does not reproduce protected franchise logos, characters, exact title treatments, props, or story elements.

## Final release tasks

- Confirm the builder/photographer credit line and copyright year.
- Obtain releases for any future identifiable person, especially a minor.
- Obtain written permission for any third-party product photo, logo, diagram, or restricted document.
- Visually inspect every image at full resolution after any new crop or replacement.
- Ask the printer to check effective resolution, crop, paper response, black detail, and color proof.
