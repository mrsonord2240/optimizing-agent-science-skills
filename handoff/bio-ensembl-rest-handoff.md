# Handoff: bio-ensembl-rest / fix-scientific-skill

> RUN PAUSED 2026-10-03 by Sam after the initial audit. Nothing is in flight. Resume at fix-scientific-skill; candidate is untracked and uncommitted in the working tree below.

- Updated: 2026-10-03T00:00:00-07:00
- Lane: 2
- Status: ready-for-phase
- Owner leaving: initial-audit worker (Sonnet), lane 2, batch database-access light
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ensembl-rest
- Working tree: F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest
- Branch/worktree: fix/dbaccess-ensembl-rest at 2f38178 (shelf main)
- Candidate tree hash: 3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2 (sha256-manifest-v1, files=6, bytes=24508; unchanged, no pycache)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-ensembl-rest\candidate@3d116ba2e1c5-initial-audit-run\report.json (identity above)

## Completed this phase

- Score 70 (static 74, exec 67.6, assertions 15/23), Beta Only, no veto. Run dir: F:\OpenScience\audits\bio-ensembl-rest\initial-audit-run\ (report.json, viewer.md with ordered ledger, source-identity.json, scripts/).
- Executed every client function, all three examples, e110/e111/e116/GRCh37/e90 archives, divisions, POST lookup, doc endpoint table against live Ensembl 116.
- Confirmed leads T1 -> ENS-001 and T2 -> ENS-002; N1 narrowed: e116 archive host (jun2026) 503 is an outage, e110/e111 reproducible.
- Published record; audits:index and audits:check pass.

## Required next actions

1. Fix ENS-001 .. ENS-004 (P1) first; they are doc/example edits plus optional `multiple_sequences` client option.
2. Then ENS-005 .. ENS-008 (P2). Re-run the three examples and the run_core/run_claims probes after fixing.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ENS-001 | P1 | open | evidence/core.txt, example_lookup_and_overlap.txt | gene ID + protein returns 400; use ENSP/ENST ID or add multiple_sequences |
| ENS-002 | P1 | open | evidence/core.txt, example_vep_annotation.txt | HGVS c.803G>A wrong ref base; use c.803C>T or BRAF c.1799T>A |
| ENS-003 | P1 | open | evidence/core.txt | usage-guide 17:41276135 is GRCh37; 400 on GRCh38 host |
| ENS-004 | P1 | open | evidence/claims.txt, regulatory.txt | /regulatory/.../feature/{id} and /homology/id/{id} 404; correct or remove |
| ENS-005 | P2 | open | evidence/claims.txt | renamed symbol is 400 not 404; Homo_sapiens accepted |
| ENS-006 | P2 | open | evidence/claims.txt, claims2.txt | no timeout/5xx/non-JSON handling; e90 HTML 200; e116 503 |
| ENS-007 | P2 | open | evidence/example_compara_homology.txt | empty paralog section, stale confidence/many2one text |
| ENS-008 | P2 | open | preflight warn | no Skill-root LICENSE |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-ensembl-rest\TOOLS.md
- Environment fingerprint: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397
- Run evidence: F:\OpenScience\audits\bio-ensembl-rest\initial-audit-run\evidence\
- Deferred/blocked surfaces: none (local VEP and BioMart are out of scope)
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-ensembl-rest\initial-audit-run\; records under audits\skills\bio-ensembl-rest\ and regenerated audits\INDEX/BACKLOG/STATUS (uncommitted)
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\test\validate.bats (untracked)
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
