# codex-notes consolidation manifest

Date: **2026-08-03**

The following six regular files were copied with permissions and timestamps
preserved, compared byte-for-byte against their sources, and then relocated into
project namespaces. The two empty source directories were removed only after
verification.

| Former path under /Users/raramayo/dev | Canonical path under codex-notes | Original SHA-256 |
|---|---|---|
| Cerebro/codex-notes/2026-08-03-gemini-runtime-controls-and-quality-handoff.md | Cerebro/2026-08-03-gemini-runtime-controls-and-quality-handoff.md | 9f8feb951a440fbdd1b05827f35be02d801b6c18ba82f009376a3b49143c0f5c |
| Cerebro/codex-notes/2026-08-03-local-improvisation-handoff.md | Cerebro/2026-08-03-local-improvisation-handoff.md | b1165df3e5c920fe5c4a87e713f02dd23be8dfee154a913ed0ed581dd2ecff71 |
| Cerebro/codex-notes/README.md | Cerebro/README.md | e7c117227ca785dff7de6c64207633404b1ae77d11d7aed7ff5c0ad2de6f9a04 |
| ORobotics/codex-notes/NEXT-AGENT-INSTRUCTIONS.md | ORobotics/NEXT-AGENT-INSTRUCTIONS.md | 6a3d2e2b8513aac84826a101383237e42ab698af4cd308dbc7d54809a391bad5 |
| ORobotics/codex-notes/PROJECT-HANDOFF.md | ORobotics/PROJECT-HANDOFF.md | d8f33c7a2fa6f627c331995c4809457dd233b101fa5b9726d9d8f3e7fd3649e2 |
| ORobotics/codex-notes/README.md | ORobotics/README.md | 74ba4514b22061206377bf5f3411172bfc49bd9882a05c6731e22cf06cb5c37a |

The hashes above identify the original contents before central-location
addenda were appended. No same-name file was overwritten. The two README files
remain separate because their contents and purposes differ.

Canonical layout:

~~~text
/Users/raramayo/dev/codex-notes/
├── README.md
├── NEXT-AGENT-INSTRUCTIONS.md
├── MIGRATION-MANIFEST.md
├── Cerebro/
├── ORobotics/
└── ROB-Books/
~~~

## Post-consolidation validation

- A workspace search returned exactly one directory named codex-notes:
  /Users/raramayo/dev/codex-notes.
- The central tree contains 12 Markdown files: three preserved Cerebro files,
  three preserved ORobotics files, three central navigation/manifest files, and
  three new ROB-Books handoff files.
- A local Markdown-link check covered the 12 central files plus the ROB-Books
  project README and found zero missing relative targets.
- Cerebro and ORobotics no longer report a project-local codex-notes path.
- The ROB-Books validation suite still passed for all five PDFs in the collection
  that existed at consolidation time after its README gained the central handoff link.
