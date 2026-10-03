# Handoff: bio-machine-learning-biomarker-discovery / fix-scientific-skill

- Updated: 2026-10-03T14:55:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: audit worker (lane 3a, initial audit, batch with omics-classifiers)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71 (files=5, bytes=29728), re-verified with `tools/skill_preflight.py --offline` before and after execution (PASS)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-biomarker-discovery\candidate@e0d8efc0e1b0-initial-lane3-20261003 (audits the identity above; score 81, grade Beta Only after the assertion-rate floor; both vetoes PASS)

## Completed this phase

- Ran all SKILL.md snippets (leakage-safe Pipeline, BorutaPy, elastic net, stability/Nogueira, mRMR) and both bundled scripts on real Golub ALL/AML with no supervised step before the split; run dir F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\initial-lane3-20261003 (report, viewer, ledger, scripts, evidence).
- Leakage thesis reproduced (10 permutations: 0.85 leaky vs 0.49 in-pipeline). Tooling ConvergenceWarning lead did not reproduce on real labels. Tooling's Golub AUC 1.000 not used.
- Normalizer scoring change judged correct but unstated and it triples signature size (BD-002).
- No audit-local repair; Skill bytes untouched.

## Required next actions

1. Fix BD-001 (P1): stability snippet standardize inside subsample, justify C, add permuted-label null; SKILL.md only.
2. Fix BD-002..BD-004, BD-006 in SKILL.md (scoring sentence; scaler + label + nested note; seed + NaN guard; in-fold mRMR snippet).
3. Fix BD-005 in scripts/boruta_feature_selection.py and scripts/lasso_biomarker.py (print strings/comments). This is the only runnable-byte change; the changed SKILL.md snippets also need re-execution.
4. Classify tooling impact: scripts change and new mRMR/stability snippets need a tooling-delta check; Golub is already staged.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| BD-001 | P1 | open | evidence/c4.json | stability snippet scale/null (SKILL.md text) |
| BD-002 | P2 | open | evidence/c3.json | state scoring/legacy-attribute choice and its effect (text) |
| BD-003 | P2 | open | evidence/c1.json, c7.json | add scaler, fix "Nested-safe" label (text) |
| BD-004 | P2 | open | evidence/c4.json | seed + empty-selection guard (text) |
| BD-005 | P2 | open | evidence/c6.json | script narrative strings (runnable bytes) |
| BD-006 | P2 | open | evidence/c5.json | in-fold mRMR pattern (text) |

Deferred/static-only: R glmnet prose (no code). Blocked: none. Evidence dir: initial-lane3-20261003\evidence.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md (sha256 9af55f461bebaeda2ce6823e3a89eb7f3a04a6fb2f29deae77747548fb5c6e32)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (sklearn 1.9.1, numpy 2.5.3, Boruta 0.4.3, mrmr-selection 0.2.8)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\initial-lane3-20261003\ (ledger: finding-ledger.md)
- Restricted-access items: none
- Tooling impact: uncertain until fixes land (BD-005 changes scripts; new snippets need execution)

## Worktree safety

- Run-owned changes: audit run dir above; records `audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-initial-lane3-20261003/`; regenerated audits views; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs and audit records; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
