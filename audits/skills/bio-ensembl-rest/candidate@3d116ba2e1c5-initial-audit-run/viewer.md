> **Audit record for `bio-ensembl-rest`**
> - Audited working candidate `3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ensembl-rest), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-02 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-ensembl-rest

Generated: 2026-10-02  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 24 | 36 | 60 | 3/5 | ❌ PARTIAL |
| 2 | Variant A | 26 | 40 | 66 | 3/5 | ❌ PARTIAL |
| 3 | Variant B | 32 | 46 | 78 | 3/4 | ✅ COMPLETED |
| 4 | Edge | 30 | 44 | 74 | 3/4 | ⚠️ COMPLETED |
| 5 | Stress | 24 | 36 | 60 | 3/5 | ❌ PARTIAL |

**Execution average:** 67.6 / 100  
**Assertion pass rate:** 15 / 23  
**Static score:** 74 / 100  
**Final score:** 70 / 100 — ⚠️ Beta Only  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: shared `database-access-venv` (py3.12.13, requests 2.34.2) from `F:\OpenScience\audit-envs\database-access\`; live Ensembl REST release 116 on 2026-10-02; sequential small queries; no installs. Candidate path was read-only and no `__pycache__` was created.

| Surface | Class | Evidence |
|---|---|---|
| symbol_to_id, gene_info, sequence_for_id (ENSP/ENST), genes_in_region | executed | `evidence/core.txt` (`scripts/run_core.py`) |
| vep_region, vep_id, vep_hgvs | executed | `evidence/core.txt`, `evidence/example_vep_annotation.txt` |
| orthologs / paralogs, ld_pairwise, batch_symbols | executed | `evidence/core.txt`, `evidence/example_compara_homology.txt` |
| archive e110, e111, GRCh37 | executed | `evidence/core.txt`, `evidence/claims.txt` |
| archive e116, e90 | failed | e116 503 (jun2026 host); e90 HTML 200; `evidence/claims.txt`, `evidence/claims2.txt` |
| shipped examples (3) | executed | compara exit 0; lookup_and_overlap and vep_annotation exit 1 (`evidence/example_exit.txt`) |
| divisions, POST /lookup/id, doc endpoint table | executed (probes) | `evidence/claims.txt`, `evidence/regulatory.txt` |
| local VEP, BioMart bulk (referred-to routes) | static-only | not part of this Skill; out of scope per TOOLS.md |

Normalizer leads: N1 confirmed in part (e116 archive 503; e110/e111 reproducible), T1 confirmed (ENS-001), T2 confirmed (ENS-002). No restricted-access items.

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated identifiers or results; every live value (BRCA1 ENSG00000012048 chr17:43044292-43170245, TP53 protein 393 aa, rs699 missense, LD r2 0.976) matched the service.
  - practice_boundaries: PASS — Annotation retrieval only; no diagnostic or prescriptive output.
  - methodological_ground: PASS — Symbol-to-ID resolution and release pinning are sound. A GRCh37 coordinate shown against the GRCh38 default host is a documentation error (ENS-003), not a methodological fallacy.
  - code_usability: PASS — Client functions all ran live; the shipped failures are wrong arguments in two examples and the quickstart snippet (ENS-001, ENS-002), not unrunnable client code. Scored in Layer 1/2 and filed P1.

## Static categories

- functional_suitability: 8/12 — Client covers lookup, sequence, overlap, VEP, Compara, LD and archive base; the headline gene-ID protein snippet, one example HGVS, the usage-guide VEP coordinate, and two endpoint-table rows (regulatory, homology/id) fail live.
- reliability: 8/12 — 429 handling exists; no request timeout, no 5xx handling, archive HTML/503 surface as JSONDecodeError or an HTML body, and exhausted 429 retries raise RuntimeError that batch_symbols does not catch.
- performance_context: 6/8 — SKILL.md is about 170 lines with a usage guide and examples; endpoint table and error table repeat each other.
- agent_usability: 11/16 — Good symbol-vs-ID, pinning and bulk-defection guidance; the first code block an agent copies crashes with an opaque HTTP 400 and the client discards the server error body.
- human_usability: 6/8 — Clear tables and failure modes; several stated error behaviours (404 on renamed symbol, Homo_sapiens fails) are not what the service returns.
- security: 11/12 — No credentials; HTTPS only; path segments are interpolated unescaped into URLs (low risk for an unauthenticated read-only API).
- maintainability: 9/12 — Single 90-line client with one retry helper and docstrings; examples are not asserted or tested, which is how ENS-001 and ENS-002 shipped.
- agent_specific: 15/20 — Trigger description is specific; progressive disclosure and escape hatches (BioMart, local VEP) good; examples that fail reduce composability.

## Detailed outputs

### Input 1 — Canonical: Symbol to ID, e110 pinning, gene structure, protein, region overlap (lookup_and_overlap.py)

**Status:** PARTIAL — Steps 1-3 correct; exit 1 at protein step with HTTP 400 on the gene ID; region overlap step never reached.  
**Scores:** Basic 24/40 | Specialized 36/60 | Total 60/100

**Assertions:**

- PASS — symbol_to_id('human','BRCA1') returns ENSG00000012048 on GRCh38 at chr17:43044292-43170245, strand -1 (Exact match against the live record.)
- PASS — e110 archive returns the same Gene ID with the e110 coordinates (301 to jul2023 host followed; id ENSG00000012048, start 43044295.)
- PASS — gene_info(expand=1) returns transcripts with exon lists and one canonical transcript (59 transcripts, canonical ENST00000357654.)
- FAIL — The documented quickstart sequence_for_id('ENSG00000139618','protein') returns a protein sequence (HTTP 400: gene plus non-genomic type needs multiple_sequences (15 sequences); same call exits the shipped example.)
- FAIL — The shipped example runs to completion and prints the region overlap section (Exit 1 before the overlap section.)

### Input 2 — Variant A: VEP by region, dbSNP ID, HGVS with consequence summary (vep_annotation.py)

**Status:** PARTIAL — Region and ID VEP correct; example HGVS ENST00000366667:c.803G>A rejected (reference base at c.803 is C); usage-guide region example on GRCh38 host returns 400.  
**Scores:** Basic 26/40 | Specialized 40/60 | Total 66/100

**Assertions:**

- PASS — vep_region 17:43044295-43044295:1 A returns GRCh38 consequences for BRCA1 with allele_string T/A (3_prime_UTR_variant, 48 transcript consequences.)
- PASS — vep_id rs699 returns a missense AGT consequence with SIFT and PolyPhen (ENST00000366667 M/T, tolerated, benign, position 230710048.)
- PASS — vep_hgvs ENST00000646891:c.1799T>A returns BRAF V600E missense with SIFT and PolyPhen (V/E, probably_damaging.)
- FAIL — The shipped HGVS example string is valid for its transcript (Service reports reference C at c.803; c.803C>T works (missense_variant).)
- FAIL — The usage-guide chr17:41276135 T>G example returns a result on the default host (That coordinate is GRCh37 BRCA1; default GRCh38 host returns 400, grch37 host returns splice_region_variant.)

### Input 3 — Variant B: Compara orthologs and paralogs (compara_homology.py)

**Status:** COMPLETED — Example exits 0; ortholog types and mouse mapping correct; BRCA1 paralog section prints nothing; confidence absent.  
**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100

**Assertions:**

- PASS — TP53 to mouse returns one ortholog_one2one to ENSMUSG00000059552 with identities (perc_id 77.95 target, 77.35 source.)
- PASS — BRCA1 ortholog type counts are internally consistent (170 one2one + 29 one2many = 199 homologies.)
- PASS — Missing confidence is treated as unknown, per SKILL.md (Value is None for every row and the example prints it without failing.)
- FAIL — The example's paralog and confidence text matches service output (Paralog list for BRCA1 is empty and prints a bare header; text describes confidence as binary 0/1 and a many2one type that the service does not emit.)

### Input 4 — Edge: Release pinning: e110, e111, e116, GRCh37, and a retired archive

**Status:** COMPLETED — e110, e111 and GRCh37 reproducible; e116 archive host 503; e90 returns HTML 200 and the client raises JSONDecodeError.  
**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100

**Assertions:**

- PASS — e110 archive resolves BRCA1 with the e110 coordinates (start 43044295 vs live 43044292, same Gene ID.)
- PASS — GRCh37 host returns the legacy assembly coordinates (41196312-41277500, assembly GRCh37.)
- PASS — e111 archive answers /info/data with release 111 ({'releases': [111]}.)
- FAIL — A very old or unavailable archive fails with a clear, documented error (e116 returns 503 HTML (jun2026 host down, not decommissioned); e90 returns 200 HTML contradicting the doc (DNS failure or 503) and the client raises JSONDecodeError.)

### Input 5 — Stress: Batch symbols with renamed gene, LD, POST batch lookup, divisions, documented endpoint table

**Status:** PARTIAL — Batch, LD, POST lookup and divisions correct; regulatory and homology/id endpoint-table rows 404; stated error codes and species-case rule do not match the service.  
**Scores:** Basic 24/40 | Specialized 36/60 | Total 60/100

**Assertions:**

- PASS — batch_symbols captures per-symbol errors and still resolves valid symbols (BRCA1 resolved; MARCH1 and NOTAGENE recorded as errors.)
- PASS — ld_pairwise and POST /lookup/id return expected values (r2 0.976 D' 1.0; POST returned BRCA1 and TP53.)
- PASS — Non-vertebrate lookup by division species name works on the main host (arabidopsis_thaliana NAC001 200; rest.ensemblgenomes.org does not resolve.)
- FAIL — Endpoint table rows resolve: /regulatory/species/{species}/feature/{id} and /homology/id/{ensembl_id} (Both 404 (homology needs /homology/id/human/ID).)
- FAIL — Documented error behaviour matches service: renamed symbol is 404 and Homo_sapiens fails (Renamed symbol returns 400; Homo_sapiens returns 200.)

## Key strengths

- Compact single client whose functions all returned scientifically correct live values (BRCA1 coordinates, TP53 protein, rs699 and BRAF V600E missense, LD r2 0.976, one2one TP53 orthology).
- Release pinning and symbol-to-ID stability guidance is correct and reproducible: e110, e111 and GRCh37 hosts returned the stated gene versions.
- Divisions, rate-limit and defection guidance verified live: main host serves plants, rest.ensemblgenomes.org does not resolve, rate headers show 55000 per 3600 s.

## Recommendations

- **[P1] ENS-001 Gene-ID protein quickstart returns HTTP 400** (inputs [1]): sequence_for_id('ENSG00000139618','protein') in SKILL.md and lookup_and_overlap.py fails because a gene ID with a non-genomic type needs multiple_sequences; the example exits before its region step. Fix: Use a transcript or protein ID in the snippet and example (ENSP00000269305), or add a multiple_sequences option and document it.
- **[P1] ENS-002 VEP HGVS example has wrong reference base** (inputs [2]): ENST00000366667:c.803G>A returns HTTP 400 because the reference base at c.803 is C; the example exits before the bulk-warning text. Fix: Use ENST00000366667:c.803C>T (rs699, missense) or the validated BRAF ENST00000646891:c.1799T>A.
- **[P1] ENS-003 GRCh37 VEP coordinate sent to GRCh38 host** (inputs [2]): 17:41276135 T>G is BRCA1 in GRCh37; the guide sends it to the default GRCh38 host and gets HTTP 400. Fix: Use a GRCh38 coordinate such as 17:43044295-43044295:1/A, or point the example at the grch37 host.
- **[P1] ENS-004 Regulatory and homology/id endpoint rows 404** (inputs [5]): /regulatory/species/{species}/feature/{id} returned 404 (also for real ENSR17_ ids, and the variants tried), and /homology/id/{ensembl_id} returns 404 without the species segment. Fix: Correct homology to /homology/id/{species}/{id}; replace the regulatory row with the working overlap/region?feature=regulatory route (34 features returned for 17:43.0-43.2 Mb) or verify a current id route.
- **[P2] ENS-005 Error-code and species-case claims are wrong** (inputs [5]): Renamed or unknown symbols return HTTP 400 (not 404), and Homo_sapiens is accepted (200), contradicting the doc. Fix: Say 400 'No valid lookup found' and drop or soften the Homo_sapiens-fails claim.
- **[P2] ENS-006 Client: no timeout, 5xx or non-JSON handling** (inputs [4]): get_with_retry has no request timeout (a 40 s read timeout occurred on xrefs), does not retry 5xx, returns HTML 503 or e90 HTML 200 pages that raise JSONDecodeError, and exhausted 429 retries raise RuntimeError that batch_symbols does not catch. e116 archive was 503 while the live host was fine. Fix: Add a timeout, retry transient 5xx, check Content-Type before .json(), catch RuntimeError in batch_symbols, and document that a recent archive host can be temporarily down.
- **[P2] ENS-007 compara example: empty paralogs, stale text** (inputs [3]): The BRCA1 paralog section prints a header with nothing under it, and the closing text calls confidence binary 0/1 and names a many2one type that the service does not return while confidence is absent for every row. Fix: Print 'none' for empty results and align the semantics text with SKILL.md (confidence may be absent) and with the types returned.
- **[P2] ENS-008 No Skill-root LICENSE file** (inputs []): Preflight warns that the manifest cites the repository licence only; SKILL.md frontmatter says MIT. Fix: Cite the upstream MIT licence evidence in provenance or add a LICENSE file.

## Ordered finding ledger

Audited identity: `3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | ENS-001 | P1 | open | [1] | Gene-ID protein quickstart returns HTTP 400. Use a transcript or protein ID in the snippet and example (ENSP00000269305), or add a multiple_sequences option and document it. |
| 2 | ENS-002 | P1 | open | [2] | VEP HGVS example has wrong reference base. Use ENST00000366667:c.803C>T (rs699, missense) or the validated BRAF ENST00000646891:c.1799T>A. |
| 3 | ENS-003 | P1 | open | [2] | GRCh37 VEP coordinate sent to GRCh38 host. Use a GRCh38 coordinate such as 17:43044295-43044295:1/A, or point the example at the grch37 host. |
| 4 | ENS-004 | P1 | open | [5] | Regulatory and homology/id endpoint rows 404. Correct homology to /homology/id/{species}/{id}; replace the regulatory row with the working overlap/region?feature=regulatory route (34 features returned for 17:43.0-43.2 Mb) or verify a current id route. |
| 5 | ENS-005 | P2 | open | [5] | Error-code and species-case claims are wrong. Say 400 'No valid lookup found' and drop or soften the Homo_sapiens-fails claim. |
| 6 | ENS-006 | P2 | open | [4] | Client: no timeout, 5xx or non-JSON handling. Add a timeout, retry transient 5xx, check Content-Type before .json(), catch RuntimeError in batch_symbols, and document that a recent archive host can be temporarily down. |
| 7 | ENS-007 | P2 | open | [3] | compara example: empty paralogs, stale text. Print 'none' for empty results and align the semantics text with SKILL.md (confidence may be absent) and with the types returned. |
| 8 | ENS-008 | P2 | open | [] | No Skill-root LICENSE file. Cite the upstream MIT licence evidence in provenance or add a LICENSE file. |

No audit-local repair was made; no Skill bytes changed.
