# ROB-Books repository refresh handoff

Checkpoint: **2026-08-23**

Project directory: `/Users/rob/dev/Presentation/ROB-Books`

This edition incorporates the implementation changes inspected across the ROB
repositories through August 23, 2026. The five materially edited PDFs were
rebuilt, validated, and visually reviewed. The remaining volumes were rebuilt
to confirm that the complete series still compiles and validates as one set.

## Inspected repository coordinates

| Repository | Branch and commit | Snapshot status |
|---|---|---|
| Cerebro | `Gemini-Workspace` at `e76d515a56e8018c96d07efb251470a40f9de174` | Clean and synchronized with `origin/Gemini-Workspace`. |
| ROBController | `main` at `50a2229f542990d4e1757ae7a059604d4ac69e24` | Clean and synchronized with `origin/main`. |
| ROBControllerVision | `main` at `63b9d9e569e5f84a70940a671226c27195e64b22` | Clean, but three commits ahead of `origin/main`; the latest immersive-orientation behavior is local-only. |
| M2M1-RPLIDAR-iOS-MacOS-Catalyst- | `master` at `d6ad4554e8dde9f3c106cd63e9b66b3d4d659197` | Clean and synchronized with `origin/master`. |
| ROBArduino | `main` at `92a9337d1118bfcd43a99c93ca2c8a90fd802088` | Clean and synchronized with `origin/main`. |
| Amber-HomeFolder | `main` at `722378a70da458d331ecbc45a0bcf196a0500b7f` | Clean and synchronized with `origin/main`. |
| ROBTrainingGames | `main` at `92a773876369b31561a4ed9eb606b76984420857` | Clean and synchronized with `origin/main`. |
| ORobotics | `main` at `b1cc1a2e588323c50938f84abc17feda4a9943bc` | Clean and synchronized with `origin/main`. |

The full artifact hashes, firmware evidence, status distinctions, and refresh
procedure are in `ROB-Books/SOURCE_SNAPSHOT.md`.

## Material book changes

- **Volume 4: Mission Control** now teaches explicit control ownership, dual-arm
  intent, three distinct camera feeds, bounded Messages use, recording consent,
  current lidar mapping, and the rule that a recognized face is context rather
  than a key.
- **Volume 5: AI Robotics with Codex** now includes the August 14-23 change
  atlas, cross-repository integration, face-model and Messages implementation
  prompts, synchronized recording, current camera roles, and current
  controller/Vision behavior.
- **Volume 7: Engineering ROBControllerVision** now documents Request/Release
  ownership, independent arm grants, paired PSVR Sense joint jogging,
  three-feed video, immersive 360 presentation, scene lifecycle, and the
  local-only status of the latest heading/orientation commits.
- **Volume 8: Engineering Cerebro** now documents explicit recording sessions,
  the consent-based face gallery and selectable AdaFace pipeline, the private
  Messages bridge, bounded destination autonomy, three camera roles, and
  updated operational checklists.
- **Complete Builder's Field Manual** now carries the same contracts and safety
  boundaries across its integrated technical chapters, source map, review
  checklist, and production notes.
- The source snapshot, open-source code map, editorial gaps, print/safety review,
  README, and Volume 5 change atlas were updated to match the inspected code.

## Face model record

- The face feature is disabled by default and requires local, consented
  enrollment. It stores an encrypted, model-tagged gallery under opaque profile
  IDs; identity is untrusted scene context and never control authority.
- Enrollment uses 24 quality-filtered samples. Matching is open-set and
  temporally gated; stale recognized context expires after 15 seconds.
- The default encoder is AdaFace IR18 WebFace4M with checkpoint SHA-256
  `7a789f6696e5abb7ac7013a8a3e272abd9bffed84e7a2ebd8145b42c9382d828`.
- The optional comparison encoder is AdaFace IR18 VGGFace2 with checkpoint
  SHA-256
  `2360a615b1198c27888b2a2e885afe4d6db109afbf730ea7554e52db529caf28`.
- Both use 112 x 112 BGR input, `pixel * (2/255) - 1`, a 512-value
  L2-normalized embedding, and model-specific profiles. Cross-model comparisons
  are forbidden. The documented defaults are cosine threshold `0.35` and
  ambiguity margin `0.06`.
- PyTorch/Core ML conversion cosine agreement was `0.9999932050704956` for
  WebFace4M and `0.9999903440475464` for VGGFace2; compiled runtime smoke tests
  returned unit-normalized embeddings.

## Messages bridge record

- Messages is disabled by default. It uses Full Disk Access only for local
  `chat.db` reads and Automation only to reply.
- The bridge accepts exact-allowlisted one-to-one senders, maintains a durable
  high-water mark, processes each message at most once, never replays history,
  fails closed on group or ambiguous chats, and limits accepted traffic to five
  messages per minute.
- Each chat has an isolated AI session. There are no motor, file, device,
  Music, camera, or microphone tools.
- One JPEG, PNG, HEIC, or HEIF attachment up to 10 MB and 24 megapixels may be
  normalized to a metadata-free image no larger than 2048 pixels. Gemini may
  receive it when configured; otherwise MLX receives pixels and Apple
  Foundation Models receive bounded textual visual analysis.
- Optional transcript memory is encrypted per sender/account and remains off by
  default. It has explicit export and clear controls.
- Exact `Shutdown` and `Reboot` requests enter a fixed local script path only
  after the same sender and chat reply with exact `YES` within 90 seconds. The
  fixed script runs through `/bin/zsh -f -s`, receives no interpolated message
  text, and has a 30-second timeout.

## Other current contracts captured

- Recording sessions preserve RGB, aligned lossless depth, stereo,
  calibration, lidar, pose, odometry, authority, labels, and three separately
  encoded camera movies. Autonomous commands may be recorded but cannot label
  their own training examples.
- Face, belly, and Insta360 cameras remain distinct provider roles. The live
  system advertises independent front, belly, and panoramic streams; Vision
  opens them only during an authenticated control session.
- Controller ownership uses explicit Request/Release semantics. The latest
  authenticated request wins only after a stop. Left and right arm grants are
  independent; both grips are dead-man inputs for joint jogging, not IK.
- The lidar publisher uses compact `RLS1` scans for all bounded valid points,
  authenticated local App Group IPC with QUIC fallback, pose-aligned maps, and
  `.robomap` persistence.
- Destination autonomy stays behind operator authority and stale-state gates.
  Traversability learns only from manually confirmed samples and never from its
  own autonomous commands.

## Build and verification

Commands run from `ROB-Books`:

```text
bash tools/build_books.sh
bash tools/validate_books.sh
bash tools/render_previews.sh
```

Final physical PDF page counts:

| Artifact | Pages |
|---|---:|
| Volume 1 | 37 |
| Volume 2 | 35 |
| Volume 3 | 36 |
| Volume 4 | 39 |
| Volume 5 | 41 |
| Volume 6 | 34 |
| Volume 7 | 38 |
| Volume 8 | 48 |
| Story | 23 |
| Complete manual | 231 |

Validation passed for all ten PDFs: US Letter geometry, no encryption, no
private paths, no retired assets, approved image-overlap accounting, and no
prepared-photo GPS or camera make/model metadata. The build logs contain no
overfull boxes, LaTeX errors, undefined control sequences, or fatal errors.

The five edited PDFs were raster-compared against the prior Git revision. All
351 materially changed pages were inspected at readable resolution, including
all 231 pages of the integrated manual through contact-sheet coverage. No
clipping, overflow, broken tables, or malformed page furniture was found.

## Remaining release boundaries

- Push or intentionally publish the three local ROBControllerVision commits
  before claiming that the exact immersive-orientation implementation is
  reproducible from the remote repositories.
- Perform hardware-in-the-loop validation before presenting controller, arm,
  camera, lidar, or autonomy behavior as commissioned.
- Complete biometric calibration, false-accept/false-reject review, data
  retention decisions, Messages privacy review, and public-show release review.
- Preserve the visible builder-input placeholders until dated evidence is
  supplied. The PDFs remain publication proofs, not certified engineering plans
  or printer-approved press files.
