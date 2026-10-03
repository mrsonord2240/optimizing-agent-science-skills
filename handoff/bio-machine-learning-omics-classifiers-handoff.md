# Handoff: bio-machine-learning-omics-classifiers / prepare-scientific-skill-tooling

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: normalize worker (lane 3, machine-learning batch)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Source identity (skill_preflight, measured on F:\OpenScience\bioSkills-Improved): 9b15406c8ee9a33c32f7a34242885fae32b8c971a29366e97f26885d736c6953 (files=4, bytes=28453)
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (sparse cone: the four machine-learning Skills of this batch; shared with the three sibling Skills)
- Candidate tree hash: 1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047 (files=5, bytes=29444), taken from `python tools/skill_preflight.py`
- Preflight: PASS; warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter `license: MIT` is present, shelf root LICENSE is MIT, GPTomics)
- Applicable audit: none

## Completed this phase

- Directory named to the Skill ID; frontmatter gains `category: Data Analysis` (name, license, author unchanged).
- `examples/*.py` moved to `scripts/` with only version headers and deprecated-API fixes changed; SKILL.md routes to each with a run line.
- "Per-Method Failure Modes" (and reconciliation table where present) moved to `references/failure-modes.md`, routed from SKILL.md with a read-when line.
- Version drift resolved: compat line (sklearn 1.9, xgboost 3.4, imbalanced-learn 0.14, numpy 2.5, pandas 3.0); `penalty=` replaced by `l1_ratio`/`l1_ratios`; `LogisticRegressionCV` explicit `scoring='neg_log_loss'`, `use_legacy_attributes=False`; `CalibratedClassifierCV(cv='prefit')` row now says removed in 1.8; duplicate calibration prose trimmed.
- Scripts re-run against the current environments (see Environment); LF, UTF-8 no BOM, no pycache.

## Structural summary

- `SKILL.md` (core workflow, taxonomy, decision tree, thresholds, common errors, citations), `usage-guide.md` (unchanged), `references/failure-modes.md`, `scripts/` (2 files).
- Scientific content, defaults, thresholds, and citations unchanged.

## Runnable-surface inventory

- `scripts/logistic_regression.py` - synthetic elastic-net + batch-confounding demo, CPU, seconds; ran OK.
- `scripts/rf_xgboost_classifier.py` - synthetic linear vs RF vs XGBoost, AUC + Brier, CPU, seconds; ran OK.
- SKILL.md inline snippets smoke-ran on synthetic data: FrozenEstimator calibration, imblearn SMOTE pipeline, XGBoost constructor early stopping, StratifiedGroupKFold batch check. LightGBM/CatBoost/SVM/DLDA are prose only.

Dependency clues: scikit-learn, xgboost, imbalanced-learn, pandas, scipy (chi-square snippet).

## Required next actions

1. Tooling worker: map the surfaces above to the staged environment and record coverage; flag any surface needing public inputs.
2. Do not edit Skill bytes without re-running preflight and updating the identity above.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | No blocker. Notes for audit: `scoring='neg_log_loss'` is sklearn's announced 1.11 default (old default accuracy); chosen to avoid the FutureWarning. rf_xgboost script: elastic net (AUC 0.75) beats RF/XGB on a purely linear signal by design; not re-evaluated. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\ shared venv (scikit-learn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2, numpy 2.5.3, pandas 3.0.5); TOOLS.md there
- Run evidence: scripts executed in place from the worktree with `PYTHONDONTWRITEBYTECODE=1`; no transcripts saved.
- Restricted-access items: none
- Tooling impact: changed (scripts moved from `examples/` to `scripts/`; deprecated sklearn API replaced)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers\ (untracked, new to the shelf); this handoff
- Pre-existing/user-owned changes: records repo untracked `test/validate.bats` and a modified `handoff/bio-splicing-quantification-handoff.md` (another worker); shelf untracked `.vscode/`; none touched
- Records state: uncommitted handoff file
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
