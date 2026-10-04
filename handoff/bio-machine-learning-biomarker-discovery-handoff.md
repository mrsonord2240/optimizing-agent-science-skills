# Handoff: bio-machine-learning-biomarker-discovery / orchestrator (commit as candidate-ready)

- Updated: 2026-10-03T23:30:00-07:00
- Lane: 3 (3a-1)
- Status: done (shelf e58c885, intake accepted at validator a1d820d, exported to bioSkills-Improved fff47bd; worktree removed)
- Owner leaving: reaudit worker (fresh auditor, FULL mode; did not normalize, tool, audit or fix this Skill)
- Next role: none; open P2s wait for a later refinement run

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery (untracked by design)
- Branch/worktree: normalize/ml-lane3 from 29f5446
- Candidate tree hash: 27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134 (sha256-manifest, files=6, bytes=37081); preflight PASS before and after, no __pycache__, bytes untouched
- Applicable audit: audits/skills/bio-machine-learning-biomarker-discovery/candidate@27580088c038-reaudit-lane3a1-20261003 (exact identity). Superseded baseline: candidate@e0d8efc0e1b0-initial-lane3-20261003.

## Completed this phase

- Decision: candidate-ready. Score 88 Production Ready; static 91; execution avg 85.6; Layer 1 34.1; Layer 2 51.4; assertions 27/29 (93.1%); vetoes PASS; no open P0/P1.
- BD-001 to BD-006 all resolved on independent re-test (stability: seeded bit-identical, unit-invariant, null 0 in 8 own noise draws and 11/11 permuted at 7,129 probes; scoring table 601/203/148, 16/0/0, 0.991/0.983/0.991 reproduced; nested/in-fold selection verified by held-out perturbation).
- Description trim verified: parses as YAML, separates from model-validation, prediction-explanation, omics-classifiers, survival-analysis, atlas-mapping.
- Run evidence: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\reaudit-lane3a1-20261003\ (logs\, scripts\); published record above; `npm run audits:check` passes.

## Required next actions

1. Orchestrator: commit exact bytes; run `npm run audits:inventory` after the shelf commit per readiness-and-records.
2. Optional: text-only fix of RA-001 and RA-002 below, then delta re-audit (changed prose only; a docstring note would change script bytes).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| RA-001 | P2 | open (new) | logs\imbalance.log | Rare-class labels (<=8 of 72 positives): stability_selection raises a misleading liblinear "multiclass" ValueError because n/2 subsamples are unstratified; say in SKILL.md that both classes must survive every subsample (text-only), or stratify (script change) |
| RA-002 | P2 | open (new) | logs\bd002.log | Text-only: over 3 partitions neg_log_loss 436-601, roc_auc 53-203, accuracy 148-150 probes |

No blockers. Failed or blocked surfaces: none. Static-only: R glmnet (one prose row, no explicit "not executed" marker, nothing claimed executed). No tooling-delta needed.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md, sha256 d6c742a3a070e4a0fd1541b5cda456bf7efe6ed0f7d99715476c474eb4537021; environment fingerprint UNCHANGED 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6
- Run evidence: reaudit-lane3a1-20261003\logs\ (own_null, planted_strong, leakage, bd002, boruta_inspect, imbalance, determinism_*, stab_*, snip*); first leakage run was my own test bug, kept as leakage_run1_flawed_*.log, not evidence
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-lane3a1-20261003\; records repo audits\skills\bio-machine-learning-biomarker-discovery\candidate@27580088c038-reaudit-lane3a1-20261003\ plus regenerated audits\INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (uncommitted); this handoff
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
