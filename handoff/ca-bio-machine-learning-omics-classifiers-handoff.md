# Handoff: ca-bio-machine-learning-omics-classifiers / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-machine-learning-omics-classifiers` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-machine-learning-omics-classifiers`; no git writes made
- Candidate identity (preflight `--shape`, PASS): `4fccbc81108d37f18649ecb95aa14f445a1208c3d97c159b3742a43ab0f8e133`, 14 files
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, author GPTomics kept)

## Structural summary

- `SKILL.md`: 35 lines, 6 routes (baseline, trees, batch-check, imbalance, calibration, algorithm-choice) plus a pointer to `ca-bio-machine-learning-model-validation` for estimation, nested CV and leakage.
- References: `background.md` (measured figures, failure modes), `citations.md`. `failure-modes.md` folded into routes and background; `usage-guide.md` dropped.
- Scripts (all rewritten as CLIs over one CSV, one results file): `logistic_regression.py` (`--signature` for the 1-SE lasso), `rf_xgboost_classifier.py`, `batch_checks.py`, `calibration_check.py`, shared loader `omics_data.py`. The synthetic self-tests and measured-claim demos were removed.
- Traps in scripts: loader refuses non-binary label, non-numeric columns, NaN (except XGBoost), a class under 5; `batch_checks.py` refuses one batch or batches under 2 samples; `calibration_check.py` refuses a calibration split with under 3 in a class and flags degenerate calibrators; `rf_xgboost_classifier.py` marks an XGBoost best round of 0 as a null model.
- Version notes: scikit-learn 1.9.1 API used (`FrozenEstimator`, `l1_ratios`, `use_legacy_attributes=False`); XGBoost constructor-based early stopping.

## Scripts

Run scope was cut mid-task by the coordinator. Environment used: WSL `science`, env `as-lr` (sklearn 1.9.1, xgboost 3.4.2, pandas 3.0.6). Input: Golub leukemia (OpenML 1104), top 2,000 variance probes.

- `logistic_regression.py`: executed once with `--signature`, seed 1: 143 non-zero coefficients, test AUC 0.991, Brier 0.038 (test n=22). The dense path crashed on `C_[0]` (scalar under `use_legacy_attributes=False`); fixed in source after the crash and NOT rerun.
- `omics_data.py`: exercised via the above only.
- `rf_xgboost_classifier.py`, `batch_checks.py`, `calibration_check.py`: unexecuted (the run was cut before reaching them).

## Open ambiguities for audit

- `imbalanced-learn` is in no WSL environment, so the SMOTE path in `routes/imbalance.md` is untested.
- The measured figures in routes come from the shelf text (earlier runs), not re-measured here.
- Dense-path fix above is unverified.

## Evidence

- `F:\OpenScience\fix-evidence\ca-recut\bio-machine-learning-omics-classifiers\` (`run.sh`, `run.log`, `make_inputs.py`, `input\`, `out\`).

## Worktree safety

- Run-owned: the skill folder, this handoff, one row in `skills\README.md`. Pre-existing/user-owned files untouched. No commits.
