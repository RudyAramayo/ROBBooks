# Central Codex project notes

Canonical notes directory: /Users/raramayo/dev/codex-notes

Consolidated: **2026-08-03**

This is the single continuation-notes tree for projects under
/Users/raramayo/dev. Earlier project-local codex-notes directories were copied,
checksum-verified, and removed after their contents were preserved here under
project-named subdirectories.

## Start here

1. Read [NEXT-AGENT-INSTRUCTIONS.md](NEXT-AGENT-INSTRUCTIONS.md).
2. Choose the project in scope.
3. Read that project's README and every handoff it identifies.
4. Inspect the live repository or project directory before editing. Notes are a
   checkpoint; current source and current user instructions are authoritative.

| Project | Working directory | First note to read |
|---|---|---|
| Cerebro | /Users/raramayo/dev/Cerebro | [Cerebro/README.md](Cerebro/README.md) |
| ORobotics | /Users/raramayo/dev/ORobotics | [ORobotics/README.md](ORobotics/README.md) |
| ROB-Books | /Users/raramayo/dev/ROB-Books | [ROB-Books/README.md](ROB-Books/README.md) |

The original six files and their pre-append hashes are recorded in
[MIGRATION-MANIFEST.md](MIGRATION-MANIFEST.md).

## Maintenance contract

- Keep notes grouped by project. Do not flatten same-named files.
- Preserve existing handoffs. Append dated corrections or add a new
  YYYY-MM-DD-topic-handoff.md instead of silently replacing history.
- Update the project README's reading order whenever a new handoff is added.
- Record live status, exact validation commands and results, unresolved work,
  safety boundaries, and whether changes are committed.
- Never copy credentials, tokens, private addresses, sensitive screenshots, raw
  media, or session-resumption handles into these notes.
- Do not infer authority to commit, push, deploy, download large models, operate
  ROB, or publish the books merely because a handoff describes those actions.

## Relocation rule

Older preserved notes may say to read codex-notes/... from inside a repository.
Interpret those historical paths through this central tree:

- Cerebro/codex-notes/... becomes
  /Users/raramayo/dev/codex-notes/Cerebro/...
- ORobotics/codex-notes/... becomes
  /Users/raramayo/dev/codex-notes/ORobotics/...

Repository source paths and validation commands still run from each repository's
own working directory.

