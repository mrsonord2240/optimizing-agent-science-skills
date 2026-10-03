# Handoff: bio-uniprot-access / fix-scientific-skill

> RUN PAUSED 2026-10-03 by Sam after the initial audit. Nothing is in flight. Resume at fix-scientific-skill; candidate is untracked and uncommitted in the working tree below.

- Updated: 2026-10-03T00:50:00-07:00
- Lane: 2
- Status: ready-for-phase
- Owner leaving: initial-audit worker (Sonnet), lane 2, batch database-access light
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/uniprot-access
- Working tree: F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access
- Branch/worktree: fix/dbaccess-uniprot-access at 2f38178 (shelf main)
- Candidate tree hash: 7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240 (sha256-manifest-v1, files=5, bytes=24298; unchanged, no pycache)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-uniprot-access\candidate@7f82b9d5aae0-initial-audit-run\report.json (identity above)

## Completed this phase

- Score 61 (static 68, exec 56.0, assertions 11/22), Beta Only, no veto. Run dir: F:\OpenScience\audits\bio-uniprot-access\initial-audit-run\ (report.json, viewer.md with ordered ledger, source-identity.json, scripts/).
- Executed every client function against UniProt 2026_03, both examples, and the documented query/field/endpoint tables; confirmed leads T1 (UNI-001), T2 (UNI-002), T3 (UNI-003), uniref mislabel (UNI-007).
- Published record; audits:index and audits:check pass.

## Required next actions

1. Fix UNI-001 .. UNI-004 (P1) first, then UNI-005 .. UNI-009 (P2).
2. Rerun scripts/run_core.py, run_claims.py, run_claims2.py, run_claims3.py, run_examples.py after fixing; map_ids needs a regression on the three example Ensembl genes (44 rows via idmapping/stream; BRCA2 must appear).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| UNI-001 | P1 | open | evidence/core.txt, claims3.txt | map_ids first page only (25 of 44; BRCA2 lost, empty failedIds); use idmapping/stream, report unmapped, document UniProtKB-Swiss-Prot target |
| UNI-002 | P1 | open | evidence/core.txt | /proteomes/{upid}.fasta.gz is 400; use uniprotkb/stream?query=proteome:UPID&format=fasta&compressed=true |
| UNI-003 | P1 | open | evidence/examples.txt | isoforms_and_xrefs.py formats a list; join ids |
| UNI-004 | P1 | open | evidence/claims.txt, claims2.txt | xref:pdb returns 0 (use database:pdb); ft_active_site invalid (ft_act_site) |
| UNI-005 | P2 | open | evidence/core.txt | 500 shown as total (640); keyword quote vs KW-0418; TrEMBL count stale |
| UNI-006 | P2 | open | evidence/claims.txt | inactive accession -> KeyError 'sequence' |
| UNI-007 | P2 | open | evidence/core.txt | uniref identity/representative mislabel |
| UNI-008 | P2 | open | static | no timeouts/retries/429/FAILED handling |
| UNI-009 | P2 | open | preflight warn | no Skill-root LICENSE |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-uniprot-access\TOOLS.md
- Environment fingerprint: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397
- Run evidence: F:\OpenScience\audits\bio-uniprot-access\initial-audit-run\evidence\
- Deferred/static-only: full human reference proteome download (about 20 MB, not staged)
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed)

## Worktree safety

- Run-owned changes: run dir above; records under audits\skills\bio-uniprot-access\ and regenerated audits\INDEX/BACKLOG/STATUS (uncommitted)
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\test\validate.bats (untracked)
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
