# Change Atlas

This appendix is the factual spine of *Building R.O.B.* Dates, hashes, author
labels, and subjects come from Git. The thematic summaries condense the changed
files and commit messages. “Codex-accelerated era” is a narrative period, not a
Git authorship field.

## ROBController

| Date | Commit | Recorded author | Change |
|---|---:|---|---|
| 2022-04-09 | `4c3aaf9` | Orbitus | Rebased the controller around new AutoNet/ROBONet and removed experimental ML-model use; initial 65-file import. |
| 2023-09-24 | `e83bc93` | Orbitus | Custom iPhone UI, text command work, speech lifecycle work, and lidar polar view. |
| 2023-09-30 | `6ccb1f3` | Orbitus | Watch prototype, speech recognizer, volume experiments, TCP no-delay, constraints and animation cleanup. |
| 2025-08-05 | `4d3b9c1` | Orbitus | Target rename, yaw/pitch/roll display, RPLidar map views, UDP experiments, and shared schemes. |
| 2025-08-05 | `1db16a9` | RudyAramayo | README-only initial commit on another history line. |
| 2025-08-05 | `551cfd3` | Orbitus | Merged the histories. |
| 2025-08-05 | `41ac4be` | Orbitus | Reduced controller update speed to avoid inundating the Cerebro M1. |
| 2025-08-05 | `2ae5c6a` | RudyAramayo | README update. |
| 2025-08-30 | `3e69afc` | Orbitus | Propagated output-language selection. |
| 2025-09-10 | `b65c63b` | Orbitus | Added the operator “shut up” control and UI. |
| 2026-08-01 | `b01083e` | Rudy Aramayo | Large v2/Watch implementation: secure transport foundation, Watch relay/controller, action protocols, autonomy/operator UI, tests, and docs; about 5,345 insertions and 605 deletions. |
| 2026-08-01 | `c93380e` | Rudy Aramayo | README marker describing secure v2 transport and Watch companion as a breaking control-plane change. |
| 2026-08-02 | `65891f9` | Rudy Aramayo | Refined client connection/approval behavior and Objective-C++ controller integration. |
| 2026-08-10 | `eb57375` | Rudy Aramayo | Restored QUIC pairing when iOS Bonjour TXT metadata is unavailable; added hello-first handshake while preserving pinning and proof. |

## Cerebro

| Date | Commit | Recorded author | Change |
|---|---:|---|---|
| 2025-08-05 | `4c4f1d4` | Orbitus | Fresh v5 repository import containing the existing macOS robot stack. |
| 2025-08-05 | `0ca9d2e` | RudyAramayo | Created README. |
| 2025-08-05 | `a1bfde4` | RudyAramayo | Updated README. |
| 2025-08-05 | `01442e0` | Orbitus | Recorded Foundation Models availability problem on Tahoe beta 5. |
| 2025-08-05 | `2797cc4` | RudyAramayo | Colab-created artifact/change. |
| 2025-08-11 | `07d713b` | Orbitus | Gemini integration, speech fixes, component categorization, UTC flow, and OAK Pro webcam color feed. |
| 2025-08-11 | `6278bd9` | Orbitus | Merged remote main. |
| 2025-08-13 | `ec40848` | Orbitus | Dynamic AV device discovery and new head upper-neck-tilt servo. |
| 2025-08-14 | `4423cd4` | Orbitus | Updated upper-neck-tilt calibration values. |
| 2025-08-30 | `21753ff` | Orbitus | Repaired RPLidar path assumptions and wake-word/speech continuation. |
| 2025-08-30 | `0b2496a` | Orbitus | Restart-required checkpoint. |
| 2025-08-30 | `54fb96a` | Orbitus | Tested speech synthesizer and multilingual output-language flow. |
| 2025-09-07 | `21dbfe0` | Orbitus | Added Amber arm v1/v2 scripts and R11/L10 experiments plus speech stop control. |
| 2025-09-07 | `03a17be` | Orbitus | Removed command behavior that was unsafe when sent too rapidly. |
| 2025-09-09 | `ac643bd` | Orbitus | Added camera bind/toggle test controls. |
| 2025-09-10 | `a1678a4` | Orbitus | Corrected port behavior and explored packaging Python Amber dependencies. |
| 2025-09-10 | `98b9aa7` | Orbitus | Working arm suite and first chess-piece pickup experiment; identified pose-angle gap. |
| 2025-09-10 | `2dbcb4d` | Orbitus | Began automating Amber core, surfaced logs, and rebuilt UI for keyframes. |
| 2025-09-12 | `70b9c22` | Orbitus | Updated L10/R11 core functions and validated L10 position commands. |
| 2025-09-12 | `2d8a7c4` | Orbitus | Corrected L10 watch-position output. |
| 2025-09-12 | `1ed61d0` | Orbitus | Added tailed logs, repaired URDF/STL paths and position emission; documented drag-mode limitations. |
| 2025-09-15 | `69ff3dd` | Orbitus | Made Amber host IP adaptable and advanced 3D body-pose rendering. |
| 2025-09-16 | `5a186a3` | Orbitus | Composited segmentation, SceneKit 3D pose, and skeleton rendering. |
| 2025-09-16 | `dcf9442` | Orbitus | Checkpointed the correction that avoids rebuilding pose UI every camera frame. |
| 2025-09-16 | `2479720` | Orbitus | Added whole-body camera overlay. |
| 2025-09-18 | `b748d12` | Orbitus | Working dual-arm animations and sequence direction; recorded real connector damage. |
| 2025-09-18 | `4804e7f` | Orbitus | End-of-session checkpoint. |
| 2025-09-19 | `5e21c0a` | Orbitus | Expanded keyframe model and UI toward dynamic battle sequences. |
| 2025-09-24 | `dee4b6b` | Orbitus | Wordiness and speech-stop controls, camera/head tracking, and audio input repairs. |
| 2025-09-25 | `237131f` | Orbitus | Speech restart and greeting acknowledgement. |
| 2026-08-01 | `c4b5946` | Rudy Aramayo | Major coordinated release: secure control v2, Gemini Robotics Live, autonomy, supervised DepthAI/Python, Vision Pro video, safer subprocesses, protocols, tests, and docs; about 16,478 insertions and 1,646 deletions. |
| 2026-08-02 | `fe1ae72` | Rudy Aramayo | Canonical Keychain certificate/re-pairing work plus robustness refinements across AI, dependency, action, and control components; about 2,015 insertions. |
| 2026-08-02 | `63c676c` | Rudy Aramayo | Fixed rapid camera-toggle crash and requested final robot-Mac hardware confirmation. |
| 2026-08-03 | `46ca05c` | Rudy Aramayo | Safe local improvisation, llama.cpp provider, stage-show coordinator/UI, diagnostics, schemas, fixtures, and extensive docs; about 7,069 insertions. |
| 2026-08-10 | `d45f9c9` | Rudy Aramayo | Prevented QUIC pairing deadlock by waiting for and validating a padded client hello before issuing the challenge. |

## Reading the author labels correctly

All observed author labels use `orbitus@orbitusrobotics.com`. The most economical
explanation is the one supplied by the project owner: one person used multiple
computers with different Git `user.name` values. The history contains no
`Co-authored-by: Codex` or equivalent attribution. The change in engineering
style supports discussion of AI acceleration, but it cannot identify which
individual lines were generated, rewritten, reviewed, or merely inspired by AI.

