# Handoff: bio-interaction-databases / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix worker (lane 1, batch database-access light)
- Next role: reaudit-scientific-skill (tooling impact: changed, no new tooling needed; see below)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/interaction-databases
- Working tree: F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases
- Branch/worktree: fix/dbaccess-interaction-databases at 2f38178; Skill directory untracked and uncommitted by design
- Candidate tree hash: 7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5 (sha256-manifest-v1, files=6, bytes=41606); preflight --offline PASS
- Prior audited identity: 588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42 (report.json under audits\skills\bio-interaction-databases\candidate@588996fc143f-initial-audit-run\)
- Note: after the verification run, two example print strings were reworded (text only; ast parse checked, no pycache).

## Finding ledger

| ID | Sev | State | Change | Evidence |
|---|---|---|---|---|
| IDM-001 | P0 | fixed | signor_for_gene resolves symbol to UniProt, organism=9606&id=, headerless 29-col parse, warns on 'No result found.'; SKILL.md SIGNOR paragraph rewritten (open question removed) | verify_fix.txt: TP53 333 rows, ATM->TP53 phosphorylation, empty-case warning |
| IDM-002 | P0 | fixed | server `license` param does not filter; client now screens by /resources license purpose (only 'commercial' kept; sources and references filtered, empty rows dropped); claims corrected in SKILL.md and usage-guide.md; SIGNOR license row reconciled | verify_fix.txt: commercial 343 of 344 rows, PhosphoSite/HPRD absent, no non-commercial source remains |
| IDM-003 | P1 | fixed | examples/string_network.py uses queryIndex | both examples exit 0, output in verify_fix.txt |
| IDM-004 | P1 | fixed | string_network(network_type=) added; example and docs use physical network; escore described as mixed | physical 22 edges subset of functional 35 |
| IDM-005 | P2 | fixed | max_score replaced by string_score (0-1, None for non-STRING); invented 0.5/0.7 removed; CSV column added | edge TP53-MDM2 string_score 0.999 |
| IDM-006 | P2 | fixed | aggregate_networks restricts OmniPath/BioGRID to pairs inside the query set; docs say overlap, not confidence | TP53+MDM2: 2 nodes, edge from 3 sources |
| IDM-007 | P2 | fixed | _get re-raises without URL or chained exception; 401 documented; per-experiment rows documented | bad key raises "HTTP 401 Unauthorized" only; live key run 3081 rows / 831 pairs; key scan of fix-run and Skill: 0 hits |
| IDM-008 | P2 | fixed | 60 s timeouts, 1 s STRING pacing, caller_identity parameter, n_resources dropped | verify_fix.txt |
| IDM-009 | P2 | fixed | upstream MIT LICENSE copied byte-identical to Skill root; Provenance sentence corrected to point at it |

No new findings. Residual notes: OmniPath commercial screen is source-level only (is_stimulation/consensus_* and curation_effort stay server-computed, stated in docs); SIGNOR license kept as share-alike pending a check on the SIGNOR site.

## Changed files

SKILL.md, usage-guide.md, scripts/interaction_clients.py, examples/string_network.py, examples/interaction_query.py, LICENSE (added, IDM-009), SKILL.md Provenance sentence.

## Execution record

- Script: F:\OpenScience\audits\bio-interaction-databases\fix-run\scripts\verify_fix.py; output F:\OpenScience\audits\bio-interaction-databases\fix-run\evidence\verify_fix.txt (30/30 checks) and aggregated_interactions.csv
- Interpreter: F:\OpenScience\audit-envs\database-access\Scripts\python.exe (py3.12.13, requests 2.34.2, pandas 3.0.5, networkx 3.7), PYTHONDONTWRITEBYTECODE=1
- Live services used: STRING v12.5, OmniPath, SIGNOR, BioGRID (key loaded at run time only), UniProt REST (new dependency, no key)
- Not re-executed: Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients (static prose only, as before)

## Tooling impact: changed

Reason: runnable surfaces changed (signor_for_gene, omnipath_interactions, string_network, aggregate_networks, biogrid_lt_physical error path) and the Skill now calls the UniProt REST search endpoint. No new package, runtime, key or staged dataset is needed.

## Tooling (delta, 2026-10-03)

- TOOLS.md: F:\OpenScience\audits\bio-interaction-databases\TOOLS.md (refreshed; UniProt REST added as a listed external service, SIGNOR and example rows replaced). Shared: F:\OpenScience\audit-envs\database-access\TOOLS.md.
- Fingerprint verified live: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397.
- Identity unchanged (preflight --offline PASS): 7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5, files=6, bytes=41606.
- Installed: nothing. Downloaded: nothing. BioGRID key loaded at run time only (TP53 3081 rows); not printed or written.
- Live spot check: STRING, UniProt accession, SIGNOR (333 rows), BioGRID pass; OmniPath returned HTTP 502 once (intermittent, not retried).
- Not made ready: none beyond OmniPath flakiness.

## Re-audit pointers

- Regression probes to rerun: scripts in F:\OpenScience\audits\bio-interaction-databases\initial-audit-run\scripts plus fix-run\scripts\verify_fix.py
- BioGRID key: F:\OpenScience\audit-envs\database-access\private\biogrid.env (BIOGRID_ACCESS_KEY); load at run time only, never write it

## Worktree safety

- Run-owned changes: Skill tree above (untracked), fix-run directory, this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\test\validate.bats (untracked, untouched)
- Product commits/pushes/staging: none; no pycache or generated files in the Skill tree

## Transition assertion

- Next-phase prerequisites met: yes
