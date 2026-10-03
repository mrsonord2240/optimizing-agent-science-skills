# Handoff: bio-machine-learning-biomarker-discovery / reaudit-scientific-skill (full mode)

- Updated: 2026-10-03T16:10:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling-delta worker (lane 3a-1)
- Next role: reaudit-scientific-skill (full mode)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery (untracked by design)
- Branch/worktree: normalize/ml-lane3 from 29f5446
- Candidate tree hash: c64a3bcb57681c24d76debd7fe4788b3bd3fc5377b358595d62df7d955aaf3c7 (files=6, bytes=36037); `tools/skill_preflight.py --offline` PASS (warn only: no Skill-root LICENSE)
- Applicable audit: audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-initial-lane3-20261003 (audited identity e0d8efc0..., superseded; fixes BD-001..BD-006 in fix-lane3-20261003)

## Completed this phase

- Tooling delta done: new `scripts/stability_selection.py`, changed `lasso_biomarker.py` / `boruta_feature_selection.py`, SKILL.md blocks 0-5 all run rc 0 under `-W error::FutureWarning` at 1,000 and at full 7,129 probes; nothing timed out.
- Refreshed TOOLS.md (below) with per-surface wall times, light/heavy call, three findings for the re-auditor.
- Staged `derived\biomarker-discovery\` (top-1,000 subset, 10 permuted-label sets + snippet permutation, runner scripts) and extended the INDEX.md `machine-learning` row.
- Joblib `WinError 6` did not recur. Environment unchanged; nothing installed or removed.

## Required next actions

1. Re-audit all six BD findings against c64a3bcb... Rerun every claim from staging: `python F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\biomarker-discovery\run_all.py <Skill dir> <1000|full> <logdir>` (README beside it).
2. Weigh the tooling findings (details in TOOLS.md "Findings"):
   - `stability_selection(seed=0)` is not reproducible: liblinear has no `random_state`; identical calls differ in frequency by up to 0.10 and in stable count (rescaled run 5 vs 4). Docstring/SKILL.md imply seeded. Fixer's "rescaled = 6" not reproduced (4/5/5).
   - Permuted null is not always 0 (1 stable on the snippet's permutation at full size; seed 109 at 1,000 probes).
   - SKILL.md gives no wall time for saga/Boruta at p=7,129; only the p>20k pre-filter row and "measured on 1,000 probes".

## Open findings and blockers

None blocking. Candidate findings above are for the re-auditor to grade.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md (sha256 e6d2297cad470fb9ea90924265a46c049c40ab5b86f6fd2aa6ab6c7c27494377)
- Environment fingerprint: 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 (unchanged; venv freeze 9ba94225...be0a hash matches freeze\pip-freeze-shared.txt)
- Wall times (1,000 / full): blocks 0-5 2/7, 14/96, 28/84, 68/104, 34/263, 5/41 s; stability table 22/306 s; lasso 6 s, boruta 6 s (synthetic). All light.
- Run evidence: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\tooling-delta-20261003\logs\; fix evidence in fix-lane3-20261003\
- Restricted-access items: none. R glmnet prose only, not executed.
- Tooling impact: changed (handled in this phase)

## Worktree safety

- Run-owned changes: TOOLS.md; tooling-delta-20261003\logs; audit-envs\derived\biomarker-discovery\; INDEX.md row (one clause); this handoff. Skill bytes unchanged (a stray `scripts\__pycache__` from my helper was removed; hash re-verified).
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
