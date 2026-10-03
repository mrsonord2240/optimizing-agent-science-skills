# Handoff: bio-machine-learning-omics-classifiers / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 3
- Status: phase-failed (final re-audit: NOT candidate-ready; text-only P2 fixes plus one small script change)
- Owner leaving: reaudit worker (lane 3a-2, independent of fixer and initial auditor)
- Next role: fix-scientific-skill, then reaudit-scientific-skill in delta mode (the fix must stay within prose/comments/frontmatter plus one localized script change of at most 20 lines, else full mode)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c (files=7, bytes=48515); `tools/skill_preflight.py --offline` PASS before and after the audit; bytes untouched
- Applicable audit: audits/skills/bio-machine-learning-omics-classifiers/candidate@ac3c92e83a1c-reaudit-lane3-20261003 (this identity). Prior: candidate@1d68da6e6ef8-initial-lane3-20261003 (previous identity, superseded)

## Readiness decision

Not candidate-ready. Score 85, grade Limited Release (band Production Ready, one tier down for the assertion floor). Static 85, execution average 85.6, Layer 1 34.3, Layer 2 51.3, assertions 29/33 = 87.9% (gate 90%). Vetoes pass, no open P0/P1.

## Completed this phase

- OC-001..OC-006 independently retested and resolved (numbers in the record viewer, "Finding verdicts"). Tooling caveats T-1 (prose attributes numbers to the right setups), T-3/T-2 (cwd) and T-4 (demo 2 'warnings raised: 0'; warning path itself works) judged.
- Record published and views regenerated: audits/skills/bio-machine-learning-omics-classifiers/candidate@ac3c92e83a1c-reaudit-lane3-20261003 (report.json, viewer.md, source-identity.json, 9 scripts); `npm run audits:index` and `npm run audits:check` pass.
- Raw run: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit-lane3-20261003\ (evidence/, scripts/, build_*.py).

## Required next actions

1. Fix OC-007 to OC-011 below (all P2); changes limited as noted, no new measurement needed except re-running the touched script.
2. Re-audit in delta mode against the published record; rerun `scripts/rf_xgboost_classifier.py` and the touched snippets under `-W error::FutureWarning` from the Skill directory and from another cwd.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| OC-007 | P2 | open | viewer input 2; evidence/ra_calibration.out (RF AUC 0.776 -> 0.812 balanced, 6/6 seeds); staged calibration_part1.json (0.648 -> 0.720) | Text-only: "changes scale, not ranking" and "no AUC gain" (SKILL.md Approach, decision tree, thresholds table; failure-modes) hold for logistic, not for RF; say so, keep the advice |
| OC-008 | P2 | open | evidence/ra_cwd.out | Text-only: say the blocks run from the Skill directory or anchor the path on the Skill's location |
| OC-009 | P2 | open | SKILL.md algorithm table, tips; usage-guide | Text-only: mark LightGBM, CatBoost, linear SVM, DLDA as prose guidance, not executed |
| OC-010 | P2 | open | evidence/script_rf_xgboost_classifier.out (best round 0 of 2000, AUC 0.597, spread [0.46, 0.49]) | Script (few lines): choose rounds by CV as SKILL.md advises, or drop the XGBoost spread line and label the row non-informative; update the SKILL.md sentence describing the script if behaviour changes |
| OC-011 | P2 | open | viewer "New findings" | Text-only: usage-guide add "100 in the rarer class"; explain 'warnings raised: 0' in demo 2 (sigmoid branch, warning only on isotonic); noise caution applies at any small batch count (SD 0.09-0.10 at 2, 3, 6); say recalibration at n<=100 can lose to raw probabilities; set random_state in saga snippets |

Standing caveats (not findings): sample-size rule from synthetic RF/XGBoost bases (my own logistic base agrees); no public multi-batch cohort staged; small-n early-stopping advice measured at n_train=120 only; Golub near-separable. LightGBM, CatBoost, SVM, DLDA never executed (static-only, not heavy-optional-labelled in the Skill: OC-009).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 481d854386ebb5cf91301ef6f54c999b3ad032112168ffa641e193ac908c2800); environment fingerprint UNCHANGED 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; pip freeze identical to staged freeze
- Run evidence: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit-lane3-20261003\evidence\; staged claims F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\omics-classifiers-claims\
- Restricted-access items: none
- Tooling impact: none expected (a script edit uses numpy/sklearn/xgboost already staged)

## Worktree safety

- Run-owned changes: the reaudit run dir above; published record and regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (other workers regenerate the same views); this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (fix phase can start from this handoff and the record)
