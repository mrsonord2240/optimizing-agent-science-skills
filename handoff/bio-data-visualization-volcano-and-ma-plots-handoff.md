# Handoff: bio-data-visualization-volcano-and-ma-plots / fix-scientific-skill

- Updated: 2026-10-03T15:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76 (files=7, bytes=33343); skill_preflight --offline PASS before and after execution
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@b94e14b191a0-initial-dv1-20261003\report.json (Beta Only, final 70; static 72, exec 68.0; research veto PASS)
- Run root: F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\initial-dv1-20261003\ (report.json, viewer.md, finding-ledger.md, scripts\, logs\, out\)

## Completed this phase

- Ran volcano_phd.R, volcano_plot.R and ma_plot.py on the real airway dds (29,391 genes); opened volcano, EnhancedVolcano, MA and adjustText figures.
- Tested every tooling lead: threshold-line mismatch, sanbomics module path, max shrunken > MLE reproduce; EPS lead n/a here; labels overlap does not occur (max.overlaps = Inf).
- New: unconditional y cap hides 49 significant genes (VOL-001); ashr returns no svalue (VOL-004); selectLab gotcha does not reproduce (VOL-006).
- No audit-local repair; no Skill bytes changed. Published record candidate@b94e14b191a0-initial-dv1-20261003.

## Required next actions

1. Fix VOL-001, VOL-002, VOL-003, VOL-008 in scripts/volcano_phd.R and volcano_plot.R (runnable bytes; VOL-002 also SKILL.md/failure-modes text).
2. Fix VOL-004..VOL-007 (text only): SKILL.md, usage-guide.md, references/failure-modes.md, references/reconciliation-thresholds-pushback.md.
3. Re-run scripts\v1_phd.R and v2_python.py from the run root on the fixed bytes; classify tooling impact (none expected).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| VOL-001 | P1 | open | logs\v1_phd.log; out\phd\volcano_phd_view.png | coord_cartesian(ylim=c(0,50)) hides 49 significant genes, 9/13 labels pile at edge; make cap opt-in or squish (script) |
| VOL-002 | P1 | open | logs\v1_phd.log | raw-p axis with -log10(fdr) hline (1.30 vs 2.02 boundary), contradicts SKILL.md rule 3; plot padj or move line (script + text) |
| VOL-003 | P2 | open | out\phd\enhancedvolcano_skill.png | EnhancedVolcano Up and Down both #D55E00; '-Log10 P' on padj axis (script) |
| VOL-004 | P2 | open | logs\v1_phd.log | ashr returns no svalue; apeglm svalue=TRUE does (text) |
| VOL-005 | P2 | open | logs\v2_python.log | sanbomics.tools.volcano does not exist; use sanbomics.plots.volcano (text) |
| VOL-006 | P2 | open | logs\v1_phd.log | selectLab-threshold gotcha does not reproduce on EnhancedVolcano 1.24.0 (text, 5 places) |
| VOL-007 | P2 | open | logs\v1_phd.log | apeglm raised |LFC| for 108 genes (max 9.51 to 10.99); soften 'pull toward zero' (text) |
| VOL-008 | P2 | open | logs\v2_python.log | rasterization comments not implemented; '5MB+' claim not reproduced (script + text) |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-volcano-and-ma-plots.md ; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/r.sh scripts/v1_phd.R <skilldir> <outdir>`; Python with `PYTHONPATH=...\py-extra\sanbomics py.sh scripts/v2_python.py <skilldir> <r_outdir> <outdir>`
- Deferred/blocked surfaces: edgeR glmTreat, ggbreak, plotMA static-only here (executed in the tooling smoke)
- Restricted-access items: none
- Tooling impact: none (no new input or package needed)

## Worktree safety

- Run-owned changes: run root above; published record dir in records repo; this handoff; audits\ index regeneration (orchestrator commits)
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: uncommitted paths (audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@b94e14b191a0-initial-dv1-20261003, audits index views, this handoff)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a
