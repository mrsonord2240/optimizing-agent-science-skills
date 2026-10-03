# Handoff: bio-data-visualization-ggplot2-fundamentals / reaudit-scientific-skill

- Updated: 2026-10-03 (tooling-delta worker, lane 1)
- Lane: 1
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (delta)
- Next role: reaudit-scientific-skill (full mode; runnable bytes changed)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120 (files=5, bytes=22972); skill_preflight --offline PASS (re-verified this phase)
- Applicable audit: none for this identity. Prior failed re-audit applies to 9d22bac5b1ee only.

## Completed this phase

- Tooling delta pass; no Skill bytes touched. Label-overlap measurement staged and rerun from staging on ggplot2 4.0.3 and 3.5.2: `tools\lane1_gg_overlap_measure.R` (+ `lane1_gg_lib_overlap.R`), logs smoke\lane1_gg_overlap_gg4.log / _gg35.log (about 5-8 min each; run in background).
- New derived input: `public-data\derived\airway_dex_deseq2_results_symbol.csv` (airway results + HGNC symbol), built by `tools\make_airway_results_symbol.R`, README row added.
- Result: default labels Ensembl 3 / symbols 10; every zero-overlap row the Skill claims reproduces with 0 pairs on both versions (symbols 183x128, 120x84, 89x70 standalone and 183x120/183x150 3- and 4-panel; Ensembl 183/150/120 standalone and 183 composites). PCA fraction warning fires, percent input silent.

## Required next actions

1. Full re-audit: create_volcano default labelling, PCA warning, GG-004 and GG-009 dispositions, using the staged measure script.
2. Auditor note: the 120x110 symbol rows are non-deterministic in ggrepel (4-panel 10 or 11 pairs; 3-panel 9). The fix-log's "4.0.3 = 3.5.2 in every row" is not exact there; the Skill claims only the zero rows, which were identical in all logs.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-004 | P1 | fixed (pending re-audit) | smoke\lane1_gg_overlap_gg4.log, _gg35.log | confirm |
| GG-009 | P2 | fixed (pending re-audit) | fix-dv2-20261003\fix-log.md | confirm |

No tooling blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md (sha256 5d13e5750af0ab3b172603d035311317491057206d2c3e576c2fd4f73c73c55f)
- Environment fingerprint: UNCHANGED, sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Run evidence: F:\OpenScience\audit-envs\data-visualization\smoke\lane1_gg_overlap\{gg4,gg35}\; fix evidence F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-dv2-20261003\
- Restricted-access items: none
- Tooling impact: none further

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\data-visualization (tools, smoke, public-data\derived + README); TOOLS file; this handoff. Skill bytes untouched.
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
