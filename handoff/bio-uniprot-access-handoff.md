# Handoff: bio-uniprot-access / orchestrator (commit, then intake)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready
- Owner leaving: delta re-audit worker (lane 1; did not fix or initially audit this Skill)
- Next role: optimize-scientific-skills (orchestrator)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/uniprot-access
- Working tree: F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access
- Branch/worktree: fix/dbaccess-uniprot-access @ 2f381782596c6569fe5a8357556856512b7fbb6c (Skill dir untracked, uncommitted by design)
- Candidate tree hash: sha256-manifest-v1 `7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b`, files=6, bytes=30468 (unchanged by the audit; `skill_preflight.py --offline` PASS, no pycache)
- Applicable audit: `audits\skills\bio-uniprot-access\candidate@7a203a5063ea-delta-reaudit-run\` (identity 7a203a5063ea, 88, Production Ready; supersedes `candidate@ea100b041caf-reaudit-run`, certified 86 at ea100b041cafcbf6...)

## Completed this phase

- Delta mode qualified: text-only (SKILL.md Proteome FASTA table cell; one print literal in `examples/isoforms_and_xrefs.py`). Reverting each reproduces the certified per-file sha256; ASTs differ only in that Constant; other four files byte-identical.
- Claims verified: 147,520 entries and 37.8 MB gz (certified run); 86,650,690 raw bytes = ~87 MB; live `AND reviewed:true` on `/uniprotkb/stream` returned 20,416 sp and 0 tr records; changed example re-ran exit 0.
- Score 88 (static 87, execution avg 88.7, L1 35.5, L2 53.2, assertions 30/30); no veto, no open P0.
- UNI-010 (P2): verified-fixed.

## Required next actions

1. Commit the candidate bytes to make them `ready`, then run Marketplace intake.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | | | | |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\database-access\TOOLS.md (sha256 1362072e8a6d0a1f...; env pip-freeze sha256 5fdd1350df2cf397; UniProt release 2026_03)
- Run evidence: F:\OpenScience\audits\bio-uniprot-access\delta-reaudit-run\ (`evidence\text_claims.txt`, `evidence\example.txt`); certified baseline F:\OpenScience\audits\bio-uniprot-access\reaudit-run\
- Restricted-access items: none
- Tooling impact: none (text-only change; no tool, input or environment affected)

## Worktree safety

- Run-owned changes: the delta record under `audits\skills\bio-uniprot-access\`, regenerated `audits\INDEX.md`, `BACKLOG.md`, `STATUS.md`, `STATUS.html`, this handoff
- Pre-existing/user-owned changes: `test\validate.bats` (untracked, untouched)
- Records state: committed in 4e13dc2a
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
