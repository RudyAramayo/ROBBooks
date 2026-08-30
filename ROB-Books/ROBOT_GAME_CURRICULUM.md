# ROB books and game curriculum crosswalk

Updated: 29 August 2026

The browser, iOS, and visionOS games are companion simulations for the
*Building R.O.B.* books. They do not connect to the physical robot. Circuit
Quest uses 90 builds; ROB Training uses a 15-level campaign plus multiplayer
practice. Their shared vocabulary lets a learner move between reading,
flat-screen play, camera AR, and spatial computing without relearning the
system model.

| Campaign band | Play objective | Robotics idea | Book connection |
|---|---|---|---|
| 1–4 — Calibration and navigation | Drive independent treads, gather energy, read obstacles, and dock | Differential drive, command intent, energy paths, observation before action | Volume 1 systems map; Volume 2 signals and power; Volume 3 tracked motion |
| 5–9 — Tools and feedback | Add bounded tools while layouts, moving obstacles, and timing become harder | Sensor limitations, feedback, state, timing, control ownership | Volumes 2–4; Field Manual verification and operator boundaries |
| 10–14 — Integrated missions | Coordinate perception, mobility, tools, energy, and recovery under pressure | Interfaces, fault response, resource budgeting, safe failure | Volumes 4–7; Volume 8 bounded autonomy and review |
| 15 — Capstone | Complete a whole-system mission with the learner's portable droid profile | System integration, evidence, operator responsibility, iteration | All volumes; Field Manual commissioning and operations |

## Shared component-explorer vocabulary

- **Tracked Base:** independent left and right treads; learners compare equal, unequal, and opposite commands.
- **Base Lift Flipper:** a separate motor, direction/brake control, home feedback,
  and timeout-controlled lever that may help the virtual base recover. It is not
  a weapon and does not imply that an unguarded physical mechanism is safe.
- **Power System:** batteries, protection, disconnects, motor electronics, and the difference between energy and information paths.
- **Cerebro:** the Mac-based coordination layer for operator intent, cameras, networking, and diagnostics.
- **Sensors:** cameras, lidar, inertial sensing, and infrared observations; sensor output is evidence, not permission to move.
- **ROB Audio:** digital samples move from the computer through an audio output
  stage to speakers, whose changing magnetic fields move cones and make sound.
  The game uses original procedural techno and exposes level limiting as an
  engineering choice.
- **Conference Microphone:** a far-field input model for sound level,
  signal-to-noise ratio, voice activity, echo cancellation, confidence, and
  control authority. A visible listening state and local processing boundary
  are part of the lesson.
- **Arms and Tools:** reach, joint limits, loads, and pinch hazards.
- **Safety Layer:** trained operator, exclusion zone, bounded trials, and an independently verified physical stop.

These summaries are intentionally high-level. When the detailed hardware documentation is expanded, update this file first, then synchronize `GameSession.swift`, the website simulator copy, and the relevant book sections. Do not infer current installed hardware from historical photographs or source filenames.

## Circuit Quest Book Bridge: builds 81–90

A review of all nine books and the complete field manual found three ideas that
were described in parts but lacked one continuous learner path: recovery
mechanics, sound output, and far-field voice input. These ten builds close that
gap without presenting the simulator as a physical commissioning result.

| Build | Learner investigation | Reading bridge | Section earned |
|---:|---|---|---|
| 81 | Trace the protected energy loop from the base supply through a motor driver and lift motor | Volume 1 energy paths; Volume 2 power versus signal | Base flipper |
| 82 | Command direction, PWM, and brake separately from the treads; label the historical D6/D7/D29 map without claiming it is the present harness | Volume 2 digital/PWM signals and Arduino pin ownership; Field Manual firmware map | Base flipper |
| 83 | Add home feedback, current/jam detection, and a motion timeout | Volume 2 watchdogs; Field Manual bounded tests and fault evidence | Base flipper |
| 84 | Compare lever arm, load, center of mass, tilt, and current during recovery | Volume 3 loads, torque, stability, and mechanisms | Recovery-ready base |
| 85 | Follow electrical energy through a coil, magnetic field, speaker cone, and pressure wave | Volumes 1–2 systems and signals; Volume 4 installed audio hardware | ROB audio |
| 86 | Carry digital audio from Cerebro through conversion and amplification without confusing data with power | Volumes 2 and 4 interfaces, computer responsibility, and diagnostics | ROB audio |
| 87 | Assemble a procedural techno pattern, mix it, and prevent clipping with a limiter | Volume 5 public shows; Volume 7 local audio engineering and testing | Techno playback |
| 88 | Measure speech, background noise, distance, and signal-to-noise ratio at a conference microphone | Volume 4 microphone inventory and privacy; Volume 8 public-operation boundaries | Far-field voice |
| 89 | Keep playback out of commands with echo cancellation, voice activity, confidence, and explicit authority | Volumes 4, 7, and 8 control ownership, speech, and bounded AI | Voice-command path |
| 90 | Run a cancellable show that coordinates motion, recovery readiness, music, and listening indicators | Volumes 5 and 8 show design; Field Manual verification, operations, and stop ownership | Show-ready ROB |

The 80-build Maker Faire passport remains the reward requirement. Builds 81–90
are an advanced Book Bridge so an existing passport or prize record is never
silently invalidated. A portable droid profile may record completed section
identifiers and appearance choices; it must not contain raw microphone audio,
physical ROB credentials, or authority to control hardware.

## Suggested read–build–play loops

1. Read the named pages or chapter, predict what will happen, and draw the
   energy and information paths separately.
2. Complete the matching Circuit Quest build and explain the measurement or
   state transition in the learner's own words.
3. Inspect the newly visible section in the droid workshop, then use the system
   in ROB Training. The base-lift control is a recovery action; speakers provide
   game music; microphone behavior is simulated and visibly bounded.
4. Record one difference between the simulation and the physical evidence in
   the books. An adult mentor should treat that difference as a question, not
   permission to energize ROB.

## Scoring language

- Energy cell: 150 points
- Training target hit: 50 points
- Training obstacle disabled: 300 points
- Objective completion and level time bonuses: progressively larger by level
- Score is motivational feedback, not a safety or engineering competency certification

## AR learning boundary

The iOS camera mode and visionOS immersive mode let learners place, move,
rotate, scale, and inspect a virtual ROB. Virtual clearance, collision, base
recovery, sensing, audio, and component labels do not validate the physical
robot. The games must never reuse real ROB credentials or silently gain a
physical-control path.

## ROB Voice learning companion

The iOS and visionOS games include an explicitly activated listener. On-device speech recognition converts the learner's question to text; Apple's available on-device Foundation Model answers as ROB; speech synthesis reads the answer aloud. The model receives only bounded simulation context such as level, score, cells, and remaining training enemies. Its personality may make playful, kid-safe sarcastic observations about simulated obstacles, but it must never ridicule the learner, fabricate physical-robot facts, provide unsafe operating instructions, or confuse game clearance with real-world safety. When Apple Intelligence is unavailable, a small scripted response set preserves basic game commentary without pretending that a model answered.
