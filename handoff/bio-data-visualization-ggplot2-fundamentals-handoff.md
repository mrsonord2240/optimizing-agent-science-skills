# Handoff: bio-data-visualization-ggplot2-fundamentals / reaudit-scientific-skill

- Updated: 2026-10-03T23:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 1a, run fix-dv2-20261003)
- Next role: reaudit-scientific-skill (full mode; runnable bytes changed)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120 (files=5, bytes=22972); skill_preflight PASS (offline and online)
- Applicable audit: none for this identity. Prior failed re-audit applies to 9d22bac5b1ee (audits\skills\...\candidate@9d22bac5b1ee-reaudit-dv1-20261003)

## Completed this phase

- GG-004 (P1) fixed in behaviour: create_volcano top_n default NULL (10 labels for symbols <= 8 chars, else 3); SKILL.md states only the measured envelope.
- GG-009 (P2) fixed: failure-modes.md says the ggrepel drop is silent (verbose = TRUE only).
- PCA percent contract explicit; fraction input warns; tested on both ggplot2 versions.
- Evidence and per-size overlap counts: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-dv2-20261003\ (fix-log.md, measure4.log, measure35.log, scripts\measure.R, out4\, out35\).

## Required next actions

1. Re-audit the changed runnable surfaces: create_volcano default labelling (3 Ensembl / 10 symbol) via label-box measurement at 183x120, 183x150 composites, 120x84 and 89x70 standalone; 120x110 composite is expected to collide and the Skill says so; create_pca_plot fraction warning; open figures.
2. Spot-check unchanged surfaces only as risk dictates; GG-001..003, 005, 007, 008 were verified corrected on 9d22bac5b1ee.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-004 | P1 | fixed (pending re-audit) | fix-dv2-20261003\measure4.log, measure35.log | confirm |
| GG-009 | P2 | fixed (pending re-audit) | fix-dv2-20261003\fix-log.md | confirm |

Known limits (not defects): Ensembl IDs standalone at 89x70 mm still overlap 1 pair (tie) and 120 mm composites collide for both label types; both are stated in SKILL.md. Two top Ensembl labels in the 183 mm composite nearly touch (boxes clear).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md (fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721, unchanged)
- Run evidence: fix run dir above; changed files: SKILL.md, scripts/publication_figures.R, references/failure-modes.md
- Restricted-access items: none
- Tooling impact: none (no dependency, runtime, version, wrapper or executable path changed; same helper interface, same R/ggplot2 stack, executed via existing r.sh/r-gg35.sh). Runnable bytes did change, so full re-audit, not delta.

## Worktree safety

- Run-owned changes: the three Skill files above; fix-dv2-20261003 run dir; this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/ (untouched); sibling Skill dirs in the worktree untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a
