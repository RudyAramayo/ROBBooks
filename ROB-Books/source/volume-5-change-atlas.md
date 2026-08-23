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
| 2026-08-14 | `25fd718` | Rudy Aramayo | Added early singleton locking, wake health refresh, a crash-limited LaunchAgent supervisor, debug/production handoff, and Keychain-backed Gemini credentials. |
| 2026-08-14 | `5c7e5f0`–`e1be0bf` | Rudy Aramayo | Added supervised headless Insta360 Pro II control/preview/perception, MLX VLM preparation, and selectable Vision/Core ML detectors. |
| 2026-08-14 | `283340f`–`7491688` | Rudy Aramayo | Added persisted per-camera processing ceilings, demand-driven panoramic decoding, provider-aware realtime AI, optimized pose analysis, and a geometric training-sword tracker. |
| 2026-08-14 | `08963bc`–`097dbe0` | Rudy Aramayo | Restored hand/finger analysis and corrected projected 3D skeleton alignment. |
| 2026-08-14 | `daa98a9`–`dd2171a` | Rudy Aramayo | Added the ROB AI chat composer, modernized settings and exact speech completion, and expanded paced stage-show content. |
| 2026-08-15–16 | `e5a725f`–`9a1b1a3` | Rudy Aramayo | Added multilingual voice routing, deterministic no-silent-failure conversational fallback, and repaired wrapped speech-bubble layout. |
| 2026-08-16 | `b18803c` | Rudy Aramayo | Added a fixed-publisher, read-only news tool; later repository state expands the publisher list. |
| 2026-08-18–20 | `ae4057d`–`89679b0` | Rudy Aramayo | Added startup panoramic perception and a cached system-status dashboard; separated face/belly OAK roles; added sidewalk/chess/depth overlays; fixed retained image buffers; made main RGB-D resolution selectable. |
| 2026-08-19 | `06c5f56` | Rudy Aramayo | Added on-device sidewalk segmentation and bounded background autonomy context while retaining tread authority behind explicit operator sessions; also capped MLX memory. |
| 2026-08-20–21 | `d49a7c8`, `d3efab0`, `cbd64fb`, `8a3f9e0` | Rudy Aramayo | Added explicit recoverable synchronized training capture for cameras, depth, lidar, pose, authority, and labels, plus the recording-control UI and layout tests. |
| 2026-08-21–22 | `c0877e6`–`7b76a67` | Rudy Aramayo | Built and hardened the disabled-by-default one-to-one Messages AI bridge: sender allowlists, isolated sessions, bounded images, local current information, encrypted optional memory, and exact-confirmation administrator scripts. |
| 2026-08-22 | `c3c8dcd`–`54403ea` | Rudy Aramayo | Added three independent authenticated video feeds, explicit controller ownership, live-session video binding, compact lidar telemetry, and same-Mac authenticated IPC with network fallback. |
| 2026-08-22 | `104a8de`, `1308a37` | Rudy Aramayo | Made local tread controls momentary/ramped and hardened `ticcmd` process termination. |
| 2026-08-22 | `f5528c2` | Rudy Aramayo | Added consent-based local face enrollment, an encrypted gallery, open-set/temporal recognition gates, and the explicit rule that identity never grants authority. |
| 2026-08-23 | `e76d515` | Rudy Aramayo | Added selectable AdaFace IR18 WebFace4M and VGGFace2 Core ML encoders, model-tagged profiles, a validated installer, and comparison-safe model switching. |

## August 2026 companion-repository expansion

### ROBController

| Date | Commit | Change |
|---|---:|---|
| 2026-08-21 | `6e7980c` | Added operator-authorized destination navigation with Nominatim search and compatibility with bounded social roam. |
| 2026-08-22 | `c5bf774` | Hardened speech-service teardown against crashes. |
| 2026-08-22 | `51e2e0d`, `fb939ea` | Redesigned phone and iPad consoles around Map, Controls, Auto, and Settings with adaptive controls and lidar/map context. |
| 2026-08-22 | `f45e336` | Added push-to-talk chirps and audio-session/tap hardening while preserving joystick priority. |
| 2026-08-22 | `a6500b5`, `50a2229` | Refreshed three-camera affordances and added selectable OSM, OpenTopoMap, and Apple satellite layers with persisted overlay scale/north rotation. |

### ROBControllerVision

| Date | Commit | Change |
|---|---:|---|
| 2026-08-15–16 | `f3b5833`, `e6721df` | Progressed from arm telemetry/preview to independent left/right `rob-arm-control/2` leases and simultaneous dead-man-gated PSVR Sense joint jogging. |
| 2026-08-22 | `bed352f`, `98c9462` | Worked around visionOS 26.5 speech UI behavior and hardened dictation permission/audio teardown. |
| 2026-08-22 | `a754472` | Added explicit Request/Release Control and authoritative owner display across phone and Vision clients. |
| 2026-08-22 | `2474618`–`29d944f` | Bound video to the live control session, required the client to open the QUIC stream, and introduced multi-scene/360 launch support. |
| 2026-08-22 | `cef8af4`–`137d147` | Implemented the mixed immersive Insta360 path, inward-facing panorama sphere, texture replacement, diagnostics, and session survival across immersive transitions while braking inactive scenes. |
| 2026-08-22 | `63b9d9e` | Added the verified -90-degree startup heading, step/slider rotation, and Face Robot Front reset. This local commit is part of the three-commit lead over `origin/main` at inspection. |

### RPLidar and maps

| Date | Commit | Change |
|---|---:|---|
| 2026-08-20 | `4b07ef8` | Hardened the app against crash paths. |
| 2026-08-21 | `7082103` | Aligned occupancy-map updates with scan-captured pose and explicit world/raster orientation. |
| 2026-08-22 | `f819ed6`–`8ac5635` | Added `.robomap` save/load/reset, recovery fallbacks, and blank-screen repairs. |
| 2026-08-22 | `b8b9040` | Added persisted lidar overlay scale and north rotation; north remains manual without a trusted heading source. |
| 2026-08-22 | `4e831a3`, `2459684` | Added compact bounded `RLS1` scan frames and authenticated App Group local IPC with paired QUIC fallback. |
| 2026-08-22 | `e02fe1e`, `d6ad455` | Added an active-route badge and refreshed breakpoint landmarks. |

### AMBER, training games, and website

| Repository/date | Commit range | Change |
|---|---:|---|
| Amber, 2026-08-11–16 | `64a0e6e`–`722378a` | Added the persistent Cerebro-to-AMBER gateway, allowlisted 36-file synchronization, the corrected right-arm URDF selection, and a recovery helper; the gateway remains non-authoritative for motion. |
| ROBTrainingGames, 2026-08-11–14 | `6128366`–`92a7738` | Added iOS/visionOS training games and ROB Voice, expanded the tank campaign, improved keyboard control and crash handling, and repaired lock/key progression with new spatial puzzles. |
| ORobotics, 2026-08-10–15 | `8953be3`–`b1cc1a2` | Added the interactive USB 5 V lab and Three.js ROB training campaign, then expanded mobile/fullscreen controls, levels, puzzles, and native-game website coverage. |

## Reading the author labels correctly

All observed author labels use `orbitus@orbitusrobotics.com`. The most economical
explanation is the one supplied by the project owner: one person used multiple
computers with different Git `user.name` values. The history contains no
`Co-authored-by: Codex` or equivalent attribution. The change in engineering
style supports discussion of AI acceleration, but it cannot identify which
individual lines were generated, rewritten, reviewed, or merely inspired by AI.
