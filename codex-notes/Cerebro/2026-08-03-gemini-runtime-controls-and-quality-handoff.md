# Cerebro Gemini runtime controls and quality handoff

Date: 2026-08-03

Repository: `/Users/raramayo/dev/Cerebro`

Status: implemented and deterministic-contract/build validated in a dirty,
uncommitted checkout. No billable Gemini request, physical microphone test,
physical camera test, or robot-motion test was run for this final runtime-control
pass.

This note supplements
[`2026-08-03-local-improvisation-handoff.md`](2026-08-03-local-improvisation-handoff.md).
Read both before making changes.

## Instructions for the resuming agent

1. Work only in `/Users/raramayo/dev/Cerebro` unless the user explicitly
   expands scope.
2. Run `git status --short` before editing. This checkout intentionally contains
   overlapping user and agent work. Do not reset, clean, discard, or overwrite
   unrelated changes.
3. Read this note completely, then read:
   - `codex-notes/2026-08-03-local-improvisation-handoff.md`
   - `docs/gemini-robotics-live.md`
   - `docs/gemini-robotics-stage-action-plan.md`
   - `docs/local-improvisation-provider.md`
   - `docs/rob-control-v2.md`
4. Treat current source as authoritative. Reinspect the named symbols because
   line numbers and concurrent work may have moved since this snapshot.
5. Preserve the runtime privacy and ordering invariants below. They are part of
   the feature contract, not incidental implementation details.
6. Keep Gemini camera demand independent from Cerebro perception and
   ROBController/Vision Pro subscriptions.
7. Keep `stop_motion` on the priority local safety path. A model response or
   cancellation is never evidence that hardware stopped.
8. Re-run the standalone fixtures, unsigned macOS build, project lint, and
   `git diff --check` after material edits. The project currently has one app
   target and no Xcode unit-test target.
9. Do not log or copy credentials, media, transcript bodies, tool arguments,
   raw provider messages, or session-resumption handles into diagnostics,
   fixtures, or handoff notes.
10. Do not make a billable provider request, operate hardware, rotate a secret,
    rewrite Git history, commit, or push unless the user explicitly authorizes
    that action.

## Current Gemini implementation

An older audit described `ROBAI.swift` as one-shot `generateContent` code. That
is no longer current. The present source implements a persistent Gemini Live
WebSocket session and a Swift/Objective-C facade. Always verify current source,
but do not restart from the obsolete one-shot premise.

### Operator runtime controls

The main-window **Gemini...** control opens
`ROBGeminiDiagnosticsWindowController`. It exposes three independent choices:

- connect or disconnect Gemini Live;
- send or stop raw microphone audio;
- send or stop sampled JPEG camera frames.

`GeminiRoboticsRuntimeSettings` persists only operator intent in
`UserDefaults`:

```text
com.orbitusrobotics.cerebro.gemini.connection-enabled
com.orbitusrobotics.cerebro.gemini.audio-streaming-enabled
com.orbitusrobotics.cerebro.gemini.video-streaming-enabled
```

On first use, launch configuration supplies the defaults. With no valid launch
configuration, all three settings fail closed. Credentials, model, response
modality, system instruction, and tool exposure remain launch configuration and
are not written to `UserDefaults`. Malformed boolean launch values for media or
tool exposure also fail closed.

The panel distinguishes requested policy from actor-applied policy, shows the
active input route, and reports redacted video/session diagnostics. A locally
completed WebSocket send is not a Gemini receipt, semantic acknowledgement, or
billing record.

### Runtime transition invariants

`ROBAI` and `GeminiRoboticsLiveSession` use a monotonically increasing policy
revision plus independent connection, audio, and video generations. Preserve
these guarantees:

- Connection off closes admission before asynchronous cleanup, prevents
  reconnect, clears stale media, and terminates accepted queued/in-flight work
  with explicit failure rather than silence.
- Cerebro requests its local priority software stop before network-side
  cancellation of controller-authorized physical actions.
- Audio off sends `audioStreamEnd`. A locally recognized text fallback waits
  behind the actor-applied audio-off revision so text cannot overtake the end
  marker on the WebSocket.
- Video off invalidates old encoded frames. Stale work must not cross a socket
  or generation boundary after any `await`.
- Tool-response, audio, and video drain loops retain explicit owner identities;
  a stale loop must not clear or mutate a replacement loop's state.
- A failed text send is correlated to its own turn/context and must not fail a
  newer turn.
- A requested switch is not effective until the session actor applies it. UI
  and camera demand should use effective state where egress correctness depends
  on that acknowledgement.

Relevant implementation areas are `ROBAI.swift`,
`GeminiRoboticsProtocol.swift`, `ROBGeminiDiagnosticsWindowController.swift`,
`ROBMainViewController.mm`, and `ROBMainWindowController.m`.

### Speech behavior

`sendText` now reports whether a request was accepted. Cerebro should not say
only "let me think" and then silently stop: unavailable, disabled, queue-full,
send-failure, timeout, and response-without-usable-text paths must produce a
clear terminal result. Wake-name matching must remain token-aware rather than a
substring test. Local spoken stop remains available even when Gemini is off.

Raw microphone audio and Apple local-recognition text are alternative input
routes. A remaining architecture issue is that the route is chosen from current
ready state at the final local transcript callback; pin the route once per
utterance before expanding this subsystem.

### Camera and controller/Vision Pro independence

`CameraViewController.setGeminiVideoDemandActive(_:)` adds Gemini as one camera
consumer. Camera-session reconciliation must continue to account separately
for:

- the local camera view;
- remote `ROBVideoServer` demand from ROBController or Vision Pro;
- actor-applied Gemini video demand.

Turning Gemini video off must never stop an active controller/Vision Pro stream
or Cerebro's local perception. Conversely, a remote subscriber must be able to
start camera capture while the Gemini switch is off. Video is sampled semantic
context, not a visual-servoing or collision-avoidance channel.

## Validation baseline

The final runtime-control pass reported these successful checks on 2026-08-03:

- Swift type checking for the changed Swift surface;
- Gemini protocol fixture executable;
- robot-action fixture executable;
- local improvisation fixture executable;
- stage-show fixture executable;
- unsigned Debug macOS build using a writable `/tmp` DerivedData path;
- `plutil -lint Cerebro.xcodeproj/project.pbxproj`;
- `git diff --check`;
- a temporary 720 by 700 diagnostics-window layout harness with no clipped or
  ambiguous constraints.

The layout harness lived in `/tmp`, not in this repository, so it is evidence
from that run rather than a durable automated test. `xcodebuild -list` currently
reports one target and one scheme, both named `Cerebro`; there is no Xcode test
target. Xcode may emit existing CoreSimulator, provisioning-profile, storyboard,
deprecation, and legacy Objective-C warnings even when the unsigned macOS build
exits successfully. Judge the exit status and separate source failures from
environment noise.

Use the fixture and build commands already recorded under **Validation** in
`docs/gemini-robotics-live.md` and in the local-improvisation handoff. Give each
run a fresh writable output or DerivedData path if concurrent agents may be
building. Do not infer that deterministic fixtures exercised a real Gemini
account, physical microphone/camera, controller, or robot.

## Highest-priority quality and safety findings

These were open at handoff. Reconfirm each against current code before editing.

### 1. Remove exposed Wi-Fi secrets and unsafe credential handling

`ROBMainViewController.mm` contains real-looking Wi-Fi SSID/password literals
near the `joinWifi:` actions and splits an incoming credential string blindly on
`:`. The actual values are deliberately omitted here. In
`TaskControllers/JoinWifiTaskController.m`, the password is passed as a process
argument, making it observable to other local processes.

Recommended response: rotate affected credentials, remove literals from source
and history through a separately authorized security operation, store operator
secrets in Keychain, replace the delimiter format with a typed validated
request, and avoid command-line arguments for secret transfer. Do not rotate or
rewrite history without explicit authorization.

### 2. Replace unchecked controller-motion parsing

`ROBMainViewController.mm` parses a multi-line controller message with fixed
array indices and nested delimiter splits, then accepts `floatValue` results
without finite/range validation. Authentication establishes identity, not
payload safety. Malformed input can index out of bounds, and NaN or extreme
values can reach motion-related code. `ROBSerialBox.m` has incomplete clamping
at downstream boundaries.

Introduce a versioned typed controller snapshot decoder that validates exact
field counts, labels, booleans, finite numeric values, units, and calibrated
ranges before producing an immutable command. Reject an entire invalid frame;
do not partially apply it. Add malformed/truncated/NaN/infinity/boundary
fixtures before connecting the decoder to hardware.

### 3. Serialize serial-port lifecycle and remove busy waits

`ROBSerialBox.m` closes file descriptors while read-thread flags are shared
without synchronization, busy-waits for those flags, and calls `sleep(0.5)`;
the integer-seconds API truncates that value to zero. Other paths mutate AppKit
objects from background work.

Move each serial context to an owned serial queue or actor-like state machine,
use explicit cancellation/completion rather than shared polling flags, and use
an appropriate subsecond timing API only off the main thread. Marshal UI state
to the main queue. Add reconnect, close-during-read, partial-read, and repeated-
open tests with fake descriptors before hardware validation.

### 4. Validate and sequence keyframes off the main thread

`ROBTorsoControlsViewController.m` defaults an absent selection to index zero,
indexes the keyframe array without proving it is nonempty, and blocks with
`sleep(2)`. `KeyframeAnimationManager.swift` decodes persisted keyframes without
a validation boundary for finite values, joint limits, duration limits, or
schema migration.

Add a versioned validated keyframe model, calibrated per-joint envelopes, and a
cancellable nonblocking sequencer. UI code should request a validated plan and
observe progress; it should not sleep or issue an unchecked persisted frame
directly to servos.

### 5. Correlate speech completion to its stage cue

`ROBMainViewController.didFinishProcessingSpeech` forwards every speech
completion to `ROBStageShowCoordinator.speechDidFinish()`. The coordinator
advances whenever it is awaiting any speech, so unrelated Gemini or operator
speech can finish the wrong stage cue.

Carry an immutable utterance/cue identifier from the stage speak request through
`ROBSpeechBox` completion and require an exact match before advancing. Invalidate
the identifier on stop, timeout, reload, or replacement. Add tests for unrelated,
late, duplicate, and post-cancellation callbacks.

## Reusable AI interface development order

After the security and motion-safety issues above, use this order:

1. Extract a provider-neutral `AIConversationService` with typed text, audio,
   video, tool-call, lifecycle, error, cancellation, and usage events. Keep
   Gemini wire types inside one adapter.
2. Inject credential provider, WebSocket transport, clock, retry sleeper, and
   preferences store. Add ephemeral-token refresh without exposing secrets to
   logs or persistent settings.
3. Add an Xcode test target for the session actor. Cover rapid-toggle last-write-
   wins behavior, acknowledged no-egress boundaries, stale sockets/generations,
   bounded media backpressure, reconnect cancellation, and exactly one terminal
   result for every accepted request.
4. Pin the audio-versus-text route per utterance and make that route observable
   in redacted diagnostics.
5. Add local counters for session duration, text requests, audio bytes/chunks,
   video bytes/frames, and dropped work. Provider usage metadata or its console
   remains authoritative for billing.
6. Split the roughly 2,100-line `ROBAI.swift`, 2,100-line
   `ROBMainViewController.mm`, and 2,500-line `ROBSerialBox.m` into cohesive
   services with narrow Objective-C bridges. Keep robot safety policy out of a
   provider adapter.

## Suggested restart objective

> Resume Cerebro from both files in `codex-notes`. Preserve the dirty tree and
> first rerun deterministic fixtures plus the unsigned macOS build. Then address
> one isolated high-risk boundary—preferably the typed controller-frame decoder
> with malformed-input tests, or cue-correlated stage speech—without mixing it
> with the provider-neutral AI refactor. If the user instead prioritizes Gemini,
> introduce dependency seams and an Xcode actor test target before changing Live
> behavior. Preserve actor-applied runtime controls, `audioStreamEnd` ordering,
> independent Vision Pro/controller camera demand, diagnostic redaction, and
> the priority local stop path.

## Provider references

Refresh these before changing the Live wire contract because preview APIs can
change:

- <https://ai.google.dev/gemini-api/docs/live-api/session-management>
- <https://ai.google.dev/api/live>
- <https://ai.google.dev/gemini-api/docs/live-api/capabilities>

## Notes relocation addendum — 2026-08-03

This handoff now lives in /Users/raramayo/dev/codex-notes/Cerebro. References
above to codex-notes/2026-08-03-local-improvisation-handoff.md resolve to the
sibling file in that central directory. Source and validation commands still
run from /Users/raramayo/dev/Cerebro. Preserve this historical handoff and
append a new dated checkpoint for later implementation work.
