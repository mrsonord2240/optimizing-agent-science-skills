# Handoff: bio-machine-learning-atlas-mapping / prepare-scientific-skill-tooling (delta) -> reaudit

- Updated: 2026-10-03
- Lane: 3 (batch 3b-1)
- Status: ready-for-phase
- Owner leaving: tooling worker (delta, lane 3b-1)
- Next role: reaudit-scientific-skill (fresh auditor)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (branch normalize/ml-lane3, Skill dirs untracked by design)
- Candidate tree hash: ba864911e88a7d48e4576f9f7f4f1668ef0ed85ddd429c151bbb6ebfc39cd094 (files=7, bytes=39154), `skill_preflight.py` PASS before and after, no pycache. Skill bytes not edited.
- Prior audit (identity d4048dcc887b, 77, Limited Release) is superseded by these bytes.

## Completed this phase (tooling delta)

- TOOLS.md refreshed in place: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 0818c47cd78b8dc26256c0fd3e0d28c04a1602c0ef60b5cbd2c74669aad225d1)
- Environment fingerprint UNCHANGED: 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 (single-cell freeze re-hashed read-only, identical b82090ff...). No package touched.
- Executed from staged inputs (4 runs, all rc 0): scarches_annotation.py seeded, two baseline runs identical (labels 2638/2638, latent diff 0.0, `query_annotated.h5ad` written); Monocytes-removed; B-removed; label_marker_check.py (curated and reference-derived) on each; ood_gating_demo.py (100% / 0%). All numbers reproduce the fix log.
- Staged and indexed (ecosystem `machine-learning`): `derived\atlas-pair-holdout\{reference_no_monocytes,reference_no_bcells}.h5ad` + `make_holdouts.py` under `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\`; README rows and INDEX.md row updated. Baseline = existing `derived\atlas-pair\reference_labeled.h5ad`.
- Rerun harness: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\tooling-delta-lane3b-20261003\run_case.py (`none|mono|bcell <tag>`; reads staged files only); evidence in the same dir (summary_*.json, logs\, work\).

## Required next actions

1. Re-audit on the new identity; run SKILL.md snippets as written (not covered by this pass beyond the scripts), and rerun `run_case.py` cases.
2. Check AM-001 claim table in SKILL.md against the numbers: kNN gate no-holdout 1.67%, Monocytes removed 1.59% Unknown (604/630 called DC), B removed 76.3% Unknown; curated markers flag DC at 0.160 (Mono) and 0.525 (B), nothing at baseline; derived markers miss Monocytes (DC 0.730), falsely flag T cells for B removed (0.563), T cells 0.605 at baseline. T cells NOT CHECKED with curated markers (absent from 1604-HVG set).

## Open findings and blockers

Findings AM-001..AM-005 as dispositioned in the fix log (F:\OpenScience\audits\bio-machine-learning-atlas-mapping\fix-lane3b-20261003\fix-log.md); AM-001 gate not improved, limitation documented. Blockers: none. Restricted-access items: none.
Not executed by design (Skill must label): scPoli, popV, treeArches/scHPL, foundation models (heavy-optional); Symphony, Azimuth (prose only).

## Worktree safety

- Run-owned changes: tooling-delta-lane3b-20261003\, TOOLS.md, derived\atlas-pair-holdout\, README/INDEX rows, this handoff
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs; untouched
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
