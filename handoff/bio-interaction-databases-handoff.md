# Handoff: bio-interaction-databases / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (independent final re-audit)
- Next role: orchestrator (commit the bytes to make them `ready`, then intake)

## Candidate identity (unchanged before and after the run)

- sha256-manifest-v1 `7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5`, files=6, bytes=41606; `skill_preflight.py --offline` PASS
- Tree: `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design, sparse worktree, no pycache)

## Result

- Final 85 (static 84, execution average 86.0), Production Ready, margin thin (85.2); L1 34.3, L2 51.7, assertions 33/35, no veto, no open P0
- Report: `audits\skills\bio-interaction-databases\candidate@7430509d403c-reaudit-run\report.json` (viewer.md beside it)
- Run dir and raw evidence: `F:\OpenScience\audits\bio-interaction-databases\reaudit-run\` (scripts, evidence)
- Views regenerated (`audits:index`, `audits:check` clean)

## Initial findings

IDM-001..IDM-009: all verified-fixed on the final bytes against live services (details in the viewer). None open, none regressed.

## New findings (both P2, not blocking)

- IDM-010: `aggregate_networks` admits BioGRID self-interactions as self-loops; `summary()` reports density 3.0 for TP53+MDM2 (pre-existing, not caused by the fix). Evidence `evidence\selfloops.txt`.
- IDM-011: non-empty unparseable SIGNOR answer returns an empty frame with no warning. Evidence `evidence\signor_junk.txt`.

## Executed and not executed

- Executed on final bytes: both examples (exit 0), STRING, UniProt, SIGNOR, OmniPath (healthy today), BioGRID with the real key, key-leak retest with real and fake keys (message, Skill traceback frames, chained exceptions: no URL or key); real key scan of Skill, run dir, report: 0 hits
- Not executed (static only, no client ships): Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients
- OmniPath commercial screen is source-level only (documented); surviving sources still need terms review

## Worktree state

- Skill tree untracked and untouched; records repo has the new untracked record directory and regenerated `audits` views, nothing staged or committed
- `test\validate.bats` untracked and pre-existing, untouched
- Environment: `F:\OpenScience\audit-envs\database-access` (py3.12.13, requests 2.34.2, pandas 3.0.5, networkx 3.7), nothing installed or downloaded

## Next

Orchestrator: commit the Skill bytes (optionally fix IDM-010/011 first via fix-scientific-skill, which would require a new re-audit), then intake.
