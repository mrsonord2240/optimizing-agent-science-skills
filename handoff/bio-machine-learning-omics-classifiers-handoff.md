# Handoff: bio-machine-learning-omics-classifiers / reaudit-scientific-skill (full mode)

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling-delta worker (lane 3a-2)
- Next role: reaudit-scientific-skill (full mode)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c (files=7, bytes=48515); `tools/skill_preflight.py --offline` PASS before and after tooling
- Applicable audit: candidate@1d68da6e6ef8-initial-lane3-20261003 covers the PREVIOUS identity only; none for these bytes

## Completed this phase

- Tooling delta done; Skill bytes untouched. TOOLS.md refreshed in place with coverage rows and wall times.
- All 4 scripts and all 7 SKILL.md python blocks run clean under `-W error::FutureWarning` (Golub and synthetic).
- Fix-claim generators and multi-batch synthetic inputs staged for rerun without constructing inputs: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\omics-classifiers-claims\` (README.md maps claim to script and wall time; indexed in INDEX.md and the root TOOLS.md addendum).
- Rerun results: early stopping and scoring json identical to the fix run; isotonic rule, RF 2.6x/1.16x, per-batch AUC 0.54/0.70/0.45, 8% prevalence 0.99/4.2/1.11x all reproduce; 1-SE sizes 45/143/59 vs prose 45/142/60 (saga noise).
- No run over 10 minutes (longest 579 s, `exp_scoring.py`); whole claim suite about 31 min.

## Required next actions

1. Re-audit independently, full mode, from TOOLS.md and the staged `derived\omics-classifiers-claims\`.
2. Scrutinise the caveats below.

## Caveats found during tooling (not fixed here; Skill bytes frozen)

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| T-1 | P2 | open | `derived\...\out\calibration_part1.json`, README | SKILL.md attributes "4.2x balanced" to `calibration_check.py` (1,500 train, 50 features), which reproduces it; `exp_calibration.py 1` (500 train, 300 features) gives 1.60x for logistic, 2.58x for RF. Check the prose names the setup that produced each number. |
| T-2 | P3 | open | TOOLS.md | SKILL.md snippets import from `scripts/` by relative path; they fail from any cwd other than the Skill dir. Decide whether the Skill states that. |
| T-3 | P3 | open | `delta_rf_xgboost_classifier.log` | In the script's default synthetic run XGBoost early stopping picks best round 0 of 2000 on 63 validation samples; the script prints a note. Judge whether that demo teaches the intended point. |
| T-4 | P3 | open | `delta_calibration_check.log` | `calibration_check.py` demo 2 prints "warnings raised: 0" (sigmoid branch); the degenerate-warning branch runs only in `check_recalibrate_paths.py`. |

Prior caveats stand: sample-size rule from synthetic bases; 2-3 batch leave-one-batch-out is noisy; no public multi-batch set; small-n advice measured at n_train=120 only; Golub near-separable.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 in the worker reply); environment fingerprint UNCHANGED 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; freeze identical to pip-freeze-shared.txt
- Run evidence: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\delta_*.log; derived\omics-classifiers-claims\out\; fix run F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix-lane3-20261003\
- Restricted-access items: none
- Tooling impact: changed (resolved by this delta pass; LightGBM, CatBoost, SVM, DLDA stay prose only and must be labelled not executed)

## Worktree safety

- Run-owned changes: TOOLS.md above; `derived\omics-classifiers-claims\` (new); one row each in audit-envs INDEX.md and cheminformatics-hit-triage-analyst TOOLS.md; delta_*.log files; this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs and handoffs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
