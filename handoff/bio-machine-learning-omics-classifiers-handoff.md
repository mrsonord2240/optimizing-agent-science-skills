# Handoff: bio-machine-learning-omics-classifiers / orchestrator (commit and intake)

- Updated: 2026-10-03
- Lane: 3
- Status: candidate-ready
- Owner leaving: final re-auditor (lane 3a-2, fresh, did not fix or audit earlier)
- Next role: orchestrator (commit the exact bytes, then Marketplace intake); optional fix-scientific-skill for OC-012 (text-only)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f (files=7, bytes=50806); `tools/skill_preflight.py --offline` PASS before and after; no `__pycache__` left
- Applicable audit: audits/skills/bio-machine-learning-omics-classifiers/candidate@906900fae480-reaudit2-lane3-20261003 (supersedes candidate@ac3c92e83a1c-reaudit-lane3-20261003)

## Completed this phase

- Readiness: candidate-ready for the identity above. Score 88 (Production Ready), static 88, execution average 87.9, Layer 1 35.1/40, Layer 2 52.7/60, assertions 31/33 (93.9%), both veto gates PASS, no P0/P1.
- OC-001..OC-011 all verified resolved on the current bytes with own generators (RF 0.876 vs 0.891 and 0.821 vs 0.836, 6/6; logistic unchanged; test-split perturbation leaves XGBoost round, selection and predictions bit-identical; round-0 warning fires at n=300; Brier 0.1985 / 0.2089 / 0.2356 at n=20).
- All four scripts and 7/7 SKILL.md blocks (Golub, synthetic) rc 0 under `-W error::FutureWarning`; relative path OK from the Skill dir, absolute OK from a foreign cwd, foreign relative fails as the text says.
- Record published and views regenerated; `npm run audits:check` passes.

## Required next actions

1. Orchestrator: commit the Skill bytes at the identity above, then intake.
2. Optional text-only fix OC-012 (P2) would change the identity and needs a delta re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| OC-012 | P2 | open, non-blocking | `F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit2-lane3-20261003\evidence\xgb_threads.log`, `golub_oc3_oc6.log`, `batch.log` | XGBoost demo round is 160 / 133 / 397 / 223 for n_jobs 1 / 2 / 4 / default (AUC 0.83-0.84), but SKILL.md and a script comment quote 223 and 0.577 / 0.601 / 0.632; Golub 1-SE counts 369 and 273 on two further splits vs quoted 45 / 142 / 60; the 0.09-0.10 spread names no setup (0.07-0.11 on an independent generator). State variability or setup. |

No blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 10db0209615ba7f57514bcd4d89fe2d614552cbf09aeda5864e8dd72d77ea9b9); fingerprint 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6, unchanged
- Run evidence: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\reaudit2-lane3-20261003\ (`evidence\`, `scripts\`); published copy under audits/skills/bio-machine-learning-omics-classifiers/candidate@906900fae480-reaudit2-lane3-20261003
- Not executed (labelled in the Skill): LightGBM, CatBoost, linear SVM, DLDA. Caveats: sample-size rule from synthetic bases; no public multi-batch cohort; Golub near-separable.
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: the run dir above; records repo: audits/skills/bio-machine-learning-omics-classifiers/candidate@906900fae480-reaudit2-lane3-20261003/, audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (regenerated); this handoff
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
