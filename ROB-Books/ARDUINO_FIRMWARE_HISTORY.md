# ROB Arduino firmware: current role and historical architecture

Reviewed: 10 August 2026

## Publication conclusion

`ROBArduino/` preserves firmware for an earlier architecture with three named Arduino roles: Base, Torso, and Head. The builder reports that present-day ROB uses only the Base code. The books therefore use this vocabulary consistently:

- **Current firmware reference:** `ROBOT_CEREBELLULAR_BASE_APP.ino` describes the only Arduino role reported in present use.
- **Retired historical firmware:** the Torso and Head sketches document earlier experiments and must not appear in a current block diagram, current startup checklist, or current device count.
- **Installed state still requires evidence:** a source file does not prove what is flashed on a physical board. A release record must capture the connected board, firmware hash, toolchain/libraries, upload date, wiring revision, and bounded bench-test result.

This is documentation of inspected source, not an endorsement of the firmware as a safety controller.

## Inspected files

| Role | File | Lines | SHA-256 | Publication status |
|---|---|---:|---|---|
| Base | `ROBArduino/ROBOT_CEREBELLULAR_BASE_APP/ROBOT_CEREBELLULAR_BASE_APP.ino` | 802 | `af7cec9c49496eb4a7a638bd3e3e42b160eec4ce5974a67915b48d6e6ca6b8b1` | Current role reported by builder; exact flashed artifact unverified |
| Head | `ROBArduino/ROBOT_CEREBELLULAR_HEAD_APP/ROBOT_CEREBELLULAR_HEAD_APP.ino` | 436 | `63b32d3149d9d78d7db9dadeb819414155e57f09ff902bb8c699447ed6329305` | Retired historical reference |
| Torso | `ROBArduino/ROBOT_CEREBELLULAR_TORSO_APP/ROBOT_CEREBELLULAR_TORSO_APP.ino` | 695 | `97b238fe9bf7772c43dc0f4834cfc322cf826de7adb7ec61faa3c4fde9c3c3a7` | Retired historical reference |
| Torso duplicate | `ROBArduino/ROBOT_CEREBELLULAR_TORSO_APP/ROBOT_CEREBELLULAR_TORSO_APP 2.ino` | 695 | `97b238fe9bf7772c43dc0f4834cfc322cf826de7adb7ec61faa3c4fde9c3c3a7` | Byte-identical duplicate; not a fourth role or revision |

## Current Base firmware reference

The Base sketch opens USB serial at 250,000 baud and parses a historical 42-byte ASCII frame beginning with `~`. Seven signed five-character fields, separated by six commas, request:

1. left-tread brake;
2. left-tread speed;
3. right-tread brake;
4. right-tread speed;
5. flipper brake;
6. flipper speed;
7. linear-actuator speed.

The existing sketch prints `BEGIN BASE STARTUP SEQUENCE` after its IMU initialization. Cerebro pulses DTR to restart each USB serial candidate and passively listens up to 15 seconds for that exact legacy line; the archived retired sketches instead print `BEGIN HEAD STARTUP SEQUENCE` or `BEGIN TORSO STARTUP SEQUENCE`. This permits hub-independent Base discovery without changing or flashing show-day firmware and without sending command bytes to unknown devices. The operator's refresh action closes the former Base connection and repeats detection. A matching startup line identifies a firmware role; it does not prove wiring, motor polarity, safety behavior, or that the flashed bytes match the archived source hash.

The sketch defines the following source-level map. These are facts about code identifiers, not proof of the present harness:

| Function | Source declaration |
|---|---|
| Right tread | speed D2, brake D3, direction D25 |
| Left tread | speed D4, brake D5, direction D27 |
| Flipper | speed D6, brake D7, direction D29 |
| Linear-actuator serial | SoftwareSerial RX D22 and TX D23 at 19,200 baud; RX is declared but not used by the command path |
| IR sensors | front-left A5, front-right A4, left A3, right A2, back-left A1, back-right A0 |
| IMU | MPU9250 through `Wire`/I²C |
| Host link | USB `Serial` at 250,000 baud |

Tread and flipper PWM use `255 - abs(command)`, so the source assumes an active-low speed input. Brake field zero writes HIGH and is described by the code as releasing the brake; a nonzero field writes LOW. Left and right tread direction polarity differs in the helper functions. None of those source-level statements replaces a measured pin-to-connector, driver, and physical-direction test.

The actuator path emits compact serial commands: `0x83` exits safe start, `0x85` requests forward, and `0x86` requests reverse. Nominal magnitude is -3200 through +3200. Historical values -3201 and +3201 first exit safe start and are then converted to the corresponding 3200-magnitude command.

Six SharpIR objects exist. The active routine evaluates front and rear pairs against 25 cm thresholds and prints warnings after repeated close readings. Its six-value numeric printout is commented out, so the existing flashed firmware cannot provide reliable per-sensor distances to Cerebro without a future firmware change. The assignments that would assert forward or backward motion-inhibit flags are also commented out; side sensors do not participate in that decision. The MPU9250 path calculates orientation telemetry, but it does not independently stop motion.

The loop-count keepalive eventually calls the motor command path with zero speeds and zero brake fields. Because zero brake fields are described as released, the physical timeout response may be coast rather than hold and must be measured. Timing depends on loop execution rather than a monotonic elapsed-time deadline.

## Retired Torso firmware

The Torso sketch records an earlier Arduino-to-Maestro servo architecture. It opens host serial at 250,000 baud, uses SoftwareSerial pins 19/18 at 9,600 baud for a `MicroMaestro`, initializes an MPU9250, and contains disabled GPS processing through `Serial1`.

After `~`, its parser reads fourteen four-character target fields for Maestro channels:

- 0 and 1: head pan and head tilt;
- 6–11: right shoulder pan, shoulder tilt, elbow, wrist pan, wrist tilt, and gripper;
- 12–17: the equivalent six left-arm channels.

The file sends these values directly to `maestro.setTarget`. It does not validate complete-frame availability, separators, numeric ranges, servo calibration, joint limits, collision constraints, or checksum. Its keepalive expiration resets counters, but the stop call is commented out. Two Torso files in the archive are byte-identical, so they are duplicates rather than separate installed controllers.

Present documentation must not imply that this Arduino still owns ROB's head or arms. Current Cerebro source contains direct serial/Maestro-era helpers, but the actual installed arm/head control route and hardware must be verified independently.

## Retired Head firmware

The Head sketch records a sensor-oriented experiment. It opens host serial at 250,000 baud, initializes a long-range PIR sensor on enable D5/input D6, and initializes an MPU9250. GPS declarations and processing are commented out.

Despite retaining copied Base command examples and variable names in its header, the active parser consumes only the first five-character field after `~` and stores it in a legacy brake variable; it does not implement the Base motor frame. IMU processing remains active, while direct PIR processing is commented in the main loop. Its keepalive prints an expiration message, but its motor-stop call is commented out. It must not be described as a current motor or safety controller.

## Shared historical defects and publication cautions

All three sketches use fixed-position reads after seeing a start marker without first proving that a complete frame is buffered. Their small character arrays are not explicitly null-terminated before `atoi` and some debug printing. They refresh keepalive state on byte availability before full message validation, do not validate separators or ranges, and do not provide version, sequence, length, checksum, or authentication fields.

The Base sketch is the only present role, but “current role” does not mean “modernized implementation.” Before any firmware change or upload:

1. preserve the known working binary and source hash;
2. identify the exact board, core, libraries, and programmer settings;
3. map every pin through connector, driver, and physical load;
4. test boot, malformed input, serial loss, timeout, brake, direction, and bounds with motion isolated;
5. use current limiting, lifted/guarded mechanisms, a spotter, and an independent physical emergency stop;
6. record the exact tested hardware/firmware combination.

## Language for diagrams and captions

Use: “Present ROB uses one Arduino Base controller, according to the builder. The archive also preserves retired Torso and Head sketches from an earlier three-Arduino architecture.”

Avoid: “ROB has three Arduinos,” “the Head Arduino currently reads ROB’s sensors,” or “the Torso Arduino currently controls the arms,” unless new as-built evidence proves those claims.
