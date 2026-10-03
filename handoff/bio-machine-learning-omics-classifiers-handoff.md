# Handoff: bio-machine-learning-omics-classifiers / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase (fix loop 2 done; OC-007..OC-011 fixed, executed)
- Owner leaving: fix worker (lane 3a-2), did not audit and will not certify
- Next role: prepare-scientific-skill-tooling in delta mode (tooling impact changed), then reaudit-scientific-skill in FULL mode (no certified identity exists)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f (files=7, bytes=50806); `tools/skill_preflight.py` and `--offline` both PASS (only the no-root-LICENSE warn)
- Previous identity (failed re-audit, superseded): ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c (files=7, bytes=48515)
- Applicable audit: audits/skills/bio-machine-learning-omics-classifiers/candidate@ac3c92e83a1c-reaudit-lane3-20261003 (score 85, assertions 29/33; superseded by this identity)

## Completed this phase

- OC-007..OC-011 fixed; per-file before/after sha256 in `edits.json` (run dir below). Changed: SKILL.md, usage-guide.md, references/failure-modes.md, scripts/rf_xgboost_classifier.py. Unchanged: batch_checks.py, calibration_check.py, logistic_regression.py.
- All 7 SKILL.md python blocks run OK on Golub and synthetic data, and all four scripts rc 0, under `-W error::FutureWarning`, no warnings; evidence/snippets_*.out, script_*.out.

## Finding dispositions (all fixed; evidence under evidence/ in the run dir)

| ID | Disposition | Measured |
|---|---|---|
| OC-007 | fixed | reproduced (oc007_rf_weights.out, 6 seeds): logistic AUC 0.826 plain vs 0.820 balanced (scale only); RF 0.776 vs 0.812, higher in 6/6; RF risk ratio 1.11x vs 2.43x. SKILL.md decision row, imbalance Approach + measured paragraph, thresholds row, usage-guide tip and failure-modes symptom now say logistic ranking unchanged, RF ranking can change, recalibrate in both |
| OC-008 | fixed (text) | snippet comment says relative to cwd: run from the Skill dir or use the absolute scripts path; oc008_cwd_check.out: foreign cwd fails relative, passes with absolute path |
| OC-009 | fixed (text) | "Not executed here" paragraph before the algorithm table (LightGBM, CatBoost, linear SVM, DLDA) and a usage-guide tip |
| OC-010 | fixed (script) | before: n=300, best round 0 of 2000, XGB test AUC 0.597 (script_rf_xgboost_classifier.before.out). After: n=600, learning rate unchanged at 0.03, best round 223, validation logloss 0.588, XGB test AUC 0.834 (elastic net 0.944, RF 0.729; .after.out). Basis: oc010_explore.out, validation logloss only, test split not scored (n=600: lr 0.03 0.577 vs 0.1 0.601 vs 0.3 0.632 on the script's seed). Loud "!!! WARNING" when best round is 0, shown firing at n=300 (oc010_warn_check_n300.out) |
| OC-011 | fixed (text) | usage-guide adds 100-rarer-class condition and the n=20 recalibration-can-lose note; SKILL.md noise sentence now any batch count (SD 0.09-0.10 at 2/3/6); n=20 RF Brier raw 0.1985 vs sigmoid 0.2089 vs isotonic 0.2356 (sigmoid ties raw at n=100, 0.1980); `random_state=0` in all three saga snippets |

Not done (outside the brief): demo 2 'warnings raised: 0' remains unexplained in script output (sigmoid branch at n=20; tooling note T-4 explains it).

## Required next actions

1. Tooling delta refresh of the rf_xgboost_classifier.py row, then full-mode independent re-audit of the identity above; rerun rf_xgboost_classifier.py (21 s class) and the SKILL.md blocks.
2. Standing caveats unchanged: sample-size rule from synthetic bases; no public multi-batch cohort; Golub near-separable; LightGBM/CatBoost/SVM/DLDA unexecuted (now labelled).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md; interpreter F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe (3.12, sklearn 1.9.1, xgboost 3.4.1); environment untouched
- Fix run: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix2-lane3-20261003\ (edits.json, before.sha256, scripts/, evidence/)
- Restricted-access items: none
- Tooling impact: changed (surface `scripts/rf_xgboost_classifier.py` runnable bytes changed: n=300 to 600, new warning branch; no new dependency or environment change; the TOOLS.md row's numbers (AUC 0.741/0.639/0.597, best round 0, 21 s) are stale and the SKILL.md block text changed). Route note: tooling-delta only to refresh that row, may run in parallel with or before the full re-audit as the relay decides

## Worktree safety

- Run-owned changes: the four Skill files above; fix2 run dir; this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes, subject to the tooling-delta refresh of the one stale TOOLS.md row
