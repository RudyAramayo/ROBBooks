# Cerebro Codex handoff

Start with [2026-08-03-local-improvisation-handoff.md](2026-08-03-local-improvisation-handoff.md).
It records the current repository state, architecture, safety invariants,
validation commands, and unfinished work for the local llama.cpp/MLX stage
director and Gemini Live integration.

## Instructions for the next agent

1. Work only in `/Users/raramayo/dev/Cerebro` unless the user explicitly
   expands the scope.
2. Read the detailed handoff completely, followed by:
   - `docs/local-improvisation-provider.md`
   - `docs/gemini-robotics-live.md`
   - `docs/gemini-robotics-stage-action-plan.md`
3. Run `git status --short` before editing. The checkout intentionally contains
   uncommitted user and agent work. Do not reset, clean, discard, or overwrite
   unrelated changes.
4. Treat the source as authoritative. Reinspect current code rather than
   assuming these notes are still current.
5. Preserve the safety invariants in the handoff. In particular, local model
   text is dialogue-only, stage-originated Gemini actions cannot authorize
   motion, and `stop_motion` remains the priority exception.
6. Re-run the documented deterministic fixtures and unsigned macOS build before
   and after material changes.
7. Do not claim live llama.cpp interoperability until **Test Local** completes
   against an actual `llama-server` and named GGUF model. No live server was
   available during this handoff.
8. Do not claim that native MLX is implemented. The current MLX selection is a
   fail-safe provider seam; it still needs a pinned package/model and adapter.
9. Do not commit, push, install a model, or download multi-gigabyte artifacts
   unless the user asks for that action.

## Suggested restart objective

> Resume Cerebro development from `codex-notes/2026-08-03-local-improvisation-handoff.md`.
> First verify the dirty working tree and rerun the local-provider, stage-show,
> Gemini protocol, robot-action, and unsigned macOS build checks. Then perform
> the highest-value unfinished task that is authorized: preferably a real
> loopback llama.cpp model smoke test and recorded compatibility result, or a
> separately isolated native MLX Swift adapter with the same strict plan schema.
> Preserve all stage-origin tool suppression, context cancellation, response
> limits, and authored fallback behavior.

## Gemini runtime controls and quality addendum (2026-08-03)

Continue with
[`2026-08-03-gemini-runtime-controls-and-quality-handoff.md`](2026-08-03-gemini-runtime-controls-and-quality-handoff.md)
after reading the local-improvisation handoff. It records the completed
connection/audio/video runtime switches, actor-applied transition guarantees,
Vision Pro and ROBController camera-demand separation, final validation
boundary, and current high-priority code-quality findings.

Additional instructions for the next agent:

1. Do not rely on the older description of `ROBAI.swift` as one-shot
   `generateContent` code. Current source is a persistent Gemini Live WebSocket
   implementation; reinspect it before changing its lifecycle.
2. Preserve actor-applied policy revisions, independent connection/audio/video
   generations, `audioStreamEnd` ordering, stale-work rejection, and explicit
   terminal outcomes for accepted requests.
3. Never make the Gemini video switch own the camera globally. Local perception
   and active ROBController/Vision Pro video subscriptions are independent
   consumers.
4. Keep diagnostics redacted and distinguish requested state, effective local
   egress state, provider acknowledgement, and provider billing.
5. Before broad AI refactoring, isolate the exposed Wi-Fi credentials,
   controller-frame parsing, serial lifecycle, keyframe playback, and
   stage-speech correlation findings described in the addendum.
6. No final runtime-control pass made a billable Gemini request or exercised a
   physical microphone, camera, controller, or robot. Do not describe those
   paths as revalidated without new supervised evidence.

## Alternate restart objective: Gemini and reusable AI

> Resume from
> `codex-notes/2026-08-03-gemini-runtime-controls-and-quality-handoff.md`,
> confirm the dirty tree and validation baseline, and preserve every listed
> privacy, camera-demand, ordering, and stop-motion invariant. For reusable AI
> work, first add provider, credential, transport, clock, sleeper, and preference
> seams plus an Xcode actor test target; then extract a provider-neutral
> conversation interface. Keep any controller parser, serial, keyframe, or stage
> speech safety repair in a separately reviewable change.

## Centralized notes location — 2026-08-03

This instruction set was preserved and moved from the repository-local
Cerebro/codex-notes directory to:

/Users/raramayo/dev/codex-notes/Cerebro

Read the central index first:

/Users/raramayo/dev/codex-notes/README.md

Older references in these handoffs to codex-notes/filename.md mean the sibling
file in this central Cerebro directory. Continue to run source, fixture, and
build commands from /Users/raramayo/dev/Cerebro. Append future Cerebro
checkpoints here; do not recreate a second project-local codex-notes tree.
