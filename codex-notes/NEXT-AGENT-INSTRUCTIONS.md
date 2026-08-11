# Instructions for the next development agent

## Starter prompt

> Resume the requested project under /Users/raramayo/dev. First read
> /Users/raramayo/dev/codex-notes/README.md and the complete project-specific
> handoff it names. Inspect the live filesystem and, where applicable, Git status
> and diff before editing. Preserve all unrelated user and agent work. Treat
> current source as authoritative, rerun the project's documented validation,
> and do not commit, push, deploy, publish, download large artifacts, or operate
> physical hardware unless explicitly authorized.

## Required restart sequence

1. Confirm the central notes tree:

   ~~~sh
   find /Users/raramayo/dev -type d -name codex-notes -prune -print
   ~~~

   The expected result is exactly:
   /Users/raramayo/dev/codex-notes

2. Read this index and the relevant project notes completely:

   ~~~sh
   sed -n '1,260p' /Users/raramayo/dev/codex-notes/README.md
   sed -n '1,360p' /Users/raramayo/dev/codex-notes/NEXT-AGENT-INSTRUCTIONS.md
   ~~~

3. Select only the project authorized by the user:

   - Cerebro:
     /Users/raramayo/dev/codex-notes/Cerebro/README.md
   - ORobotics:
     /Users/raramayo/dev/codex-notes/ORobotics/README.md
   - ROB-Books:
     /Users/raramayo/dev/codex-notes/ROB-Books/README.md

4. If the project is a Git repository, establish its current state before
   editing:

   ~~~sh
   git status --short --branch
   git diff --stat
   git diff --check
   git ls-files --others --exclude-standard
   ~~~

   Do not use reset, checkout-discard, clean, or other destructive cleanup
   commands. Dirty-tree changes belong to the user unless proven otherwise.

5. Reinspect every source file relevant to the new task. Handoff dates, commit
   identifiers, line numbers, provider APIs, build tools, and hardware state can
   drift.

6. Run the project's recorded baseline before and after material changes. Report
   environment blocks separately from source failures. Never describe a
   deterministic fixture as a live provider, hardware, privacy, or safety test.

7. At handoff, append a dated checkpoint or add a dated topical handoff in this
   central tree. Preserve earlier instructions and update the project README's
   reading order.

## Project routing

### Cerebro

Read both dated Cerebro handoffs. Preserve the dirty working tree, priority local
stop path, dialogue-only local improvisation boundary, stage-origin action
suppression, actor-applied Gemini privacy controls, independent camera consumers,
and diagnostic redaction. Revalidate current source before relying on any older
description.

### ORobotics

Read the project handoff and next-agent instructions. Preserve the uncommitted
QR3D work, exact uppercase /QR3D/ route, Hugo/GitHub Pages contract, gallery and
subpath validators, and custom domain. Do not commit, push, deploy, or alter
repository settings without explicit authorization.

### ROB-Books

Read the ROB-Books project handoff and restart instructions. The folder is not a
standalone Git worktree. Preserve the evidence/status distinctions, visible
builder-input placeholders, private-image quarantine, youth-safety boundaries,
and original unbranded retro-space visual treatment. The current PDFs are
editorial/layout proofs, not certified construction plans or printer-specific
press files.

## Scope and safety guardrails

- Work only in the project requested by the user unless scope is explicitly
  expanded.
- A software stop is not proof that high-energy hardware stopped.
- Do not expose or copy credentials, location data, private UI, or identifiable
  people into documentation or fixtures.
- Keep AI-generated art labeled as illustration, not engineering evidence.
- Obtain accountable engineering, privacy, rights, youth-safety, and physical
  print review before public distribution of the ROB books.

