> **Audit record for `bio-uniprot-access`**
> - Audited working candidate `7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/uniprot-access), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-uniprot-access

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 28 | 40 | 68 | 3/5 | ⚠️ COMPLETED |
| 2 | Variant A | 18 | 20 | 38 | 2/4 | ❌ PARTIAL |
| 3 | Variant B | 28 | 42 | 70 | 3/4 | ❌ PARTIAL |
| 4 | Edge | 20 | 26 | 46 | 1/4 | ❌ PARTIAL |
| 5 | Stress | 24 | 34 | 58 | 2/5 | ❌ PARTIAL |

**Execution average:** 56.0 / 100  
**Assertion pass rate:** 11 / 22  
**Static score:** 68 / 100  
**Final score:** 61 / 100 — ⚠️ Beta Only  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: shared `database-access-venv` (py3.12.13, requests 2.34.2, pandas 3.0.5) from `F:\OpenScience\audit-envs\database-access\`; live UniProt release 2026_03 on 2026-10-03; sequential small queries; no installs. Candidate path read-only, no `__pycache__`.

| Surface | Class | Evidence |
|---|---|---|
| fetch_entry_json (reviewed, TrEMBL, secondary, inactive accession) | executed | `evidence/core.txt`, `evidence/claims.txt` |
| search_tsv, stream_tsv, cursor paging | executed | `evidence/core.txt`, `evidence/claims.txt` |
| map_ids, resolve_obsolete (versus idmapping/stream) | executed | `evidence/core.txt`, `evidence/claims3.txt` |
| list_isoforms, fetch_isoform_fasta (all 9 P04637 isoforms), xref_summary | executed | `evidence/core.txt` |
| uniref_cluster | executed | `evidence/core.txt` |
| download_proteome | failed (HTTP 400); replacement stream route executed (first bytes only) | `evidence/core.txt` |
| shipped examples | executed: uniprot_query.py exit 0 (with truncations), isoforms_and_xrefs.py exit 1 | `evidence/examples.txt` |
| documented query syntax, fields table, endpoint table, suffixes | executed (probes) | `evidence/claims.txt`, `evidence/claims2.txt` |
| Full human reference proteome download (about 20 MB) | static-only | not staged; E. coli proteome stream verified by first bytes |

Normalizer leads: T1 (map_ids first page) confirmed as UNI-001; T2 (proteome route) confirmed as UNI-002; T3 (example TypeError) confirmed as UNI-003; uniref_cluster entryType mislabel confirmed in UNI-007. No restricted-access items.

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated identifiers or values; P04637 393 aa, 311 PDB, 9 isoforms and 20431 human Swiss-Prot rows matched independent service totals.
  - practice_boundaries: PASS — Sequence and annotation retrieval only.
  - methodological_ground: PASS — Silent first-page truncation in map_ids and the quickstart search is a data-completeness defect filed as UNI-001 and UNI-005; the Skill itself warns about the 500-record cap and stream vs search.
  - code_usability: PASS — Every client function ran; failures are a rejected proteome route (UNI-002), a list formatted as text in one example (UNI-003) and a missing inactive-entry guard (UNI-006), scored in Layers 1-2 and filed P1/P2.

## Static categories

- functional_suitability: 7/12 — Entry, search, stream, isoform and xref functions correct live; map_ids drops mappings, download_proteome route is rejected, uniref_cluster mislabels fields, and two documented query/field names do not work.
- reliability: 6/12 — No request timeouts or 429 handling; map_ids truncates silently with no failedIds signal; an inactive accession raises KeyError; stream_tsv buffers the whole response.
- performance_context: 6/8 — SKILL.md about 200 lines with large reference tables that duplicate UniProt's own docs.
- agent_usability: 11/16 — Good stream-vs-search, async-mapping and fields guidance; the quickstart ID-mapping and kinase examples print truncated results as complete.
- human_usability: 6/8 — Clear tables; the Combine query example silently returns 0 hits and one documented field name is rejected with HTTP 400.
- security: 10/12 — No credentials; HTTPS only; accessions interpolated into URL paths without validation (low risk).
- maintainability: 8/12 — One 140-line client with docstrings; no tests, so truncation and the dead proteome route shipped.
- agent_specific: 14/20 — Specific trigger description and escape hatches; one example crashes and another presents capped output as totals.

## Detailed outputs

### Input 1 — Canonical: Entry parse, bulk search and stream (uniprot_query.py first three sections)

**Status:** COMPLETED — Entry and stream are exact (stream 20431 rows equals server total); the kinase search returns 500 of 640 matches and the example prints '500 reviewed human kinases' as if complete.  
**Scores:** Basic 28/40 | Specialized 40/60 | Total 68/100

**Assertions:**

- PASS — fetch_entry_json('P04637') returns TP53, 393 aa, reviewed, 311 PDB, AlphaFold P04637 (Exact; pdb_count matches the xref_pdb TSV field (311).)
- PASS — stream_tsv returns every human Swiss-Prot entry without duplicates (20431 rows equal X-Total-Results; no duplicate accessions; P04637 present.)
- PASS — Secondary and unreviewed accessions parse correctly (Q15086 resolves to P04637; a TrEMBL entry yields reviewed=False and a protein name.)
- FAIL — The shipped kinase search reports the full match set (500 rows versus 640 server total; nothing in the output flags the cap.)
- FAIL — Documented keyword:"Kinase" and keyword:KW-0418 are equivalent (640 versus 625 matches for the same human reviewed filter.)

### Input 2 — Variant A: Async Ensembl-to-UniProtKB ID mapping (map_ids, uniprot_query.py last section)

**Status:** PARTIAL — Job runs and polls correctly but only the first results page is read: 25 of 44 rows; BRCA2 (ENSG00000139618) is absent with no failedIds entry and PTEN has 7 of 12 rows.  
**Scores:** Basic 18/40 | Specialized 20/60 | Total 38/100

**Assertions:**

- PASS — Submit, poll and fetch complete for three Ensembl gene IDs (Job finished; invalid from_db raises HTTP 400.)
- FAIL — All mapped rows for every input ID are returned (Client 25 rows versus 44 from idmapping/stream; X-Total-Results 44 and a Link next header were ignored.)
- FAIL — A dropped input is reported, not silent (BRCA2 has zero rows and failedIds is empty; the example prints no NOT MAPPED line.)
- PASS — Reviewed-only mapping is reachable (to_db='UniProtKB-Swiss-Prot' returns P04637, P60484, P51587 within one page.)

### Input 3 — Variant B: Isoforms, FASTA and cross-reference summary (isoforms_and_xrefs.py)

**Status:** PARTIAL — Library calls are correct (9 isoforms, one canonical, FASTA lengths 393/341/346/354/302/307/261/209/214, 104 databases, PDB 311); the shipped example exits 1 with TypeError formatting a list.  
**Scores:** Basic 28/40 | Specialized 42/60 | Total 70/100

**Assertions:**

- PASS — list_isoforms('P04637') returns nine isoforms with exactly one canonical (P04637-1 canonical.)
- PASS — fetch_isoform_fasta returns sequences for every isoform (Nine FASTA records; P04637-2 is 341 aa.)
- PASS — xref_summary agrees with the xref_pdb field (PDB 311 both ways; Ensembl 22.)
- FAIL — The shipped example runs to completion (TypeError: unsupported format string passed to list.__format__ at the isoform print.)

### Input 4 — Edge: Proteome download, UniRef cluster, inactive and secondary accessions

**Status:** PARTIAL — download_proteome returns HTTP 400 on the documented route (stream route works, gzip magic 1f8b); uniref_cluster labels entryType as identity and returns an entry name; a deleted accession raises KeyError.  
**Scores:** Basic 20/40 | Specialized 26/60 | Total 46/100

**Assertions:**

- FAIL — download_proteome('UP000000625') downloads the proteome (HTTP 400 'upid value has invalid format'.)
- FAIL — uniref_cluster returns a representative accession and a cluster identity (representative is P53_HUMAN (entry name); identity is the string 'UniRef50' from entryType; JSON has no identity field.)
- FAIL — An inactive accession fails with a clear error (HTTP 200 'Inactive' record raises KeyError: 'sequence'.)
- PASS — resolve_obsolete maps a secondary accession to the current primary (Q15086 -> P04637, P04637 -> P04637.)

### Input 5 — Stress: Documented query syntax, field names, endpoint table, cursor paging

**Status:** PARTIAL — Most routes, suffixes and queries work and cursor paging returns 500 + 125 = 625 rows; xref:pdb silently returns 0 hits and ft_active_site is rejected.  
**Scores:** Basic 24/40 | Specialized 34/60 | Total 58/100

**Assertions:**

- PASS — Documented endpoints and .json/.fasta/.tsv/.xml/.txt/.gff suffixes respond (All 200 including /uniprotkb/accessions, /uniref/search, /proteomes/{upid}, /taxonomy/{id}.)
- PASS — Cursor paging returns the remainder of a 625-hit result (Second page 125 rows via the Link header.)
- FAIL — The documented Combine query returns hits (keyword:KW-0067 AND xref:pdb returns 0; database:pdb returns 904 for the same filter.)
- FAIL — Every documented fields name is accepted (ft_active_site gives HTTP 400; the valid name is ft_act_site.)
- FAIL — Stated corpus sizes are current (TrEMBL is described as about 250M; live release 2026_03 reports 149.4M (Swiss-Prot 575,748).)

## Key strengths

- Entry, stream, isoform and cross-reference functions return exact values verified two ways: P04637 393 aa, 311 PDB, 9 isoforms with FASTA lengths, human Swiss-Prot stream 20431 rows equal to the server total.
- Stream-vs-search, async mapping with a hard timeout, isoform suffix handling and secondary-accession resolution are accurate and verified live.
- Most documented endpoints, suffixes and query operators work, and cursor paging reproduces the full 625-hit result.

## Recommendations

- **[P1] UNI-001 map_ids reads only the first results page** (inputs [2]): Ensembl-to-UniProtKB mapping returned 25 of 44 rows; BRCA2 vanished with empty failedIds and PTEN lost 5 rows; the quickstart and example print the partial list as complete. Ensembl-to-UniProtKB also returns many TrEMBL fragments (18 rows for TP53). Fix: Fetch /idmapping/stream/{jobId} (or follow Link), report inputs with no rows, and document to_db='UniProtKB-Swiss-Prot' for reviewed-only mapping; add a regression on the three example genes.
- **[P1] UNI-002 download_proteome documented route returns 400** (inputs [4]): /proteomes/{upid}.fasta.gz is rejected for UP000000625 and the endpoint table and client both use it. Fix: Use /uniprotkb/stream?query=proteome:{upid}&format=fasta&compressed=true (200, gzip verified) and correct the endpoint table.
- **[P1] UNI-003 isoforms_and_xrefs.py raises TypeError** (inputs [3]): The example formats iso['ids'] (a list) with a width specifier and exits at the first isoform line, before the FASTA, xref and proteome sections. Fix: Join the ids (', '.join(iso['ids'])) and rerun the whole example.
- **[P1] UNI-004 xref:pdb and ft_active_site documented but broken** (inputs [5]): The query table and the Combine example use xref:pdb, which silently returns 0 hits (database:pdb returns 904), and the fields table lists ft_active_site, which the service rejects with HTTP 400. Fix: Replace xref:pdb with database:pdb (or structure_3d:true) and ft_active_site with ft_act_site.
- **[P2] UNI-005 Capped results and stale counts shown as totals** (inputs [1, 5]): The kinase example prints 500 as the number of reviewed human kinases (server total 640), keyword:"Kinase" differs from keyword:KW-0418 (640 vs 625), and TrEMBL is stated as about 250M (live 149.4M). Fix: Warn when rows equal the cap (or return the total), use KW-0418 in the example, and update the corpus sizes.
- **[P2] UNI-006 Inactive accession raises KeyError** (inputs [4]): A deleted accession returns HTTP 200 with entryType Inactive and no sequence, so fetch_entry_json raises KeyError; SKILL.md says obsolete accessions return 404 or 301. Fix: Detect entryType == 'Inactive', raise a clear error naming inactiveReason, and correct the failure-mode text (secondary accessions redirect and resolve).
- **[P2] UNI-007 uniref_cluster mislabels identity and representative** (inputs [4]): identity is the entryType string 'UniRef50' (there is no identity field) and representative is the entry name P53_HUMAN, not an accession. Fix: Return identity as the numeric tier parsed from the id and the first representativeMember accession (P04637) alongside the member id.
- **[P2] UNI-008 No timeouts, retries or 429 handling in the client** (inputs []): Every request lacks a timeout and Retry-After handling; stream_tsv buffers the full response in memory, and map_ids treats any non-RUNNING status as finished. Fix: Add one helper with timeout and Retry-After, check FAILED job status, and stream large responses to disk.
- **[P2] UNI-009 No Skill-root LICENSE file** (inputs []): Preflight warns that the manifest cites repository license evidence only; frontmatter says MIT. Fix: Cite the upstream MIT licence evidence in provenance or add a LICENSE file.

## Ordered finding ledger

Audited identity: `7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | UNI-001 | P1 | open | [2] | map_ids reads only the first results page. Fetch /idmapping/stream/{jobId} (or follow Link), report inputs with no rows, and document to_db='UniProtKB-Swiss-Prot' for reviewed-only mapping; add a regression on the three example genes. |
| 2 | UNI-002 | P1 | open | [4] | download_proteome documented route returns 400. Use /uniprotkb/stream?query=proteome:{upid}&format=fasta&compressed=true (200, gzip verified) and correct the endpoint table. |
| 3 | UNI-003 | P1 | open | [3] | isoforms_and_xrefs.py raises TypeError. Join the ids (', '.join(iso['ids'])) and rerun the whole example. |
| 4 | UNI-004 | P1 | open | [5] | xref:pdb and ft_active_site documented but broken. Replace xref:pdb with database:pdb (or structure_3d:true) and ft_active_site with ft_act_site. |
| 5 | UNI-005 | P2 | open | [1, 5] | Capped results and stale counts shown as totals. Warn when rows equal the cap (or return the total), use KW-0418 in the example, and update the corpus sizes. |
| 6 | UNI-006 | P2 | open | [4] | Inactive accession raises KeyError. Detect entryType == 'Inactive', raise a clear error naming inactiveReason, and correct the failure-mode text (secondary accessions redirect and resolve). |
| 7 | UNI-007 | P2 | open | [4] | uniref_cluster mislabels identity and representative. Return identity as the numeric tier parsed from the id and the first representativeMember accession (P04637) alongside the member id. |
| 8 | UNI-008 | P2 | open | [] | No timeouts, retries or 429 handling in the client. Add one helper with timeout and Retry-After, check FAILED job status, and stream large responses to disk. |
| 9 | UNI-009 | P2 | open | [] | No Skill-root LICENSE file. Cite the upstream MIT licence evidence in provenance or add a LICENSE file. |

No audit-local repair was made; no Skill bytes changed.
