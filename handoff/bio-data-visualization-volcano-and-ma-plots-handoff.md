# Handoff: bio-data-visualization-volcano-and-ma-plots / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 1c)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008 (files=7, bytes=37956); skill_preflight --offline and full PASS (warn: no Skill-root LICENSE, intentional)
- Previous identity: b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76 (files=7, bytes=33343)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@b94e14b191a0-initial-dv1-20261003\report.json (Beta Only, 70)

## Completed this phase

- All eight findings fixed and executed on the airway dds; figures opened. Fix log: F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\fix-dv1-20261003\fix-log.md
- Changed: SKILL.md, usage-guide.md, references\failure-modes.md, references\reconciliation-thresholds-pushback.md, scripts\volcano_phd.R, scripts\volcano_plot.R (ma_plot.py unchanged)
- Evidence: fix-dv1-20261003\logs\ (f1 scripts run, f3 API facts, f5/f6 sanbomics, f7/f8 raster sizes) and \out\ (figures)

## Finding dispositions

| ID | Sev | State | Evidence (under fix-dv1-20261003) |
|---|---|---|---|
| VOL-001 | P1 | fixed | no cap by default; y_cap marks capped genes as triangles; 817/817 significant plotted (out\volcano_phd_view.png, volcano_plot_fn_cap.png) |
| VOL-002 | P1 | fixed | y = -log10(padj); hline equals colour boundary (logs\f1.log PASS) |
| VOL-003 | P2 | fixed | EnhancedVolcano colCustom Up/Down, ylab adjusted P (out\enhancedvolcano_fixed.png) |
| VOL-004 | P2 | fixed | svalue=TRUE works for apeglm and ashr, drops padj; normal errors (logs\f3.log) |
| VOL-005 | P2 | fixed | sanbomics.plots.volcano verified (logs\f5.log, f6.log) |
| VOL-006 | P2 | fixed | selectLab threshold claim removed; absent names ignored (logs\f3.log) |
| VOL-007 | P2 | fixed | stated observed: apeglm raised 108 genes, ashr none (logs\f3.log) |
| VOL-008 | P2 | fixed | 5MB+/crash claims removed, measured sizes (logs\f7.log, f8.log) |

New small defects fixed inline: zero-length repel segments drew dark blobs over labelled points (min.segment.length 0.3); padj=NA drop reported; missing label genes warn.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-volcano-and-ma-plots.md ; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/r.sh scripts/f1.R <skilldir> <outdir>` from F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\fix-dv1-20261003
- Restricted-access items: none
- Tooling impact: none (no new dependency/runtime/input; ggrastr 1.0.2 already staged, only an optional mention)

## Worktree safety

- Run-owned changes: the Skill dir above; fix-dv1-20261003 run dir; this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched); sibling Skill dirs untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a
