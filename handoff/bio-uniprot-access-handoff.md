# Handoff: bio-uniprot-access / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 1 (re-audit worker)
- Status: candidate-ready (independent final re-audit)
- Next role: orchestrator (commit the bytes to make them `ready`, then intake)

## Candidate identity (unchanged before and after the run)

- sha256-manifest-v1 `ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1`, files=6, bytes=30291; `skill_preflight.py --offline` PASS
- Tree: `F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access` (untracked, uncommitted by design, no pycache)

## Result

- Final 86 (static 85, execution average 87.0), Production Ready; L1 34.8, L2 52.2, assertions 29/30, no veto, no open P0
- Report: `audits\skills\bio-uniprot-access\candidate@ea100b041caf-reaudit-run\report.json` (viewer.md beside it)
- Run dir and raw evidence: `F:\OpenScience\audits\bio-uniprot-access\reaudit-run\`
- Views regenerated (`audits:index`, `audits:check` clean)

## Initial findings

UNI-001..UNI-009: all verified-fixed on the final bytes against UniProt 2026_03 (details in the viewer). None open, none regressed.

## New finding (P2, not blocking)

- UNI-010: `download_proteome('UP000005640')` returns 147,520 entries (20,416 reviewed + 127,104 TrEMBL), 37.8 MB gzip; the example prints "~20 MB compressed; ~80 MB unpacked; ~20K proteins" and no text says TrEMBL is included. Function works and equals the server count. Evidence `evidence\proteome.txt`, `evidence\proteome_counts.txt`.

## Executed and not executed

- Every surface executed on final bytes: all client functions, both examples (exit 0), retry helper (stubbed 429/503/connection errors), stuck and FAILED ID-mapping jobs (stubbed status), E. coli and human proteome downloads (temporary files deleted)
- Not executed: none

## Worktree state

- Skill tree untracked and untouched; records repo has the new untracked record directory and regenerated `audits` views, nothing staged or committed
- `test\validate.bats` untracked and pre-existing, untouched
- Environment: `F:\OpenScience\audit-envs\database-access` (py3.12.13, requests 2.34.2, pandas 3.0.5), nothing installed

## Next

Orchestrator: commit the Skill bytes (optionally fix UNI-010 first via fix-scientific-skill, which would require a new re-audit), then intake.
