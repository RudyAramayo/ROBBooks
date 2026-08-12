# Building R.O.B. — inspected source snapshot

Inspection date: **2026-08-10**
Workspace: `/Users/rob/dev`

The books are a synthesis of a changing workshop archive. These identifiers make the first edition reproducible enough to review while the builder selects a true publication release.

| Source | Identifier at inspection | Working-tree note |
|---|---|---|
| `Cerebro` | `63c676c8bd6176ddf60e2325f4a8ab0a27150f36` | Modified and untracked Gemini/stage-show work was also inspected; tag the chosen publication state. |
| `ROBController` | `65891f92003c33e1f862bd428dc6ed1b61b882be` | Clean at inspection. |
| `ROBControllerVision` | `09a94b02764abc32598441511699b0534da03ad0` | Clean at inspection. |
| `M2M1-RPLIDAR-iOS-MacOS-Catalyst-` | `9de8bf0acc791b06bb231b2da320bcf9cee55a4f` | Clean at inspection. |
| `ORobotics` | `9ae07d270d44334bad2c9faa5bea63b9c156c7f6` | Site edits were present; gallery originals and metadata were inspected directly. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_BASE_APP.ino` | SHA-256 `af7cec9c49496eb4a7a638bd3e3e42b160eec4ce5974a67915b48d6e6ca6b8b1` | Builder reports this is the only Arduino role presently used. Its existing Base-specific startup line supports Cerebro discovery; flashed binary remains to be recorded. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_HEAD_APP.ino` | SHA-256 `63b32d3149d9d78d7db9dadeb819414155e57f09ff902bb8c699447ed6329305` | Retired Head-role firmware from the earlier three-Arduino architecture. |
| `ROBArduino/.../ROBOT_CEREBELLULAR_TORSO_APP.ino` | SHA-256 `97b238fe9bf7772c43dc0f4834cfc322cf826de7adb7ec61faa3c4fde9c3c3a7` | Retired Torso-role firmware; the ` 2.ino` file is byte-identical. |
| `AmberHomeFolder/amber/L-10/amber_core_L` and `R-11/amber_core_R` | SHA-256 `554e7088b94b98f03f152f394c5e5b1d1ecfd16dacd470889e65dc83c36d2100` | Byte-identical captured core binaries; complete corresponding source and rebuild recipe were not found. Do not infer reproducibility from the matching files. |
| `AmberHomeFolder/amber/L-10/launch.json` | SHA-256 `baea5d73603f3e44eb603fde26c8d06268e2949b1adc4fb880f65a73a901f572` | Observed left configuration: `can10`, `Left_`, UDP 26001, and `DualArmL.urdf`. |
| `AmberHomeFolder/amber/R-11/launch.json` | SHA-256 `d7860ef102917bdb947834352de39408e8d299fbb10c1d595d53ef86fc35ed78` | Observed right configuration: `can11`, `Right_`, UDP 26002, and `DualArm.urdf`; reconcile the alternate `DualArmR.urdf` configuration before operation. |
| `Amber URDF/amber_b1.urdf` | SHA-256 `7d83fa365e619f39b58daa61e48b162f1902d02d3f704a3f40c53a1401cf0a4f` | Independent single-arm seven-joint model; not proof of ROB mounting, zero, or safe limits. |
| `Cerebro/Amber-PythonAPI/Amber V2 API/amber_api/amber_robot.py` | SHA-256 `3fc574ca827d8054b33a9545337fa07d4d7f000be4de5ed60a8a77a0202f24ce` | High-level UDP wrapper inspected with its packed command structures. |
| `Presentation/ROB_v3.pdf` | SHA-256 `67dbe60571e22f705f3838848bce0011bda8e00e1c357734ee07dadcdf1f346b` | 95 pages; 1920 × 1080 pt slide pages. |

## Snapshot cautions

- A Git commit alone does not identify the inspected Cerebro behavior because relevant work was uncommitted. Create an intentional release commit/tag and update the manuscript before final publication.
- Photographs show several revisions. A visible component in one year is not proof that it remains installed now.
- Presentation slides are design-history evidence. A proposed diagram or component is not automatically current topology.
- The archive records an earlier Base/Torso/Head Arduino architecture. Present-day documentation names only Base as active. Head and Torso are historical artifacts, and none of the sketches is a certified safety controller.
- Vendor PDFs in `ROBOT Build/` carry restrictive notices. Their pages and specifications are outside the publication asset set pending authorization.
- `AmberHomeFolder` contains credential-bearing and machine-specific material. The books use selected runtime configuration as evidence but deliberately exclude SSH material, histories, logs, cached dependencies, virtual environments, and adapter serial values from reproduction instructions.
- Two archived CAN serial maps disagree, and the right-arm launch variants select different dual-arm URDF files. Both differences are commissioning blockers until reconciled with labeled hardware and controlled tests.

## Refresh procedure

Before the next edition, record each repository's full commit, whether the tree is clean, the firmware/PDF hashes, hardware revision, calibration bundle, and test-report revision. Then search all manuscripts for the old date and replace only claims that have been reverified.
