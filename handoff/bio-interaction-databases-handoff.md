# Handoff: bio-interaction-databases / fix-scientific-skill

> RUN PAUSED 2026-10-03 by Sam after the initial audit. Nothing is in flight. Resume at fix-scientific-skill; candidate is untracked and uncommitted in the working tree below.

- Updated: 2026-10-03T00:30:00-07:00
- Lane: 2
- Status: ready-for-phase
- Owner leaving: initial-audit worker (Sonnet), lane 2, batch database-access light
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/interaction-databases
- Working tree: F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases
- Branch/worktree: fix/dbaccess-interaction-databases at 2f38178 (shelf main)
- Candidate tree hash: 588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42 (sha256-manifest-v1, files=5, bytes=31873; unchanged, no pycache)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-interaction-databases\candidate@588996fc143f-initial-audit-run\report.json (identity above)

## Completed this phase

- Score 59 (static 67, exec 54.0, assertions 9/20), Reject by score only; no veto fired. Run dir: F:\OpenScience\audits\bio-interaction-databases\initial-audit-run\ (report.json, viewer.md with ordered ledger, source-identity.json, scripts/).
- Executed STRING, OmniPath, BioGRID (with key), SIGNOR, aggregate_networks and both examples live; confirmed leads T1 (IDM-003), T2 (IDM-001); T3 strengthened to a license-compliance failure (IDM-002).
- Key scan of run dir and published record: zero hits for the BioGRID key value; the only `accesskey=` text was a fake-key error URL, now redacted.
- Published record; audits:index and audits:check pass.

## Required next actions

1. Fix IDM-001 and IDM-002 (P0) first, then IDM-003, IDM-004 (P1), then IDM-005 .. IDM-009 (P2).
2. After fixing, rerun scripts/run_string_omnipath.py, run_omnipath_license.py, run_biogrid.py (needs the key; never write it), run_examples.py. SIGNOR needs a regression with expected TP53 row count.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| IDM-001 | P0 | open | evidence/string_omnipath.txt | signor_for_gene empty; use organism=9606&id=<UniProt>, headerless 29 cols (A col0, B col4, effect col8, mechanism col9, PMID col21); warn on 'No result found.' |
| IDM-002 | P0 | open | evidence/omnipath_license.txt, omnipath_resources2.txt | license=commercial returns PhosphoSite/HPRD (academic); drop the claim or filter by /resources license purpose |
| IDM-003 | P1 | open | evidence/examples.txt, string_network_patched.txt | queryItem -> queryIndex; later sections verified |
| IDM-004 | P1 | open | evidence/string_omnipath.txt | escore>0.4 != network_type=physical (5 of 26 differ) |
| IDM-005 | P2 | open | evidence/examples.txt | max_score STRING/1000 and invented 0.5/0.7 |
| IDM-006 | P2 | open | evidence/biogrid.txt | aggregate_networks unions unequal scopes (1 vs 564 vs 1269 edges) |
| IDM-007 | P2 | open | evidence/biogrid.txt | key in HTTPError URL; invalid key is 401; per-experiment rows |
| IDM-008 | P2 | open | static | timeouts, STRING pacing, shared caller_identity, n_resources field |
| IDM-009 | P2 | open | preflight warn | no Skill-root LICENSE |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-interaction-databases\TOOLS.md
- Environment fingerprint: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397
- BioGRID key: F:\OpenScience\audit-envs\database-access\private\biogrid.env, variable BIOGRID_ACCESS_KEY; load at run time only
- Run evidence: F:\OpenScience\audits\bio-interaction-databases\initial-audit-run\evidence\
- Deferred/static-only: Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client (liveness probe only), R clients
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed)

## Worktree safety

- Run-owned changes: run dir above; records under audits\skills\bio-interaction-databases\ and regenerated audits\INDEX/BACKLOG/STATUS (uncommitted)
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\test\validate.bats (untracked)
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
