# Handoff: bio-machine-learning-biomarker-discovery / prepare-scientific-skill-tooling (delta mode)

- Updated: 2026-10-03T18:00:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: fix worker (lane 3a-1, second fix pass)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery (untracked by design)
- Branch/worktree: normalize/ml-lane3 from 29f5446
- Candidate tree hash: 8d764451560e123e485b6e9f01fb0b5fd84170f4e221db7616571045bba2a19e (files=6, bytes=37468); `tools/skill_preflight.py` PASS (warn only: no Skill-root LICENSE). Previous: c64a3bcb... (36037 bytes)
- Applicable audit: audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-initial-lane3-20261003 (superseded identity)

## Completed this phase

- Fixed non-determinism: `scripts/stability_selection.py` now seeds the liblinear fit (`random_state` drawn from the seeded generator, one per subsample). Two identical calls give identical frequencies and index, raw and rescaled, at 1,000 and 7,129 probes (fix2-lane3-20261003\logs\determinism_*.log).
- Re-measured and restated every number (SKILL.md stability table): real 2/2/2 (1,000) and 5/5/5 (full) for raw/standardized/rescaled; permuted null 0 in 10 of 11 with one stable probe (freq 0.81, seed 109) at 1,000, 0 in 11 of 11 at full (incl. the snippet's permutation). Old "5/5/6" and "0 in each of 10" removed. Unit invariance stated as approximate.
- Added measured cost note: saga elastic-net snippet ~34 s / ~263 s (1,000 / 7,129 probes); one stability call 1-6 s / 16-24 s.
- Reran all SKILL.md blocks 0-5 and the three scripts under `-W error::FutureWarning` at both sizes: all rc 0, no warning/traceback (logs\final\). BD-002..BD-006 untouched and not regressed (blocks 0-4 unchanged).

## Finding dispositions

| ID | State | Note |
|---|---|---|
| BD-001..BD-006 | fixed (earlier pass, fix-lane3-20261003) | no regression this pass |
| BD-007 (new, P2) stability_selection not reproducible; stated counts wrong | fixed | evidence above |
| BD-008 (new, P2) no cost disclosure for 7,129 probes | fixed | SKILL.md Cost note |

Observation (not a defect): `scripts/lasso_biomarker.py` stable set on its synthetic data is g0-g3 (4 of 5 true genes); its print label says "true signal = g0..g4". No doc claims 5/5.

## Required next actions

1. Tooling delta: `stability_selection.py` runnable bytes changed (RNG draw order changed, so previous frequencies differ; staging scripts `check_determinism.py` / `check_rescaled.py` now pass trivially). Update TOOLS.md numbers (stale: stable cols 328/858, 5/5/4, perm 0-of-10 wording).
2. Re-audit against 8d764451...; weigh BD-007/008 and the 11-permutation null counts.

## Open findings and blockers

None.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md (stale numbers for stability surface; environment unchanged, no install)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\fix2-lane3-20261003\ (logs\, determinism.py, hashes.py, sha256-before-reconstructed.json, sha256-after.json)
- Final-run wall times 1,000 / full: blocks 0-5 3/9, 18/119, 23/86, 72/103, 41/268, 7/50 s; stability table 29/296 s; lasso 8/6 s; boruta 7/5 s. Machine shared.
- Restricted-access items: none. R glmnet prose only.
- Tooling impact: changed (surface: scripts/stability_selection.py and its callers, SKILL.md block 5, lasso_biomarker.py; no dependency/env change)

## Worktree safety

- Run-owned changes: Skill SKILL.md and scripts/stability_selection.py; fix2-lane3-20261003\; this handoff. Other files byte-identical (hashes in evidence). Before-hashes are reconstructed by reversing my edits (original manifest c64a3bcb... was the reference).
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- No __pycache__ in Skill dir, LF only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
