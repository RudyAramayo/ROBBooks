# Building R.O.B. — editorial gaps for the builder

The manuscripts use visible placeholders instead of inventing missing facts. Answer these questions with measurements, drawings, dated photographs, test records, or a short first-person story. When two revisions differ, keep both and label the date; do not silently merge them into one imagined robot.

## 1. Identity and build story

- The archive now establishes ROB-specific Cerebro source in 2017-2018 and the first surviving Cerebro Git root on 1 January 2018. What does “R.O.B.” mean, when did the physical project begin, and how did the first serial-control software relate to that beginning?
- The v1-v5 source record is documented. Add the builder's first-person account of why the Mac controller was named Cerebro, what “Rob Makina” meant in the early headers, and why the v5 code moved into a fresh repository in August 2025.
- What did you want ROB to do at the start? What is the current mission?
- Which people, shops, clubs, schools, vendors, or events contributed?
- What were the most important failed attempts, repairs, and design changes?
- Which photographs show distinct hardware revisions rather than one continuous build?
- What changed after each public demonstration, including Maker Faire appearances?

## 2. Current physical envelope

- Ready-to-run height, width, length, mass, center of mass, ground clearance, and transport dimensions.
- Current chassis and body materials, plate thicknesses, coatings, and remaining wooden parts.
- Safe lifting points, number of people or lift equipment required, and transport restraints.
- Full motion envelope for treads, flippers, torso/body, head/neck, linear actuators, arms, and grippers.
- Pinch, crush, entanglement, hot-surface, sharp-edge, and tip-over zones in every pose.

## 3. Chassis, treads, and drivetrain

- Dimensioned as-built drawings or CAD for the base, tread frames, shafts, mounts, openings, and guards.
- Tread, wheel, sprocket, shaft, bearing, collar, chain, motor, gearbox, and controller part identities.
- Tread-tension and chain-alignment procedure, acceptable ranges, wear limits, and inspection interval.
- Final flipper geometry, intended job, limits, loads, and relationship to the third-wheel proposal.
- Verified speed, slope, stopping distance, traction, turning, thermal, and current results on hard floor and grass.
- The exact installed role of each central/torso/third-wheel actuator in each revision.

## 4. Fabrication record

- Final templates, CAD, material grades, thicknesses, fasteners, fits, tolerances, and torque values.
- Actual order of milling, drilling, cutting, bending, welding, deburring, coating, and assembly.
- Machine, cutter, workholding, feeds and speeds, coolant/chip control, PPE, inspection tools, and acceptance checks for every operation.
- Which parts were made in-house or by an outside shop, and which are commercial components?
- Rejected parts and lessons: what failed inspection, interfered, cracked, loosened, overheated, or had to be remade?
- Costs, lead times, substitutes, service-access decisions, and reusable fixtures.

## 5. Electrical and energy system

- Authoritative single-line schematic for the current robot, with revision and date.
- Battery chemistry, model, quantity, series/parallel topology, BMS, chargers, isolation, enclosure, and retirement criteria.
- Main disconnect and emergency-stop circuit, contactor/relay details, fault state, reset behavior, and test procedure.
- Fuse/breaker values and interrupt ratings; branch currents; converters; inverter or shore-power details.
- Wire gauge, insulation, color/label convention, connectors, strain relief, grounding/bonding, and cable routing for every branch.
- Measured startup, steady, peak, regenerative, stalled, and fault currents plus runtime and temperature data.
- Logic-voltage compatibility and isolation between Arduino, motor controllers, actuator controller, sensors, USB, and computers.

## 6. Arduino base and low-level motion

- Exact Arduino-compatible board and core, installed library versions, firmware revision, and build instructions.
- Connector-to-pin table, including active polarity, voltage, destination, cable label, and expected safe state.
- Verified tread/flipper direction, brake truth table, PWM convention, allowed command bounds, slew limits, and boot state.
- Corrected framing/parser design, valid-message watchdog behavior, timeout state, and independent physical stop behavior.
- Actuator controller model, its compact serial protocol, end stops, feedback, current limits, travel, load, duty cycle, and safe-start reset behavior.
- Encoder hardware and final pins; resolve the conflicting historical D18/D19 notes and the proposed D20/I²C conflict.
- IR sensor models, positions, shrouds, calibration, grass/terrain test results, and date/reason each channel was enabled or disabled.
- IMU model, mounting orientation, offsets, calibration storage, sample rate, and use in actual control.

## 7. macOS, controllers, and networking

- Tagged release or commit for Cerebro, ROBController, ROBControllerVision, and lidar software used at publication.
- Mac model, macOS version, ports, powered hubs, USB device names, selected Python runtime, packages, and startup order.
- Current network diagram: router/access point, discovery, services, ports, trust boundaries, video path, and no secrets.
- Pairing, enrollment, certificate replacement, revocation, role changes, controller handoff, and recovery after reinstall.
- Measured command rate, latency, packet loss, freshness/lease behavior, reconnect behavior, and stop result for every controller.
- Supported iPhone, Watch, and Vision Pro hardware/OS matrix and verified current feature set.
- Remove, minimize, or justify live controller location data; define log retention, redaction, and public-show privacy policy.

## 8. Perception, arms, speech, autonomy, and AI

- Exact camera, OAK-D, lidar, IR, and IMU models; mounts; coordinate transforms; timestamp behavior; calibration; accuracy; lighting limits.
- Current lidar host, transport, model, filtering, map format, and behavior when scans become stale.
- Arm and neck models, joint definitions, zeroing, limits, payload, reach, current limits, feedback, collision model, and gripper behavior.
- Approved keyframes, calibration file, cancellation behavior, and pose-by-pose clearance checks.
- Local speech settings versus optional external/cloud audio or video; consent, indicator, retention, and disable procedure.
- Face-identity release record: enrolled people and consent, administrator enrollment policy, retention/deletion, false-accept/false-reject targets, on-robot threshold calibration, replay and presentation-attack tests, lighting/pose/occlusion limits, liveness/depth plan, and proof that identity never grants control authority.
- AdaFace release choice and profile migration: selected WebFace4M or VGGFace2 encoder, installer/checkpoint hashes, Core ML validation record, model-specific enrollment inventory, comparison protocol, and rollback/delete/re-enroll procedure.
- Messages bridge release record: exact enabled accounts and allowlisted senders, Full Disk Access and Automation grants, one-to-one/group rejection tests, attachment and rate limits, cloud/local model routing, fixed news/weather sources, transcript-memory default and retention, plaintext export/clear procedure, and incident response.
- Administrator-message policy: locally configured administrator handles, exact command names, 90-second same-chat confirmation tests, reviewed shutdown/reboot scripts, local critical warning, output retention, and proof that message content cannot be interpolated into a shell.
- Recording and training-data governance: session owner and purpose, explicit start/stop indication, storage estimate and free-space floor, recovery tests, dataset retention/deletion/export, bystander consent, calibration/version binding, train/validation separation, and review of every derived label. Preserve the rule that autonomous commands never label themselves.
- Autonomy speed, radius, obstacle criteria, containment evidence, abort rules, and actual on-robot test results.
- For every AI-exposed action: implemented executor, bounds, approval policy, timeout, cancellation, telemetry, failure response, and fixture/on-robot evidence. Keep unavailable actions explicitly unavailable.

## 9. Verification and public operation

- Hazard analysis, risk controls, owners, acceptance criteria, sign-off authority, and re-test triggers.
- Test ladder results from lifted treads through controlled floor tests, slopes, grass, flippers, actuators, arms, and multi-controller failures.
- Failure injection for malformed/stale commands, serial silence/noise, lost network, helper crashes, stale sensors, bad calibration, low battery, and E-stop activation.
- Measured end-to-end stopping time and distance for each mode, surface, load, speed, and battery condition.
- Maker Faire barrier dimensions, speed limit, scripted missions, camera/microphone signage, operator/spotter roles, charging plan, fire response, and abort criteria.
- Maintenance intervals, wear limits, lubrication, torque checks, spares, battery retirement, backup/restore, and configuration-release record.

## 10. Publication and credits

- Confirm photographer ownership, identifiable-person releases, venue requirements, and permission for third-party product imagery.
- Obtain authorized public datasheets or written permission before publishing restricted vendor facts or pages.
- Supply preferred acknowledgments, sponsor names/logos with permission, contact information, license, ISBN/imprint decisions, and age/safety review.
- Approve the final photo captions and clearly identify every historical concept, removed component, and current configuration.
