# Handoff: bio-machine-learning-omics-classifiers / fix-scientific-skill

- Updated: 2026-10-03T15:20:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: audit worker (lane 3a, initial audit, batch with biomarker-discovery)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/omics-classifiers
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-omics-classifiers
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047 (files=5, bytes=29444), re-verified with `tools/skill_preflight.py --offline` before and after execution (PASS)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-omics-classifiers\candidate@1d68da6e6ef8-initial-lane3-20261003 (audits the identity above; score 77, grade Beta Only after the execution-average and assertion-rate floors; both vetoes PASS)

## Completed this phase

- Ran the Core Workflow, quick-reference, XGBoost, SMOTE, calibration and batch snippets plus both bundled scripts; Golub ALL/AML for API/behaviour, synthetic data with a known generative model for discrimination and calibration claims. Run dir F:\OpenScience\audits\bio-machine-learning-omics-classifiers\initial-lane3-20261003 (report, viewer, ledger, scripts, evidence).
- SMOTE leakage and "no AUC gain, inflated risk" reproduced. Tooling's Golub AUC 1.000 not used (near-separable).
- Normalizer scoring change judged correct and stated here, but it removes sparsity on Golub (OC-003).
- No audit-local repair; Skill bytes untouched.

## Required next actions

1. Fix OC-001 (P1): drop class_weight=balanced from risk-model snippet/decision tree/usage-guide; state it shifts predicted risk like SMOTE.
2. Fix OC-002 (P1): batch snippet needs a multiclass-safe metric and LeaveOneGroupOut.
3. Fix OC-003 (P1): document that scoring governs sparsity; recommend roc_auc / 1-SE for small signatures.
4. Fix OC-004 (P1): calibration snippet default sigmoid at small n; state isotonic minimum n.
5. Fix OC-005 (SKILL.md sentence; optional script) and OC-006 (script docstring/captions + usage-guide). Scripts are the only runnable-byte changes; changed snippets need re-execution. Optionally request a tooling-delta pass for a public multi-batch set.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| OC-001 | P1 | open | evidence/o2.json | class_weight vs calibration (SKILL.md, usage-guide, failure-modes text) |
| OC-002 | P1 | open | evidence/o6.json | batch snippet metric + LOBO (SKILL.md snippet) |
| OC-003 | P1 | open | evidence/o1.json, o8.json | scoring vs sparsity (SKILL.md text) |
| OC-004 | P1 | open | evidence/o4.json | isotonic at tiny n (SKILL.md snippet) |
| OC-005 | P2 | open | evidence/o5.json | early-stopping validation reuse (text; optional script) |
| OC-006 | P2 | open | evidence/*.run1.out | script docstring/captions, usage-guide tip (runnable bytes) |

Deferred/static-only: LightGBM, CatBoost, SVM, DLDA (prose). Blocked: none (no public multi-batch set staged; synthetic batches used, failures are API-level).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\TOOLS.md (sha256 7f4a80ba28ac74641a3bf4ad8d7f5d8cfa2cb7664f7d8320debadc4daea1db73)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-omics-classifiers\initial-lane3-20261003\ (ledger: finding-ledger.md)
- Restricted-access items: none
- Tooling impact: uncertain until fixes land (scripts and snippets change)

## Worktree safety

- Run-owned changes: audit run dir above; records `audits/skills/bio-machine-learning-omics-classifiers/candidate@1d68da6e6ef8-initial-lane3-20261003/`; regenerated audits views; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs and audit records; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
