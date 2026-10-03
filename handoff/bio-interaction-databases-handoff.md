# Handoff: bio-interaction-databases / fix-scientific-skill (text-only batch)

- Updated: 2026-10-03
- Status: ready-for-phase
- Next role: reaudit-scientific-skill (delta mode, text-only change to certified bytes)
- Tooling impact: none

## Candidate identity

- New: sha256-manifest-v1 `f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d`, files=6, bytes=42364; `skill_preflight.py --offline` PASS, no pycache
- Previously certified (87, Production Ready): `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024`, files=6, bytes=42142, record `audits\skills\bio-interaction-databases\candidate@16290147ab41-reaudit-run-2\`
- Tree: `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design)

## Findings

- IDM-012 (P2): fixed (text-only). SKILL.md aggregate bullet now says self-interactions/homodimers are excluded from the aggregate, a gene whose only evidence is a self-interaction is not a node, and `gene_a == gene_b` rows remain in `biogrid_lt_physical`. The `aggregate_networks` docstring now says homodimers and points to `biogrid_lt_physical` (docstring only; ast.parse OK).
- IDM-013 (P2): open, deferred (needs a code change, not needed for readiness).
- Files changed: `SKILL.md`, `scripts/interaction_clients.py` (docstring only). Exact diff: `F:\OpenScience\audits\bio-interaction-databases\text-fix-run\diff.txt`
- Not executed this phase (text-only; delta re-audit executes).

## Worktree

Nothing staged, committed or pushed; `test\validate.bats` untouched.
