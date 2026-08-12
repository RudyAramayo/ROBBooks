# ROB books and game curriculum crosswalk

Updated: 11 August 2026

The browser, iOS, and visionOS games are companion simulations for the *Building R.O.B.* books. They do not connect to the physical robot. Each experience uses the same three-level learning arc, scoring vocabulary, and component names so a learner can move between reading, flat-screen play, camera AR, and spatial computing without relearning the model.

| Game level | Play objective | Robotics idea | Book connection |
|---|---|---|---|
| 1 — Calibration Deck | Drive independent treads, pass the gate, collect three cells, clear two training obstacles, and dock | Differential drive, command intent, energy paths, observation before action | Volume 1 systems map; Volume 2 signals and power; Volume 3 tracked motion |
| 2 — Neon Foundry | Navigate a tighter layout with four cells and three stronger moving obstacles | Sensor limitations, feedback, state, timing, bounded tests | Volume 2 sensing labs; Volume 3 mechanisms; Volume 4 command freshness and simulation |
| 3 — Sentinel Maze | Coordinate five cells, four moving obstacles, and a final dock under time pressure | System integration, autonomy boundaries, operator responsibility, safe failure | Volume 4 mission control; Volume 5 AI-assisted engineering and verification |

## Shared component-explorer vocabulary

- **Tracked Base:** independent left and right treads; learners compare equal, unequal, and opposite commands.
- **Power System:** batteries, protection, disconnects, motor electronics, and the difference between energy and information paths.
- **Cerebro:** the Mac-based coordination layer for operator intent, cameras, networking, and diagnostics.
- **Sensors:** cameras, lidar, inertial sensing, and infrared observations; sensor output is evidence, not permission to move.
- **Arms and Tools:** reach, joint limits, loads, and pinch hazards.
- **Safety Layer:** trained operator, exclusion zone, bounded trials, and an independently verified physical stop.

These summaries are intentionally high-level. When the detailed hardware documentation is expanded, update this file first, then synchronize `GameSession.swift`, the website simulator copy, and the relevant book sections. Do not infer current installed hardware from historical photographs or source filenames.

## Scoring language

- Energy cell: 150 points
- Training target hit: 50 points
- Training obstacle disabled: 300 points
- Objective completion and level time bonuses: progressively larger by level
- Score is motivational feedback, not a safety or engineering competency certification

## AR learning boundary

The iOS camera mode and visionOS immersive mode let learners place, move, rotate, scale, and inspect a virtual ROB. Virtual clearance, collision, sensing, and component labels do not validate the physical robot. The games must never reuse real ROB credentials or silently gain a physical-control path.

## ROB Voice learning companion

The iOS and visionOS games include an explicitly activated listener. On-device speech recognition converts the learner's question to text; Apple's available on-device Foundation Model answers as ROB; speech synthesis reads the answer aloud. The model receives only bounded simulation context such as level, score, cells, and remaining training enemies. Its personality may make playful, kid-safe sarcastic observations about simulated obstacles, but it must never ridicule the learner, fabricate physical-robot facts, provide unsafe operating instructions, or confuse game clearance with real-world safety. When Apple Intelligence is unavailable, a small scripted response set preserves basic game commentary without pretending that a model answered.
