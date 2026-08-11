# Instructions for the next ROB-Books agent

## Required restart sequence

1. Read the central and project handoffs completely:

   ~~~sh
   sed -n '1,260p' /Users/raramayo/dev/codex-notes/README.md
   sed -n '1,420p' /Users/raramayo/dev/codex-notes/ROB-Books/PROJECT-HANDOFF.md
   sed -n '1,320p' /Users/raramayo/dev/codex-notes/ROB-Books/NEXT-AGENT-INSTRUCTIONS.md
   sed -n '1,220p' /Users/raramayo/dev/ROB-Books/README.md
   sed -n '1,220p' /Users/raramayo/dev/ROB-Books/SOURCE_SNAPSHOT.md
   sed -n '1,260p' /Users/raramayo/dev/ROB-Books/EDITORIAL_GAPS.md
   sed -n '1,220p' /Users/raramayo/dev/ROB-Books/PRINT_AND_SAFETY_REVIEW.md
   sed -n '1,180p' /Users/raramayo/dev/ROB-Books/ASSET_CREDITS.md
   ~~~

2. Work from the project directory:

   ~~~sh
   cd /Users/raramayo/dev/ROB-Books
   ~~~

   This folder is not a standalone Git worktree. Do not run destructive cleanup
   commands or assume every file is reproducible from version control.

3. Establish the live artifact baseline:

   ~~~sh
   find source tools output/pdf output/previews -maxdepth 2 -type f -print
   rg -n ROBPlaceholder source
   bash tools/validate_books.sh
   ~~~

   The recorded baseline is five PDFs, 168 pages, and 26 placeholders. If that
   differs, determine whether a legitimate later edit exists before changing
   anything.

4. Reinspect the underlying evidence relevant to the task. If software claims
   are being updated, record current Git status and full commits for Cerebro,
   ROBController, ROBControllerVision, ORobotics, and the lidar repository.
   Rehash the Arduino sketch and presentation when either source changes.

5. Make the smallest evidence-backed manuscript change. Update every affected
   youth explanation, advanced-manual section, caption, diagram, source
   snapshot, editorial question, and release note together.

6. Rebuild and verify:

   ~~~sh
   bash tools/build_books.sh
   bash tools/render_previews.sh
   bash tools/validate_books.sh
   ~~~

   If the public image set changes, first run:

   ~~~sh
   bash tools/prepare_assets.sh
   ~~~

7. Inspect every rendered page at readable zoom. Contact sheets are navigation
   aids, not the complete visual check. Look for blank pages, orphan headings,
   clipped text, unreadable tables, misleading crops, weak contrast, sensitive
   details, and inconsistent captions.

8. Append a dated handoff describing edits, evidence, exact commands/results,
   unresolved questions, and release impact. Preserve this instruction set.

## Acceptance checklist

- [ ] Every technical claim is current, dated historical, proposed,
      experimental, unavailable, or commanded-but-unmeasured as appropriate.
- [ ] No placeholder was filled by guessing.
- [ ] Shared terminology and hardware/software facts agree across all affected
      books.
- [ ] Arduino polarity, boot, parser, watchdog, actuator, IR, and physical-stop
      limitations remain visible until verified changes replace them.
- [ ] Youth activities do not direct readers toward ROB's high-energy wiring,
      machine tools, live drivetrain, or unrestricted actuator experiments.
- [ ] Quarantined images and sensitive metadata remain absent.
- [ ] Generated art remains labeled as illustration.
- [ ] Restricted vendor material is not reproduced or paraphrased without
      permission or an authorized public source.
- [ ] All PDFs rebuild, validate, and visually inspect cleanly.
- [ ] Page counts and placeholder counts are recorded after the edit.
- [ ] The physical print and publication release gate remains open until every
      accountable reviewer signs it.

## Editing conventions

- source/robbook.sty affects every book; rebuild and review all five after
  changing it.
- Use ROBPlaceholder for facts that require builder input.
- Use the established fact, design/history, safety, maker decision, and evidence
  callouts rather than inventing new visual semantics.
- Keep image filenames descriptive and the preparation allowlist authoritative.
- Do not modify the quarantined copies merely to make them publishable.
- Keep tools/mac_serial_frame_lab.py offline and non-actuating.
- Use apply_patch for intentional text/source edits and preserve unrelated
  workspace files.

## Printer handoff boundary

The current PDFs are RGB US Letter layout proofs. A printer may require bleed,
crop marks, CMYK conversion, imposed signatures, a separate cover, or a measured
spine. Create those as separate printer-specific outputs after receiving the
printer's written specification; do not silently scale or overwrite the master
PDFs.

