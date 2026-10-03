> **Audit record for `bio-interaction-databases`**
> - Audited working candidate `7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/interaction-databases), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit: bio-interaction-databases

**Date:** 2026-10-03
**Candidate:** `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5` (6 files, 41,606 bytes), unchanged before and after the run
**Result:** Candidate-ready: **85/100, Production Ready** (static 84, execution average 86.0). The margin is thin and is limited by two P2 findings.

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | 85 (33.6 + 51.6 = 85.2) | 85 |
| Static | 84 | 80 |
| Execution average | 86.0 | 85 |
| Layer 1 average | 34.3 / 40 | 32 |
| Layer 2 average | 51.7 / 60 | 48 |
| Assertions | 33 / 35 (94%) | 90% |
| Veto / open P0 | none / none | none |

## Initial findings

| ID | Sev | Disposition | Independent evidence |
|---|---|---|---|
| IDM-001 | P0 | verified-fixed | `evidence/signor.txt`: 333 TP53 records equal to the raw 29-column answer (field multiset), ATM->TP53 phosphorylation, MDM2->TP53 ubiquitination, AKT1 456 rows, empty answer warns |
| IDM-002 | P0 | verified-fixed | `evidence/omni.txt`: server parameter still does not filter (344 = 344); client keeps 343 rows equal to an independent expectation; no non-commercial source survives |
| IDM-003 | P1 | verified-fixed | `evidence/ex_string_network.txt`: example exits 0 |
| IDM-004 | P1 | verified-fixed | `evidence/string.txt`: physical network 22 edges, subset of 35 functional; 5 of 26 escore edges not physical |
| IDM-005 | P2 | verified-fixed | `evidence/aggregated_interactions.csv`: string_score 0.716-0.999 on STRING edges only |
| IDM-006 | P2 | verified-fixed | `evidence/agg.txt`: nodes stay inside the query set |
| IDM-007 | P2 | verified-fixed | `evidence/biogrid.txt`: real key 3081 rows / 831 pairs; fake, empty and real-key error paths carry no URL, key or chained exception |
| IDM-008 | P2 | verified-fixed | timeout 60 s, STRING pacing 1.66 s for two calls, caller_identity accepted |
| IDM-009 | P2 | verified-fixed | upstream MIT LICENSE present at the Skill root; preflight PASS |

## New findings

- **IDM-010 (P2):** `aggregate_networks` admits BioGRID homodimer rows as self-loops; `summary()` then reports 2 nodes, 3 edges, density 3.0, mean degree 3.0 for TP53+MDM2 (`evidence/selfloops.txt`). Present since the original code; not caused by the fix.
- **IDM-011 (P2):** a non-empty SIGNOR answer that is not "No result found." and has no parseable rows returns an empty frame with no warning (`evidence/signor_junk.txt`). One transient one-line raw answer was seen once during the run and was not reproduced in 12 later calls (`evidence/signor_transient.txt`).

## Execution

Interpreter `F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (py3.12.13, requests 2.34.2, pandas 3.0.5, networkx 3.7), no installs or downloads. Live services answered normally on this run (OmniPath and UniProt included). The BioGRID key was loaded into the process environment only; a scan of all run output, scripts, report and handoff for its value found no hit.

| Surface | Status | Evidence |
|---|---|---|
| STRING resolve, network (tiers, physical), pacing, caller_identity | executed | `evidence/string.txt` |
| UniProt `uniprot_accession`, SIGNOR `signor_for_gene` | executed | `evidence/signor.txt`, `evidence/signor_junk.txt` |
| OmniPath interactions, commercial screen, /resources | executed | `evidence/omni.txt` |
| BioGRID LT physical, key-leak retest (real key, fake keys, connection failure, HTTP 404) | executed | `evidence/biogrid.txt` |
| aggregate_networks, summary, multi_source_edges | executed | `evidence/agg.txt`, `evidence/selfloops.txt` |
| examples/string_network.py, examples/interaction_query.py (final bytes) | executed, exit 0 | `evidence/ex_string_network.txt`, `evidence/ex_interaction_query.txt` |
| Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients | static-only: no client or recipe ships | none |

## Veto review

Skill veto PASS (stability, contract, determinism, security). Research veto PASS (scientific integrity, practice boundaries, methodological ground, code usability); see `report.json`.

## Per-input scores

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---:|---:|---:|---:|
| 1 STRING example | Canonical | 35 | 53 | 88 | 5/5 |
| 2 Directed aggregate example | Variant A | 34 | 52 | 86 | 5/5 |
| 3 BioGRID and key leak | Variant B | 36 | 54 | 90 | 5/5 |
| 4 SIGNOR TP53 / AKT1 | Edge | 34 | 51 | 85 | 4/5 |
| 5 OmniPath commercial screen | Stress | 34 | 51 | 85 | 5/5 |
| 6 aggregate_networks / summary | Stress | 31 | 47 | 78 | 4/5 |
| 7 STRING physical claim | Variant A | 36 | 54 | 90 | 5/5 |

The OmniPath screen is source-level only (stated in the Skill); the surviving sources still need per-resource terms review. Rerun: `Scripts\python.exe reaudit-run\scripts\reaudit_idm.py <signor|omni|string|biogrid|agg>` with the key file in place.
