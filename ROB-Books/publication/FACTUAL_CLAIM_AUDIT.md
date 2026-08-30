# Building R.O.B. — factual claim and copyedit audit

**Audit date:** 2026-08-29

**Dated source coordinate:** Cerebro `e76d515a56e8018c96d07efb251470a40f9de174`, with the other repository and artifact identifiers in `SOURCE_SNAPSHOT.md`

**SOFTWARE, PRIVACY, AND SAFETY-LANGUAGE CLAIM AUDIT: COMPLETE AGAINST THE DATED SNAPSHOT**

**CODEX-ASSISTED PUBLISHER COPYEDIT: COMPLETE AGAINST THE DATED SNAPSHOT AND AUTHOR ANSWERS**

This record covers the high-risk factual and language pass for the ten-book historical edition. It does not convert source inspection into proof of deployed configuration, physical performance, legal clearance, professional engineering approval, accessibility approval, or final publisher acceptance. Statements about current behavior mean behavior supported by the dated source coordinate, not by later working-tree changes.

## Scope and method

- Read the youth volumes, advanced manuscripts, story source, complete manual, shared front matter, captions, catalog metadata, and release records for revision labels, attribution, unresolved instructions, cross-volume consistency, and claims that could be mistaken for construction or operational approval.
- Compared software, camera, microphone, identity, Messages, recording, cloud, retention, authorization, transport, and stop-language claims with committed source and operational notes at the dated Cerebro commit.
- Compared project-history statements with the archive identifiers in `SOURCE_SNAPSHOT.md`, the author responses in `AUTHOR_INTERVIEW_RECORD.md`, and the public-event records cited there.
- Rebuilt manuscript cross-references are required to show no LaTeX errors, undefined references, or missing characters. EPUBCheck and the structural EPUB audit remain separate machine checks; the human device review remains open.
- Ran CSpell 10.1.1 over the 21 Markdown and TeX manuscript files in US English using its likely-typo report. The only two reports were the split protocol term `STAP-A` in Volumes 7 and 8; both are intentional H.264/RTP terminology. This diagnostic supports, but does not replace, the final publisher reading.
- Searched for unresolved editorial instructions, duplicate words, incorrect ROB-acronym claims, private paths, obsolete controller-timeout wording, product-name inconsistencies, and language that could imply certification. Source TODOs and unknowns are retained only when the prose explicitly identifies historical code debt or future measured-edition work.

## Corrections from this pass

1. Volumes 5 and 8 previously paraphrased controller expiry as a fixed count of three missed 5 Hz updates. At the dated commit, `ROBSerialBox.m` sets `kControllerSnapshotFreshnessSeconds` to 0.6 and compares that limit with local `receivedAtUptime`. The implementation is time based. The books now say 0.6 seconds, note that this is only roughly three expected publication intervals, and preserve the one-neutral/braked-frame-then-silence behavior.
2. A Volume 4 caption still instructed the editor to confirm the current head configuration. It now distinguishes the historical OAK-D Lite slide concept from the builder's current account of the Insta360 Pro II and autofocus OAK-D Pro head cameras.
3. Rights records previously asked about venue-photo terms even though the closed 77-file allowlist contains no event, venue, or bystander photograph. The question now concerns photographer exceptions and product/component photographs only. Venue-photo permission is recorded as not applicable to this edition.

## Dated high-risk claim matrix

| Topic | Dated evidence inspected | Publication result |
|---|---|---|
| Controller freshness and Base stop | `Cerebro/ROBSerialBox.m`: 0.6-second local receipt-age gate, fresh/stale transition, `stopBaseMotionAndDropHeartbeat` | Corrected to a time-based gate. One neutral/braked frame and subsequent USB silence are source behavior; actual Arduino elapsed timeout and physical stopping remain unmeasured. |
| Face enrollment and retention | `Cerebro/ROBFaceIdentityGallery.swift`, `ROBFaceIdentityWindowController.swift`, `ROBFaceRecognitionService.swift`, face-threshold note | Enrollment requires explicit consent; local profiles and samples are encrypted; deletion controls exist. Recognition and an `administrator` label never grant motion, pairing, approval, secrets, or command authority. Biometric performance and public-use policy remain unapproved. |
| Messages permissions and isolation | `Cerebro/ROBMessagesBridge.swift`, `ROBMessagesAIResponder.swift`, transcript store, `docs/messages-ai-bridge.md`, fixtures | Disabled by default; local Messages reading requires Full Disk Access and sending requires Automation permission. The AI profile has no live camera, room microphone, arbitrary file, controller, actuator, or autonomy authority. Allowlists, one-to-one isolation, bounds, and cloud disclosures are described as dated implementation behavior, not a general privacy certification. |
| Messages images, transcripts, and administrator commands | Messages bridge/responder/store and administrator-command policy | Image upload to Gemini is separately configured; local paths receive bounded normalized input as described. Optional encrypted transcript memory defaults off and can send selected text excerpts to Gemini when used. Shutdown/reboot require exact same-chat `YES` confirmation within 90 seconds; this remains privileged Mac maintenance, not robot-motion authorization. |
| Recording and training data | `docs/recording-and-training.md`, recording coordinator/window, dataset paths | Recording begins through explicit operator controls, exposes a visible state, and leaves interrupted sessions recoverable. Autonomous commands cannot label their own traversability images as truth. Consent, retention, capacity, and export decisions remain operator/publisher responsibilities. |
| Local and cloud models | `ROBMLXRuntime.swift`, local-provider and stage-observation code, `ROBAI.swift`, Gemini protocol and notes | MLX/llama.cpp paths are local; Gemini is optional remote processing. Model observations and proposals are bounded context, not direct serial, servo, tread, shell, or AMBER commands. The books disclose cloud paths and preserve deterministic validation and operator authority. |
| Camera and H.264 transport | `ROBVideoServer.swift`, `ROBVideoProtocol.swift`, `ROBCameraH264Encoder.swift`, `docs/vision-pro-video.md` | Three independent `front`, `belly`, and `insta360` feeds, their dated caps, separate `robvideo/1` QUIC/TLS service, bounded queues, control-session binding, and live-view/no-server-retention design match the dated source. Deployment identity, network conditions, and client behavior still require testing. |
| Location and sensitive operational data | controller snapshot definitions and current location-request path at the dated source | The complete manual correctly calls active latitude/longitude carriage and Always-location authorization current privacy debt. It directs removal, minimization, purpose/consent documentation, and screenshot redaction rather than normalizing the behavior. |
| Emergency and physical authority language | serial stop path, autonomy coordinator, Gemini action path, manuscript safety boxes | A software stop is not described as an independent certified E-stop. Base neutral/heartbeat behavior is source evidence; AMBER arm hold and physical stop results remain explicitly unverified. Face identity, Messages, VLM labels, and cloud confidence cannot open physical authority. |

## Editorial consistency result

- ROB is consistently explained as a friendly name derived from “robot,” not an acronym.
- Johnny 5 is limited to personal historical inspiration; no franchise art, logo, copied design, endorsement, or affiliation claim appears in the selected edition.
- CakeChat is described as an early pre-ChatGPT dialogue experiment visible in the archive, not as an ancestor of ChatGPT.
- The 2025 Cerebro v5 Git root is labeled as a fresh-repository migration around an existing application, not the beginning of Cerebro.
- Supplier names identify component sources and do not imply coauthorship, sponsorship, endorsement, integration responsibility, or professional review.
- Hardware values based on recollection or visible labels remain labeled as recollection, provisional evidence, or future measurement work. Controlled vendor drawings are not used as public construction sources.
- The historical edition repeatedly states that it lacks as-built CAD, a traced current schematic, measured qualification, and outside engineering approval. It does not invite readers to infer dimensions or safe wiring from photographs.
- The 2019, 2023, 2024, and 2025 Maker Faire history is supported in the author record. The September 2026 event is future as of this audit and is not described as a completed appearance.

## Author-answer reconciliation and remaining approvals

Q01 and Q03–Q05 in `AUTHOR_INTERVIEW_RECORD.md` were answered on August 29, 2026. The manuscripts and metadata now identify College Station, Texas, and approximately 2016 for the treaded prototype; credit Rodolfo Aramayo as the photographer of every selected real image; identify OrbitusRobotics LLC as publisher, imprint, and worldwide copyright owner; and record that ROB, the pictured components, and the selected product photographs belong to the author. All ten PDFs and EPUBs were rebuilt, the changed PDF pages were visually reviewed, and the EPUBs were revalidated after reconciliation.

Rodolfo Aramayo's final publisher acceptance of the remaining trademark, privacy, safety-language, and legal risk is still open. Apple Books device review, account-side submission evidence, printer-specific file review, and physical proofs remain separate release gates.
