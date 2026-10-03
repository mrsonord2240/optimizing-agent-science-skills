# Handoff: bio-machine-learning-survival-analysis / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03T16:00:00-04:00
- Lane: 3 (batch 3b-2)
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 3b-2)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39 (files=5, bytes=33891), `tools/skill_preflight.py` PASS (full and --offline-equivalent run, no pycache)
- Previous identity: 2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b
- Applicable audit: audits\skills\bio-machine-learning-survival-analysis\candidate@2dc45fa24b13-initial-lane3b-20261003\ (audited the previous identity; stale for these bytes)

## Completed this phase

- All five findings fixed; fix log and ledger: F:\OpenScience\audits\bio-machine-learning-survival-analysis\fix-lane3b-20261003\fix-log.md
- SA-001: GBSG2 KM-baseline IBS 0.263 -> 0.178, equals lifelines/hand KM. SA-002: p>>n (n=150, p=1000) 161 nonzero / Uno C 0.708 -> CV alpha, 6 nonzero / 0.791; GBSG2 0.668 -> 0.669.
- SKILL.md snippets execute as written (logs\run_skill_snippets.log); competing-risks and prose-only claims corrected.
- Changed files: scripts/cox_regression.py, SKILL.md, usage-guide.md.

## Required next actions

1. Tooling delta: re-smoke scripts/cox_regression.py (`--data synthetic|gbsg2`, new surface flag) and the SKILL.md snippet block; update TOOLS.md surface rows (old KM IBS 0.290 and "snippets 0.178 KM-only" figures are superseded).
2. Reaudit the new identity with a fresh auditor (full mode: runnable bytes changed).

## Findings

| ID | Severity | State | Evidence |
|---|---|---|---|
| SA-001 | P1 | fixed | fix-lane3b-20261003\logs\verify_fixes.log |
| SA-002 | P1 | fixed | same log, parts C-E |
| SA-003 | P2 | fixed | logs\run_skill_snippets.log |
| SA-004 | P2 | fixed | logs\competing_impl_check.log |
| SA-005 | P2 | fixed | SKILL.md Version Compatibility and Model Taxonomy |

Deferred: none. Blocked: none. R packages (cmprsk, riskRegression, randomForestSRC) are named, not installed or executed.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-survival-analysis\TOOLS.md (sha256 f74308bb8b2fd623cc27e8529cd61ce9f7a8045cbf5844f119e963cf63453e63); survival-venv, no new dependency
- Run evidence: F:\OpenScience\audits\bio-machine-learning-survival-analysis\fix-lane3b-20261003\ (scripts\, logs\, fix-log.md)
- Restricted-access items: none
- Tooling impact: changed (scripts/cox_regression.py algorithm and CLI; SKILL.md snippets)

## Worktree safety

- Run-owned changes: the Skill dir above, the run directory, this handoff
- Pre-existing/user-owned: records untracked test/validate.bats; shelf .vscode/; sibling Skill dirs untouched
- Incident: three unidentified python.exe PIDs (50840, 46632, 59468) were force-killed while stopping my own slow job; owner unknown, may include sibling workers' runs
- Records state: uncommitted; Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
