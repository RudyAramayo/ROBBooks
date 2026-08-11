# Instructions for the next development agent

## Starter prompt

Use the following prompt when handing this repository to another agent:

> Resume development of the ORobotics Hugo website. Begin by reading
> codex-notes/README.md, codex-notes/PROJECT-HANDOFF.md, and
> codex-notes/NEXT-AGENT-INSTRUCTIONS.md completely. Inspect the current Git
> status and diff before editing. Preserve the uncommitted QR3D landing-page
> implementation and verify it with npm test. Do not commit, push, deploy, or
> alter GitHub Pages settings unless I explicitly authorize it. Report the
> current state and then continue with my newest requested task.

## Required restart sequence

1. Enter the repository without assuming a machine-specific path:

   ~~~sh
   cd <OROBOTICS_REPOSITORY>
   ~~~

2. Read the handoff before touching files:

   ~~~sh
   sed -n '1,240p' codex-notes/README.md
   sed -n '1,320p' codex-notes/PROJECT-HANDOFF.md
   sed -n '1,320p' codex-notes/NEXT-AGENT-INSTRUCTIONS.md
   ~~~

3. Establish the current state:

   ~~~sh
   git status --short --branch
   git diff --stat
   git diff --check
   git ls-files --others --exclude-standard
   ~~~

   Do not use git reset, git checkout --, git clean, or other destructive
   cleanup commands. Existing changes belong to the user unless proven
   otherwise.

4. Inspect the QR3D implementation and its integration points:

   ~~~sh
   git diff -- content/QR3D.md layouts/qr3d/single.html
   git diff -- hugo.yaml layouts/partials/nav.html
   git diff -- layouts/partials/footer.html layouts/partials/meta.html
   git diff -- assets/css/main.css scripts/validate-subpath.mjs
   ~~~

   Because the two QR3D implementation files are currently untracked, also open
   them directly if git diff does not show their contents.

5. Verify the toolchain:

   ~~~sh
   node --version
   npm --version
   hugo version
   ~~~

   The project expects Node.js 20 or newer and Hugo Extended 0.164.0. Run npm ci
   only when dependencies are absent or need a clean reinstall.

6. Establish a live baseline:

   ~~~sh
   npm test
   git diff --check
   ~~~

   Do not call the work validated if either command fails. Distinguish a real
   source failure from a missing local dependency or restricted environment.

7. Confirm the generated route when work touches QR3D:

   ~~~sh
   test -f public/QR3D/index.html
   python3 -m http.server 4173 --directory public
   ~~~

   In another terminal, check:

   ~~~sh
   curl --head http://127.0.0.1:4173/QR3D
   curl --head http://127.0.0.1:4173/QR3D/
   ~~~

   Stop the temporary server afterward. The first URL should redirect to the
   slash form; the second should return HTML successfully.

## Acceptance checklist for future QR3D work

- content/QR3D.md still declares url: "/QR3D/".
- Hugo generates public/QR3D/index.html.
- The page contains exactly one main and one h1.
- The primary action reaches the site home page.
- Every enabled params.social_media entry renders exactly once and points to
  its configured URL.
- External links retain accessible labels and rel="noopener noreferrer".
- The QR artwork uses a subpath-safe URL.
- The compact footer is present and the ineffective theme toggle is absent.
- The canonical URL ends in /QR3D/.
- npm test and git diff --check pass.
- A physical scan is tested after deployment.

## How to continue responsibly

- Lead with the user's newest requested outcome.
- Keep changes inside the ORobotics repository unless the user expands scope.
- Reuse the existing Hugo layouts, Tailwind build, and validation scripts.
- Update both source CSS and generated tracked CSS through the normal build.
- Add regression coverage whenever a route or configuration contract changes.
- When the task is finished, update codex-notes/PROJECT-HANDOFF.md with the new
  checkpoint, commands run, results, and any remaining work.
- If asked only to review or diagnose, do not silently implement, commit, push,
  or deploy.

## Centralized restart path — 2026-08-03

The instructions above are preserved, but their note paths were written before
workspace consolidation. Read the files from:

- /Users/raramayo/dev/codex-notes/ORobotics/README.md
- /Users/raramayo/dev/codex-notes/ORobotics/PROJECT-HANDOFF.md
- /Users/raramayo/dev/codex-notes/ORobotics/NEXT-AGENT-INSTRUCTIONS.md

Run all repository commands from /Users/raramayo/dev/ORobotics. When work is
finished, append the checkpoint to the central PROJECT-HANDOFF.md or add a dated
ORobotics handoff beside it and update the central project README.
