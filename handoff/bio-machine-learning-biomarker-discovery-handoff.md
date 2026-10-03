# Handoff: bio-machine-learning-biomarker-discovery / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03T16:05:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: fix worker (lane 3a-1)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design)
- Candidate tree hash: c64a3bcb57681c24d76debd7fe4788b3bd3fc5377b358595d62df7d955aaf3c7 (files=6, bytes=36037); `tools/skill_preflight.py` PASS (only warn: no Skill-root LICENSE)
- Superseded identity (audited): e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71; audit at audits/skills/bio-machine-learning-biomarker-discovery/candidate@e0d8efc0e1b0-initial-lane3-20261003

## Completed this phase

- All six findings fixed; changed files: SKILL.md, usage-guide.md, scripts/lasso_biomarker.py, scripts/boruta_feature_selection.py, new scripts/stability_selection.py.
- Every SKILL.md python block (6) executed as written under `-W error::FutureWarning` on real Golub (1,000 top-variance probes, label-free filter); both scripts rc 0, no warnings.
- Evidence dir: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\fix-lane3-20261003\ (evidence/, scripts/).

## Finding dispositions

| ID | State | Result (evidence under fix-lane3-20261003/evidence) |
|---|---|---|
| BD-001 | fixed | New `stability_selection()`: standardize per subsample, fixed per-subsample budget q (MB bound q=sqrt(EV(2pi-1)p)=37 at p=7129) instead of C. Full Golub raw: 5 stable vs 0 stable in each of 10 permuted-label runs (max freq 0.23-0.48). Standardized input: same 5. Unit-rescaled input: 6 (one marginal probe flips, max freq diff 0.08; docstring says so). Old procedure (audit): 61-64 real, 35 permuted. bd001.json |
| BD-002 | fixed | scoring pinned to `accuracy`, stated with measured sizes (1,000 probes, scaler in pipeline, cv=5): neg_log_loss 601 (16 on permuted labels), roc_auc 203 (0), accuracy 148 (0); held-out AUC 0.991/0.983/0.991. Synthetic 5-true-of-2000: 56/57/57 selected. Single dataset/partition caveat in text. scoring_1000.json |
| BD-003 | fixed | StandardScaler first in the pipeline (AUC 0.990); label now "In-pipeline CV AUC (k fixed)"; nested GridSearchCV snippet added. |
| BD-004 | fixed | seed arg (default_rng); NaN index when nothing selected, caller prints "no features selected". |
| BD-005 | fixed | boruta script now fits a CV L1 pipeline and prints what it keeps (4/5 vs Boruta 5/5); lasso script prints numbers, no stale "~0.7+" comment. |
| BD-006 | fixed | `MRMRSelect` in-fold transformer snippet; runs (Golub 5-fold AUC 0.987 real, 0.41 permuted, t4 run). |

Added to the workflow: permuted-label null count reported next to the real stable count; unit-rescaling check in lasso_biomarker.py.

## Required next actions

1. prepare-scientific-skill-tooling delta: register new surface `scripts/stability_selection.py` (import + lasso_biomarker.py), changed `scripts/*.py`, SKILL.md blocks 0-5 (pipeline, nested, MRMRSelect, Boruta, enet, stability). No new dependency.
2. Re-audit with the harness at fix-lane3-20261003/scripts/run_skill_snippets.py (cwd = Skill dir; arg 1000 probes). Full 7,129-probe saga fits are too slow (>10 min per scoring).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-biomarker-discovery\TOOLS.md
- Environment: audit-envs\cheminformatics-hit-triage-analyst (Python 3.12.13, sklearn 1.9.1, numpy 2.5.3, pandas 3.0.5, mrmr-selection 0.2.8, Boruta 0.4.3); unchanged
- Restricted-access items: none
- Tooling impact: changed (new script surface scripts/stability_selection.py; changed snippets and both scripts)

## Notes

- One mRMR pipeline run printed a joblib `OSError: [WinError 6]` at interpreter exit once (not reproduced; results printed first).
- A background 7,129-probe scoring run I started was killed by me (PID 99552/80212, confirmed own command line and start time).

## Worktree safety

- Run-owned changes: Skill dir above (5 changed/new files); fix-lane3-20261003 evidence; this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
