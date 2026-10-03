# Handoff: bio-data-visualization-volcano-and-ma-plots / orchestrator

- Updated: 2026-10-03T19:00:00-07:00
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (lane 1 re-audit, fresh auditor)
- Next role: orchestrator (commit to shelf; optional text fixes for VOL-009/VOL-010 first, which would require a new re-audit or delta pass)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008 (files=7, bytes=37956); preflight PASS at start and end, bytes unchanged
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@fa3ec8783a79-reaudit-dv1-20261003\ (run dir F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\reaudit-dv1-20261003)

## Re-audit result

- Decision: candidate-ready. Final 87 (Production Ready), static 87, execution avg 86.8, L1 34.2, L2 52.6, assertions 22/24 = 91.7 percent, no veto, no P0.
- Prior VOL-001..008: all resolved, independently reproduced on the real airway dds (817/817 significant plotted with and without y_cap; line = colour boundary in -log10(padj); EnhancedVolcano Up/Down differ; svalue/sanbomics/selectLab/apeglm-vs-ashr statements hold).
- Failed/blocked surfaces: none blocked; edgeR glmTreat paragraph and usage-guide static-only (prose). Heavy-optional: none.

## Open findings (P2, non-blocking)

| ID | Evidence | Required disposition |
|---|---|---|
| VOL-009 | scripts\logs\r2b_cap50.log, r3_stats_claims.log, r5_ma_python.log | stale numbers: 49 hidden genes is 39 (failure-modes.md, reconciliation-thresholds-pushback.md); median 0.77 is 0.7648; volcano_phd.R save comment (29,391 points, ~1 MB) should read 17,994 points, 0.56/0.69 MB; MA 23/444 KB belongs to 29,391 rows, not 17,994. Text-only |
| VOL-010 | scripts\figures\vol_cap30_labels_overlap.png | volcano_plot(res, y_cap=30) with default top_n labels overprints the capped labels at y=30; usage-guide recommends this cap. Document label_genes below the cap or spread labels (small script change) |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-volcano-and-ma-plots.md (fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721, unchanged)
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/r.sh <run>\scripts\r1_core.R <skilldir> <outdir>` (r2, r3, r4, r6 per headers); Python r5 needs PYTHONPATH=...\py-extra\sanbomics; pdfinfo/pdffonts via WSL scripts
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run dir above; published record dir under audits\skills; regenerated audits INDEX/BACKLOG/STATUS (audits:index, audits:check clean)
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/, sibling ggplot2 and matplotlib Skill dirs untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- Orchestrator: commit exact bytes (identity above) to make the Skill ready; any edit to resolve VOL-009/VOL-010 changes the identity and returns it to re-audit
