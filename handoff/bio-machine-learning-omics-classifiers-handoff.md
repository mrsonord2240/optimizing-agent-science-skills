# Handoff: bio-machine-learning-omics-classifiers / orchestrator (commit and intake)

- Updated: 2026-10-03
- Lane: 3
- Status: done (shelf e58c885, intake accepted at validator a1d820d, exported to bioSkills-Improved fff47bd; worktree removed)
- Owner leaving: delta re-auditor (lane E3, fresh, did not normalize, tool, audit or fix)
- Next role: none; open P2s wait for a later refinement run

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f (files=7, bytes=50363); `tools/skill_preflight.py --offline` PASS before and after
- Applicable audit: audits/skills/bio-machine-learning-omics-classifiers/candidate@a2d417f41e37-reaudit-delta-20261003 (supersedes candidate@906900fae480-reaudit2-lane3-20261003, identity 906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f)

## Completed this phase

- Delta qualified: reverting `fix-description-20261003/edits.json` on a scratch copy reproduces 906900fa...; `diff -r` shows only SKILL.md line 4 (`description:`).
- New frontmatter parses as YAML; description is accurate and a valid trigger; no false statement. Behaviour unchanged, so the certifying record's execution evidence is reused.
- Readiness: candidate-ready for the identity above. Score 88 (Production Ready), static 88 (unchanged), execution average 87.9, assertions 34/36 (94.4%), both veto gates PASS, no P0/P1.
- New P2 OC-013 (description alone separates less sharply from model-validation and prediction-explanation); the trim itself is not a defect.
- Record published and views regenerated; `npm run audits:check` passes.

## Required next actions

1. Orchestrator: commit the Skill bytes at the identity above, then intake.
2. Optional text-only fixes OC-012 and OC-013 (P2) would change the identity and need another delta re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| OC-012 | P2 | open, non-blocking, unchanged | `F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit2-lane3-20261003\evidence\xgb_threads.log`, `golub_oc3_oc6.log`, `batch.log` | XGBoost demo round is 160 / 133 / 397 / 223 for n_jobs 1 / 2 / 4 / default (AUC 0.83-0.84), but SKILL.md and a script comment quote 223 and 0.577 / 0.601 / 0.632; Golub 1-SE counts 369 and 273 on two further splits vs quoted 45 / 142 / 60; the 0.09-0.10 spread names no setup. State variability or setup. |
| OC-013 | P2 | open, non-blocking, new | report.json recommendation in the published record | Optional: tie the "suspiciously perfect AUC" clause to building a classifier, and name imbalance/batch shortcuts, if routing should be sharper. |

No blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 10db0209615ba7f57514bcd4d89fe2d614552cbf09aeda5864e8dd72d77ea9b9), unchanged
- Run evidence: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit-delta-20261003\ (`scripts\revert_check.py`, `scratch\rev`); certified execution evidence in reaudit2-lane3-20261003\
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: the run dir above; records repo: audits/skills/bio-machine-learning-omics-classifiers/candidate@a2d417f41e37-reaudit-delta-20261003/, audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (regenerated); this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
