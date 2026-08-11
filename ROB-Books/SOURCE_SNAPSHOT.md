# Building R.O.B. — inspected source snapshot

Inspection date: **2026-08-02**  
Workspace: `/Users/raramayo/dev`

The books are a synthesis of a changing workshop archive. These identifiers make the first edition reproducible enough to review while the builder selects a true publication release.

| Source | Identifier at inspection | Working-tree note |
|---|---|---|
| `Cerebro` | `63c676c8bd6176ddf60e2325f4a8ab0a27150f36` | Modified and untracked Gemini/stage-show work was also inspected; tag the chosen publication state. |
| `ROBController` | `65891f92003c33e1f862bd428dc6ed1b61b882be` | Clean at inspection. |
| `ROBControllerVision` | `09a94b02764abc32598441511699b0534da03ad0` | Clean at inspection. |
| `M2M1-RPLIDAR-iOS-MacOS-Catalyst-` | `9de8bf0acc791b06bb231b2da320bcf9cee55a4f` | Clean at inspection. |
| `ORobotics` | `9ae07d270d44334bad2c9faa5bea63b9c156c7f6` | Site edits were present; gallery originals and metadata were inspected directly. |
| `ROBOT Build/ROBOT_CEREBELLULAR_BASE_APP.ino` | SHA-256 `af7cec9c49496eb4a7a638bd3e3e42b160eec4ce5974a67915b48d6e6ca6b8b1` | Historical standalone firmware file. |
| `Presentation/ROB_v3.pdf` | SHA-256 `67dbe60571e22f705f3838848bce0011bda8e00e1c357734ee07dadcdf1f346b` | 95 pages; 1920 × 1080 pt slide pages. |

## Snapshot cautions

- A Git commit alone does not identify the inspected Cerebro behavior because relevant work was uncommitted. Create an intentional release commit/tag and update the manuscript before final publication.
- Photographs show several revisions. A visible component in one year is not proof that it remains installed now.
- Presentation slides are design-history evidence. A proposed diagram or component is not automatically current topology.
- The Arduino sketch records historical behavior with known parser, watchdog, initialization, sensor, and safety limitations. Preserve it as an artifact; do not treat it as a certified controller.
- Vendor PDFs in `ROBOT Build/` carry restrictive notices. Their pages and specifications are outside the publication asset set pending authorization.

## Refresh procedure

Before the next edition, record each repository's full commit, whether the tree is clean, the firmware/PDF hashes, hardware revision, calibration bundle, and test-report revision. Then search all manuscripts for the old date and replace only claims that have been reverified.
