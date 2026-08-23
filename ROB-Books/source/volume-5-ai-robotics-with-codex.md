# Building R.O.B.

## AI, Robotics, and the Codex-Accelerated Evolution of ROBController and Cerebro

**A source-based field guide**  
Expanded repository-integration edition, August 23, 2026

---

## Preface: one builder, many keyboards

R.O.B. did not begin as an “AI-written robot.” It began the normal way: one
person, several computers, physical hardware, partial ideas, experiments that
worked once, experiments that broke connectors, and commits made before a
fragile discovery disappeared.

The Git record uses three author-name spellings—`Orbitus`, `RudyAramayo`, and
`Rudy Aramayo`—but the same `orbitus@orbitusrobotics.com` email. That is
consistent with one builder committing from differently configured computers.
It is not evidence of three developers. Nor can Git prove which lines were
suggested by an AI. Commit metadata records the person who accepted and
committed a change, not every tool involved in producing it.

Still, the history has a visible hinge. Through September 2025, commits read
like a lab notebook: tune a servo, repair a port, checkpoint an animation,
avoid sending commands too quickly. Beginning August 1, 2026, the repositories
gain coordinated transport protocols, certificate pinning, Keychain-backed
pairing, formal message schemas, fixture tests, failure boundaries, and long
operator documents. ROBController's first large 2026 change adds roughly 5,345
lines and Cerebro's adds roughly 16,478. That is the point at which the work
*looks AI-accelerated*.

This book treats August 1, 2026 as the start of the Codex-accelerated era. That
is an interpretation based on scale and engineering form, not an authorship
claim. Rudy remains the author and operator: the person choosing the goal,
checking the diff, testing the hardware, and assuming responsibility for what
the robot does.

---

## 1. The robot is a distributed system

> **SOURCE TRAIL — ANALYZING NOW:** use Cerebro's main Objective-C++ view controller, ROBController's `ConsciousViewController.mm`, and ROBControllerVision's `ContentView.swift`. These are three entry points into one distributed robot. `OPEN-SOURCE-CODE-MAP.md` prints the exact full paths.

R.O.B. is best understood as two cooperating products.

`ROBController` is the operator edge. It runs on Apple mobile devices, accepts
human intent, shows state, relays Watch commands, and acts as the approval
console. `Cerebro` is the robot-side macOS application. It owns perception,
speech, AI sessions, serial hardware, Python helpers, arm scripts, autonomy,
stage shows, and the server side of the control link.

The important flow is:

```text
human / Apple Watch
        |
        v
ROBController -- authenticated intent --> Cerebro -- bounded commands --> hardware
        ^                                  |
        |                                  +--> cameras / lidar / speech / AI
        +---------- status and results ----+
```

This architecture implies a rule that should govern every future change:

> Generative AI may propose intent; deterministic software and an accountable
> operator decide whether that intent can become physical motion.

Robot code has consequences that ordinary application code does not. A UI bug
is inconvenient. A stale nonzero tread command, a wrong joint sign, or an
unbounded action queue can injure someone or damage hardware. The mature code
therefore does more than add intelligence. It constrains intelligence.

---

## 2. Era one: handmade foundations, 2022–2023

ROBController's 2022 root commit established the controller around AutoNet and
ROBONet after earlier ML-model experiments were removed. It mixed Objective-C,
Objective-C++, Swift, C, and C++, plus Apple's AurioTouch sample-derived audio
machinery. This was a practical choice: keep the old hardware-facing code and
add modern Apple code where it helped.

In September 2023, the controller gained a custom iPhone storyboard, text
commands, lidar visualization, speech-recognition work, system-volume tests,
TCP no-delay tuning, layout cleanup, and an early Watch app. These changes are
recognizably exploratory. UI, network behavior, and speech lifecycle were
being discovered together.

### What Codex should learn from this era

Do not begin a legacy-robot task by rewriting the language mix. First ask Codex
to map ownership and data flow:

```text
Inspect ROBController without changing files. Trace a command from the iPhone
or Watch UI through AutoNet serialization to the network send. Identify the
Objective-C/Swift boundary, thread or queue transitions, and every place a
stale command can survive. Cite files and line numbers. Mark uncertainty.
```

The useful output is a map, not code. Once the map is reviewed, request the
smallest change that proves the model correct. This protects working legacy
behavior while Codex builds context.

---

## 3. Era two: the solo workshop, August–September 2025

Cerebro's fresh repository begins August 5, 2025, but its initial import is
already a substantial robot program. It includes a macOS storyboard, camera
management, speech, serial control, AutoNet, lidar, Kinect/RealSense-era
components, Leap Motion, RTSP video, task launchers, Core ML assets, and a large
body of mixed Objective-C++ and Swift.

The following weeks read like a maker's engineering diary:

- Gemini is connected, speech delays are adjusted, and OAK camera input begins.
- Camera devices become discoverable at runtime.
- A new upper-neck servo is introduced and calibrated.
- RPLidar launch paths and wake-word handling are repaired.
- Output language propagates from controller to robot voice.
- Amber arm v1/v2 scripts are integrated, corrected, and exercised against real
  L10 and R11 arms.
- Keyframes and dual-arm sequences grow from manual experiments.
- Vision person segmentation, 3D body pose, SceneKit skeletons, and whole-body
  overlays are added.
- Speech wordiness, “shut up,” camera toggling, and head tracking become
  operator features.

The commit messages are valuable technical evidence. One warns that arm values
are “very scary if the values go wrong.” Another records a damaged CAN
connector. Another checkpoints code before rebuilding a pose view on every
camera frame. These are not embarrassing details. They express the central
truth of robotics: hardware provides the final test, and the cost of a bad
assumption can be physical.

### Turning workshop knowledge into specifications

Before asking Codex to touch hardware code, translate lived knowledge into
invariants:

```text
Goal: add a head-tilt command.

Constraints:
- Never emit a value outside the calibrated channel-2 range.
- A missing device must disable only head tilt.
- Manual stop must preempt queued motion.
- Preserve existing torso and camera behavior.
- Add a pure serialization fixture before editing the serial path.
- Do not claim hardware validation; give me an exact on-robot checklist.
```

This prompt is good because it tells Codex what must remain true. It does not
dictate an implementation before the repository has been inspected.

---

## 4. The acceleration hinge: August 1, 2026

The paired August 1 commits transform both applications.

In ROBController, the large change introduces secure v2 transport, the Watch
companion path, action and Watch command protocols, approval/status surfaces,
autonomy controls, tests, and documentation.

In Cerebro, the corresponding change introduces the server side of the secure
control plane, Gemini Robotics Live integration, an autonomy coordinator,
camera H.264 transport for Vision Pro, a supervised Python runtime, system
dependency management, action/video protocols, extensive tests, and a major
documentation set.

This is the maturity jump. The old system primarily moved bytes and trusted its
environment. The new system names roles, versions messages, authenticates
peers, bounds queues, records operator intent, and fails closed.

### Why this resembles AI-assisted engineering

No single clue proves AI use. Together, these clues make acceleration a
reasonable inference:

1. Change size increases by an order of magnitude.
2. Both sides of a distributed protocol evolve together.
3. Production code arrives with fixture and integration tests.
4. Threat-model concerns—pinning, replay resistance, downgrade prevention,
   revocation, role checks—are addressed systematically.
5. Operator documentation explains contracts and incomplete capabilities.
6. Later commits use structured conventional-commit language and detailed
   implementation summaries.

The right conclusion is not “AI replaced the programmer.” It is “the builder
acquired a fast engineering collaborator, and the repository began to preserve
more of the reasoning that previously lived only in the builder's head.”

---

## 5. Rebuilding the secure control plane with Codex

> **SOURCE TRAIL — ANALYZING NOW:** compare the identically named protocol files in ROBController's `AutoNetClient` and Cerebro's `AutoNetShared`. Then read the transport-security and integration fixtures. The code map gives every exact filename and full path.

The v2 control plane is the strongest example of how to use Codex on a
cross-repository change.

### 5.1 Start with a contract

Ask for a design before edits:

```text
Analyze ROBController and Cerebro together. Design a versioned replacement for
the plaintext robot-control path. Requirements: QUIC with TLS 1.3, exact server
certificate pinning, per-device pairing secrets in Keychain, reciprocal proof
of possession, controller and lidar roles, persistent revocation, no automatic
legacy downgrade, bounded framing, and deterministic fixture tests. Identify
the files on both sides and list migration risks. Do not edit yet.
```

Review the design for four separations:

- **Identity:** which Cerebro instance is this?
- **Pairing:** has this device been enrolled?
- **Authorization:** is it an operator or telemetry publisher?
- **Freshness:** is this proof from the current connection rather than a replay?

Only then authorize implementation in checkpoints.

### 5.2 Implement the shared wire format first

Message formats should have explicit magic bytes, versions, lengths, limits,
and error behavior. Generate the same golden fixtures on client and server.
Codex is especially useful here because it can compare two implementations and
find drift.

```text
Implement only the v2 frame codec and fixtures in both repositories. Do not
open sockets and do not modify UI. Reject unknown mandatory versions, oversized
payloads, truncated frames, and invalid role/action combinations. Run the
fixture tests and show the exact diff.
```

### 5.3 Add transport without weakening authentication

QUIC/TLS encrypts a connection, but encryption alone does not tell a controller
that it reached *its* robot. ROBController pins Cerebro's certificate. Pairing
then proves possession of a separate per-device secret, while Cerebro resolves
the device role from its own registry.

The August 10 fixes demonstrate why network handshakes need state-machine tests.
iOS did not always expose Bonjour TXT metadata, and both peers could wait for
the other to speak. The repair adds a padded pairing hello before the server
sends its challenge, validates the controller ID, and preserves pinning and
reciprocal proof.

A productive debugging prompt is:

```text
Diagnose the QUIC pairing stall using both repositories. Draw the client and
server state machines from connection start through authenticated readiness.
Find any state where both peers await input. Preserve certificate pinning,
device-role lookup, and reciprocal proof. Add a regression fixture for the
deadlock before changing production code.
```

Never “fix” a handshake by skipping verification or silently falling back to
plaintext. Availability bugs must not become authentication bugs.

---

## 6. Operator authority, Watch control, and autonomy

ROBController becomes more than a joystick in the mature system. It relays
Watch intent, advertises accepted action capabilities, approves proposed robot
actions, and starts a bounded autonomy session.

The autonomy model is intentionally a session, not indefinite permission. The
`social_roam` profile captures an activation pose, stays within a radius, uses
fresh lidar, moves slowly, and ends on manual control, explicit stop, or
Cerebro restart. Meanwhile `ROBSerialBox` expires controller snapshots after
three missed 5 Hz updates, sends one neutral/braked frame, then stops USB
writes so the Arduino deadman can de-energize the treads.

This yields a useful authority hierarchy:

```text
emergency / stop intent
        > direct operator control
        > bounded approved autonomy
        > AI proposal
        > idle
```

Ask Codex to encode this hierarchy in tests, not just comments:

```text
Add table-driven tests for authority arbitration. Stop must preempt every
state. Manual control must end autonomy. Restart must default to autonomy off.
An expired controller snapshot must produce exactly one neutral/braked write
and no continuing heartbeat. Do not add arm movement.
```

The final sentence matters. Mature agents are capable of expanding a coherent
feature beyond its safe scope. Tell Codex which adjacent capability is
explicitly excluded.

---

## 7. Vision, depth, and video as bounded pipelines

> **SOURCE TRAIL — ANALYZING NOW:** `CameraManager.swift` owns separate face/belly RGB-D delivery, the `ROBInsta360` services own the panoramic path, and `ROBVideoServer.swift` owns three-feed video serving. Vision Pro receivers and flat/immersive presentation live in ROBControllerVision's video feature and platform directories.

Cerebro's camera path evolves from selecting webcams to a multi-provider
perception system.

The 2026 implementation runs each OAK role in a supervised Python helper and
sends synchronized RGB and aligned depth over a private Unix socket. Face and
belly cameras have distinct MXIDs, sockets, lifecycle state, and on-device
pipelines. Keeping the SDK outside Cerebro isolates USB disconnects, malformed
packets, missing packages, and Python crashes. AVFoundation remains an RGB
fallback, but only one provider may own a physical OAK device. A third
headless service controls and decodes Insta360 Pro II panoramic video on demand.

The separate Vision Pro service exposes independent `front`, `belly`, and
`insta360` H.264 pipelines on its own authenticated QUIC connection. Each feed
has bounded send state and newest-frame admission. Slow video cannot back up
robot control. Dropped frames trigger keyframe recovery rather than an
unbounded queue, and the panoramic feed can move from a flat panel to an
inward-facing mixed-immersive sphere without preserving motion authority.

The reusable design lesson is **separate by failure domain**:

- control and video use different services and queues;
- Python SDK faults do not terminate Cerebro;
- camera ownership is exclusive;
- camera role, calibration, rate budget, and demand are explicit;
- perception drops old work instead of accumulating latency;
- an unavailable optional device degrades one capability.

Codex prompt:

```text
Trace camera frames from provider to Vision, Gemini, and Vision Pro. For each
consumer record queue, ownership, backpressure, timestamp, and failure policy.
Then add the smallest change that keeps only the newest pending frame for the
slow consumer. Prove robot-control queues are untouched. Add malformed IPC and
slow-consumer tests; separate simulator evidence from hardware validation.
```

---

## 8. AI inside Cerebro: proposals, tools, and speech

> **SOURCE TRAIL — ANALYZING NOW:** `Cerebro/Cerebro/ROBAI.swift` is the optional AI integration, while `Cerebro/Cerebro/GeminiRoboticsProtocol.swift` defines bounded high-level proposals. Search callers before assuming that a declared action has a physical executor.

The repositories currently document Gemini Robotics Live as the runtime model
integration. OpenAI enters this story in two different ways:

1. **Codex develops and maintains the codebase.**
2. **The OpenAI Responses API can power a future model-neutral robot brain.**

These roles should not be conflated. A coding agent may edit a protocol while
an application model later uses that protocol as a tool.

For an OpenAI-backed adapter, preserve Cerebro's deterministic boundaries. The
model receives observations and returns structured proposals. Cerebro validates
the schema, allow-list, session, deadline, and current authority. ROBController
approves where required. Only a deterministic executor may touch hardware.

Conceptual Swift-like pseudocode:

```swift
let proposal = try await openAI.responses.create(
    model: configuredModel,
    input: currentRobotContext,
    tools: [robotActionProposalSchema]
)

let action = try RobotActionProtocol.validate(proposal)
try authority.requireActiveSession(action.sessionID)
try policy.requireAllowed(action)
await operatorConsole.requestApproval(action)
```

Use the Responses API for multi-turn reasoning and tool calling, and choose the
model through configuration rather than scattering a model name through UI and
network code. Keep credentials outside source control. Do not send secrets,
pairing material, faces, audio, or private surroundings unless the product's
data policy and operator consent explicitly allow it.

The current Cerebro implementation makes that privacy boundary concrete in two
new subsystems. The face recognizer keeps consented embeddings and samples
encrypted on the Mac and contributes only expiring untrusted scene context;
WebFace4M and VGGFace2 profiles remain model-specific. The Messages bridge is
disabled by default, exact-sender allowlisted, one-to-one only, at-most-once,
and stripped of motor, file, Music, device, camera, and microphone tools. Its
optional encrypted transcript memory is sender/account scoped; when Gemini is
used, selected text excerpts leave the Mac and that disclosure must be explicit.
Neither “administrator” face identity nor conversational memory is authorization.

### A safe OpenAI integration task for Codex

```text
Add an OpenAI Responses API provider behind the existing model-neutral
improvisation/proposal interface. First inspect the current official OpenAI
documentation. Keep the existing provider as default. Read the API key from a
secure runtime source, never source or logs. Return only the existing strict
schema. No model output may directly invoke serial, shell, network-control, or
arm code. Add mocked success, timeout, malformed output, refusal, and
cancellation tests. Do not enable the provider automatically.
```

The official OpenAI model guidance recommends the Responses API for reasoning,
tool use, and multi-turn workflows. Models and capabilities change; let Codex
consult current official documentation during implementation instead of
freezing this book's August 2026 model names into the architecture.

---

## 9. Local improvisation and stage shows

The August 3 Cerebro change adds a safe local-improvisation layer, a
connection-tolerant show coordinator, diagnostics, a llama.cpp provider, strict
show schemas, fixture tests, and a Maker Faire opening show.

This feature demonstrates layered trust:

- authored dialogue is the mandatory fallback;
- local generation may select only allow-listed beats and delivery;
- Gemini may add live context to a trusted brief;
- show files cannot contain raw joints, servo values, hosts, ports, or shell;
- uncalibrated gestures fail closed;
- expired stage contexts permanently reject non-stop tool calls;
- `stop_motion` remains available through a priority stop lane.

Generative language becomes safe not because the model is guaranteed to behave,
but because untrusted output has a narrow grammar and a deterministic fallback.

When asking Codex to extend a show format, request the validator and negative
fixtures before the runner:

```text
Extend robshow v1 with an optional audience-response beat. The JSON may select
only a named response policy and timeout. It may not contain executable code,
raw motor values, file paths, hosts, ports, or arbitrary tool names. Update the
schema, parser, negative fixtures, dry-run renderer, and docs before enabling
runtime behavior. Preserve authored fallback and stop preemption.
```

---

## Interlude: the August 14–23 integration sprint

The ten days after the original local-model edition changed the unit of work.
Instead of one isolated feature at a time, the repositories began moving in
cross-system slices whose contracts had to agree across the Mac, iPhone/iPad,
Vision Pro, lidar publisher, camera helpers, and AMBER runtime.

The material changes include:

- an always-on, singleton Cerebro process with wake recovery and crash-limited supervision;
- separate face, belly, and headless Insta360 camera roles, selectable detectors, per-camera budgets, and a system-status dashboard;
- three authenticated H.264 feeds and a physically aligned mixed-immersive panorama;
- explicit Request/Release Control arbitration between phone and Vision clients;
- independent left/right `rob-arm-control/2` authority and simultaneous bounded PSVR Sense joint jogging;
- destination navigation, sidewalk segmentation, stale-sensor gates, and manually confirmed traversability learning;
- compact `RLS1` lidar frames, authenticated same-Mac IPC with QUIC fallback, pose-aligned maps, `.robomap` persistence, and map/base-layer calibration;
- explicit synchronized recording for RGB, lossless depth, stereo, lidar, calibration, pose, odometry, authority, labels, and separate camera movies;
- a disabled-by-default, allowlisted one-to-one Messages AI bridge with bounded images, local current-information tools, optional encrypted transcript memory, and exact-confirmation local administrator scripts; and
- a disabled-by-default consented face gallery with local encrypted enrollment and selectable AdaFace WebFace4M/VGGFace2 encoders.

The strongest architectural result is not any individual model. It is the
repeated separation of **identity**, **memory**, **observation**, **operator
ownership**, and **physical authority**. A face label can personalize a
greeting but cannot approve a command. A Messages sender can enter a narrow
allowlisted conversation or exact administrator-command path but cannot inherit
robot tools. A recorded autonomous command can document a run but cannot label
its own ground truth. A panoramic window can survive a scene transition while
drive is independently braked.

This is also a lesson in evidence. The Volume 5 Change Atlas now records the
commit families across all affected repositories. The August 23 snapshot notes
that ROBControllerVision's latest three panorama-orientation commits were clean
but still ahead of its public remote. “Implemented locally” and “reproducible
from the public branch” are different claims, and a good AI collaborator should
surface that distinction before publication.

---

## 10. Dependencies are part of robot safety

Earlier Cerebro code contained machine-specific paths and assumed tools were
installed. The mature version treats dependencies as fallible inputs.

Python can be selected, auto-detected, or created in an app-managed virtual
environment. Package installation occurs only after an operator action.
`sshpass`, `ticcmd`, and RPLidar are resolved and validated before launch.
Missing optional tools disable their feature rather than crash Cerebro.
Privileged MacPorts installation is shown to the operator in Terminal; the app
does not capture an administrator password. The SSH password travels through an
anonymous pipe rather than the process argument list.

This is an excellent Codex refactoring pattern:

```text
Inventory every Process/NSTask launch in Cerebro. Do not edit yet. Classify the
executable as required or optional; list path source, validation, credentials,
timeout, restart behavior, and user-visible failure. Then centralize only the
shared preflight while preserving each feature's behavior. Add tests for
missing, directory, non-executable, and disappearing executables.
```

Codex can search every launch site more reliably than a tired human, but the
operator must decide which dependency failures are tolerable.

---

## 11. A repeatable Codex workflow for these repositories

### Step 1: protect the worktree

Start every session with:

```text
Inspect git status in ROBController and Cerebro. Existing changes belong to me.
Do not overwrite, revert, stage, or commit them. Identify generated Xcode user
state separately. Summarize the relevant architecture before editing.
```

The current worktrees, for example, contain modified
`UserInterfaceState.xcuserstate` files. They are user state, not permission to
discard anything.

### Step 2: state outcome and invariants

Prefer “When control packets stop, the base brakes once and becomes silent” to
“refactor ROBSerialBox.” The former is testable and safety-relevant.

### Step 3: ask for read-only diagnosis

For cross-language and cross-repository behavior, have Codex trace the entire
path before implementation. Ask it to cite evidence and say what it cannot
know without hardware.

### Step 4: divide at stable boundaries

Good checkpoints are codec, fixtures, client state machine, server state
machine, UI, and documentation. Avoid one request that changes wire format,
physical actuation, and user experience without intermediate review.

### Step 5: make Codex edit and verify

```text
Implement the approved codec checkpoint. Preserve unrelated changes. Run the
narrow fixture tests first, then the relevant build. Review your own diff for
security, concurrency, compatibility, and accidental secrets. Report commands,
results, remaining hardware checks, and files changed.
```

### Step 6: inspect the diff yourself

Use `git diff --check`, `git diff --stat`, and `git diff`. Pay special attention
to entitlements, Info.plist permissions, Xcode project membership, networking,
Keychain accessibility, dispatch queues, and motor values.

### Step 7: validate in layers

1. Pure codec/schema fixtures
2. Unit tests with mocked time and I/O
3. Client/server integration tests on loopback
4. Xcode build and static diagnostics
5. Simulator/UI checks where meaningful
6. Bench hardware with motors disabled or lifted
7. Low-speed supervised robot test with an accessible stop

Codex may complete layers one through five. It must never imply that they prove
layers six and seven.

### Step 8: commit the reasoning

A mature message explains behavior and risk:

```text
fix(network): prevent QUIC pairing handshake deadlock

- send a bounded client hello before awaiting the challenge
- validate device identity against the paired registry
- preserve certificate pinning and reciprocal proof
- add a regression fixture for simultaneous-read startup
```

The history then becomes usable context for the next human or AI session.

---

## 12. Prompt recipes for the actual change families

### Cross-repository protocol change

```text
Trace protocol X in both repos. Produce a compatibility matrix for old client,
new client, old server, and new server. Design golden fixtures before edits.
Reject malformed and oversized input. No automatic security downgrade. Make
changes in reviewable checkpoints and run both test suites.
```

### Concurrency bug

```text
Build a state machine from code, queues, callbacks, and cancellation paths.
Identify races, double completion, and mutual waits. Add a deterministic
regression test. Keep UI updates on the main actor/queue and network state on
its owning queue. Do not mask the bug with sleeps.
```

### Camera crash

```text
Diagnose only first. Trace device discovery, selected device lifetime, session
mutation, and frame consumers. Explain the exact crash precondition. Separate
what can be fixture-tested from the rapid-toggle test required on the robot Mac.
```

### New AI tool

```text
Treat model output as untrusted. Define a versioned strict schema, limits,
allow-list, authority check, deadline, cancellation, idempotency rule, operator
approval, terminal result, and audit event. Add negative fixtures. Do not wire
physical execution until the protocol review is complete.
```

### Arm feature

```text
No motion yet. Inventory joint names, signs, units, calibrated ranges, feedback,
URDF assumptions, transforms, collision checks, and emergency stop path. Mark
every missing fact. Build a dry-run command preview and fixtures. Require a
separate explicit request before enabling hardware output.
```

### Face-identity feature

```text
Treat face recognition as consented local context, never authorization. Preserve
explicit enrollment confirmation, complete deletion, encrypted model-tagged
profiles, open-set and temporal gates, and no upload. Compare only embeddings
from the same encoder. Add false-accept/false-reject, lookalike, lighting,
occlusion, replay, model-switch, corrupt-gallery, and key-loss tests. Document
liveness limitations and keep motion, shell, secrets, and approvals out of scope.
```

### Private Messages feature

```text
Keep the bridge disabled by default, exact-sender allowlisted, one-to-one,
at-most-once, rate-limited, and isolated per chat. Fail closed on groups,
outgoing/reaction/stale/partial items, unexpected accounts, and unsupported
attachments. Give the responder no robot, file, Music, device, camera, or
microphone tools. Encrypt optional memory and bound cloud disclosure. Route
exact administrator commands before AI, require same-chat one-shot confirmation,
use reviewed fixed scripts through stdin, and never interpolate message text.
```

### Training-data recorder

```text
Recording must begin only after explicit operator intent and remain visibly
active. Bind RGB, depth, stereo, lidar, calibration, pose, odometry, authority,
labels, and encoded footage to one recoverable session with validated geometry
and timestamps. Record autonomous commands as events but never let them create
their own labels. Add low-space, crash recovery, corrupt frame, camera restart,
consent, export, retention, and delete tests before using data for training.
```

### Documentation from code

```text
Update the operator document from the implemented diff. Distinguish implemented,
tested in fixtures, built, simulator-tested, and hardware-validated. List known
gaps plainly. Do not describe planned behavior as present behavior.
```

---

## 13. Reviewing AI-generated robot code

An AI-generated diff is a proposal. Review it in five passes.

### Safety

- Does loss of input converge to neutral?
- Is stop independent, prioritized, and idempotent?
- Are speeds, positions, payload sizes, and durations bounded?
- Does restart return to a safe state?
- Does an unavailable sensor prevent motion that depends on it?

### Security

- Are identity, enrollment, authorization, and freshness distinct?
- Are secrets absent from source, logs, process arguments, and Bonjour?
- Is there any fallback to plaintext or unauthenticated behavior?
- Can revocation terminate a live session?
- Can a telemetry role become a control role by editing its payload?

### Concurrency

- Which queue owns each mutable state variable?
- Can both peers wait forever?
- Can cancellation race with completion or a late tool call?
- Can a slow camera/model consumer block control?

### Compatibility

- Are protocol versions explicit?
- Are unknown fields tolerated only where intended?
- Do both repositories share golden fixtures?
- Is legacy behavior opt-in, observable, and removable?

### Evidence

- What tests ran?
- What could not run in the environment?
- Was hardware actually exercised?
- Are documentation claims no stronger than the evidence?

---

## 14. What remains intentionally unfinished

Mature engineering is visible in the features a system refuses to fake.
Cerebro reports general picking and arm motion as unavailable because the
repository still lacks calibrated camera-to-arm transforms, complete neck
mapping, joint feedback, inverse kinematics, collision checking, and a verified
grasp executor. Gesture cues fail closed without a calibrated catalog and
feedback-capable executor. Approval records operator intent but does not by
itself start physical action.

These are the next safe milestones:

1. Establish measured coordinate frames and calibration artifacts.
2. Add feedback and freshness to joint state.
3. Build offline IK with joint and velocity bounds.
4. Add collision models and swept-volume checks.
5. Simulate and dry-run named motions.
6. Validate one arm on a bench at low speed.
7. Introduce a deterministic executor with stop preemption.
8. Only then expose a narrow, schema-constrained AI proposal tool.

Codex can help at every milestone, but it cannot supply missing physical facts
from code. Calibration measurements, payload limits, wiring, clearances, and
the location of humans around the robot belong to the real world.

---

## 15. The developer after code generation

Programming is not disappearing so much as moving upward. A developer once
spent most of a day translating a known solution into syntax. An AI coding
agent can now perform much of that translation, search a repository, connect
call sites, write tests, run tools, and revise a patch. The scarce skill becomes
the ability to define the right system, communicate its invariants, recognize
false confidence, and decide whether the evidence is strong enough to ship.

This is a profound change. Source code remains real and must still execute, but
manually typing every line is no longer the center of the job. The new
developer operates at several levels at once:

- **Purpose:** What human outcome should improve?
- **System:** Which components, data, authorities, and failure boundaries exist?
- **Contract:** What must inputs, outputs, timing, and errors mean?
- **Evidence:** What observation would prove the behavior works?
- **Operations:** How will the system be deployed, monitored, stopped, and repaired?
- **Responsibility:** Who accepts the consequences when software affects people or machines?

The syntax layer has not become worthless. Reading code is still one way to
audit the agent's interpretation, locate a security defect, or understand why
a test passes for the wrong reason. But fluency increasingly means being able
to move between intent, architecture, executable artifacts, and evidence. A
developer can be less concerned with remembering an API name and more
concerned with whether the API belongs in the design at all.

### From implementation task to outcome contract

A weak request says:

```text
Add controller position support.
```

A strong outcome contract says:

```text
ROBControllerVision has two spatial controllers. Capture a fresh left and
right world-space pose, preserve chirality, and transmit position in meters
plus normalized quaternion orientation through the authenticated control path.

Cerebro must validate finite values, bounds, version, and freshness before
storing a pose. Missing tracking must invalidate the pose instead of retaining
the last arm target. Preserve the historical tread snapshot for older peers.
Do not actuate an arm yet. Build both apps, add a wire-format fixture, and state
what still requires a physical Vision Pro test.
```

The second request does not prescribe every class or function. It gives the AI
room to inspect and design while making the result falsifiable. It names the
world in which the code must be correct.

### The new literacy

The developer of this wave needs four complementary literacies.

1. **Domain literacy** identifies what matters in robotics, medicine, finance,
   media, education, or another field.
2. **Systems literacy** traces state, timing, trust, feedback, and failure across
   boundaries.
3. **AI communication literacy** supplies goals, context, constraints, and
   acceptance evidence without burying the task in ceremony.
4. **Verification literacy** distinguishes plausible output from demonstrated
   behavior.

AI magnifies all four. It also magnifies their absence. A vague request can
produce a large, polished, internally consistent mistake faster than a person
could have typed it.

---

## 16. How an AI development system actually works

An AI coding system is more than a chat box. It is a loop that combines a model
with context, instructions, tools, an execution environment, and feedback.
Understanding those parts helps a developer diagnose failures without treating
the model as magic.

### Model

The model predicts and reasons over the information available in the current
interaction. It can synthesize patterns across languages and domains, but it
does not automatically know the current repository, physical robot, private
requirements, or latest external facts. Confidence in its prose is not a
measurement of truth.

### Context

Context includes the request, conversation, selected files, repository
instructions, tool results, images, logs, and sometimes retrieved documents.
Good context is not the largest possible pile of text. It is the smallest set
that changes the decision.

For a deadlock, the relevant context is usually both peers' state machines,
the first reads and writes, cancellation behavior, and a reproducible trace.
Hundreds of unrelated UI files can make the important relationship harder to
see. Ask the agent to search first, then load the narrow data path.

### Instructions and precedence

An agent may receive durable project instructions in addition to the current
request. These can define build commands, architectural rules, formatting,
security restrictions, or files that must not be changed. Treat these files as
part of the engineering system. Keep them concise, current, and testable.

Instructions should express durable policy:

```text
- Run protocol fixture tests after changing either wire implementation.
- Never enable an unauthenticated fallback.
- Do not send arm commands from a generative model directly.
- Preserve user changes in a dirty worktree.
```

Temporary details belong in the task, not the permanent policy file.

### Tools

Tools let the agent observe and change the world: search files, inspect Git,
apply patches, compile, run tests, browse official documentation, render a PDF,
or view an image. A model answer without tools is a proposal. A tool-using
agent can produce evidence, although that evidence still needs interpretation.

Tool authority should match the task. Reading and testing are lower risk than
publishing, deleting, deploying, spending money, messaging another person, or
energizing hardware. High-impact actions need explicit boundaries and often a
human approval step.

### Execution environment

Local and cloud agents do not necessarily see the same files, credentials,
devices, network, simulators, or operating-system APIs. State the important
environment facts and ask the agent to report what it could not reproduce.
“Build passed” may mean a simulator target compiled; it does not mean two real
controllers tracked correctly on Vision Pro.

### Feedback loop

The most productive unit of AI development is not one perfect prompt. It is a
controlled loop:

```text
state goal -> inspect -> form hypothesis -> change -> verify -> review -> revise
```

Each loop should reduce uncertainty. If an agent makes five speculative edits
without producing new evidence, stop and return to inspection.

---

## 17. Communicating for reliable results

Official OpenAI prompting guidance describes four useful ingredients for
important work: goal, context, output, and boundaries. It also recommends
starting with the result, adding only context that can change it, using
follow-up messages, and reviewing the final result yourself. These ideas map
especially well to software development.

### Goal: define observable behavior

“Improve networking” is a theme. “Reconnect after Wi-Fi interruption without
reviving an expired motion lease” is a goal. Use nouns and verbs from the real
system. Say which user, device, event, input, and output matter.

When the goal contains multiple interpretations, name a concrete scenario:

```text
With Cerebro already listening, launch the Vision client. Both peers currently
wait for the other to speak and the connection times out. Change the handshake
so the client sends a bounded hello first and the server can associate it with
the paired identity before issuing its challenge.
```

### Context: provide decision-changing facts

Context is not a biography of the project. Useful context includes:

- reproduction steps and exact error text;
- affected repositories and platforms;
- a known-good comparison implementation;
- protocol fixtures, schemas, or hardware limits;
- recent changes that might explain a regression;
- files that contain user work and must be preserved.

If you believe two bugs share a cause, offer that as a hypothesis rather than a
command: “This resembles the QUICK simultaneous-read deadlock we fixed in
ROBController; compare the state machines and confirm before reusing the fix.”
That invites transfer without forcing a false analogy.

### Output: say what done looks like

Name the artifacts required at handoff: implementation, migration, tests,
documentation, screenshot, fixture, benchmark, or printable PDF. Specify the
audience and level when it affects the result. Ask for a concise final report
with changed files, test commands, limitations, and the next physical check.

### Boundaries: protect what matters

The best boundaries prevent expensive mistakes. They do not micromanage every
keystroke.

```text
- Keep the legacy 14-line controller snapshot byte-compatible.
- Do not change pairing identity or certificate validation.
- Never retain a stale pose as a valid target.
- Do not actuate hardware in this task.
- Do not discard unrelated working-tree changes.
```

Boundaries can also define when the agent must ask. A request to draft release
notes does not authorize publishing them. A request to diagnose a robot motion
fault does not authorize sending a test command.

### Acceptance evidence

Acceptance criteria turn communication into an engineering contract:

```text
Acceptance:
- a valid left/right pose round-trips through the authenticated archive;
- malformed, nonfinite, out-of-range, and unsupported-version poses fail closed;
- an older payload still parses;
- ROBControllerVision and Cerebro Debug builds pass;
- physical-device validation remains clearly marked pending.
```

This is stronger than “make sure it works.” It tells both human and AI which
claims the evidence must support.

### Steering without restarting

When the agent is already working, correct direction with the smallest useful
message. Examples:

```text
Preserve the existing wire keys; add versioned optional keys instead.
```

```text
The green connection light is accurate. Focus on profile classification and
controller aggregation, not discovery.
```

```text
Do not stop at storage. Include pose validity and timestamp fields in the model,
but leave arm actuation for a calibrated follow-up.
```

Good steering adds evidence or a constraint. It does not require restating the
whole project.

---

## 18. Context engineering for large repositories

AI performance depends on what it can see and how the repository exposes its
meaning. Context engineering is the practice of arranging code, tests,
documentation, and instructions so the agent can recover the right model of
the system.

### Give the repository a map

A short project map should name entry points and ownership:

```text
ROBControllerVision/App          UI and session presentation
ROBControlCore/Control           typed intent and dead-man policy
ROBCerebroTransport/Control      authenticated wire compatibility
Cerebro/ROBMainViewController    legacy receive integration
Cerebro/ROBBaseControllerModel   shared accepted controller state
```

This does not replace search. It reduces the chance that the agent edits a
similarly named but inactive path.

### Preserve executable knowledge

Tests and fixtures are better context than prose alone because they can reject
a misunderstanding. For every important promise, ask whether it can become:

- a unit test for a pure transformation;
- a golden byte fixture for a protocol;
- an integration test across a fake transport;
- a state-machine test for cancellation and timeout;
- a simulator scenario for operator behavior;
- a physical checklist for facts software cannot prove.

When a hardware discovery is made, first write it down, then encode the portion
that can be checked automatically. “The arm sign is reversed” should become a
calibration artifact or mapping test, not remain only in a chat transcript.

### Separate durable truth from session history

Conversation is useful working memory but a poor sole archive. After a task,
place durable knowledge where the next developer and agent will find it:

- protocol contracts beside the implementation;
- operational steps in a runbook;
- repository conventions in project instructions;
- architectural decisions in a short decision record;
- verified limits in machine-readable configuration;
- uncertain physical facts in a clearly labeled validation checklist.

Avoid copying an entire conversation into the repository. Preserve decisions,
evidence, and unresolved questions.

### Ask for evidence-backed exploration

For an unfamiliar system, use a staged request:

```text
Inspect without editing. Trace a controller sample from GameController through
the dead-man lease, transport encoder, Cerebro receiver, and accepted model.
Cite symbols and files. Identify where chirality, freshness, and invalidation
could be lost. Separate confirmed behavior from hypotheses.
```

Review that map before implementation. This is not bureaucracy; it is a cheap
way to discover that the visible UI and active data path are different.

### Manage context decay

Long tasks accumulate superseded hypotheses. Periodically restate the current
facts:

```text
Current verified state:
- connection succeeds and the green indicator is correct;
- both PSVR controllers enumerate;
- the remaining defect is unsupported profile mapping;
- tread values must remain independent floats;
- dead-man behavior is retained.
```

This compact checkpoint helps the agent stop pursuing an earlier diagnosis.

---

## 19. Verification is the product

AI makes producing an implementation inexpensive. Therefore the value moves to
proof. A professional AI-assisted change should carry an evidence ladder whose
top rung matches the risk of the claim.

### The evidence ladder

1. **Static inspection:** types, call sites, schemas, and configuration agree.
2. **Focused test:** the changed transformation or failure case is executable.
3. **Regression suite:** neighboring promises still hold.
4. **Build:** the real target, SDK, and language mode compile.
5. **Integration:** both sides communicate under representative timing.
6. **Simulation:** user interaction and state transitions behave together.
7. **Bench test:** hardware is constrained, low energy, and supervised.
8. **Operational test:** the complete system runs with stop paths and observers.

Do not skip from static inspection to a claim about physical behavior. Each
rung answers a different question.

### Ask the agent to falsify its own patch

After implementation, change roles. Ask:

```text
Review this diff as a skeptical maintainer. Find ways the new pose can become
stale, swap chirality, bypass validation, break an older Cerebro receiver, or
increase motion authority. Add focused tests for credible failures. Do not
expand scope into arm control.
```

An AI can generate both the patch and the critique, but independence is not
guaranteed. The critique still improves coverage by forcing a different search
objective. Human review, separate test design, and real measurements remain
valuable.

### Evaluate repeated AI workflows

When the same task occurs often—triaging controller logs, drafting protocol
tests, reviewing dependencies, or generating release notes—build a small eval
set. Include normal cases, difficult edge cases, and cases that should be
refused or escalated.

Record measurable outcomes:

- Did the agent identify the active implementation?
- Did it preserve backward compatibility?
- Did it distinguish compilation from hardware validation?
- Did it avoid secrets and destructive actions?
- Did the test fail before the fix and pass after it?
- Did the final report accurately describe limitations?

Run the eval when instructions, tools, models, or repository architecture
change. A beautiful demonstration is one sample; an eval set measures a
pattern.

### Stop conditions are part of verification

Define when work must pause:

- the requested behavior depends on an unknown physical limit;
- the only available test could move unguarded hardware;
- credentials or permissions are missing;
- a generated migration could irreversibly alter user data;
- two authoritative specifications conflict;
- the diff overlaps unexplained user changes.

Stopping with a precise blocker is a successful safety behavior, not a failure
of intelligence.

---

## 20. Designing AI-native software systems

Using AI to write an ordinary application is only the first wave. An AI-native
system is designed around uncertain model output, typed tools, observable
state, evals, and deterministic boundaries.

### Separate proposal from execution

The model should propose a bounded intent:

```text
turn 20 degrees left at inspection speed
```

A deterministic layer should decide whether that intent is allowed, translate
it into units, apply limits, acquire authority, monitor freshness, and stop.
The model should not manufacture raw motor bytes or bypass the controller
lease.

For an arm, a safer progression is:

```text
language goal
  -> typed task proposal
  -> scene and capability checks
  -> deterministic planner / IK
  -> joint, velocity, and collision validation
  -> operator approval when required
  -> feedback-controlled executor
  -> independent stop
```

Each arrow is an inspectable contract.

### Give tools narrow schemas

A tool named `run_any_shell_command` offers enormous accidental authority. A
robot tool should expose the smallest operation that can be made safe. Its
schema should constrain units, ranges, identifiers, and optionality before
execution code sees the request.

```text
propose_named_pose(
  pose_id: one of the calibrated catalog IDs,
  speed_fraction: 0.0 through 0.2,
  reason: short operator-visible text
)
```

Even a valid schema does not prove the pose is currently collision-free. Tool
validation, world state, executor feedback, and operator policy remain separate
layers.

### Treat retrieval as evidence selection

An AI system can retrieve manuals, logs, code, and prior decisions. Retrieval
quality determines which evidence reaches the model. Store documents with
source, date, version, authority, and scope. Prefer a current verified wiring
map over an old brainstorming note, and make conflicts visible rather than
silently blending them.

### Design for uncertainty

Model output may be incomplete, inconsistent, or wrong. The system needs:

- structured outputs that reject invalid shapes;
- timeouts and cancellation;
- bounded retries and queue sizes;
- idempotent operations where possible;
- explicit unavailable and uncertain states;
- audit events for proposals, approvals, actions, and outcomes;
- human escalation for consequential ambiguity.

Do not convert “the model did not answer” into a default motion. In robotics,
absence of valid intent should converge to neutral.

### Observe the whole loop

Measure more than model latency. Track tool selection, validation failures,
approval delays, execution outcomes, cancellation, stale state, and recovery.
Keep sensitive data out of logs and define retention. An AI system that cannot
explain which source and tool produced an action will be difficult to debug and
unsafe to trust.

---

## 21. A thirty-day AI developer practice

The fastest way to learn this new form of development is to practice on real,
bounded work while increasing authority slowly.

### Week 1: learn to specify

Each day, take one vague task and write an outcome contract with goal, context,
output, boundaries, and acceptance evidence. Ask the AI to inspect before
editing. Compare its system map with the code.

Exercises:

1. Trace one UI action to its side effect.
2. Explain one protocol field and its validation.
3. Find one timeout and list what state it protects.
4. Turn one bug report into reproducible steps.
5. Convert one workshop fact into a testable invariant.

### Week 2: build evidence loops

Choose low-risk bugs. Require a failing reproduction or fixture before the
patch. Ask the agent to run the smallest test, then the neighboring suite, then
the real build. Review every claim in the handoff against command output.

Keep a notebook with three columns: claim, evidence, remaining uncertainty.
This trains the distinction between “the code looks right” and “this behavior
was observed.”

### Week 3: direct cross-system changes

Work across two components without expanding physical authority. Examples are
a versioned optional field, a status message, or a simulator-only control.
Require a shared fixture and independent validation at the receiver.

Practice steering when the first hypothesis is wrong. Give the agent the new
fact without rewriting its entire plan. Watch whether it updates the causal
model or merely patches around the symptom.

### Week 4: design an AI-native capability

Design—but do not energize—a narrow AI proposal tool. Define its schema,
authorization, freshness, deterministic checks, refusal cases, audit record,
and eval set. Threat-model prompt injection, stale retrieval, malformed tool
arguments, repeated calls, cancellation races, and operator confusion.

Finish with a review packet:

- system diagram;
- typed contract;
- ten normal eval cases;
- ten adversarial or failure cases;
- deterministic validator tests;
- simulator demonstration;
- physical validation plan owned by a qualified operator.

### Graduation test

You are ready for greater autonomy when you can reliably answer:

1. What exact outcome is requested?
2. Which source is authoritative for each fact?
3. What authority does the AI have?
4. What deterministic boundary contains it?
5. What evidence supports each completion claim?
6. How does the system fail neutral?
7. Who can stop it, and how?

The future developer is not the person who types the most code. It is the
person who can turn human intent into a well-bounded system, use AI to explore
and construct it rapidly, and produce evidence strong enough for others to
trust.

---

## 22. The AI change contract worksheet

Complete this worksheet before a consequential AI-assisted change. Short,
specific answers are more valuable than polished language.

### Outcome

- Who experiences the problem?
- What behavior should become observably different?
- What example demonstrates success?
- What is explicitly outside this change?

### Sources and system map

- Which repository, branch, target, and device are involved?
- Which files or symbols are likely entry points?
- What specification, fixture, measurement, or operator statement is authoritative?
- Which facts are hypotheses that the agent must confirm?
- What recent known-good implementation should be compared?

### Invariants and authority

- What existing behavior must remain byte-compatible or user-compatible?
- Which values, rates, sizes, lifetimes, and coordinate systems are bounded?
- Who owns mutable state?
- What may the AI read, edit, execute, or propose?
- Which actions require approval?
- Which actions are forbidden in this task?

### Failure behavior

- What happens when input disappears, tracking is lost, or a peer disconnects?
- What happens when a value is malformed, nonfinite, stale, duplicated, or unsupported?
- Can cancellation race with completion?
- Can one optional subsystem block control or stop handling?
- Does restart preserve an emergency stop or accidentally clear it?

### Acceptance evidence

- What test must fail before the fix?
- What focused test proves the new contract?
- What regression suites and builds must pass?
- What integration or simulator scenario must be observed?
- What remains a physical-device test?
- What limitation must appear in the final report?

### Ready-to-use prompt

```text
Goal:
[Describe the observable result.]

Context:
[Name the repositories, reproduction, relevant evidence, and known-good comparison.]

Boundaries:
[List the few invariants and authority limits that prevent real harm.]

Acceptance:
[List executable tests, builds, and remaining physical checks.]

Start by inspecting the active data path and reporting confirmed facts versus
hypotheses. Then implement the smallest complete change, verify it, review the
diff for regressions and unsafe authority expansion, and give me an evidence-
backed handoff. Do not claim validation that the available environment cannot
perform.
```

### Human sign-off

Before shipping or energizing hardware, the responsible developer should be
able to say: I understand the intended behavior; I reviewed the authority and
failure boundaries; the cited evidence supports the claims; unresolved
physical facts are labeled; and a tested independent stop exists where motion
can affect people or equipment.

---

## 23. Local intelligence on Apple silicon: Swift, MLX, and Llama

> **SOURCE TRAIL — ANALYZING NOW:** find the current local-model implementation with `rg -n "MLX|Llama|MLXVLM|LocalModel" Cerebro`. Package declarations and lockfiles establish which library revision is actually available; prose examples do not.

Cerebro can now run a small language model directly on the Mac inside the
robot. This is not one product called “SwiftMLX.” The pieces have distinct
jobs:

- **Swift** is the programming language used by Cerebro's local-AI layer.
- **MLX Swift** is the Swift interface to Apple's MLX array and machine-learning
  framework for Apple silicon.
- **MLXLLM** loads and runs text-generating large language models.
- **Llama** is a family of language-model architectures and weights. It is a
  model, not the runtime around it.
- **llama.cpp** is a separate local runtime with an HTTP server. Cerebro can
  use it as an alternative provider.
- **MLXVLM** runs vision-language models. “VLM” means vision-language model;
  this repository does not use a framework named VLX.

That vocabulary matters. A model is the learned set of weights. A runtime
loads the weights and performs inference. A tokenizer turns text into numeric
tokens. A model container holds the loaded model and tokenizer. Application
code supplies a prompt, validates the result, and decides what the result is
allowed to influence.

### 23.1 The actual Cerebro model stack

`ROBMLXRuntime.swift` imports `MLX`, `MLXLLM`, `MLXLMCommon`, `MLXVLM`, and the
tokenizer and Hugging Face loaders. Its current defaults are:

```swift
static let defaultLLMModel =
    "mlx-community/Llama-3.2-1B-Instruct-4bit"
static let defaultVLMModel =
    "mlx-community/Qwen2-VL-2B-Instruct-4bit"
static let defaultEmbeddingModel = "TaylorAI/gte-tiny"
```

The suffix `4bit` means the weights have been quantized to use fewer bits per
value. Quantization reduces memory and often makes local inference practical,
at the cost of some numerical precision. A one-billion-parameter model is not
small in the everyday sense, but it is deliberately modest for an embedded
stage assistant.

The engine is a Swift `actor`:

```swift
public actor ROBMLXEngine {
    private var llm: ModelContainer?
    private var vlm: ModelContainer?

    public func generate(prompt: String) async throws -> String {
        let container = try await loadLLM(modelID: Self.defaultLLMModel)
        let input = try await container.prepare(
            input: UserInput(prompt: prompt)
        )
        let stream = try await container.generate(
            input: input,
            parameters: GenerateParameters(
                maxTokens: 256,
                temperature: 0.4
            )
        )
        // Collect bounded text chunks and reject tool calls.
    }
}
```

An actor serializes access to its mutable model state. That prevents two tasks
from racing while a model is loading or diagnostics are changing. `async`
does not mean the robot waits helplessly: generation runs independently from
the deterministic motor-control path.

### 23.2 Tokens, context, temperature, and hallucination

A token is a model-sized piece of text, not necessarily a whole word. The
prompt and response both consume context. `maxTokens` places an upper bound on
response growth. `temperature` changes sampling: low values tend to be more
repeatable; higher values create more variation but can also create more
mistakes.

The model does not retrieve truth from its weights like a database. It predicts
likely next tokens. Fluent output can therefore be wrong. ROB never treats
local prose as a servo command. For the stage, the model returns a tiny JSON
plan, and deterministic code verifies its exact keys, enum values, length, and
prohibited control language.

### 23.3 Llama through MLX versus llama.cpp

Cerebro supports two local-provider paths:

```text
MLX Swift provider
  Cerebro process -> MLX model container -> validated plan

llama.cpp provider
  Cerebro process -> bounded localhost HTTP -> llama.cpp server
                  -> validated plan
```

MLX Swift keeps inference native and private inside Cerebro. The llama.cpp
path is useful when a builder already operates a compatible local server or
wants a model format supported by that ecosystem. They can run the same Llama
family, but they are not interchangeable APIs. In both cases the output must
pass `ROBLocalImprovisationPlanCodec`; the provider does not gain hardware
authority merely because it runs locally.

### Lab: trace one local sentence

1. Open Cerebro's Stage Show window.
2. Select **MLX Swift (private/offline)** as the local provider.
3. Run the provider health check before the audience arrives. The first run
   may download model files and will be much slower than a warm run.
4. Load `MakerFaireOpening.robshow.json` and choose **Local improv**.
5. At `model_turn`, follow the data from scene goal, to Llama tokens, to the
   decoded local improvisation plan, and finally to ROB's speech box.
6. Disconnect the network and repeat. An already downloaded model should
   remain local; the authored fallback still protects a failed generation.

Record model-load time, generation time, tokens per second, peak memory, the
validated output, and whether fallback was used. Performance is part of the
lesson, but predictable failure is the more important result.

---

## 24. Giving a language model eyes with MLXVLM

A text-only Llama model receives text. It cannot inspect a camera frame merely
because the prompt says “look.” Cerebro's `MLXVLM` path supplies both a prompt
and a selected `CIImage` to a vision-language model:

```swift
let input = try await container.prepare(
    input: UserInput(prompt: prompt, images: [.ciImage(image)])
)
```

The current Qwen2-VL model is asked for a deliberately narrow stage
observation: whether an audience is present, an estimated person count,
whether the presenter and demonstration object are visible, an audience
activity category, one short scene-change sentence, and confidence.

```text
{
  "audience_present": true,
  "estimated_people": 4,
  "presenter_visible": true,
  "demonstration_object_visible": false,
  "audience_activity": "watching",
  "scene_change": "two people approached",
  "confidence": 0.71
}
```

`ROBMLXStageObservationCodec` rejects extra keys, wrong types, counts outside
zero through fifty, inconsistent audience values, nonfinite confidence, and
multiline scene changes. A valid observation is still an uncertain fact. It is
not an instruction.

### 24.1 Sampling protects the camera and controls

Analyzing every frame would waste memory and compute and could interfere with
video delivery. Cerebro accepts at most one selected frame per bounded interval,
with a minimum of three seconds, and runs VLM work on the MLX actor. The camera
capture callback returns immediately. This creates two clocks:

```text
fast clock: camera, safety state, input leases, deterministic control
slow clock: sampled image -> VLM -> validated observation -> dialogue context
```

The slow clock may help ROB say, “I see the audience gathering.” It must not
become a hidden motion loop. Navigation should continue to use measured lidar,
validated free-space geometry, explicit autonomy policy, and stop behavior.

### 24.2 Confidence is a gate, not decoration

Cerebro includes stage observations only when they are fresh and meet the
configured confidence threshold. If the fact is old or weak, the dialogue
prompt says that no reliable camera fact is available. This avoids turning an
uncertain guess into a confident claim about a person.

Do not infer identity, emotion, disability, ethnicity, or other sensitive
traits from a Maker Faire camera. The stage schema asks only for coarse,
performance-relevant facts and must never identify an individual child.

### Lab: make the vision result fail safely

Test five frames: an empty stage, one presenter, a small audience, a partially
covered camera, and a deliberately ambiguous scene. For each frame:

1. Save only the validated observation and latency, not unnecessary audience
   imagery.
2. Compare the estimate with a human count.
3. Confirm malformed JSON is rejected.
4. Confirm a low-confidence observation does not enter the stage prompt.
5. Confirm disabling vision does not interrupt speech, stop handling, or
   manual robot control.

### 24.3 Learning is a release pipeline, not a reflex

Cerebro also contains the beginnings of a teachable object-detector workflow:
`ROBDatasetManager` saves reviewed images and normalized YOLO boxes;
`TrainProjectModel.py` fine-tunes YOLOv8n, exports ONNX, and compiles a Myriad X
blob; the DepthAI helper can load a project-specific blob and manifest. That is
an exciting path toward a robot that can learn new workshop objects, but it
must not become ``see once, train once, trust forever.''

The current dataset manager writes training and validation metadata to the
same image directory, while the trainer correctly refuses identical train and
validation directories. Preserve that refusal. Split data by collection event,
keep a locked test set, compare PyTorch/ONNX/OAK outputs, require declared
accuracy and latency thresholds, package a signed model manifest, run the
candidate in shadow mode, and require a named human to promote or roll it back
while the affected autonomy is disarmed.

AI assistance can help create annotation tools, tests, manifests, evaluation
reports, and deployment code. It cannot supply missing ground truth. The most
valuable model-generation prompt asks the coding agent to make the candidate
falsifiable: name the dataset hashes, likely leakage, per-class failures,
runtime differences, acceptance thresholds, and rollback evidence.

---

## 25. Implementing model-safe show logic

Stage-show files are data, not programs. They may contain dialogue, timing,
named gestures, checkpoints, and model scene goals. They may not contain raw
joint values, servo positions, hosts, ports, or shell commands.

New shows should use the provider-neutral `model_turn` cue:

```text
{
  "id": "live-joke",
  "kind": "model_turn",
  "duration_seconds": 15,
  "text": "Deliver one family-friendly robot joke. Do not request motion.",
  "fallback_text": "My local joke generator is taking a dramatic pause."
}
```

Older `gemini_turn` cues remain valid for compatibility. Both enter the same
coordinator. The name `model_turn` better describes the actual policy:

```text
model_turn
  |
  +-- Speech only ----------> authored fallback
  |
  +-- Local improv ---------> MLX Swift or llama.cpp
  |                              |
  |                              +-- invalid/timeout -> authored fallback
  |
  +-- Adaptive -------------> bounded local plan
                                 |
                                 +-- time remains -> Gemini Live dialogue
                                 +-- no time/failure -> local or authored line
```

The local model is constrained to a five-field dialogue plan: schema, version,
beat, delivery, and `offline_line`. It cannot return a gesture name or a tool
call. Gesture cues remain separately authored and resolved through a named,
allowlisted action. This separation is the core implementation lesson: AI can
shape performance language without inheriting control of the machine.

### 25.1 How to add a safe model cue

1. Write a narrow scene goal describing the desired spoken result.
2. Explicitly forbid physical actions and unsupported factual claims.
3. Author a complete fallback sentence that works with no model and no network.
4. Give the cue a short deadline. A show should advance or fall back rather
   than wait indefinitely.
5. Validate the entire show before rehearsal.
6. Rehearse in **Dry run**, then **Speech only**, then **Local improv**.
7. Use **Adaptive** only after both the local provider and cloud path have
   passed preflight.

### 25.2 A show is a state machine

At any moment the coordinator awaits exactly one event: speech completion,
local generation, Gemini, a named gesture, a checkpoint, or a timer. Stop
cancels pending model requests and timers. Each asynchronous completion carries
an identifier so a late response cannot complete a newer cue. This pattern is
useful far beyond theater: give every delayed operation an identity, deadline,
cancel path, and deterministic fallback.

### Rehearsal checklist

- The physical E-stop is reachable and independently tested.
- The stage is clear before any gesture cue.
- The model and VLM are downloaded before relying on offline operation.
- The local provider health check and generated-plan preflight pass.
- Every `model_turn` has acceptable authored fallback text.
- Camera confidence is visible to the operator.
- Dry-run logs show no unknown fields, late completions, or unbounded waits.
- Speech-only mode can complete the entire show without AI.

---

## 26. Vision Pro as ROB's voice and spatial control desk

> **SOURCE TRAIL — ANALYZING NOW:** `OperatorSpeechPanel.swift`, `ControlPanel.swift`, `ArmControlPanel.swift`, and `VideoPanel.swift` implement operator-facing features. Transport and the `rob-arm-control/2` domain live separately in the ROBControllerVision package named `ROBControlCore`. The code map prints each full path.

ROBControllerVision now adds a **Voice & Puppet Speech** panel beside the
camera and telemetry controls. It supports two intentionally different
meanings for the same recognized sentence.

**Command** sends the finalized phrase to Cerebro's normal `inputText:` path.
ROB interprets it just as if the operator typed into Cerebro. Existing local
handling—such as stop-oriented text—and the configured AI path remain in one
place.

**ROB Says It** sends the phrase to `ROBSpeechBox` verbatim. It does not ask a
language model to interpret the sentence. This is puppet speech: the human is
performing ROB's voice.

```text
Vision Pro microphone
  -> Speech framework partial transcript
  -> editable text field
  -> final transcript + selected mode
  -> authenticated ROBOperatorTextV1 message
       +-- command -------> Cerebro inputText:
       +-- puppetSpeech --> ROBSpeechBox sayIt:
```

The controller requests microphone and speech-recognition permission, displays
partial recognition locally, and automatically sends the final phrase in the
selected mode. The operator can edit or type text and use **Send as Input** or
**ROB Says It** manually. Cerebro verifies the version, sender, mode, length,
and control characters before dispatching on its main queue.

### 26.1 Demonstrating the new controls

1. Start Cerebro, then connect ROBControllerVision until its status is green.
2. In **Voice & Puppet Speech**, select **ROB Says It**.
3. Tap **Dictate**, say “Welcome to the robot workshop,” and pause. Confirm ROB
   says exactly that sentence.
4. Select **Command**, dictate a harmless informational request, and compare it
   with the same phrase entered through Cerebro's text field.
5. Disconnect and verify the buttons cannot send across a nonexistent session.
6. Deny microphone permission and verify typed text still works.

The voice feature does not arm motion, grant motion authority, or bypass the
physical emergency stop. Never present a spoken phrase as a replacement for a
dead-man control.

### 26.2 The rest of the spatial control path

The Vision Pro interface also makes previously invisible robot state easier to
teach:

- the front camera is the large center view, while belly and Insta360 feeds have independent authenticated pipelines;
- the panorama can open in a flat window or on a heading-adjustable inward-facing mixed-immersive sphere;
- side panels keep connection, voice, telemetry, and controls visible without
  vertical scrolling;
- Request/Release Control shows the authoritative owner and brakes before a new operator takes over;
- head orientation can drive the robot camera/neck while the required
  dead-man control is active;
- torso rotation follows the bounded head-turn control path when enabled;
- separate left/right AMBER authorities support measured on-screen joint lanes and simultaneous PSVR Sense jogging only while both grips are held;
- controller triggers remain reserved for the left and right grippers;
- controller pose and head commands are reflected in the SceneKit view for
  debugging, but pose is not converted into arm IK;
- transport remains paired and authenticated, and stale motion converges to
  neutral.

These features demonstrate an important design distinction. Spatial drive and
joint input are continuous, leased, and separately authorized. Voice input is
discrete text. Puppet speech is performance output. Flat and immersive media
are observation. They may share one headset and paired identity, but they
should not share ambiguous authority.

### Build exercise: add a third text mode without adding authority

Imagine a `captionOnly` mode that displays a sentence on ROB's screen but does
not speak or interpret it. Implement it on paper first:

1. Add a new enum value to the shared command schema.
2. Preserve a strict maximum length and reject control characters.
3. Add an explicit Cerebro receiver branch.
4. Route only to a caption view—never to `inputText:`, speech, or motion.
5. Add encode/decode and legacy-payload tests.
6. Build both applications and test an older peer's behavior.

This exercise teaches the safest way to grow a robot protocol: make meaning
explicit, keep authority narrow, validate on both ends, and prove the fallback.

---

## Epilogue: authorship after acceleration

The early repositories preserve the voice of one person working from several
machines: informal, immediate, hardware-aware, and willing to checkpoint an
uncertain experiment. The newer code does not erase that voice. It gives it
leverage.

The mature system is better not merely because it contains more code. It has
contracts where there were assumptions, bounded queues where there could be
backlogs, explicit authority where there was trust, tests where there was only
memory, and documentation where knowledge once lived in the workshop.

That is the best use of Codex in robotics. Let AI search widely, trace deeply,
draft quickly, compare both sides of a protocol, and remember every edge case
you name. Keep the human responsible for scope, evidence, physical validation,
and the decision to energize the machine.

---

## Sources and further reading

### Repository sources

- `ROBController` Git history through `50a2229`, August 22, 2026
- `Cerebro` Git history through `e76d515`, August 23, 2026
- `ROBControllerVision` local Git history through `63b9d9e`, August 22, 2026 (three commits ahead of its remote at inspection)
- `M2M1-RPLIDAR-iOS-MacOS-Catalyst-` Git history through `d6ad455`, August 22, 2026
- `Amber-HomeFolder` Git history through `722378a`, August 16, 2026
- `ROBTrainingGames` Git history through `92a7738`, August 14, 2026
- `ORobotics` Git history through `b1cc1a2`, August 15, 2026
- `ROBController/docs/rob-control-v2-and-autonomy.md`
- `ROBController/docs/robot-action-console.md`
- `ROBController/docs/watch-controller.md`
- `Cerebro/docs/rob-control-v2.md`
- `Cerebro/docs/controller-activated-autonomy.md`
- `Cerebro/docs/depth-camera.md`
- `Cerebro/docs/vision-pro-video.md`
- `Cerebro/docs/recording-and-training.md`
- `Cerebro/docs/messages-ai-bridge.md`
- `Cerebro/docs/face-identity.md`
- `Cerebro/docs/gemini-robotics-live.md`
- `Cerebro/docs/gemini-robotics-stage-action-plan.md`
- `Cerebro/docs/local-improvisation-provider.md`
- `Cerebro/Cerebro/ROBMLXRuntime.swift`
- `Cerebro/Cerebro/ROBMLXImprovisationProvider.swift`
- `Cerebro/Cerebro/ROBMLXStageObservation.swift`
- `Cerebro/Cerebro/ROBRecordingCoordinator.swift`
- `Cerebro/Cerebro/ROBMessagesBridge.swift`
- `Cerebro/Cerebro/ROBMessagesTranscriptStore.swift`
- `Cerebro/Cerebro/ROBFaceIdentityGallery.swift`
- `Cerebro/Cerebro/ROBFaceEmbeddingModel.swift`
- `Cerebro/Cerebro/ROBStageShowCoordinator.swift`
- `Cerebro/Cerebro/ROBStageShowProtocol.swift`
- `ROBControllerVision/ROBControllerVision/Platform/VisionSpeechInput.swift`
- `ROBControllerVision/ROBControllerVision/Features/Control/OperatorSpeechPanel.swift`
- `ROBControllerVision/ROBControllerVision/Features/Control/ArmControlPanel.swift`
- `ROBControllerVision/.../Control/ArmControlProtocol.swift` (the full path is in the source map)
- `M2M1-RPLIDAR-iOS-MacOS-Catalyst-/README.md`

### Official OpenAI documentation

- [Prompting for ChatGPT and Codex](https://learn.chatgpt.com/docs/prompting)
- [Codex use cases](https://developers.openai.com/codex/use-cases)
- [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model)
- [OpenAI API models](https://developers.openai.com/api/docs/models)

Consult the current official documentation when implementing; models,
capabilities, availability, and SDK shapes can change after this edition.
