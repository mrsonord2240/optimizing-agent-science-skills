# Handoff: bio-interaction-databases / orchestrator (commit, then intake)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready
- Owner leaving: delta re-audit worker (lane 1; did not fix or initially audit this Skill)
- Next role: optimize-scientific-skills (orchestrator)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/interaction-databases
- Working tree: F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases
- Branch/worktree: fix/dbaccess-interaction-databases @ 2f381782596c6569fe5a8357556856512b7fbb6c (Skill dir untracked, uncommitted by design)
- Candidate tree hash: sha256-manifest-v1 `f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d`, files=6, bytes=42364 (unchanged by the audit; `skill_preflight.py --offline` PASS, no pycache)
- Applicable audit: `audits\skills\bio-interaction-databases\candidate@f4d95b083e70-delta-reaudit-run\` (identity f4d95b083e70, 87, Production Ready; supersedes `candidate@16290147ab41-reaudit-run-2`, certified 87 at 16290147ab41129829...)

## Completed this phase

- Delta mode qualified: text-only (SKILL.md aggregate parenthetical; two docstring lines in `scripts/interaction_clients.py`). Reverting each reproduces the certified per-file sha256; AST identical outside the `aggregate_networks` docstring; other four files byte-identical.
- Claim verified live with the BioGRID key: `gene_a == gene_b` rows remain in `biogrid_lt_physical` (TP53 30 of 3,081; MDM2 23 of 2,058); aggregate TP53+MDM2 has no self-loops; homodimer-only gene yields no node (certified mocked probe).
- Score 87 (static 87, execution avg 87.0, L1 34.7, L2 52.3, assertions 35/35); no veto, no open P0.
- IDM-012 (P2): verified-fixed (dropping stays silent, now documented).

## Required next actions

1. Commit the candidate bytes to make them `ready`, then run Marketplace intake. IDM-013 does not block.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| IDM-013 | P2 | open, deferred | `audits\skills\bio-interaction-databases\candidate@16290147ab41-reaudit-run-2\` | `examples/interaction_query.py` keeps last SIGNOR record per pair; needs a code change, untouched by design |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\database-access\TOOLS.md (sha256 1362072e8a6d0a1f...; env pip-freeze sha256 5fdd1350df2cf397)
- Run evidence: F:\OpenScience\audits\bio-interaction-databases\delta-reaudit-run\ (`evidence\self_rows.txt`, `evidence\skill_md.txt`); certified baseline F:\OpenScience\audits\bio-interaction-databases\reaudit-run-2\
- Restricted-access items: BioGRID key (F:\OpenScience\audit-envs\database-access\private\biogrid.env) used at run time only; scan of run dir, record and Skill tree found no hit
- Tooling impact: none (text-only change; no tool, input or environment affected)

## Worktree safety

- Run-owned changes: the delta record under `audits\skills\bio-interaction-databases\`, regenerated `audits\INDEX.md`, `BACKLOG.md`, `STATUS.md`, `STATUS.html`, this handoff
- Pre-existing/user-owned changes: `test\validate.bats` (untracked, untouched)
- Records state: committed in 4e13dc2a
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
