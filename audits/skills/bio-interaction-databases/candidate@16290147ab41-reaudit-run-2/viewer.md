> **Audit record for `bio-interaction-databases`**
> - Audited working candidate `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/interaction-databases), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-interaction-databases`**
> - Audited working candidate `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/interaction-databases), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit (second): bio-interaction-databases

**Date:** 2026-10-03
**Candidate:** `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024` (6 files, 42,142 bytes), unchanged before and after the run
**Result:** Candidate-ready: **87/100, Production Ready** (static 86, execution average 87.0).

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | 87 (34.4 + 52.2 = 86.6) | 85 |
| Static | 86 | 80 |
| Execution average | 87.0 | 85 |
| Layer 1 average | 34.7 / 40 | 32 |
| Layer 2 average | 52.3 / 60 | 48 |
| Assertions | 35 / 35 (100%) | 90% |
| Veto / open P0 | none / none | none |

## Change since the previous re-audit (identity 7430509d403c...)

Only `scripts/interaction_clients.py` (11,412 to 11,862 bytes) and `SKILL.md` changed; LICENSE, both examples and usage-guide.md hash identical to the previous identity. The full client file was re-read.

| ID | Sev | Disposition | Independent evidence |
|---|---|---|---|
| IDM-001..009 | P0-P2 | still fixed, no regression | `evidence/signor.txt`, `omni.txt`, `string.txt`, `biogrid.txt`, `agg.txt`, both examples (the previous run's probe script rerun unchanged on the new bytes, 48/48) |
| IDM-010 | P2 | verified-fixed | Live TP53+MDM2 with the real key: 1 edge (STRING, OmniPath, BioGRID), no self-loops, density 1.0. Mocked sources: homodimer rows dropped, partner edges kept, density 0.667 (`evidence/probe_idm10_11.txt`) |
| IDM-011 | P2 | verified-fixed | Mocked answers: plain text, HTML 502 and a 3-column line raise ValueError; empty, blank and "No result found." return an empty typed frame with a warning; a junk line plus a valid row returns the row; live TP53 still 333 rows |

## Targeted checks requested

- Homodimers: dropped silently (no warning, no count); a gene whose only evidence is a self-interaction does not become a node. The docstring and the SKILL.md aggregate bullet say "self-interactions are dropped" but do not name homodimers or point to `biogrid_lt_physical`, where those rows remain (IDM-012, P2).
- ValueError impact: `aggregate_networks` never calls SIGNOR, so it is unaffected. `examples/interaction_query.py` calls `signor_for_gene` per gene without a guard, so a SIGNOR error page now aborts the example with a clear message instead of finishing with an incomplete network; acceptable fail-loud behavior, not a defect. Both examples exit 0 live.
- Regression: the two previously failing assertions now pass; IDM-001..009 probes pass unchanged.

## New findings

- **IDM-012 (P2):** disclosure of dropped self-interactions is a parenthetical (see above).
- **IDM-013 (P2):** `examples/interaction_query.py` keeps the last SIGNOR record's `signed_effect`/`mechanism` per pair, so exported attributes differ between runs (MDM2->CDKN1A changed between this run and the previous one). Pre-existing, not caused by the fix.

## Execution

Interpreter `F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (py3.12.13, requests 2.34.2, pandas 3.0.5, networkx 3.7), no installs or downloads. Live services (STRING, UniProt, SIGNOR, OmniPath, BioGRID) answered normally. The BioGRID key was loaded into the process only; a scan of all run output, scripts, report, record and handoff found no hit.

| Surface | Status | Evidence |
|---|---|---|
| STRING resolve, network (tiers, physical), pacing, caller_identity | executed | `evidence/string.txt` |
| UniProt accession, SIGNOR client (live and mocked answers) | executed | `evidence/signor.txt`, `evidence/probe_idm10_11.txt` |
| OmniPath interactions, commercial screen | executed | `evidence/omni.txt` |
| BioGRID LT physical, key-leak retest | executed | `evidence/biogrid.txt` |
| aggregate_networks, summary, multi_source_edges (live and mocked) | executed | `evidence/agg.txt`, `evidence/probe_idm10_11.txt` |
| examples/string_network.py, examples/interaction_query.py | executed, exit 0 | `evidence/ex_*.txt`, `evidence/aggregated_interactions.csv` |
| Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients | static-only: no client or recipe ships | none |

## Per-input scores

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---:|---:|---:|---:|
| 1 STRING example | Canonical | 35 | 53 | 88 | 5/5 |
| 2 Directed aggregate example | Variant A | 34 | 51 | 85 | 5/5 |
| 3 BioGRID and key leak | Variant B | 36 | 54 | 90 | 5/5 |
| 4 SIGNOR TP53 / AKT1 | Edge | 35 | 53 | 88 | 5/5 |
| 5 OmniPath commercial screen | Stress | 34 | 51 | 85 | 5/5 |
| 6 aggregate_networks / summary | Stress | 33 | 50 | 83 | 5/5 |
| 7 STRING physical claim | Variant A | 36 | 54 | 90 | 5/5 |

Inputs 3, 5 and 7 are carried from the previous run: their code paths (`_get`, BioGRID, OmniPath, STRING) are unchanged and the probes were rerun and passed on the new bytes anyway. Rerun: `Scripts\python.exe reaudit-run-2\scripts\reaudit_idm.py <signor|omni|string|biogrid|agg>` and `probe_idm10_11.py`.
