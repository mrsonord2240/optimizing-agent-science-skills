# Handoff: bio-data-visualization-ggplot2-fundamentals / fix-scientific-skill

- Updated: 2026-10-03T21:30:00-07:00
- Lane: 1
- Status: phase-failed (re-audit: NOT candidate-ready; text-only fix remaining)
- Owner leaving: reaudit-scientific-skill worker (lane 1a, final mode, fresh auditor)
- Next role: fix-scientific-skill (text-only), then a delta re-audit

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e (files=5, bytes=21846); skill_preflight PASS before and after the run, bytes unchanged
- Applicable audit (this identity): audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@9d22bac5b1ee-reaudit-dv1-20261003 (published; `npm run audits:index` and `audits:check` pass)

## Completed this phase

- Readiness decision: NOT candidate-ready for 9d22bac5.... Final 85 (static 84, exec avg 85.3, L1 34.7, L2 50.7, assertions 26/29 = 89.7 %, research veto PASS). Fails the 90 % assertion gate and carries an open P1 (GG-004). The generator grades 85 as Production Ready by score alone; the gate decision overrides that grade.
- Verdicts: GG-001, 002, 003, 005, 007, 008 corrected; GG-004 partly corrected (open P1); GG-006 partly corrected (new GG-009 P2).
- Evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\reaudit-dv1-20261003\ (logs\, scripts\, out\ figures, viewer.md, verdicts.md).
- Purple minus: png() device artefact (coloured sub-pixel fringes on the thin glyph under both ggplot2 versions, absent in ggsave output). Not a Skill defect.
- Tooling: environment unchanged (fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 re-hashed identical). No tooling-delta needed.

## Required next actions

1. GG-004 (P1, text-only suffices): SKILL.md Resources line and the script comment say "top_n = 3 in panels under ~90 mm". Measured: top_n = 3 still overlaps at 89 x 70 mm (ENSG00000152583 / ENSG00000165995, 1.5 mm) and at 120 x 110 mm; the shipped create_multi_panel with the default volcano overprints 2-3 label pairs at 183 mm (a 183 mm composite gives the volcano a ~91 mm slot, of which the legend takes about a third). Gene symbols with top_n = 10 were clean in every cell (89 mm, 183 mm, both versions). Rewrite the rule: symbols (label_col) for any multi-panel or single-column volcano; Ensembl IDs only standalone at about 150 mm or wider; top_n = 3 only in composites 183 mm or wider; open the figure. Optional code improvement: legend.position = 'bottom' for panels.
2. GG-009 (P2, text-only): references/failure-modes.md says ggrepel drops labels "with a warning" and "warning buried in log". ggrepel 0.9.8 emits nothing unless verbose = TRUE (message), so the drop is fully silent. Correct the Mechanism and Symptom lines.
3. After the fix: delta re-audit (prose-only change) re-running `scripts\r2_labels.R` rows listed there; expect >=86 and no open P1.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-004 | P1 | open (partly corrected) | reaudit...\logs\r2_lab4.log, r2_lab35.log; out\lab4\*.png | rewrite narrow-panel label rule (text-only) |
| GG-009 | P2 | open (new) | reaudit...\logs\r5_repel4.log | correct failure-modes ggrepel entry (text-only) |

Failed assertions: input 4 (default multi-panel overlap; top_n = 3 at 89 mm overlap), input 6 (drop with a warning). No blocked surfaces.
Residual observation, no finding: create_pca_plot labels a fraction-valued var_explained as "PC1 (0.6%)"; contract (percent) lives only in a code comment, SKILL.md says "needs a var_explained column" without units.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md (sha256 cae2035e8e4cfff35eb86b390f183af705be7505c3106bbdfa61ea049628cb22); fingerprint above
- Run evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\reaudit-dv1-20261003\ ; label-box measurement tool scripts\lib_overlap.R (positive control: 183 mm clean, 89 mm overlaps confirmed visually)
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: the run dir above; records repo audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@9d22bac5b1ee-reaudit-dv1-20261003\ plus regenerated audits\INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (uncommitted; other workers also write these); this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/ (untouched)
- Candidate dir: no caches or outputs written into it
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a
