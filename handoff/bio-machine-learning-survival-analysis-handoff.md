# Handoff: bio-machine-learning-survival-analysis / fix-scientific-skill

- Updated: 2026-10-03T14:45:00-04:00
- Lane: 3 (batch 3b)
- Status: ready-for-phase
- Owner leaving: initial-audit worker (lane 3b)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: 2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b (files=5, bytes=27923), re-verified with `tools/skill_preflight.py --offline` after the audit (PASS, no pycache)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-survival-analysis\candidate@2dc45fa24b13-initial-lane3b-20261003\report.json (identity above; score 77, Limited Release, no veto)

## Completed this phase

- Static review plus 5 executed inputs: SKILL.md blocks verbatim on GBSG2, cox_regression.py, competing_risks_cif.py with a hand-computed table, metric-direction and pycox CPU checks, p>>n Coxnet check.
- Reproduced two silent defects: KM baseline IBS miscomputed (0.290 vs 0.236; GBSG2 0.263 vs 0.178) and Coxnet predicting at the smallest alpha (p>>n: C 0.708 vs 0.790 CV-tuned).
- Verified: lifelines 1-C trap, 1-KM vs Aalen-Johansen (hand values match), Harrell upward bias, dependency statements (sksurv sklearn <1.10 and pandas >=2.2 no cap; lifelines alone pandas <3; pycox trains on CPU).
- Published record with 20 scripts/evidence files; views regenerated, `npm run audits:check` passes.
- No audit-local repair; no Skill bytes changed.

## Required next actions

1. Fix SA-001 (P1, runnable bytes): true KM baseline in scripts/cox_regression.py and SKILL.md IBS example.
2. Fix SA-002 (P1, runnable bytes): choose Coxnet alpha by CV in the snippet and script; state which alpha predict uses.
3. Fix SA-003, SA-004, SA-005 (text only): runnable evaluation setup (t_horizon, splits); qualify RSF competing-risks claim and name implementations; label prose-only methods not executed and tighten the dependency note.
4. Report tooling impact: SA-001/SA-002 change scripts, so request a tooling delta (rerun scripts/pgtn_and_censoring_checks.py and km_baseline_check.py).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SA-001 | P1 | open | audits\skills\...\scripts\evidence\km_baseline_check.log | runnable bytes + text |
| SA-002 | P1 | open | scripts\evidence\pgtn_and_censoring_checks.log, coxnet_alpha_check.log | runnable bytes + text |
| SA-003 | P2 | open | scripts\evidence\gbsg2_skill_snippets.log | text only |
| SA-004 | P2 | open | scripts\evidence\sksurv_competing_check.log, competing_hand_check.log | text only |
| SA-005 | P2 | open | scripts\evidence\dependency_metadata.log | text only |

Deferred (static-only, prose only): Fine-Gray, landmarking, calibration curves/ICI, nested CV. Blocked: none. No real public competing-risks set is staged (script stays synthetic).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-survival-analysis\TOOLS.md (sha256 f74308bb8b2fd623cc27e8529cd61ce9f7a8045cbf5844f119e963cf63453e63)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; survival-venv and pycox-venv (CPU)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-survival-analysis\initial-lane3b-20261003\ (report.json, viewer.md, finding-ledger.md, scripts\, logs\)
- Restricted-access items: none
- Tooling impact: not applicable to this phase (no Skill bytes changed); fixes for SA-001/SA-002 will change runnable bytes

## Worktree safety

- Run-owned changes: the run directory above; records `audits/skills/bio-machine-learning-survival-analysis/candidate@2dc45fa24b13-initial-lane3b-20261003/`; regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; sibling workers' records and handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
