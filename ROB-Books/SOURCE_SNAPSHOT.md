# Building R.O.B. — inspected source snapshot

Inspection date: **2026-08-23**
Public repository index: <https://github.com/RudyAramayo/ROBBooks/blob/main/ROB-Books/OPEN-SOURCE-CODE-MAP.md>

The books are a synthesis of a changing workshop archive. These identifiers make this edition reproducible enough to review while the builder selects a tagged publication release.

| Source | Identifier at inspection | Working-tree note |
|---|---|---|
| `Cerebro` | `e76d515a56e8018c96d07efb251470a40f9de174` | Clean `Gemini-Workspace`, synchronized with `origin/Gemini-Workspace`. Includes the consent-based face gallery and selectable AdaFace backends. |
| `ROBController` | `50a2229f542990d4e1757ae7a059604d4ac69e24` | Clean `main`, synchronized with `origin/main`. |
| `ROBControllerVision` | `63b9d9e569e5f84a70940a671226c27195e64b22` | Clean local `main`, **three commits ahead of `origin/main`**. The inspected immersive-360 heading/orientation work is not yet on the remote. |
| `M2M1-RPLIDAR-iOS-MacOS-Catalyst-` | `d6ad4554e8dde9f3c106cd63e9b66b3d4d659197` | Clean `master`, synchronized with `origin/master`. |
| `ROBArduino` | `92a9337d1118bfcd43a99c93ca2c8a90fd802088` | Clean `main`, synchronized with `origin/main`; firmware file hashes below are unchanged from the earlier inspection. |
| `Amber-HomeFolder` | `722378a70da458d331ecbc45a0bcf196a0500b7f` | Clean `main`, synchronized with `origin/main`; the right launch file now selects `DualArmR.urdf`. |
| `ROBTrainingGames` | `92a773876369b31561a4ed9eb606b76984420857` | Clean `main`, synchronized with `origin/main`. |
| `ORobotics` | `b1cc1a2e588323c50938f84abc17feda4a9943bc` | Clean `main`, synchronized with `origin/main`. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_BASE_APP.ino` | SHA-256 `af7cec9c49496eb4a7a638bd3e3e42b160eec4ce5974a67915b48d6e6ca6b8b1` | Builder reports this is the only Arduino role presently used. Its Base-specific startup line supports Cerebro discovery; flashed binary remains to be recorded. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_HEAD_APP.ino` | SHA-256 `63b32d3149d9d78d7db9dadeb819414155e57f09ff902bb8c699447ed6329305` | Retired Head-role firmware from the earlier three-Arduino architecture. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_TORSO_APP.ino` | SHA-256 `97b238fe9bf7772c43dc0f4834cfc322cf826de7adb7ec61faa3c4fde9c3c3a7` | Retired Torso-role firmware; the ` 2.ino` file is byte-identical. |
| `AmberHomeFolder/amber/L-10/amber_core_L` and `R-11/amber_core_R` | SHA-256 `554e7088b94b98f03f152f394c5e5b1d1ecfd16dacd470889e65dc83c36d2100` | Byte-identical captured core binaries; complete corresponding source and rebuild recipe were not found. Do not infer reproducibility from the matching files. |
| `AmberHomeFolder/amber/L-10/launch.json` | SHA-256 `baea5d73603f3e44eb603fde26c8d06268e2949b1adc4fb880f65a73a901f572` | Observed left configuration: `can10`, `Left_`, UDP 26001, and `DualArmL.urdf`. |
| `AmberHomeFolder/amber/R-11/launch.json` | SHA-256 `5de7ef5c9e8f2315b5fc88d6b4db4dac54065cb2d0b1569484636435f649410d` | Observed right configuration: `can11`, `Right_`, UDP 26002, and `DualArmR.urdf`. |
| `Amber URDF/amber_b1.urdf` | SHA-256 `7d83fa365e619f39b58daa61e48b162f1902d02d3f704a3f40c53a1401cf0a4f` | Independent single-arm seven-joint model; not proof of ROB mounting, zero, or safe limits. |
| `Cerebro/Amber-PythonAPI/Amber V2 API/amber_api/amber_robot.py` | SHA-256 `3fc574ca827d8054b33a9545337fa07d4d7f000be4de5ed60a8a77a0202f24ce` | High-level UDP wrapper inspected with its packed command structures. |
| `ROB_v3.pdf` | SHA-256 `67dbe60571e22f705f3838848bce0011bda8e00e1c357734ee07dadcdf1f346b` | 95 pages; 1920 × 1080 pt slide pages. |

## Recovered Cerebro workshop history

The current `Cerebro` row above describes the actively developed public
repository. The following read-only archive folders establish the earlier
history. They are stored under the workshop's `Documents/Dev/R.O.B.` archive;
private absolute user paths are intentionally omitted from publication.

| Archive | Identifier at inspection | Historical meaning and preservation note |
|---|---|---|
| `Cerebro v1` | no Git metadata; key file fingerprints in `CEREBRO_ARCHIVE_HISTORY.md` | Pre-Git Cocoa serial-command archive. Upstream example headers are dated 2009; ROB-specific headers and project state are dated 2017-2018. Do not turn the upstream date into a Cerebro origin claim. |
| `Cerebro v2` | master `c27829851b9252310a7ee14337ec7c773ca52813`; 11 commits; root `0141a6461303302e53941c398ebeda4f60c1a1c7` | First surviving Git history, 2018-01-01 through 2018-05-17. The working copy has uncommitted source/project changes, so manuscript claims use committed objects. |
| `Cerebro v3` | master `00fbf6bdc4ec9c62df9173253bfe3b7e4ab1c2db`; 46 master commits, 50 across all refs | Preserves `libfreenect`, `nite2`, `rob2`, and `t265` experiment branches plus master through 2022-04-09. The working copy has iCloud-placeholder and local state; preserve it without cleanup. |
| `Cerebro v4` | master `1a3c7799bdb4b60d0d4917f5de4ad0a95d88e96e`; 50 master commits, 54 across all refs | Shares the 2018 root and old experiment branches, but master diverges from the later v3 master after their common 2019-11-09 T265/perception checkpoint `b676ced`. It continues through 2025-07-02 and was clean at inspection. |
| `Cerebro v5` archive | branch `AramayoHouse_changes` at `46ca05c8af17f32350f45a5143733474e8f8a813`; 34 commits; root `4c4f1d454253e39798c23aed4522716068aadd98` | Independent fresh repository beginning 2025-08-05. The working copy has only Xcode user-interface/breakpoint changes at inspection. The active public repository has continued beyond this archived state. |

The full interpretation, v1 SHA-256 fingerprints, commit milestones, branch
relationship, third-party attribution boundary, and preservation rules are in
[`CEREBRO_ARCHIVE_HISTORY.md`](CEREBRO_ARCHIVE_HISTORY.md).

## Material change since the August 10 snapshot

- Cerebro added an always-on supervisor, headless Insta360 Pro II capture, separate face and belly OAK roles, selectable Core ML/Vision detectors, MLX model preparation, per-camera processing budgets, a system-status dashboard, safer local tread/neck controls, and three independent live-video feeds.
- Cerebro added explicit synchronized recording sessions for RGB, lossless aligned depth, stereo, calibration, lidar, pose, odometry, authority, and separately encoded camera footage. Autonomous commands are recorded but cannot create their own traversability labels.
- The disabled-by-default Messages bridge now provides allowlisted one-to-one conversations, isolated AI sessions, bounded image handling, weather and fixed-publisher news, optional encrypted transcript memory, and exact-confirmation local administrator scripts. It has no motion, file, device, Music, camera, or microphone tools.
- The disabled-by-default face system now uses consent-based local enrollment, an encrypted gallery, open-set and temporal gates, and selectable AdaFace IR18 Core ML encoders. A recognized name is untrusted scene context, never authorization.
- ROBController added destination autonomy, a redesigned phone/iPad command console, push-to-talk, OSM/OpenTopoMap/Apple satellite layers, and persisted overlay scale and north rotation.
- ROBControllerVision added explicit control handoff, simultaneous independently authorized arm jogging with paired PSVR Sense controllers, three camera feeds, a mixed immersive 360 sphere, scene-lifecycle hardening, and headset orientation controls. The latest three orientation commits remain local-only at this snapshot.
- The RPLidar app now publishes compact `RLS1` scans, supports same-Mac authenticated App Group IPC with QUIC fallback, aligns map updates with captured pose, saves/loads `.robomap`, exposes base-map alignment controls, and publishes all bounded valid points rather than the former sub-meter front/back slice.
- Amber recovery and allowlisted file synchronization were added; the right launch configuration was reconciled to `DualArmR.urdf`.

## Face-model artifact record

The installed checkpoints and compiled models are local runtime artifacts and are deliberately excluded from Git. `Cerebro/Scripts/install_adaface_models.py` is the reproducible conversion/validation entry point.

| Model | Role | Checkpoint SHA-256 | Verified conversion |
|---|---|---|---|
| AdaFace R18 WebFace4M | Recommended default/broader comparison base | `7a789f6696e5abb7ac7013a8a3e272abd9bffed84e7a2ebd8145b42c9382d828` | PyTorch/Core ML cosine `0.9999932050704956`; compiled runtime returned a 512-value L2-normalized embedding. |
| AdaFace R18 VGGFace2 | Optional comparison backend | `2360a615b1198c27888b2a2e885afe4d6db109afbf730ea7554e52db529caf28` | PyTorch/Core ML cosine `0.9999903440475464`; compiled runtime returned a 512-value L2-normalized embedding. |

Profiles are tagged with the encoder that created them. Embeddings from different encoders are never compared; switching models requires switching back or deleting and re-enrolling the profile.

## Snapshot cautions

- A commit is an evidence coordinate, not a publication release. Create intentional tags for the tested cross-repository combination before final publication.
- Three inspected ROBControllerVision commits are not on `origin/main`; a remote reader cannot reproduce those exact orientation controls until they are pushed.
- Photographs show several revisions. A visible component in one year is not proof that it remains installed now.
- Presentation slides are design-history evidence. A proposed diagram or component is not automatically current topology.
- The archive records an earlier Base/Torso/Head Arduino architecture. Present-day documentation names only Base as active. Head and Torso are historical artifacts, and none of the sketches is a certified safety controller.
- Face recognition, VLM labels, prompt-based person labels, and transcript memory are probabilistic or private context. None grants controller ownership, action approval, shell access, or physical authority.
- Vendor PDFs in `ROBOT Build/` carry restrictive notices. Their pages and specifications are outside the publication asset set pending authorization.
- `AmberHomeFolder` contains credential-bearing and machine-specific material. The books use selected runtime configuration as evidence but deliberately exclude SSH material, histories, logs, cached dependencies, virtual environments, and adapter serial values from reproduction instructions.
- The current repository state does not replace hardware-in-the-loop verification, camera/face consent review, biometric calibration, data-retention decisions, or public-show release review.

## Refresh procedure

Before the next edition, record each repository's full commit, remote divergence, whether the tree is clean, firmware/model/PDF hashes, hardware revision, calibration bundle, privacy configuration, and test-report revision. Then search all manuscripts for the old date and replace only claims that have been reverified.
