# Handoff: bio-machine-learning-biomarker-discovery / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 3, machine-learning batch)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71 (files=5, bytes=29728), re-verified with `tools/skill_preflight.py --offline` after tooling (PASS)
- Applicable audit: none

## Completed this phase

- Both scripts re-run clean (rc 0, no warnings under `-W default`) in the shared venv; mrmr-selection 0.2.8 is installed and ran (normalizer thought it absent).
- All four SKILL.md snippets run on real Golub ALL/AML expression (72 x 7,129): leakage demo reproduces (permuted-label AUC 0.79 leaky vs 0.56 in-pipeline), Boruta 93 confirmed, 15 stable features, Nogueira 0.55.
- `LogisticRegressionCV(..., scoring=neg_log_loss, use_legacy_attributes=False)` runs clean on sklearn 1.9.1 with FutureWarning as error; `l1_ratio_`/`C_` are scalars, `coef_` (1, p).
- Added Golub (OpenML 1104) to ML public-data (README row).

## Coverage map (per surface)

- `scripts/boruta_feature_selection.py`, `scripts/lasso_biomarker.py`: executed (synthetic).
- Snippets (SelectKBest pipeline, BorutaPy, elastic net, stability/Nogueira) and mRMR: executed on Golub (`logs/golub_real.log`).
- R glmnet: prose only, no code; not exercised.

## Required next actions

1. Audit batching: **light** (every required surface runs on CPU in under 2 minutes; inputs under 30 MB).
2. Audit against the exact identity above; run from saved scripts in F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3 (logs in its `logs` folder).
3. Do not edit Skill bytes in the audit; findings go to the ledger. Needed-but-missing inputs: request a tooling-delta pass.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | Notes for audit: SelectKBest+LR snippet has no scaler; lbfgs ConvergenceWarnings on raw Golub intensities (wording, not environment). neg_log_loss was the normalizer choice; auditor may prefer AUC. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md (sha256 9af55f461bebaeda2ce6823e3a89eb7f3a04a6fb2f29deae77747548fb5c6e32)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 of F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\fingerprint-inputs.txt (hashes of four pip freezes); ecosystem root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (INDEX row `machine-learning`), addendum in its TOOLS.md and `public-data\README.md`
- Run evidence: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed; staging additions only: Golub leukemia)

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (smoke\ml-lane3, derived, public-data, tools\pycox-venv, freeze, TOOLS.md, INDEX.md); records `audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-tooling-20261003/TOOLS.md`; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
