> **Audit record for `bio-interaction-databases`**
> - Audited working candidate `588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/interaction-databases), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-interaction-databases

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 24 | 38 | 62 | 3/5 | ❌ PARTIAL |
| 2 | Variant A | 26 | 36 | 62 | 2/4 | ⚠️ COMPLETED |
| 3 | Variant B | 32 | 46 | 78 | 2/4 | ✅ COMPLETED |
| 4 | Edge | 14 | 16 | 30 | 1/3 | ❌ PARTIAL |
| 5 | Stress | 18 | 20 | 38 | 1/4 | ❌ PARTIAL |

**Execution average:** 54.0 / 100  
**Assertion pass rate:** 9 / 20  
**Static score:** 67 / 100  
**Final score:** 59 / 100 — ❌ Reject  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: shared `database-access-venv` (py3.12.13, requests 2.34.2, pandas 3.0.5, networkx 3.7) from `F:\OpenScience\audit-envs\database-access\`; live services on 2026-10-03 (STRING v12.5, OmniPath server 0.1.5); sequential small queries; no installs. BioGRID key loaded at run time from the private env file; it appears in no saved file (scan result recorded in the handoff). Candidate path read-only, no `__pycache__`.

| Surface | Class | Evidence |
|---|---|---|
| STRING string_resolve_ids, string_network (tiers, channels, physical network comparison) | executed | `evidence/string_omnipath.txt`, `evidence/string_network_patched.txt` |
| OmniPath omnipath_interactions, license filter, per-source license metadata | executed | `evidence/string_omnipath.txt`, `evidence/omnipath_license.txt`, `evidence/omnipath_resources*.txt` |
| BioGRID biogrid_lt_physical (registered key), invalid-key behaviour | executed | `evidence/biogrid.txt` |
| aggregate_networks, summary, multi_source_edges | executed | `evidence/biogrid.txt` |
| SIGNOR signor_for_gene and raw endpoint | failed (client returns empty) | `evidence/string_omnipath.txt` |
| examples/string_network.py | failed (KeyError); diagnostic copy executed | `evidence/examples.txt`, `evidence/string_network_patched.txt` |
| examples/interaction_query.py | executed (exit 0, SIGNOR 0 edges, score scaling) | `evidence/examples.txt` |
| STRING version-11-5 host, IntAct findInteractions liveness | executed (probe only) | `evidence/misc.txt` |
| Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, R clients | static-only | no client or recipe ships; prose reference only |
| IntAct client | static-only | documented as routed via OmniPath/PSICQUIC; REST liveness probe only |

Normalizer leads: SIGNOR broken confirmed (IDM-001); OmniPath license no-op confirmed and strengthened (IDM-002); STRING example KeyError confirmed (IDM-003). No restricted-access items; BioGRID access resolved by the supplied key.

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated identifiers or results in any run; observed values (STRING TP53-MDM2 0.999, BioGRID TP53 3081 LT physical rows) matched live services.
  - practice_boundaries: PASS — Interaction retrieval only; no clinical or prescriptive output.
  - methodological_ground: PASS — The escore-as-physical proxy and the license=commercial claim are overstated (IDM-004, IDM-002) but the Skill discloses the physical/functional distinction and license caveats; filed as findings, not a principled fallacy.
  - code_usability: PASS — All client functions run; signor_for_gene runs but returns empty on every query (IDM-001) and the STRING example raises KeyError on a renamed column (IDM-003). Scored in Layers 1-2 and filed P0/P1 rather than as unrunnable code.

## Static categories

- functional_suitability: 7/12 — STRING, BioGRID and OmniPath clients correct live; SIGNOR (headline signed-signaling resource) returns empty, the STRING example crashes, and the license=commercial filter does not filter.
- reliability: 7/12 — No request timeouts; SIGNOR failure is a silent empty DataFrame (false success); STRING one-request-at-a-time guidance not implemented in the client or the examples.
- performance_context: 6/8 — SKILL.md about 200 lines; resource prose for Reactome, HuRI and others has no runnable counterpart.
- agent_usability: 11/16 — Strong decision matrix, channel semantics and failure-mode tables; the SIGNOR open-question paragraph is honest, but agents are still handed a function that cannot work.
- human_usability: 6/8 — Clear tables; several stated behaviours (license=commercial, escore as physical, empty BioGRID means missing key) do not match the services.
- security: 8/12 — BioGRID access key travels as a query parameter and raise_for_status puts the full URL, key included, into the HTTPError message; the commercial-license claim creates compliance exposure.
- maintainability: 8/12 — One 140-line client with docstrings; no tests, so the dead SIGNOR path and the failing example shipped; hardcoded shared caller_identity.
- agent_specific: 14/20 — Specific trigger description and good escape hatches; examples fail or report false success and the aggregate-union semantics are unclear.

## Detailed outputs

### Input 1 — Canonical: STRING ID resolution, confidence tiers, channels, physical filter, hubs (string_network.py)

**Status:** PARTIAL — Shipped example exits 1 with KeyError 'queryItem'; a one-token diagnostic copy shows every later section works (45/35/23 edges at 400/700/900, MDM2 and TP53 degree 9).  
**Scores:** Basic 24/40 | Specialized 38/60 | Total 62/100

**Assertions:**

- PASS — string_resolve_ids maps the 10 query genes to STRING IDs (10 rows, TP53 -> 9606.ENSP00000269305; STRING v12.5.)
- PASS — string_network returns 0-1 channel scores with the documented columns (13 columns; MDM2-TP53 score 0.999 escore 0.999 dscore 0.90.)
- PASS — Confidence tiers are monotone (400 >= 700 >= 900 edges) (45, 35, 23.)
- FAIL — The shipped example runs to completion (KeyError ['queryItem'] not in index; live column is queryIndex.)
- FAIL — escore > 0.4 reproduces STRING's physical-only network as the guide claims (26 escore edges versus 22 in network_type=physical; 5 escore edges absent from it, 1 physical edge missed.)

### Input 2 — Variant A: STRING + OmniPath + SIGNOR directed provenance graph and CSV export (interaction_query.py)

**Status:** COMPLETED — Exit 0 with 8 nodes and 52 edges, but SIGNOR contributes 0 edges and the in-memory max_score is STRING score divided by 1000 (0.000994 for MDM2-CHEK2).  
**Scores:** Basic 26/40 | Specialized 36/60 | Total 62/100

**Assertions:**

- PASS — STRING and OmniPath edges are added with source provenance and direction flags (26 STRING edges (52 directed), 20 OmniPath directional edges.)
- PASS — CSV export has per-edge sources, n_sources, effect, mechanism, directional (52 edges written, columns as documented.)
- FAIL — SIGNOR signed edges appear in the aggregate (0 signed edges; the section reports success.)
- FAIL — max_score carries the 0-1 resource score (STRING 0.999 stored as 0.000999; the 0.5 and 0.7 constants for OmniPath-only and SIGNOR-only edges are invented.)

### Input 3 — Variant B: BioGRID low-throughput physical interactions with a registered key (biogrid_lt_physical)

**Status:** COMPLETED — TP53: 3081 LT physical rows, 831 unique pairs, MDM2 and CHEK2 present; filter agrees with BioGRID's own physical type for the non-expanded query (28 of 28).  
**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100

**Assertions:**

- PASS — TP53 LT physical filter returns expected partners MDM2 and CHEK2 (Both present; all rows involve TP53.)
- PASS — PHYSICAL_LT_SYSTEMS matches BioGRID EXPERIMENTAL_SYSTEM_TYPE=physical for LT rows (28 LT physical rows, all in the set; no in-set system is non-physical.)
- FAIL — Output is deduplicated to pairs or labelled per experiment (3081 per-experiment rows for 831 pairs; neither the docstring nor SKILL.md says rows are per experiment.)
- FAIL — A rejected key produces the documented empty result (HTTP 401 raised; the HTTPError text includes the full request URL with accesskey.)

### Input 4 — Edge: SIGNOR signed, directed interactions for TP53 (signor_for_gene)

**Status:** PARTIAL — Client returns an empty DataFrame (organism=human gives 'No result found.' with HTTP 200); raw organism=9606&id=P04637 returns 333 headerless 29-column rows all involving TP53.  
**Scores:** Basic 14/40 | Specialized 16/60 | Total 30/100

**Assertions:**

- FAIL — signor_for_gene('TP53') returns signed interactions with effect and mechanism (0 rows.)
- FAIL — An empty result is distinguishable from a failure (Silent empty DataFrame; no warning; one row would also be lost to the header skip.)
- PASS — The live SIGNOR route is recoverable from the Skill text (SKILL.md names organism=9606 and id=<UniProt> accurately, and flags the function unverified.)

### Input 5 — Stress: License-aware OmniPath query for a commercial pipeline (license=commercial)

**Status:** PARTIAL — commercial and academic return the same 344 TP53 rows and the same 40 sources; PhosphoSite (CC BY-NC-SA, academic purpose) and HPRD (academic) rows are present under commercial.  
**Scores:** Basic 18/40 | Specialized 20/60 | Total 38/100

**Assertions:**

- PASS — omnipath_interactions returns directed TP53 post-translational edges with sources (344 rows, sources and references columns present.)
- FAIL — license=commercial excludes sources whose OmniPath license purpose is academic (Same 344 rows; PhosphoSite and HPRD remain.)
- FAIL — The Skill's own license table is consistent with the commercial filter claim (Table says PhosphoSitePlus needs a commercial license, yet the documented filter passes PhosphoSite-derived rows.)
- FAIL — aggregate_networks gives comparable evidence across sources (TP53+MDM2: STRING contributes 1 edge (query-set only), OmniPath 564 and BioGRID 1269 edges (query neighbourhoods); 1372 nodes.)

## Key strengths

- STRING, BioGRID (with key) and OmniPath clients return scientifically correct live data: TP53-MDM2 STRING 0.999, TP53 3081 BioGRID LT physical rows, 344 OmniPath TP53 post-translational edges.
- Decision matrix, STRING channel semantics, throughput filter and version-pinning guidance are accurate; the pinned-host stale-data warning was verified (version-11-5 still answers).
- The SIGNOR open question is disclosed in the Skill and the live recovery route (organism=9606, id=UniProt) is described correctly.

## Recommendations

- **[P0] IDM-001 signor_for_gene returns empty for every query** (inputs [2, 4]): organism=human returns 'No result found.' (HTTP 200) so the client yields an empty DataFrame; interaction_query.py reports 0 signed edges as success. The live route (organism=9606&id=<UniProt>) returns headerless 29-column rows (ENTITYA col 0, ENTITYB col 4, EFFECT col 8, MECHANISM col 9, PMID col 21). Fix: Resolve symbol to UniProt, call organism=9606&id=, parse by the live layout without a header skip, raise or warn on 'No result found.', and add a TP53 regression with the expected row count.
- **[P0] IDM-002 license=commercial keeps academic-only sources** (inputs [5]): Commercial and academic queries return identical rows; PhosphoSite (CC BY-NC-SA 3.0) and HPRD (academic) rows are present under commercial, contradicting the Skill's claim in three places and its own PhosphoSitePlus row. Fix: Remove the 'commercial keeps permissive sources only' claim or filter client-side by per-resource license purpose from /resources, and state that the pipeline must still audit sources; also reconcile the SIGNOR license entry (OmniPath lists CC BY 4.0, table says CC-BY-SA).
- **[P1] IDM-003 string_network.py raises KeyError on queryItem** (inputs [1]): The first section selects a column that live STRING no longer returns; the example exits before its tier, channel, physical-filter and centrality sections. Fix: Select queryIndex (or queryItem only if present) and rerun the whole example; later sections were verified working with that one-token change.
- **[P1] IDM-004 escore > 0.4 is not STRING's physical network** (inputs [1]): For the 10-gene example, 5 of 26 escore edges are absent from network_type=physical and 1 physical edge is missed, yet the Skill tells users to use escore for 'physically interact' claims. Fix: Recommend network_type=physical (add a parameter to string_network) for physical claims and describe escore as experimental evidence, not physical.
- **[P2] IDM-005 example max_score mis-scaled and invented** (inputs [2]): interaction_query.py stores STRING score/1000 although TSV scores are 0-1 (MDM2-CHEK2 0.000994) and assigns constants 0.5 and 0.7 to OmniPath-only and SIGNOR-only edges. Fix: Use the 0-1 score as is, leave non-STRING edge scores empty, and rename the attribute so it is not read as a cross-resource confidence.
- **[P2] IDM-006 aggregate_networks unions unequal evidence scopes** (inputs [5]): STRING returns only edges within the query list while OmniPath and BioGRID return each query gene's whole neighbourhood, so multi_source_edges mostly counts BioGRID and OmniPath overlap (TP53+MDM2: 1 STRING edge versus 564 and 1269). Fix: Restrict all sources to the query set or add STRING add_nodes, or document the neighbourhood semantics and warn that multi-source support is not comparable.
- **[P2] IDM-007 BioGRID key leaks into error text** (inputs [3]): raise_for_status includes the full URL with accesskey in the HTTPError message (shown with a deliberately fake key), and a rejected key gives HTTP 401, not the empty result the Skill describes. Fix: Catch HTTPError and re-raise without the URL, document the 401, and label biogrid_lt_physical output as per-experiment rows (3081 rows, 831 pairs for TP53).
- **[P2] IDM-008 No timeouts, STRING pacing, per-user caller id** (inputs [1]): Requests carry no timeout, the client and examples issue consecutive STRING calls without the 1-2 s pause the Skill prescribes, CALLER is a shared constant, and the requested OmniPath field n_resources is not returned. Fix: Add one helper with timeout and optional pacing, let callers pass caller_identity, and drop n_resources from the field list.
- **[P2] IDM-009 No Skill-root LICENSE file** (inputs []): Preflight warns that the manifest cites repository license evidence only; frontmatter says MIT. Fix: Cite the upstream MIT licence evidence in provenance or add a LICENSE file.

## Ordered finding ledger

Audited identity: `588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | IDM-001 | P0 | open | [2, 4] | signor_for_gene returns empty for every query. Resolve symbol to UniProt, call organism=9606&id=, parse by the live layout without a header skip, raise or warn on 'No result found.', and add a TP53 regression with the expected row count. |
| 2 | IDM-002 | P0 | open | [5] | license=commercial keeps academic-only sources. Remove the 'commercial keeps permissive sources only' claim or filter client-side by per-resource license purpose from /resources, and state that the pipeline must still audit sources; also reconcile the SIGNOR license entry (OmniPath lists CC BY 4.0, table says CC-BY-SA). |
| 3 | IDM-003 | P1 | open | [1] | string_network.py raises KeyError on queryItem. Select queryIndex (or queryItem only if present) and rerun the whole example; later sections were verified working with that one-token change. |
| 4 | IDM-004 | P1 | open | [1] | escore > 0.4 is not STRING's physical network. Recommend network_type=physical (add a parameter to string_network) for physical claims and describe escore as experimental evidence, not physical. |
| 5 | IDM-005 | P2 | open | [2] | example max_score mis-scaled and invented. Use the 0-1 score as is, leave non-STRING edge scores empty, and rename the attribute so it is not read as a cross-resource confidence. |
| 6 | IDM-006 | P2 | open | [5] | aggregate_networks unions unequal evidence scopes. Restrict all sources to the query set or add STRING add_nodes, or document the neighbourhood semantics and warn that multi-source support is not comparable. |
| 7 | IDM-007 | P2 | open | [3] | BioGRID key leaks into error text. Catch HTTPError and re-raise without the URL, document the 401, and label biogrid_lt_physical output as per-experiment rows (3081 rows, 831 pairs for TP53). |
| 8 | IDM-008 | P2 | open | [1] | No timeouts, STRING pacing, per-user caller id. Add one helper with timeout and optional pacing, let callers pass caller_identity, and drop n_resources from the field list. |
| 9 | IDM-009 | P2 | open | [] | No Skill-root LICENSE file. Cite the upstream MIT licence evidence in provenance or add a LICENSE file. |

No audit-local repair was made; no Skill bytes changed.
