# Handoff: bio-machine-learning-omics-classifiers / prepare-scientific-skill-tooling (delta, then reaudit-scientific-skill)

- Updated: 2026-10-03T19:00:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: fix worker (lane 3a-2)
- Next role: prepare-scientific-skill-tooling (delta mode); then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c (files=7, bytes=48515); `tools/skill_preflight.py` and `--offline` both PASS (warn: no Skill-root LICENSE, as before)
- Applicable audit: candidate@1d68da6e6ef8-initial-lane3-20261003 audited the PREVIOUS identity 1d68da6e...; it does not cover these bytes

## Completed this phase

- All six findings fixed (ledger: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix-lane3-20261003\finding-ledger.md); all eleven failed assertions addressed.
- Every SKILL.md python block and all four scripts executed under `-W error::FutureWarning` (Golub and synthetic): evidence/snippets_golub.out, snippets_synthetic.out, *.out.
- Measured numbers are in SKILL.md prose; raw experiments in the run dir evidence/ (calibration_part1/2.json, scoring_golub.json, scoring_1se.json, earlystop.json).

## Finding dispositions

| ID | State | Result |
|---|---|---|
| OC-001 | fixed | No reweighting when probability is the output; balanced logistic 4.2x prevalence vs 0.99x unweighted, 1.11x recalibrated (8%, 20k test); balanced RF 2.6x |
| OC-002 | fixed | batch_checks.py LeaveOneGroupOut; works at 2/3/6 batches (per-batch mean AUC 0.54/0.70/0.45 vs random-split 0.82/0.88/0.86); one-class batch shown as NaN with note |
| OC-003 | fixed | scoring stays neg_log_loss; dense (Golub 1,059-2,000 of 2,000 non-zero); lasso + 1-SE gives 45/142/60 at unchanged AUC; claim reworded |
| OC-004 | fixed | sigmoid default; isotonic only at n_cal >= 1000 and >= 100 rarer-class events; recalibrate() warns at <= 3 distinct values |
| OC-005 | fixed | 3-way split; early-stopping set not reported; val 15 gives best round 4.5 and AUCPR 0.83 vs test AUC 0.61; inner-CV rounds 0.69 |
| OC-006 | fixed | scripts match docstrings/captions; usage-guide tip rewritten |

## Changed files

- SKILL.md, usage-guide.md, references/failure-modes.md (prose and snippets)
- scripts/logistic_regression.py, scripts/rf_xgboost_classifier.py (changed)
- scripts/batch_checks.py, scripts/calibration_check.py (new; import only numpy, pandas, sklearn)

## Open items for the next workers

1. Tooling delta: two new runnable surfaces (batch_checks.py, calibration_check.py), two changed scripts, new SKILL.md snippets importing them (cwd = Skill dir, `sys.path.insert(0, 'scripts')`). No new dependency or environment change. Calibration demo takes about 80 s.
2. Re-audit independently. Caveats to scrutinise: sample-size rule is from synthetic RF/XGBoost bases (not real omics); 2-3 batch leave-one-batch-out is noisy; no public multi-batch set was staged; the "small n: use CV rounds" advice was measured at n_train=120 only.
3. Golub is near-separable: used only for executability and sparsity counts.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 7f4a80ba28ac74641a3bf4ad8d7f5d8cfa2cb7664f7d8320debadc4daea1db73; needs a delta row for the new scripts)
- Fix run evidence: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix-lane3-20261003\
- Restricted-access items: none
- Tooling impact: changed (new surfaces scripts/batch_checks.py and scripts/calibration_check.py; changed logistic_regression.py and rf_xgboost_classifier.py; SKILL.md snippets rewritten; no dependency change)

## Worktree safety

- Run-owned changes: the Skill dir above; fix run dir; this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs and handoffs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
