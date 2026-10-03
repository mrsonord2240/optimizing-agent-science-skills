# Handoff: bio-interaction-databases / fix-scientific-skill (fix-run-2)

- Updated: 2026-10-03
- Lane: 1
- Status: ready-for-phase
- Next role: reaudit-scientific-skill
- Tooling impact: none (no dependency, runtime, version, wrapper, service, executable path or surface changed; two behaviors inside existing functions)

## Candidate identity

- sha256-manifest-v1 `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024`, files=6, bytes=42142; `skill_preflight.py --offline` PASS
- Prior audited identity: `7430509d403c...` (85, Production Ready). This candidate needs a fresh re-audit.
- Tree: `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design, no pycache)

## Finding ledger

- IDM-001..009: fixed (verified by the prior re-audit; untouched)
- IDM-010: fixed. `_add_edge` drops self-interactions (`a == b`), so `aggregate_networks` and `summary` stay in [0,1]. Docstring and SKILL.md aggregate bullet say self-interactions are dropped. Files: `scripts\interaction_clients.py`, `SKILL.md`.
- IDM-011: fixed. `signor_for_gene` raises ValueError when a non-empty answer has no 28+ column rows; 'No result found.' still returns an empty frame with a warning. Docstring and SKILL.md SIGNOR paragraph updated. Files: same two.

## Verification (final bytes)

- Evidence: `F:\OpenScience\audits\bio-interaction-databases\fix-run-2\` (`verify.py`, `verify_output.txt`, `ex_*.txt`)
- TP53+MDM2 with real BioGRID key: 1 edge (STRING, OmniPath, BioGRID), no self-loops, density 1.0
- SIGNOR: 'No result found.' gives 0 rows plus warning; 'Service temporarily unavailable' and HTML 502 body raise ValueError; live TP53 returns 333 rows
- Both examples exit 0; key scan of Skill and run dir: 0 hits

## Not executed

Unchanged from the prior re-audit (Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients: static only).

## Worktree safety

Nothing staged, committed or pushed; `test\validate.bats`, `fix-run\`, other Skills untouched.
