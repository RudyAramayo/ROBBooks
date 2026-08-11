# Cerebro local improvisation and Gemini Live handoff

Date: 2026-08-03

Repository: `/Users/raramayo/dev/Cerebro`

Status: implemented and deterministic-contract validated; not committed; no
live llama.cpp/model round trip was possible on this Mac.

## Development objective

Cerebro now has a bounded local improvisation provider that can add useful
offline intelligence without becoming a robot-motion authority. Its first task
is a **stage director** for `gemini_turn` cues:

1. A validated show cue supplies a trusted scene goal and mandatory authored
   fallback.
2. A local provider returns schema-constrained JSON containing only an
   allow-listed beat, allow-listed delivery style, and short offline spoken
   line.
3. In **Run Local**, Cerebro speaks the validated local line without Gemini.
4. In **Run Adaptive**, Cerebro constructs a trusted Gemini prompt from the
   authored scene goal and the two enums. Free-form local output is not copied
   into Gemini's prompt.
5. Gemini may add live camera/audio context only when its independent runtime
   input switches are enabled.
6. Gemini failure uses the validated local line when one exists; otherwise the
   cue's authored fallback is used.

This gives the droid more varied show dialogue while keeping physical behavior
inside deterministic, supervised code.

## Implemented code

### Local-provider contract

- `Cerebro/ROBLocalImprovisationProtocol.swift`
  - Provider kinds: `llama_cpp` and the future `mlx_swift` adapter.
  - Strict plan v1 fields: `schema`, `version`, `beat`, `delivery`, and
    `offline_line`.
  - Exact-field decoding, bounded single-line text, allow-listed enums, and
    prohibited obvious control language.
  - UserDefaults/environment configuration and sanitized diagnostics.
  - `ROBLocalImprovisationProviderRegistry.registerMLXFactory` is the future MLX
    injection point.
  - Selecting MLX without a registered adapter returns an unavailable provider
    instead of crashing.

### llama.cpp provider

- `Cerebro/ROBLlamaCppImprovisationProvider.swift`
  - Uses the OpenAI-compatible `POST /v1/chat/completions` endpoint with
    `response_format.type = json_object` and the strict JSON schema.
  - Uses `GET /health` before a real schema-generation preflight.
  - Accepts only literal `127.0.0.1` or `::1` HTTP(S) endpoints. DNS hostnames,
    credentials, arbitrary paths, redirects, and final-URL mismatches fail
    closed.
  - Incrementally bounds response buffering to 64 KiB for chat and 4 KiB for
    health, including early `Content-Length` rejection.
  - Protects duplicate request IDs and provides deterministic, exactly-once
    explicit cancellation completion and diagnostics.
  - Never installs, launches, or assumes the presence of `llama-server`.

### Stage coordination and UI

- `Cerebro/ROBStageShowCoordinator.swift`
  - Adds local-only and adaptive local-director routing.
  - Gives local inference at most 35 percent of an adaptive cue deadline,
    capped by the configured provider timeout.
  - Correlates and cancels late local/Gemini work by request ID.
  - Dequeues queued Gemini stage turns at timeout; an already-sent stage turn
    aborts the Live socket and reconnects without resuming that server session.
- `Cerebro/ROBStageShowWindowController.swift`
  - Provides enabled/provider/endpoint/model/timeout controls plus **Save
    Local**, **Test Local**, **Run Local**, and **Run Adaptive**.
  - Applies configuration before persisting it, so a rejected edit during a
    running show is not saved.
  - Preserves the loaded effective temperature even though temperature is
    currently environment/UserDefaults-only.
  - **Test Local** performs both health and schema-constrained generation checks.
- `Cerebro/ROBStageShowProtocol.swift`
- `Cerebro/StageShows/MakerFaireOpening.robshow.json`
- Xcode membership and bundled-resource entries are present in
  `Cerebro.xcodeproj/project.pbxproj`.

### Gemini lifecycle and physical-action boundary

- `Cerebro/ROBAI.swift`
  - `ROBAIRobotToolCall` carries immutable `originContextID` and
    `isStageOrigin` values.
  - Tool origin is captured before a combined `toolCall + turnComplete` event
    can clear the active text turn, and is preserved while tool calls wait in
    the blocking queue.
  - `cancelTextTurnWithContextID:` uses cancellation tombstones, removes queued
    work, suppresses cancelled callbacks, and aborts an in-flight stage socket
    without session resumption.
- `Cerebro/GeminiRoboticsProtocol.swift`
  - Contains the exact `stage:` context-prefix policy helper.
- `Cerebro/ROBMainViewController.mm`
  - Forwards stage cancellation into ROBAI.
  - Handles `stop_motion` first through the priority safety lane.
  - Permanently rejects every other stage-originated `robot_action`, even after
    the cue or show has ended.
  - Also rejects uncorrelated non-stop actions while the deterministic stage
    runner is active.

## Safety invariants that must remain true

1. The local provider is a dialogue planner, not a motion planner.
2. Free-form `offline_line` text is never inserted into the Gemini prompt.
3. The local response schema must not gain joints, servo values, trajectories,
   shell commands, hosts, ports, URLs, or generic tool arguments.
4. A `stage:` Gemini context can never authorize non-stop physical action,
   regardless of whether the show is still running when the tool is delivered.
5. `stop_motion` remains available and priority-dispatched before the stage
   rejection gate.
6. Timed-out/cancelled Gemini stage work must not remain queued for later send.
7. Loopback HTTP must remain literal-address-only, redirect-free, exact-final-
   URL checked, and incrementally bounded.
8. Missing providers, models, servers, malformed output, timeout, and
   cancellation must remain recoverable app states, never process crashes.
9. Show files must retain a mandatory authored `fallback_text` for every
   `gemini_turn`.
10. Named gesture cues must continue to fail closed until an immutable,
    calibrated catalog and feedback-capable executor exist.

## Effective configuration

The Show panel persists the effective configuration. Equivalent launch-time
environment settings are:

```text
ROB_LOCAL_IMPROV_ENABLED=true
ROB_LOCAL_IMPROV_PROVIDER=llama_cpp
ROB_LLAMA_CPP_ENDPOINT=http://127.0.0.1:8080
ROB_LOCAL_IMPROV_MODEL=cerebro-local
ROB_LOCAL_IMPROV_TIMEOUT_SECONDS=3
ROB_LOCAL_IMPROV_TEMPERATURE=0.6
```

Environment values take precedence when settings are loaded.

Typical server command, once a compatible GGUF chat model is available:

```bash
llama-server \
  --model /absolute/path/to/model.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --alias cerebro-local \
  --ctx-size 4096
```

Then open **Show…**, enable the local director, save, run **Test Local**, test
**Run Local**, and only then try **Run Adaptive**. For camera-aware adaptive
dialogue, connect Gemini, enable video, and confirm its encoded/sent counters in
the Gemini diagnostics panel.

## Validation baseline

Use a writable module cache in this environment.

### Local provider

```bash
swiftc -module-cache-path /tmp/cerebro-swift-module-cache \
  -parse-as-library \
  Cerebro/ROBLocalImprovisationProtocol.swift \
  Cerebro/ROBLlamaCppImprovisationProvider.swift \
  Tests/ROBLocalImprovisationFixtureTests.swift \
  -o /tmp/ROBLocalImprovisationFixtureTests

/tmp/ROBLocalImprovisationFixtureTests
```

Expected: `ROB local improvisation fixtures passed`.

### Stage routing

```bash
swiftc -module-cache-path /tmp/cerebro-swift-module-cache \
  -parse-as-library \
  Cerebro/ROBLocalImprovisationProtocol.swift \
  Cerebro/ROBLlamaCppImprovisationProvider.swift \
  Cerebro/ROBStageShowProtocol.swift \
  Cerebro/ROBStageShowCoordinator.swift \
  Tests/ROBStageShowFixtureTests.swift \
  -o /tmp/ROBStageShowFixtureTests

/tmp/ROBStageShowFixtureTests
```

Expected: `ROB stage-show fixtures passed`.

### Gemini protocol and robot-action fixtures

```bash
swiftc -module-cache-path /tmp/cerebro-swift-module-cache \
  Cerebro/GeminiRoboticsProtocol.swift \
  Tests/GeminiRoboticsProtocolFixtureTests.swift \
  -o /tmp/CerebroGeminiProtocolFixtureTests

/tmp/CerebroGeminiProtocolFixtureTests

swiftc -module-cache-path /tmp/cerebro-swift-module-cache \
  Cerebro/ROBRobotActionProtocol.swift \
  Cerebro/ROBAutonomyCoordinator.swift \
  Tests/ROBRobotActionProtocolFixtureTests.swift \
  -o /tmp/CerebroRobotActionProtocolFixtureTests

/tmp/CerebroRobotActionProtocolFixtureTests
```

Expected: both fixture suites pass.

### Unsigned macOS build

```bash
xcodebuild -quiet \
  -project Cerebro.xcodeproj \
  -scheme Cerebro \
  -configuration Debug \
  -destination 'platform=macOS' \
  -derivedDataPath /tmp/CerebroLocalImprovDerivedData \
  CODE_SIGNING_ALLOWED=NO \
  build
```

The last run exited successfully. Xcode still emitted environment/legacy
warnings involving CoreSimulator, malformed local provisioning profiles, older
Objective-C code, storyboard sources, and existing compiler warnings. Do not
misreport those warnings as a failed macOS build.

### Consistency checks

```bash
plutil -lint Cerebro.xcodeproj/project.pbxproj
jq -e . Cerebro/StageShows/MakerFaireOpening.robshow.json
git diff --check
```

The bundled and source sample hashes matched at handoff:

```text
6b98064dd2a623c9c3345436577cd98ad66761c527740b6ecb4de3eaf2d5c8e4
```

## Current evidence and limitations

- All four deterministic fixture suites, project/resource lint, JSON parsing,
  `git diff --check`, and the unsigned macOS build passed on 2026-08-03.
- `llama-server` was not found on `PATH`. The HTTP request/response contract was
  tested with deterministic local URLProtocol fixtures, not a real model.
- The provider should therefore be described as **implemented and
  contract-validated**, not proven live-working.
- MLX Swift is not linked. The registry seam targets the current
  `mlx-swift-lm` guided-generation path, but there is no pinned package,
  packaged model, model manager, warm-up flow, or crash-isolated helper yet.
- The stage director intentionally does not move the robot. Physical performance
  still needs a calibrated gesture catalog, observed completion, arm/tread
  safety envelopes, and deterministic executors.
- The working tree is dirty and includes additional Gemini diagnostics,
  autonomy, camera, pairing, and other user/agent changes. Preserve them.
- No commit was created for this implementation.

## Recommended next development sequence

1. **Real llama.cpp smoke test:** choose and record a compatible GGUF chat
   model, start `llama-server` on literal loopback, run **Test Local**, Run Local,
   then Run Adaptive. Record server/model versions, latency, actual schema
   compliance, and failure behavior. Do not auto-download or auto-install it.
2. **Quality evaluation:** create a small fixed set of show cues and score plan
   validity, latency, repetition, family-friendliness, and fallback quality.
   Keep this separate from transport correctness.
3. **Native MLX adapter:** pin compatible `mlx-swift-lm` and guided-generation
   versions in an isolated branch/target. Implement
   `ROBLocalImprovisationProviding`, reuse the exact plan codec, precompile the
   grammar off the main thread, and prefer a helper process so Metal/model
   failures cannot terminate Cerebro.
4. **Show authoring improvements:** add a safe cue editor or templates without
   expanding the schema into arbitrary physical commands.
5. **Motion only after calibration:** implement immutable named gestures with
   joint limits, timeouts, cancellation, feedback, and a supervised executor.
   Gemini/local models may choose a gesture name but must never supply raw
   trajectory values.

## Upstream references to refresh before dependency work

- llama.cpp server: <https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md>
- llama.cpp installation: <https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md>
- MLX Swift: <https://github.com/ml-explore/mlx-swift>
- MLX Swift LM: <https://github.com/ml-explore/mlx-swift-lm>
- MLX guided generation: <https://github.com/ml-explore/mlx-swift-lm/tree/main/Libraries/MLXGuidedGeneration>

These projects change quickly. Verify their current package products, platform
requirements, request schema, and release versions rather than relying only on
this note.

## Addendum: Gemini runtime controls and quality audit (2026-08-03)

After this local-improvisation handoff was written, the Gemini work received a
separate runtime-control, concurrency, diagnostics, and code-quality pass. Read
[`2026-08-03-gemini-runtime-controls-and-quality-handoff.md`](2026-08-03-gemini-runtime-controls-and-quality-handoff.md)
before resuming development.

That addendum is authoritative for the newer Gemini state. In particular,
`ROBAI.swift` is now a persistent Gemini Live WebSocket implementation, not the
older one-shot `generateContent` implementation described by an earlier audit.
It also records the independent connection/audio/video switches, actor-applied
policy boundary, `audioStreamEnd` ordering, controller/Vision Pro camera-demand
independence, validation limits, and the current security/safety backlog.

Preserve both handoffs together: the local provider remains dialogue-only and
stage-origin non-stop actions remain prohibited, while the Gemini addendum's
privacy, egress-generation, stale-socket, diagnostic-redaction, and priority
software-stop invariants also remain in force.

## Notes relocation addendum — 2026-08-03

This handoff now lives in /Users/raramayo/dev/codex-notes/Cerebro. References
above to codex-notes/2026-08-03-gemini-runtime-controls-and-quality-handoff.md
resolve to the sibling file in that central directory. Source and validation
commands still run from /Users/raramayo/dev/Cerebro. Preserve this historical
handoff and append a new dated checkpoint for later implementation work.
