# Handoff: bio-machine-learning-biomarker-discovery / reaudit-scientific-skill (FULL mode)

- Updated: 2026-10-03T21:00:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 3a-1, delta pass after second fix)
- Next role: reaudit-scientific-skill (FULL mode; this Skill has no certified identity)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery (untracked by design)
- Branch/worktree: normalize/ml-lane3 from 29f5446
- Candidate tree hash: 8d764451560e123e485b6e9f01fb0b5fd84170f4e221db7616571045bba2a19e (files=6, bytes=37468); preflight PASS before and after, no __pycache__
- Applicable audit: audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-initial-lane3-20261003 (superseded identity; no audit of this identity)

## Completed this phase

- Determinism PASS (1,000 and full, raw and rescaled): seed=0 twice bit-identical; seed=1 differs. Logs: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\tooling-delta2-20261003\logs\determinism_*.log
- All six SKILL.md blocks and three scripts rc 0 under -W error::FutureWarning at both sizes, zero warnings/tracebacks.
- Stated numbers re-measured (table in TOOLS.md): all match except one, see below.
- Staging updated: `check_determinism.py` rewritten, `check_rescaled.py` removed, `run_stability.py` adds perm_snippet + NULL SUMMARY. Environment fingerprint unchanged.

## Required next actions

1. Re-audit FULL against 8d764451...; weigh BD-007/BD-008 fixes and the items below.
2. MISMATCH in SKILL.md: "0 in all 11 (highest frequency 0.52)" at 7,129 probes: highest over the 11 named permutations is 0.57 (the snippet's own permutation); 0.52 is the max of the 10 staged sets only. Wall-time notes: saga snippet measured 33 s / 250 s vs stated ~34 / ~263 (within load noise); one stability call 15-18 s at full vs stated 16-24 (15 s just below range); 1-3 s at 1,000 vs 1-6 (inside range).
3. Lasso observation: `scripts/lasso_biomarker.py` prints `Stable features (>60%, true signal = g0..g4): ['g0', 'g1', 'g2', 'g3']` (4 of 5). No statement in script or docs claims 5/5; the label is potentially misleading, not false. Not fixed.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| (unnumbered) 0.52 vs 0.57 highest null frequency | P2 | open | TOOLS.md stated-vs-measured; logs\stab_full.log | re-auditor to adjudicate and route fix |

No environment blockers. R glmnet prose only, not executed.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md, sha256 d6c742a3a070e4a0fd1541b5cda456bf7efe6ed0f7d99715476c474eb4537021; environment fingerprint UNCHANGED 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6
- Run evidence: ...\tooling-delta2-20261003\logs\ (driver_*.txt, snip*, stab*, lasso*, boruta*, determinism_*); fix evidence fix2-lane3-20261003\
- Staging: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\biomarker-discovery\ (README.md)
- Restricted-access items: none
- Tooling impact: none further (tooling refreshed for 8d764451...)

## Worktree safety

- Run-owned changes: TOOLS.md; tooling-delta2-20261003\; derived\biomarker-discovery\{check_determinism.py, run_stability.py, README.md, check_rescaled.py removed}; this handoff. Skill bytes untouched.
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
