# Building R.O.B. — print, privacy, and safety release gate

Do not distribute the books as final construction instructions until every required item below has an accountable reviewer, evidence, and date. The current PDFs are editorial/layout proofs.

## Engineering release

- [ ] Every `ROBPlaceholder` is answered, deliberately retained as an open question, or removed with a recorded reason.
- [ ] A qualified electrical reviewer approves the as-built schematic, battery/BMS/charger system, branch protection, conductor/connector ratings, grounding/bonding, disconnect, E-stop, and fault behavior.
- [ ] A qualified mechanical reviewer approves materials, joints, fasteners/torques, welds, guards, lifting, center of mass, tip stability, motion limits, stopping distance, and public barrier.
- [ ] Arduino polarity, brake truth table, boot outputs, parser bounds, watchdog, actuator reset, end stops, and every loss-of-communication state are measured on a de-energized or safely restrained test setup first.
- [ ] Software roles, controller authority, timing, pairing/revocation, version identifiers, sensor-stale behavior, privacy settings, and AI action status match the tagged release used for the show.
- [ ] Failure-injection, emergency-stop, stopping-time/distance, thermal/current, slope, grass, flipper, actuator, arm, and recovery tests have written results and sign-off.
- [ ] The operator, spotter, safety lead, charging lead, and show-state/abort procedure are named for the event.

## Youth and workshop safety review

- [ ] An educator and the responsible adult review age ranges, vocabulary, activities, supervision language, and accessibility.
- [ ] Youth activities remain paper, simulation, or appropriately current-limited low-voltage kits; no activity silently implies access to ROB's traction batteries, mains/inverter circuits, motor wiring, actuators, machine tools, or live drivetrain.
- [ ] Fabrication photographs do not imply that visible practice is complete safety guidance. Captions distinguish what is visible from required but undocumented workholding, guarding, and PPE.
- [ ] The full-size robot is immobilized and made electrically safe before close public inspection; boundaries cover treads, arms, flippers, pinch points, cables, and camera/microphone participation.

## Privacy, permissions, and rights

- [ ] Photograph ownership, model releases, venue terms, minor/guardian releases, and third-party product-image permissions are documented.
- [ ] Every prepared photograph is visually checked at full resolution for faces, shipping labels, addresses, account UI, credentials, network identifiers, location data, reflections, screens, and legible private notes.
- [ ] Camera metadata remains stripped, and no excluded/private-review image appears in source, assets, preview sheets, PDFs, print packages, or promotion.
- [ ] Cloud audio/video behavior, local speech behavior, location collection, retention, signage, consent, visible indicators, and immediate disable paths are described accurately.
- [ ] Restricted/confidential vendor pages and specifications are omitted unless written publication permission or an authorized public source is obtained.
- [ ] A suitable trademark/legal reviewer confirms title, attribution, disclaimers, and original retro-space visual treatment for the intended distribution.

## Editorial and technical preflight

- [ ] All claims are checked against the dated source snapshot; current, historical, planned, experimental, unavailable, and commanded-but-unmeasured states are not blended.
- [ ] Measurements include units, method, revision, and uncertainty where relevant.
- [ ] Code samples are re-run in a clean environment and remain safe/offline unless explicitly marked for a restrained test rig.
- [ ] Table of contents, page numbers, cross-references, captions, credits, placeholders, spelling, and accessibility language receive a human copyedit.
- [ ] Every PDF passes `bash tools/validate_books.sh` and every rendered page receives a visual review at readable zoom—not only a contact-sheet glance.

## Printer proof

- [ ] Printer confirms final trim size, binding, safe margins/gutter, desired bleed, raster resolution, color space/profile, total ink limits, transparency handling, embedded fonts, cover/spine specification, and paper stock.
- [ ] The current PDFs use US Letter pages and RGB imagery. If the printer requires bleed, crop marks, CMYK conversion, imposed spreads, a separate cover, or a spine, generate a printer-specific export instead of scaling these files at the press.
- [ ] Full-page chapter photographs and the darkest pages are checked in a physical proof for crop, shadow detail, skin/metal color, banding, and text contrast.
- [ ] Generated illustrations are not enlarged beyond acceptable effective resolution and remain captioned as illustrations.
- [ ] A complete bound proof is reviewed under the lighting expected at Maker Faire before the production run is approved.

## Release record

| Item | Reviewer | Evidence/revision | Date | Result |
|---|---|---|---|---|
| Electrical |  |  |  |  |
| Mechanical |  |  |  |  |
| Firmware/software |  |  |  |  |
| Youth safety |  |  |  |  |
| Privacy/releases |  |  |  |  |
| Trademark/legal |  |  |  |  |
| Print proof |  |  |  |  |
| Final publisher approval |  |  |  |  |
