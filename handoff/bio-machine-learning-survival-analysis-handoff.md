# Handoff: bio-machine-learning-survival-analysis / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03
- Lane: 3 (batch 3b-2)
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (delta, lane 3b-2)
- Next role: reaudit-scientific-skill (full mode: runnable bytes changed)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis (untracked by design; no product commit)
- Candidate tree hash: c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39 (files=5, bytes=33891); `tools/skill_preflight.py --offline` PASS before and after this phase; Skill bytes untouched, no __pycache__
- Previous audit (2dc45fa24b13...) is stale for these bytes; no usable exact audit exists

## Completed this phase

- TOOLS.md refreshed in place (delta mode): F:\OpenScience\audits\bio-machine-learning-survival-analysis\TOOLS.md, sha256 4a6085401794e7b5f4dea829cdcca688faa191caa3340ae3d5c2aa136ada4c1b
- cox_regression.py both modes light: synthetic 6.5 s, gbsg2 6.4 s, 0 stderr; fit_coxnet_cv at p>>n 3.3 s (the earlier >15 min approach is gone)
- p>>n (n=150, p=1000) reproduced from staging: default path-end 161 nonzero / Uno C 0.708; CV alpha 0.1827, 6 nonzero / 0.791
- SKILL.md snippets exec unmodified, 5.8 s; sksurv `cumulative_incidence_competing_risks` == lifelines AJ (0.2499), 4.2 s
- Staged: audit-envs\cheminformatics-hit-triage-analyst\derived\survival-pgtn\ (make_pgtn.py, run_pgtn.py, time_runs.py, pgtn.npz); indexed in audit-envs\INDEX.md (machine-learning row) and the root TOOLS.md addendum

## Required next actions

1. Fresh auditor re-audits the new identity using TOOLS.md. p>>n rerun: `<survival-venv python> derived\survival-pgtn\run_pgtn.py <Skill>\scripts` (pgtn.npz already built; `make_pgtn.py` rebuilds it).
2. Not executed, Skill must keep them labelled: Fine-Gray (cmprsk), CIF-based Brier (riskRegression), randomForestSRC, landmarking. pycox smoke-tested only (30 epochs CPU), not rerun.

## Environment and evidence

- Environment fingerprint UNCHANGED: 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 (fingerprint-inputs and both freezes re-hashed identical); no package change
- Logs: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\ (cox_delta_synthetic/gbsg2, cox_delta_timing, pgtn_make, pgtn_run, snippets_delta, competing_delta)
- Fix evidence: F:\OpenScience\audits\bio-machine-learning-survival-analysis\fix-lane3b-20261003\
- Blockers, restricted access: none
- Tooling impact: delta complete

## Worktree safety

- Run-owned changes: TOOLS.md, derived\survival-pgtn\, INDEX.md and root TOOLS.md rows, smoke logs, this handoff
- Pre-existing/user-owned untouched: records test/validate.bats, shelf .vscode/, sibling Skill dirs
- No process killed. Prior fixer incident (three unidentified python.exe PIDs force-killed) stands as recorded
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
