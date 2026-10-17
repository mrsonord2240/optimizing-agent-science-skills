# Handoff: ca-bio-machine-learning-prediction-explanation / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-machine-learning-prediction-explanation` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-machine-learning-prediction-explanation`; no git writes made
- Candidate identity (preflight `--shape`, PASS): `24f0aaf7b62a88755704151f7ff36208191591d905730a741c11b03bb174ee44`, 10 files
- Warn carried: no Skill-root LICENSE (`license: MIT`, author GPTomics kept)

## Structural summary

- `SKILL.md`: 35 lines, 5 routes (shap-tree, lime-local, permutation-linear, shortcut-audit, choose-method) plus rows to biomarker-discovery and the sibling classifier and validation recuts.
- Scripts, all new from the shelf snippets and examples: `shap_tree.py` (random forest, explicit `feature_perturbation`, module aggregation, probability scale), `lime_local.py` (one prediction across seeds, top-k overlap), `omics_data.py` (loader copied from the omics-classifiers recut).
- References: `citations.md`. Dropped: `usage-guide.md`, `examples/` (simulated demos the scripts replace), the method taxonomy and failure-mode essays (folded into `choose-method`, `shap-tree`, `lime-local`, `permutation-linear`).
- Traps in scripts: both scripts refuse a model with test AUC under 0.6; `shap_tree.py` never uses `feature_perturbation='auto'` and leaves the additivity check on; `lime_local.py` refuses fewer than 2 seeds or a row out of range.
- Version notes: shelf said shap 0.44+; the `'auto'` default change at 0.47 is handled by the explicit setting. WSL environments carry shap 0.48-0.51 (not 0.52, which the Windows venv has).

## Scripts

Not run (normalize scope: no script runs). Syntax-checked only (`ast.parse`).

- `shap_tree.py`: unexecuted (shap is in WSL env `atac-scenic`, which has no xgboost; no random-forest-only dependency problem expected)
- `lime_local.py`: unexecuted (lime is in no WSL environment checked; present in the Windows `cheminformatics-hit-triage-analyst` venv)
- `omics_data.py`: unexecuted (shared with the omics-classifiers recut, where it ran once through `logistic_regression.py`)

## Open ambiguities for audit

- `shap_tree.py` handles three shap return shapes (list, 3-D array, 2-D); not tested against the installed shap.
- The default module cut (0.7 on 1 - |Spearman|) is carried from the shelf; sensitivity to it is the user's check.
- The 0.6 test-AUC refusal is a new guard, not from the shelf.
- `lime_local.py` compares top-k sets by feature index, not by LIME's discretized rule text.

## Evidence

- None for this Skill.

## Worktree safety

- Run-owned: the skill folder, this handoff, one row in `skills\README.md`. Pre-existing/user-owned files untouched. No commits.
