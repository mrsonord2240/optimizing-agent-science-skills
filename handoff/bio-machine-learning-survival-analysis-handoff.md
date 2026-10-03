# Handoff: bio-machine-learning-survival-analysis / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 3, machine-learning batch)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: 2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b (files=5, bytes=27923), re-verified with `tools/skill_preflight.py --offline` after tooling (PASS)
- Applicable audit: none

## Completed this phase

- Both scripts re-run clean (rc 0, no warnings) in tools\survival-venv; snippets run on real GBSG2 (686 pts): Coxnet Uno C 0.668, RSF 0.683, IBS 0.161 vs KM-only 0.178; lifelines 1-C sign trap reproduces.
- Constraint check from installed metadata: sksurv 0.28 needs sklearn >=1.9,<1.10 and pandas >=2.2 (no cap); lifelines 0.30.3 alone needs pandas <3.0. SKILL.md wording is accurate.
- Added tools\pycox-venv (pycox 0.3.0, torch 2.14.1 CPU, pandas 3.0.6): DeepSurv C-td 0.615 and DeepHit 0.620 on GBSG2, CPU, seconds.

## Coverage map (per surface)

- `scripts/cox_regression.py`, `scripts/competing_risks_cif.py`: executed (synthetic; survival venv).
- Snippets + lifelines CoxPH/C-index: executed on GBSG2 (sksurv bundled, no download).
- pycox DeepSurv/DeepHit (prose only): executed in pycox venv (`logs/pycox_smoke.log`).
- Fine-Gray, landmarking: prose only, no code, not exercised; no real public competing-risks set staged.

## Required next actions

1. Audit batching: **light** (every required surface runs on CPU in under 2 minutes; inputs under 30 MB).
2. Audit against the exact identity above; run from saved scripts in F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3 (logs in its `logs` folder).
3. Do not edit Skill bytes in the audit; findings go to the ledger. Needed-but-missing inputs: request a tooling-delta pass.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | Notes for audit: Use two venvs: lifelines needs pandas 2.3 (survival-venv); pycox/sksurv-only code runs on pandas 3 (pycox-venv). |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-survival-analysis\TOOLS.md (sha256 f74308bb8b2fd623cc27e8529cd61ce9f7a8045cbf5844f119e963cf63453e63)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 of F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\fingerprint-inputs.txt (hashes of four pip freezes); ecosystem root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (INDEX row `machine-learning`), addendum in its TOOLS.md and `public-data\README.md`
- Run evidence: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed; staging additions only: pycox-venv)

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (smoke\ml-lane3, derived, public-data, tools\pycox-venv, freeze, TOOLS.md, INDEX.md); records `audits/skills/bio-machine-learning-survival-analysis/candidate@2dc45fa24b13-tooling-20261003/TOOLS.md`; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
