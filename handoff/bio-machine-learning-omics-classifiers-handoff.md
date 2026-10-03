# Handoff: bio-machine-learning-omics-classifiers / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 3, machine-learning batch)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: 1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047 (files=5, bytes=29444), re-verified with `tools/skill_preflight.py --offline` after tooling (PASS)
- Applicable audit: none

## Completed this phase

- Both scripts re-run clean (rc 0, no warnings under `-W default`) in the shared venv (sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2).
- All SKILL.md snippets run on real Golub ALL/AML expression: elastic-net pipeline, RF + FrozenEstimator, XGBoost constructor early stopping, imblearn SMOTE pipeline, StratifiedGroupKFold.
- `LogisticRegressionCV` neg_log_loss/use_legacy_attributes=False runs clean on sklearn 1.9.1 with FutureWarning as error.

## Coverage map (per surface)

- `scripts/logistic_regression.py`, `scripts/rf_xgboost_classifier.py`: executed (synthetic).
- Snippets incl. chi-square batch association: executed (Golub; batch label synthetic, no small public multi-batch set staged).
- LightGBM/CatBoost/SVM/DLDA: prose only, not exercised.

## Required next actions

1. Audit batching: **light** (every required surface runs on CPU in under 2 minutes; inputs under 30 MB).
2. Audit against the exact identity above; run from saved scripts in F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3 (logs in its `logs` folder).
3. Do not edit Skill bytes in the audit; findings go to the ledger. Needed-but-missing inputs: request a tooling-delta pass.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | Notes for audit: Golub AUC 1.000 is optimistic (smoke script pre-selects 300 probes before the split; dataset near-separable); executability check only. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 7f4a80ba28ac74641a3bf4ad8d7f5d8cfa2cb7664f7d8320debadc4daea1db73)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 of F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\fingerprint-inputs.txt (hashes of four pip freezes); ecosystem root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (INDEX row `machine-learning`), addendum in its TOOLS.md and `public-data\README.md`
- Run evidence: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed; staging additions only: Golub leukemia)

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (smoke\ml-lane3, derived, public-data, tools\pycox-venv, freeze, TOOLS.md, INDEX.md); records `audits/skills/bio-machine-learning-omics-classifiers/candidate@1d68da6e6ef8-tooling-20261003/TOOLS.md`; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
