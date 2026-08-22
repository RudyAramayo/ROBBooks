# The arm system we actually have

> **SOURCE TRAIL — ANALYZING NOW:** `AmberHomeFolder/amber/L-10/launch.json` and `AmberHomeFolder/amber/R-11/launch.json`. This chapter derives the left/right topology from those two captured configuration files.

ROB's manipulation system is not one abstract “robot arm.” It is two AMBER B1 arms, each with seven revolute joints and a gripper actuator. The inspected Ubuntu snapshot names the deployed sides `L-10` and `R-11`. Their current launch files separate the sides at every important boundary:

| Concern | Left arm | Right arm |
|---|---|---|
| Ubuntu directory | `amber/L-10` | `amber/R-11` |
| CAN interface | `can10` | `can11` |
| LCM prefix | `Left_` | `Right_` |
| UDP port | `26001` | `26002` |
| end-effector link | `Lseven_Link` | `Rseven_Link` |
| gripper actuator number | `8` | `8` |

The repository supports this architecture diagram:

```text
operator / Cerebro / test client
              |
       UDP or multicast LCM
              |
      Ubuntu AMBER core processes
          /                 \
 L-10 core :26001      R-11 core :26002
       | can10                | can11
       |                      |
 seven left joints       seven right joints
 + gripper #8            + gripper #8
```

This distinction matters. The Python API does **not** place CAN frames on the wire. It sends packed UDP datagrams to an AMBER core. The core owns the CAN-side exchange with the actuators. The saved LCM types provide a higher-rate publish/subscribe route into that same core. A future replacement core would need a separately verified actuator-level CAN specification; that specification is not present in the inspected source tree.

## An evidence ledger

Use four labels throughout commissioning:

- **Observed:** directly readable in a source file, launch file, URDF, or captured configuration.
- **Derived:** calculated from observed values, such as converting radians to degrees.
- **Reported:** supplied by the builder but not independently demonstrated by the snapshot.
- **Unknown:** requires measurement, vendor documentation, or a controlled test.

The two arms, seven-joint count, ports, prefixes, core settings, UDP structures, and URDF geometry are observed. The exact mounting transforms on ROB, current safe payload, braking behavior, CAN adapter bitrate interpretation, and the firmware actually running today still require confirmation.

# Read the repository without copying a whole computer

The arm evidence is distributed across three project locations:

```text
AmberHomeFolder/
  amber/
    L-10/launch.json                 left runtime configuration
    R-11/launch.json                 right runtime configuration
    amber_core/urdf/                 single- and dual-arm models
    amber_core/init/initCan.sh       adapter discovery and CAN binding
    sin_wave/rawLcm/*.lcm            LCM message definitions
    Install/                         historical dependency scripts

Amber URDF/amber_b1.urdf             independent single-arm model

Cerebro/Amber-PythonAPI/
  Amber V2 API/amber_api/            UDP client implementation
  Amber v1 API/                      older packet examples
```

`AmberHomeFolder` is a captured home directory. It also contains histories, logs, cached packages, a virtual environment, device identifiers, and SSH material. Those files are useful forensic evidence but are not a golden image. Do not publish them, synchronize their credentials, or recursively copy them onto a replacement Ubuntu box. Build a clean host from a reviewed manifest and copy only the authorized runtime artifacts, URDFs, message definitions, and configuration.

The `amber_core_L` and `amber_core_R` programs are compiled executables. Because corresponding complete source and a reproducible build recipe are absent, record their architecture, cryptographic digest, owner, permissions, and provenance before use. Reproducing the environment is not the same as reproducing the binary.

## Snapshot record

For each deployment, record:

```text
host name and Ubuntu release:
machine architecture:
kernel:
AMBER core source/provenance:
left core SHA-256:
right core SHA-256:
left launch SHA-256:
right launch SHA-256:
URDF SHA-256:
Python API SHA-256:
CAN adapter label -> stable interface:
tested hardware revision:
operator and date:
```

Keep this manifest beside the deployment package, not inside an unfiltered home-folder archive.

# URDF is a geometric sentence

> **SOURCE TRAIL — ANALYZING NOW:** `amber_b1.urdf` in the `Amber URDF` folder defines the independent arm. `DualArm.urdf` in the captured `urdf/dual_b1` folder defines the combined model. The code map supplies full paths and side-specific alternatives.

A Unified Robot Description Format file is XML that describes a tree of **links** connected by **joints**. Links carry visual geometry, collision geometry, and optionally mass and inertia. Joints name a parent link, child link, origin transform, axis, type, and limits. Together they let visualization, forward kinematics, inverse kinematics, motion planning, and collision tools speak about the same mechanism.

A URDF answers “where would the next link be if this joint had a known angle?” It does not, by itself, answer:

- where the physical arm is mounted on ROB;
- whether an encoder zero agrees with the model zero;
- whether a limit is mechanically safe under load;
- whether collision meshes include cables, grippers, ROB's body, or a carried object;
- how quickly the real controller stops after communication loss;
- whether the physical robot matches the exported CAD revision.

URDF coordinates use SI conventions: meters, radians, kilograms, and seconds-derived units. An `origin` contains `xyz` translation and roll-pitch-yaw rotation. A revolute joint's angle rotates its child about the declared axis. Composition order and frame ownership must remain explicit; changing signs until a picture “looks right” creates hidden calibration debt.

## The single B1 chain

The independent `Amber URDF/amber_b1.urdf` defines `base_link`, seven numbered links, and joints `joint1` through `joint7`. Every joint axis is the local positive Z axis. These are model limits, not permission to drive to an endpoint:

| Joint | origin xyz (m) | origin rpy (rad) | lower / upper (rad) | modeled velocity |
|---|---|---|---|---|
| 1 | `0 0 0.0825` | `0 0 0` | -2.4435 / 2.4435 | 3.1415 |
| 2 | `0 0 0.0853` | `-1.5708 0 0` | -2.3213 / 2.3213 | 3.1415 |
| 3 | `0 -0.1289 0` | `1.5708 0 0` | -2.2863 / 2.2863 | 3.1415 |
| 4 | `0 0 0.0853` | `1.5708 0 0` | -2.2863 / 2.2863 | 3.1415 |
| 5 | `0 0.1251 0` | `-1.5708 0 0` | -2.2863 / 2.2863 | 5.23 |
| 6 | `0 0 0.0891` | `-1.5708 0 0` | -2.2863 / 2.2863 | 5.23 |
| 7 | `0 -0.1591 0` | `1.5708 0 0` | -3.05 / 3.05 | 5.23 |

The V2 Python wrapper applies a generic software range of approximately ±2.0944 radians to all seven joints. That is not identical to the joint-specific URDF limits. Treat both as inputs to a reviewed safety envelope, never select whichever value permits more motion, and add a robot-specific conservative limit layer above the vendor client.

## The dual model has a warning in its own source

`DualArm.urdf` contains both `L...` and `R...` chains attached to a shared `base_link`. Its leading comment says axes 2, 4, and 6 have opposite rotation directions at the driver layer and warns that left/right labels were defined from an observer-facing convention. The launch files likewise give the solver an alternating rotation-direction vector:

```text
[1, -1, 1, -1, 1, -1, 1]
```

This is not decorative metadata. A sign error can send a physical joint opposite the planned direction. Create one canonical mapping table with columns for physical side, software side, CAN interface, network port, LCM prefix, URDF chain, joint sign, encoder zero, and photographed hardware label. Verify one joint at a time with torque limited and the arm supported.

The current right launch file uses `DualArm.urdf`, while an alternate right configuration uses `DualArmR.urdf`. Reconcile that difference before commissioning. Do not assume the newest filename is correct merely because it is more specific.

# Measure two arms into ROB's coordinate system

The dual-arm CAD base is not automatically ROB's torso frame. Measure the rigid transform from a named ROB body frame to each arm's `base_link`. A useful frame tree is:

```text
rob_base
  -> torso_yaw
      -> left_arm_mount  -> left base_link -> Lseven_Link -> left_tool
      -> right_arm_mount -> right base_link -> Rseven_Link -> right_tool
      -> camera_mount    -> camera_optical
```

Define axes before measuring: for example, X forward, Y left, Z up. Put a durable datum on the torso and each arm plate. Measure translation with calipers, a height gauge, a jig, or a surveyed target; measure rotation from machined surfaces or a calibrated fixture. Take repeated measurements and record uncertainty rather than adding false decimal places.

## Mount-transform worksheet

For each side record:

| Field | Left | Right |
|---|---|---|
| physical label / serial |  |  |
| torso datum description |  |  |
| translation x, y, z (m) |  |  |
| roll, pitch, yaw (rad) |  |  |
| method and instrument |  |  |
| repeated-measurement spread |  |  |
| tool-center-point offset |  |  |
| cable/gripper collision additions |  |  |
| reviewer and date |  |  |

Validate the transform with several poses, not only a home pose. Compare predicted joint centers and tool pose against measured or vision-estimated landmarks. A transform that fits one image may conceal a scale, sign, time-alignment, or lens-calibration error.

# CAN: stable identity before traffic

> **SOURCE TRAIL — ANALYZING NOW:** `initCan.sh` in `amber_core/init` and its adjacent `SerialNumber.txt`. An older `amber/initCAN.sh` also exists; compare rather than merging their assumptions. The code map gives both full paths.

Linux may assign `/dev/ttyACM0`, `/dev/ttyACM1`, and later numbers according to discovery order. Moving a USB adapter to another hub can reorder them. The archived improved initialization script addresses this by reading each adapter's USB serial number, looking it up in `SerialNumber.txt`, and binding the matching adapter to a stable SocketCAN name such as `can10` or `can11`.

The script then runs `slcand` with `-o -c -s8`, brings the interface up, and sets transmit queue length to 1000. Preserve the exact adapter option as an observed configuration value; verify its bitrate meaning against the installed adapter and `slcand` version before connecting hardware.

Two archived `SerialNumber.txt` copies disagree. Unique serials are local inventory, not book content. Read the labels or query the actual adapters, create one authoritative mapping, protect it as machine configuration, and remove obsolete copies.

## Prefer a deterministic host binding

A production setup should avoid parsing historical `dmesg` text and writing temporary files in the working directory. Use udev rules or a small system service that reads `/dev/serial/by-id`, validates that exactly one adapter maps to each logical side, refuses duplicates or unknown devices, creates the intended SocketCAN interface, and verifies it before starting a core.

Read-only checks include:

```text
ls -l /dev/serial/by-id/
ip -details link show can10
ip -details link show can11
ip -statistics link show can10
ip -statistics link show can11
```

Do not transmit diagnostic frames from a generic CAN utility unless the actuator-level protocol and safe state are known. `candump` can observe traffic, but captures may contain device identifiers or operational data and must be handled accordingly.

## CAN fault questions

For each side test and record: adapter absent at boot, swapped adapters, duplicate serial mapping, bus disconnected, bus-off recovery, core crash, client timeout, stale command, Ubuntu restart, and E-stop. The safe response must be measured on the real system. A quiet bus is not proof that an energized arm will hold, brake, or become harmless.

# CAN from copper to Linux

CAN is a shared differential bus, not a USB cable with different plugs. A USB--CAN adapter contains at least three conceptual layers: a USB/serial interface the host can address, a CAN controller that forms and checks frames, and a transceiver that drives the electrical pair. ROB's captured host uses an SLCAN-style serial adapter, so `slcand` translates that serial protocol into a Linux SocketCAN network interface.

```text
Ubuntu host              USB--CAN adapter                 physical arm bus
-----------        ----------------------------      -------------------------
USB host  <------> USB/serial <-> CAN controller <-> CAN transceiver
                                                    | CANH ==================+
                                                    | CANL ==================+ arm nodes
                                                    | GND  ------------------+ reference
                                                  [120 ohm]              [120 ohm]
                                                 physical end            physical end
```

Repeat this as two independent buses: the reviewed host names the left side `can10` and the right side `can11`. Connector pin numbers are deliberately absent because the installed adapter's connector, isolation, termination switch, and pinout have not been verified. Never guess CANH, CANL, or GND from wire color.

The two signal wires carry one differential value. In a recessive state neither node forces a dominant differential. In a dominant state the transceiver separates CANH and CANL. Receivers compare the pair, which helps reject noise coupled similarly into both conductors. The reference ground keeps transceiver common-mode voltage inside its allowed range; it is not a third copy of the data.

High-speed CAN normally uses 120-ohm termination at the two physical ends of a linear trunk. With all power removed and after the hardware procedure approves resistance measurement, two 120-ohm end resistors appear in parallel as roughly 60 ohms across CANH and CANL. A very different reading can indicate missing termination, extra termination, an attached circuit, or a fault; it is a clue, not a complete diagnosis. Keep stubs short and do not build a star simply because several connectors are convenient.

## What one CAN frame teaches

A classical CAN data frame contains arbitration, control, data, error-detection, acknowledgement, and framing fields. The identifier both labels the message and participates in arbitration. A lower numerical identifier can win arbitration because dominant bits overwrite recessive bits without corrupting the winner. That is deterministic access to a busy bus, not authentication or permission.

The controller computes a CRC, receivers acknowledge a valid frame, and nodes maintain transmit/receive error counters. A sufficiently faulty node can progress through error-active, error-passive, and bus-off states. Those mechanisms detect communication faults; they do not tell an AMBER joint whether a requested angle is mechanically safe. Application policy still needs side identity, mode, limits, freshness, units, trajectory validation, and an independent stop.

Do not confuse these names:

- **USB — host transport:** connects Ubuntu to the adapter.
- **SLCAN — adapter serial protocol:** a text/binary convention consumed by `slcand`; the exact adapter dialect must match.
- **SocketCAN — Linux software interface:** exposes `can10` and `can11` through the networking API.
- **CANH/CANL — electrical physical layer:** the twisted differential pair at the arm harness.
- **CAN identifier/data — link-layer frame:** the actuator-protocol details remain proprietary or unverified in this snapshot.
- **AMBER UDP/LCM — higher-level host interfaces:** commands and feedback handled by the vendor core and ROB gateway.

## Read the deterministic initializer line by line

The reviewed `rob_amber_init_can.py` is intentionally non-motion code. Its key decisions are worth learning:

- **`EXPECTED_INTERFACES = {"can10", "can11"}`:** refuses extra or missing logical sides.
- **Open the mapping with `O_NOFOLLOW`:** rejects a substituted symbolic link.
- **Require root ownership and no group/world write bit:** prevents an ordinary account from silently swapping arm identities.
- **Walk `/sys/class/tty/.../serial`:** binds by USB serial rather than discovery order.
- **Require exactly one device per reviewed serial:** fails closed on absence or duplicates.
- **Reject a pre-existing interface:** avoids attaching a second process to stale state.
- **Run `slcand -o -c -s8 device interface`:** creates the observed SLCAN interface; the adapter-specific meaning of `-s8` must be verified.
- **Run `ip link set ... up`:** enables the SocketCAN interface only after identity succeeds.
- **Set `txqueuelen 1000`:** records the host queue choice; it does not authorize a thousand motion commands.

The process suppresses child output and applies timeouts, so an operator should diagnose through its own clear success/error lines plus service logs. It never opens a CAN socket or sends a CAN, UDP, LCM, mode, trajectory, or motion request. Keep that narrow contract.

# Configure one core per side

> **SOURCE TRAIL — ANALYZING NOW:** return to the two `launch.json` files. The executables beside them are captured binaries, not readable source; the book documents their configured boundary without claiming to analyze their internal CAN implementation.

Both current launch files select `CAN_BUS`, seven degrees of freedom, a 200 Hz control frequency, gear ratios of 50, a gripper numbered 8, Drake solving, UDP, and ROS 2. Their maximum-velocity, acceleration, and jerk arrays are controller configuration units. The files do not prove those values are safe physical SI limits.

Important left settings are:

```json
Hub_CAN_Name: can10
LCM Prefix: Left_
URDF_Path: ./urdf/dual_b1/DualArmL.urdf
EEF_Name: Lseven_Link
UDP_Port: 26001
```

Important right settings are:

```json
Hub_CAN_Name: can11
LCM Prefix: Right_
URDF_Path: ./urdf/dual_b1/DualArm.urdf
EEF_Name: Rseven_Link
UDP_Port: 26002
```

Keep separate working directories if the executable resolves the URDF path relative to its current directory. Capture standard output and standard error under a supervised service. Give each core its own non-root account where possible, explicit working directory, read-only configuration, restart policy, resource limits, and dependency on its CAN interface. Do not automatically restart into an energized motion mode.

# The observed UDP protocol

> **SOURCE TRAIL — ANALYZING NOW:** `amber_robot.py` in Cerebro's AMBER V2 API provides the high-level wrapper. Exact packed structures live in its `basic_cmd` directory: `cmd_1.py`, `cmd_4.py`, `cmd_6.py`, `cmd_7.py`, `cmd_9.py`, `cmd_10.py`, and `cmd_110.py`.

The V2 Python API uses packed `ctypes.Structure` records sent in UDP datagrams. Every observed message begins with:

| Field | Type | Meaning |
|---|---|---|
| `cmd_no` | unsigned 16-bit | operation number |
| `length` | unsigned 16-bit | structure byte length |
| `counter` | unsigned 32-bit | request/reply correlation value |

The structures set `_pack_ = 1`, so there is no padding. They do not declare explicit network byte order; current serialization therefore relies on the client's native representation. That is an implementation fact, not a good cross-platform protocol guarantee.

## Command catalogue

- **1 — status:** no request payload. The reply carries eight joint positions, eight joint speeds, six Cartesian positions, six Cartesian speeds, and arm angle.
- **4 — joint move:** eight floats plus a duration float. The reply carries a one-byte response.
- **6 — Cartesian move:** XYZ, RPY, arm angle, and duration as floats. The reply carries a one-byte response.
- **7 — calibration:** an unsigned 32-bit actuator number. The reply carries a one-byte response.
- **9 — gripper:** unsigned 16-bit action, unsigned 16-bit intensity, and Boolean version. The reply carries a one-byte response.
- **10 — set mode:** an unsigned 16-bit mode. The reply carries a one-byte response.
- **110 — get mode:** no request payload. The reply carries seven unsigned 16-bit mode values.

The high-level wrapper exposes seven joint targets even though the status and move packet allocate eight floats. Gripper control is separate and uses actuator number 8. Preserve this difference when writing another client.

Observed modes are inactive 0, active 1, position 2, speed 3, and current 4. The API documentation says transitions involving position or current pass through active mode and may briefly cut power, allowing an unsupported arm to drop. Support the mechanism before mode changes and verify actual behavior with the vendor and a controlled test.

The API uses meters and radians at its high-level interface. `move_j` accepts seven joint angles and a duration. `move_c` accepts XYZ plus roll-pitch-yaw and a duration. `get_status` returns the first seven joint positions and a six-element Cartesian pose. “Position returned” does not prove the physical pose is correctly zeroed after a controller boot.

## Gripper sequence

The V2 examples calibrate actuator 8 after each power cycle, then use action 0 for open and action 1 for close with an integer intensity. Calibration moves hardware: keep fingers, cables, and objects clear. The code alone does not establish a safe force or intensity for ROB's installed grippers.

## Protocol hardening needed

The current client waits up to three seconds and accepts the next datagram. It does not consistently validate source endpoint, command number, declared length, counter, exact received size, freshness, or authentication before decoding. UDP also offers no delivery, ordering, or uniqueness guarantee.

A production adapter should:

1. bind each arm to an allowlisted endpoint and side identity;
2. encode endianness explicitly or preserve a tested compatibility codec;
3. validate datagram size before deserialization;
4. match command and counter to an outstanding request;
5. reject stale, duplicate, unsolicited, or non-finite values;
6. enforce conservative joint, rate, workspace, and mode policy locally;
7. use an authenticated protected network or authenticated gateway;
8. stop issuing motion on timeout without claiming that a software stop replaces the E-stop;
9. log decisions without logging credentials;
10. fuzz the decoder away from hardware.

The older V1 examples commonly use port 25001, whereas the current two-core launch files use 26001 and 26002. Select ports from reviewed configuration, not from whichever example happens to run.

# LCM and ROS 2 interfaces

> **SOURCE TRAIL — ANALYZING NOW:** the captured `sin_wave/rawLcm` directory contains human-readable `.lcm` schemas. Nearby `lcmTypes` Python files are generated outputs; edit and regenerate from the schema definitions.

The saved LCM configuration composes channels from a side prefix and suffix. Examples are `Left_PosCmd`, `Left_ArmStatus`, `Right_PosCmd`, and `Right_ArmStatus`. Other configured suffixes include position plans and tasks, inverse- and forward-kinematics tasks, solver responses, mode changes, and gripper control.

The raw definitions establish these payloads:

| LCM type | fields |
|---|---|
| `posCmd_t` | seven double joint targets |
| `rosData_t` / generated arm status | seven positions, velocities, currents, and statuses |
| `cartesian_t` | six XYZ/RPY doubles and duration |
| `gripperCtrl_t` | 8-bit action and 32-bit intensity |
| `simplePositionTask_t` | timestamp, actuator count, one point, duration |
| `positionTask_t` | timestamp, actuator count, point sequence, time sequence |
| `positionPlan_t` | frequency, timestamp, actuator count, point sequence |
| `solverRespond_t` | 32-bit response |

The archived examples use multicast at `239.255.76.67:7667` with TTL 10 and add a multicast route. Multicast can reach more listeners than expected. Put it on a controlled robotics network, choose the intended interface explicitly, and firewall unrelated hosts. Generate language bindings from the checked-in `.lcm` files so the schema hash remains consistent; do not hand-maintain parallel definitions.

The hardened gateway service uses `LCM_DEFAULT_URL=udpm://239.255.76.67:7667?ttl=0`, which is more restrictive than the historical TTL-10 examples. A TTL of zero confines multicast packets to the local host. Preserve that distinction in diagrams: the local gateway subscribes to core status without granting a campus or home network permission to receive or inject arm traffic. Verify the actual LCM provider and interface with packet capture on an isolated bench before relying on the boundary.

The launch files also enable ROS 2 and historical install scripts include Humble, MoveIt, controllers, `xacro`, and joint-state tools. The snapshot does not show a complete reviewed ROS 2 launch package for ROB. Treat ROS 2 capability as enabled configuration, not proof that names, quality-of-service policy, controller ownership, and safety behavior are production-ready.

# LCM workshop: schema, generated code, and the Python bridge

LCM separates a human-readable schema from generated language bindings. Start with the `.lcm` file, not the generated Python. For example, an arm-status schema declares four fixed seven-element arrays: joint position, velocity, current, and status. The generated `armStatus_t.py` knows the binary layout and embeds a type fingerprint. If one participant edits generated code by hand while another regenerates from the schema, the system can drift in a way that looks like network failure.

A reproducible generation exercise, performed away from powered arms, is:

```text
mkdir -p build/lcm-python
lcm-gen -p --ppath build/lcm-python amber/sin_wave/rawLcm/armStatus_t.lcm
python3 -m compileall build/lcm-python
```

The exact source filename must come from the checked-in tree. Archive the generator version, input hash, generated output hash, and import-path test. A schema change is a protocol release: update every producer and consumer together, add compatibility or reject the old hash explicitly, and retain a rollback artifact.

The gateway's `LCMStatusBridge` is short enough to understand line by line:

```python
self._lcm = lcm.LCM()
self._lcm.subscribe(arm.status_channel, self._handler(name))
...
message = self._arm_status_type.decode(data)
state.positions = list(message.jointPosition)
state.monotonic_ns = time.monotonic_ns()
state.sequence += 1
...
self._lcm.handle_timeout(100)
```

1. `lcm.LCM()` reads the reviewed provider URL from the service environment.
2. `subscribe(...)` connects one side-specific channel, such as `Left_ArmStatus`, to a closure that remembers the side.
3. `decode(data)` validates the generated LCM type fingerprint and reconstructs typed arrays. It does not validate physical plausibility.
4. Copying arrays detaches gateway state from the generated message object.
5. `time.monotonic_ns()` records local receipt time so wall-clock changes cannot make stale feedback look fresh.
6. `sequence += 1` creates a gateway-local observation counter; it is not an actuator sequence from the CAN bus.
7. `handle_timeout(100)` lets the thread check its stop event at least every 100 ms instead of blocking forever.

A lock protects the shared `ArmState` while the LCM thread writes and the asyncio telemetry task reads. `snapshot()` returns copies, not the mutable lists. That is the small but crucial bridge between a callback-oriented native library and an asynchronous TCP server.

## Follow one status sample end to end

```text
joint electronics -> CANH/CANL -> AMBER core -> Left_ArmStatus LCM
  -> generated armStatus_t.decode -> locked ArmState copy
  -> gateway telemetry JSON -> authenticated Cerebro client -> operator display
```

At each arrow write what can be proven. The gateway knows when the LCM message arrived, not when the joint sensor sampled. It knows the configured channel side, not that the adapters were physically installed on the correct arms. It can reject stale gateway state, not prove encoder zero or calibration. Good telemetry carries those uncertainties instead of turning arrival into truth.

# Understand the Ubuntu services

The checked-in `rob-amber-gateway.service` is a systemd unit for the hardened Python bridge. Read it in four blocks.

- **`After=network-online.target rc-local.service`:** start ordering waits for networking and the root-owned CAN initializer.
- **`Requisite=rc-local.service`:** a failed required initializer prevents the gateway from pretending it is usable.
- **`User=amber`, `Group=amber`:** network translation runs without root privileges.
- **`WorkingDirectory=/home/amber/rob_gateway`:** relative paths have one declared base.
- **`LCM_DEFAULT_URL=...ttl=0`:** status multicast remains local to the host.
- **`--listen-host 127.0.0.1`:** the gateway accepts Cerebro only through a local or forwarded boundary in this configuration.
- **`Restart=on-failure`, `RestartSec=2`:** crashes retry after a delay; a restart does not grant motion authority.
- **`NoNewPrivileges=true`:** the process cannot gain new privilege through execution.
- **`PrivateTmp=true`:** temporary files are isolated from other services.
- **`ProtectSystem=strict`:** the normal filesystem is read-only to this unit.
- **`ProtectHome=read-only`:** home content is not writable.
- **`ReadOnlyPaths=/home/amber/sin_wave`:** LCM schemas and generated types are treated as runtime inputs.

Use read-only service commands first:

```text
systemctl cat rob-amber-gateway.service
systemctl status --no-pager rob-amber-gateway.service
journalctl -u rob-amber-gateway.service --since today --no-pager
systemctl show rob-amber-gateway.service -p User -p Group -p MainPID -p ActiveState
```

`status` tells whether the process is running, not whether CAN identities, arm calibration, feedback freshness, and physical stop are correct. Sanitize logs before sharing them: authentication tokens must never be printed, and operational poses may still be sensitive.

# The hardened Cerebro-to-AMBER gateway

The new Python gateway narrows the older collection of scripts into one explicit boundary:

```text
Cerebro
  -> authenticated, ordered newline-delimited TCP
  -> one exclusive ClientSession
  -> bounded per-arm asyncio command queue
  -> packed local UDP request to port 26001 or 26002
  -> vendor AMBER core

AMBER core -> side-specific LCM status -> LCMStatusBridge -> 20 Hz telemetry -> Cerebro
```

The gateway begins each client with a random challenge, expects protocol name `rob-amber-gateway/1` and a token checked with constant-time `hmac.compare_digest`, and permits only one authenticated controller session. A token is still a credential: load it from protected configuration, rotate it, never place it in a screenshot, and prefer an authenticated protected tunnel when the connection leaves loopback.

Motion-like operations require increasing unsigned 32-bit command IDs and a fresh heartbeat. Heartbeat authority expires after 2.5 seconds. Per-arm queues are capped at 32 entries, UDP exchanges are serialized by side, and replies must match command number and counter. A `priority_hold` purges queued work before it is inserted. Leased trajectories accept only a bounded 700--1500 ms lease and are held when that lease expires. These are strong software controls, not a replacement for a hardware stop or vendor drive limits.

The packed `ctypes.LittleEndianStructure` definitions explain the vendor UDP boundary. For a joint command, the code writes a 16-bit command number, 16-bit structure length, 32-bit counter, eight 32-bit floats, and one duration float. The public gateway accepts seven joints and deliberately sets the eighth float to zero because gripper control is a separate operation. `ctypes.sizeof(...)` becomes the declared length, and a response is rejected when it is short or its counter differs.

The concurrency lesson is as important as the bytes. Blocking UDP work runs through `asyncio.to_thread`, but each arm owns an `asyncio.Lock`. Shutdown waits for worker completion rather than cancelling a wrapper while its underlying thread may still complete a real UDP request. Session generations and motion-authority generations make late work stale after controller replacement or heartbeat expiry.

## A safe code-reading lab

With arm power isolated, trace one `mode_query` request on paper:

1. TCP parser rejects oversized or malformed JSON.
2. message allowlist accepts `mode_query`.
3. command ID and arm side are validated.
4. the request enters only that side's bounded queue.
5. its worker acquires the side operation lock.
6. the UDP codec sends command 110 to the configured side port.
7. response command/counter/size are checked.
8. the gateway returns a correlated acknowledgement.
9. independent LCM telemetry continues to report measured state.

Now inject paper faults: repeated command ID, wrong side, queue full, stale heartbeat, short UDP reply, mismatched counter, LCM older than 250 ms, and disconnect during a blocking exchange. The correct answer is often rejection or loss of authority, not a retry that could duplicate motion.

# Build a clean Ubuntu runtime

Begin with a supported Ubuntu release compatible with the authorized AMBER core binary and required Drake/ROS packages. The historical scripts target ROS 2 Humble and install CMake, `net-tools`, `can-utils`, Python 3 compatibility, gflags, glog, Drake, MoveIt, and controller packages. They are evidence, not a safe unattended installer: one script pipes a remote GitHub script directly into a shell, and package repositories and keys can change.

## Reproduction procedure

1. Record the original host manifest and binary hashes.
2. Install a fresh minimal Ubuntu system; patch it before connecting ROB hardware.
3. Create a dedicated unprivileged runtime account. Keep SSH keys outside the deployment archive.
4. Install reviewed, pinned packages from official repositories. Save package versions and repository fingerprints.
5. Install `can-utils`, the adapter's `slcand` support, required C/C++ runtime libraries, and only the ROS/Drake components actually used.
6. Copy authorized core binaries, launch JSON, URDF meshes, and LCM definitions into versioned application directories. Do not copy `.ssh`, shell history, logs, caches, or the archived virtual environment.
7. Create and verify the stable adapter-to-`can10`/`can11` mapping.
8. Validate JSON syntax, URDF XML, mesh paths, file permissions, ports, prefixes, side labels, and hashes while arm power is isolated.
9. Start each core under a service supervisor with its own working directory and logs.
10. Run network status probes before requesting any control mode.
11. Save the completed acceptance record and rollback package.

Useful non-motion checks are:

```text
uname -a
lsb_release -a
ip -br link
ss -lunp
sha256sum amber_core_L amber_core_R
xmllint --noout path/to/model.urdf
python3 -m compileall path/to/reviewed/client
```

Run `ldd` on the core executables and record every resolved library, but do not assume “not found” can be fixed by copying random libraries from the old host. Resolve dependencies from known packages or the authorized vendor distribution.

## Service order

The safe logical order is network policy, CAN discovery, CAN validation, left core, right core, read-only status clients, operator UI, then a separately authorized mode transition. Shutdown reverses authority first: stop new commands, return through the documented mode procedure, verify the result, stop clients and cores, then isolate energy according to the hardware procedure.

# A status-only Python lesson

> **SOURCE TRAIL — ANALYZING NOW:** import behavior comes from `amber_api/__init__.py` and `amber_robot.py` inside Cerebro's AMBER V2 API. Read the directory-local `README.md` and `LICENSE` before installing or redistributing it.

Use the repository's reviewed V2 package rather than reproducing packet layouts in multiple applications. The first test should only request state:

```python
from amber_api import Amber_Robot

left = Amber_Robot("LEFT_CORE_ADDRESS", 26001, joint_count=7)
right = Amber_Robot("RIGHT_CORE_ADDRESS", 26002, joint_count=7)

for name, arm in (("left", left), ("right", right)):
    joint_position, cartesian_pose = arm.get_status()
    print(name, joint_position, cartesian_pose)
```

Run this on an isolated, authorized robotics network with motion disabled. Confirm seven finite values, plausible ranges, correct side identity, stable repeated readings, and behavior when one core is intentionally unavailable. Do not call `set_mode`, `move_j`, `move_c`, zero, calibration, or gripper functions during the discovery test.

The repository wrapper has details to audit before production. Its default wait tolerances differ between layers, and one Cartesian wait default is represented differently from the code that indexes it. Add tests for defaults, short replies, wrong counters, NaN, infinity, lost packets, reordering, and simultaneous left/right requests.

# Commission from no motion to bounded motion

## Gate 0: paper review

Confirm ownership of the stop system, swept-volume boundary, side mapping, power isolation, support fixture, conservative limits, rollback, and observer roles. Resolve the right-URDF discrepancy and serial-map discrepancy.

## Gate 1: power isolated

Validate host, files, hashes, adapters, interfaces, ports, process permissions, URDF parsing, and network policy. Confirm the physical E-stop interrupts the intended energy path using the approved electrical test procedure.

## Gate 2: status only

Start one core and one read-only client. Verify source endpoint, side, joint count, finite values, update timing, disconnection behavior, and logs. Repeat independently for the second side. Then observe both without commanding either.

## Gate 3: supported, torque-limited joint identification

With the arm mechanically supported and the area clear, an authorized operator enables the minimum suitable mode and requests a tiny change to one joint. A second person watches the physical joint and stop. Record commanded sign, observed sign, encoder change, current, latency, and stop result. Return to the approved neutral state before advancing to the next joint.

## Gate 4: model agreement

Compare measured link landmarks with forward-kinematics predictions over several conservative poses. Validate left/right frames, joints 2/4/6 signs, tool transforms, and torso mounts. Do not run inverse kinematics until forward kinematics and feedback agree.

## Gate 5: independent single-arm envelopes

Test each arm alone inside a conservative workspace that excludes ROB, the other arm, cables, observers, and floor. Measure stopping and fault behavior. Add collision objects for the torso, head, shoulder structure, gripper, and cable volume.

## Gate 6: dual-arm coordination

Only after both single-arm cases pass should a planner own both arms in one collision model. Test mirrored commands, crossing workspaces, communication loss on one side, cancellation, and one-arm faults. “Two scripts happened to run” is not coordinated dual-arm control.

# Diagnose by layer

- **No `can10` or `can11`:** inspect adapter identity, udev/service state, `slcand`, and link state. Do not yet conclude that arm electronics failed.
- **Core will not start:** inspect working directory, launch JSON, URDF and mesh paths, and libraries. Do not yet conclude that CAN is defective.
- **UDP timeout:** inspect the process, listener, address, port, firewall, and route. Do not yet conclude that the arm is powered off.
- **Wrong arm responds:** inspect endpoint, port, prefix, CAN mapping, and physical label. Do not yet conclude that joint signs are correct.
- **Model bends backward:** inspect side convention, joints 2/4/6 mapping, zero, and URDF selection. Do not yet conclude that hardware must be rewired.
- **Status jumps at boot:** inspect zeroing state, mode transition, and packet validation. Do not yet conclude that visual pose is trustworthy.
- **LCM silence:** inspect multicast interface, route, channel prefix, and schema version. Do not yet conclude that UDP is also broken.
- **Gripper does nothing:** inspect actuator 8 identity, required calibration, mode, and response validation. Do not respond by assuming higher intensity is safe.

Collect one synchronized incident bundle: UTC time, host manifest, core hashes, launch hashes, interface statistics, process status, sanitized logs, request counter, response source, operator action, and physical observation. Never collect private keys or passwords into a diagnostic archive.

# Connect the arms to Cerebro responsibly

> **SOURCE TRAIL — ANALYZING NOW:** Cerebro has one AMBER V2 directory under `TaskControllers` and another under `Amber-PythonAPI`. The chapter recommends consolidating these entry points. The code map prints both exact paths.

Cerebro should expose one typed arm service rather than launching miscellaneous Python scripts with implicit addresses. Its interface should name side, joint, units, duration, correlation identifier, desired mode, deadline, and operator authority. Returned state should include measured joint position, velocity, current/status when available, receive time, source, mode, and confidence in calibration.

Keep four layers separate:

1. **Transport adapter:** validates UDP/LCM and reports communication health.
2. **State estimator:** time-aligns joint feedback, camera observations, and ROB transforms.
3. **Safety policy:** enforces state, limits, workspace, collision, freshness, and authority.
4. **Behavior layer:** asks for a grasp, gesture, or pose without gaining raw packet access.

Visual pose estimation can detect disagreement and help calibrate mounting or joint offsets, but it should not overwrite joint truth continuously without observability checks. Some poses hide joints; cameras occlude; symmetric links create ambiguous solutions; rolling shutter and latency distort motion. Fuse visual evidence with actuator feedback and keep uncertainty explicit.

For every command, the UI should show the selected physical arm, current mode, last feedback age, calibration revision, joint values, network/CAN health, and whether motion authority is present. A green connection indicator must never mean “safe to enter the workspace.”

# What remains unknown

The repository gives ROB a strong starting point, but honest documentation preserves these open items:

- authorized source and version history for the Ubuntu core binaries;
- exact actuator-level CAN identifiers, frame encodings, checksums, timing, and fault semantics;
- the adapter option's verified bitrate on the installed hardware;
- authoritative stable serial-to-side inventory;
- correct right-arm URDF selection;
- exact measured torso-to-arm and arm-to-tool transforms;
- encoder-zero behavior across power cycles;
- joint, current, temperature, payload, and gripper limits for ROB's installation;
- collision geometry including cables and body additions;
- core behavior on stale command, malformed packet, bus-off, client loss, and E-stop;
- authenticated network design and software-update provenance;
- complete reproducible source build for the AMBER core.

Unknown does not mean failure. It means the next experiment has a clear question.

# Reproduction acceptance sheet

Before labeling a replacement Ubuntu box ready, require signatures for:

- [ ] clean operating-system install and patch record;
- [ ] pinned package and repository manifest;
- [ ] authorized binary provenance and matching hashes;
- [ ] no credentials, history, caches, or old logs copied from the snapshot;
- [ ] stable physical left/right adapter mapping;
- [ ] `can10` and `can11` independently verified;
- [ ] launch JSON and URDF syntax verified;
- [ ] right-arm URDF choice resolved;
- [ ] unique UDP ports and LCM prefixes verified;
- [ ] read-only status from each side tested alone and together;
- [ ] packet source, length, command, counter, freshness, and value validation tested;
- [ ] physical E-stop and fault behavior tested by the responsible engineer;
- [ ] conservative joint and workspace policy installed;
- [ ] mounting and tool transforms measured with uncertainty;
- [ ] forward kinematics checked against multiple physical poses;
- [ ] single-arm tests passed before dual-arm tests;
- [ ] sanitized logs, rollback package, and operator procedure archived.

# Teach it as a systems lesson

The most important AMBER lesson is not a magic command. It is traceability across representations. A child may see a hand wave. An engineer must be able to follow that event backward: tool pose, seven joint angles, a planned trajectory, a side-specific channel, a validated network message, one Ubuntu core, one stable CAN interface, actuator feedback, and a physical mechanism attached to a measured frame.

Build a paper exercise with two cardboard seven-link chains. Label every joint and give each arm a different color. Learners route a “move left wrist” card through behavior, safety policy, network, Ubuntu core, CAN, joint, and feedback stations. Insert fault cards: swapped adapter, stale packet, wrong sign, hidden camera marker, blocked arm, or missing status. The team wins by refusing unsafe ambiguity and locating the layer that owns the evidence—not by moving fastest.

That is how two complex arms become understandable: not by hiding the details, but by giving every detail a name, a source, a test, and a responsible human owner.
