# Handoff: bio-machine-learning-omics-classifiers / reaudit-scientific-skill (FULL)

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase (tooling delta after second fix done)
- Owner leaving: tooling worker (lane 3a-2), did not audit and will not certify
- Next role: reaudit-scientific-skill in FULL mode (no certified identity exists)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f (files=7, bytes=50806); `tools/skill_preflight.py --offline` PASS before and after; no `__pycache__` left in the Skill dir
- Applicable audit: none for this identity (audits/skills/bio-machine-learning-omics-classifiers/candidate@ac3c92e83a1c-reaudit-lane3-20261003, score 85, failed, superseded)

## Completed this phase

- rf_xgboost_classifier.py row refreshed: AUC 0.944 / 0.729 / 0.834, XGB best round 223, 39 s and 38 s, two runs byte-identical.
- Fix-2 prose claims staged as rerunnable generators in `derived\omics-classifiers-claims` (README section "Fix-2 claims", `run_fix2_claims.py`); all numbers reproduced.
- Path handling recorded both ways: from the Skill dir (relative) OK; foreign cwd with absolute path OK; foreign cwd relative fails as the Skill says.
- 7 of 7 SKILL.md blocks (Golub 77 s, synthetic 54 s) and all four scripts rc 0 under `-W error::FutureWarning`, no warnings.
- No package or freeze change; fingerprint unchanged.

## Required next actions

1. FULL independent re-audit of the identity above, rerunning from staging: `python -W error::FutureWarning DC\run_fix2_claims.py <Skill dir>` (about 5 min) plus the earlier `time_runs.py` claims as needed (`DC` = `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\omics-classifiers-claims`).
2. Standing caveats: sample-size rule from synthetic bases; no public multi-batch cohort; Golub near-separable; LightGBM, CatBoost, linear SVM, DLDA not executed (Skill labels them).
3. Known small gap: the "warnings raised: 0" line in calibration_check.py demo 2 is the sigmoid branch at n=20 (the warning branch is exercised by `DC\check_recalibrate_paths.py`); the loud best-round-0 warning in rf_xgboost_classifier.py is not reached at n=600 (fixer showed it firing at n=300, `fix2-lane3-20261003\evidence\oc010_warn_check_n300.out`).

## Open findings and blockers

None open from the fix ledger (OC-007..OC-011 fixed, dispositions in `F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix2-lane3-20261003\edits.json` and evidence). No blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 10db0209615ba7f57514bcd4d89fe2d614552cbf09aeda5864e8dd72d77ea9b9); environment fingerprint UNCHANGED, 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 (freeze 9ba94225...be0a, live `pip freeze` identical)
- Interpreter: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe (3.12, sklearn 1.9.1, xgboost 3.4.1)
- Run evidence: `DC\out\fix2_*.log`; fix run F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix2-lane3-20261003\
- Restricted-access items: none
- Tooling impact: none further (delta refresh complete)

## Worktree safety

- Run-owned changes: TOOLS.md; staging `DC` additions (exp_rf_weights.py, exp_xgb_rounds.py, exp_batch_spread.py, run_cwd_paths.py, run_fix2_claims.py, README section, out\fix2_*.log); this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
