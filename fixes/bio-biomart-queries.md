# bio-biomart-queries — fixes (2026-09-17)

Branch `fix/db-biomart`, worktree `F:\OpenScience\wt\db-biomart`, staging base
`581dcd89a7450785c2451a0543ee822049fbf934`. Verified live 2026-09-17 against public Ensembl BioMart
(release 116) with the shared venv's pybiomart 0.2.0 (`F:\OpenScience\audit-envs\database-access\Scripts\python.exe`).
Every changed Python snippet (SKILL.md inline and `examples/`) was run to completion and its output
checked against known biology (real HGNC IDs, real chr17/chr21 loci, real one2one ortholog pairs), not
just exit code. R (`biomaRt`) could not complete a live round trip in this session (3 attempts, 2
release-pin variants) — same live-mirror unavailability the tooling pass already documented in
`TOOLS.md`; the R fix was checked by schema equivalence + docs instead (noted below).

**Judgement call (per FIX_BRIEF "Missing referenced executables" / method-level-change allowance):**
pybiomart 0.2.0's `Dataset.filters` never recurses into `id_list`-type filter collections, so
`ensembl_gene_id`, `external_gene_name` and `entrezgene_id` are real, valid, server-side filters that
`ds.query(filters={...})` can never accept — confirmed 3 independent ways by the auditor (discovery
dump, raw-XML control, live source inspection of `dataset.py`) and reconfirmed here by reading
`Dataset.query()`'s source directly. There is no correct filter *name* to substitute (the brief's
first option) — the client-side validation itself is broken, so no name will ever pass it. I switched
the documented route for every ID-list-filtered pattern to `ds.get(query=<hand-built XML>)`, which
is pybiomart's own lower-level method and bypasses only the broken validation, not the client
entirely (the brief's second option: "switch to ... the raw-XML/REST form the auditor's control
proved works" — here reached through pybiomart itself rather than bare `requests`, keeping
`primary_tool: pybiomart` honest). This also fixes the separate P1 (outage page silently parsed as
data) in one helper, since the raw body is available to check before parsing. Checked on pybiomart
0.2.0, Ensembl release 116, 2026-09-17.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Flagship "Bulk ID mapping" pattern + `examples/bulk_id_mapping.py` raise `BiomartException` on `filters={'ensembl_gene_id': ...}` before any network call | P0 | Added `query_raw()` helper (builds the XML `ds.query()` builds internally, sends via `ds.get()`) in SKILL.md "Querying with ID-list filters" and in both affected `examples/*.py`; Bulk ID mapping pattern and example rewritten to use it | ran: `examples/bulk_id_mapping.py` end-to-end, exit 0, 54 rows for BRCA2/TP53/PTEN/EGFR/MYC; collapsed table shows real HGNC IDs (TP53=HGNC:11998, BRCA2=HGNC:1101, EGFR=HGNC:3236, PTEN=HGNC:9588, MYC=HGNC:7553) and real RefSeq/UniProt accessions | see judgement call above |
| GO-annotation pattern fails the same way on `filters={'external_gene_name': [...]}` | P0 (same root cause, `observed_in: [1,4,5]`) | GO term annotation pattern in SKILL.md switched to `query_raw()` | ran (scratch copy of the pattern): 380 rows for TP53/BRCA1/MYC/EGFR, all 4 gene names present in output | |
| SKILL.md pins "pybiomart 0.9+"; no such release exists (only 0.1, 0.2.0 on PyPI) | P0 | "Version Compatibility" corrected to pybiomart 0.2.0 (checked 2026-09-17), R biomaRt 2.62.1, Ensembl release 116; added a paragraph naming the `Dataset.filters` id_list gap as the reason; both `examples/*.py` reference comments updated from "0.9+" to "0.2.0" | `pip show pybiomart` -> 0.2.0 (shared venv) | grep for "0.9+" across SKILL.md/usage-guide.md/examples/ after the edit: 0 hits |
| Coordinate-table pattern lists attribute `biotype`; real attribute is `gene_biotype` | P1 | SKILL.md inline pattern, "Common attribute selectors" table, and `examples/coordinate_table.sh` (R `getBM`) all changed `biotype` -> `gene_biotype` in the attributes list (filter usage of `biotype` unchanged, it's correct there) | Python: ran live, 1187 real protein-coding genes on chr17 with correct column `Gene type`. R: could not complete a live round trip (3 attempts: `useEnsembl(version=110)` and unpinned, all timed out reaching `jul2023.archive.ensembl.org` / mirror selection — same R-specific live-availability issue `TOOLS.md` already recorded); verified instead by schema equivalence (same `hsapiens_gene_ensembl` dataset, same underlying Ensembl BioMart schema Python confirmed live) and standard biomaRt attribute-naming convention | |
| No validation of BioMart's response before use; outage page (HTML, HTTP 200) silently parsed, `examples/ortholog_table.py` then crashes with opaque `StopIteration` | P1 | `query_raw()` checks the raw response body for `'Query ERROR'` and for an HTML/empty payload before parsing, raising a clear `RuntimeError` instead; applied to all 4 rewritten patterns (bulk ID mapping, coordinate table, ortholog table, GO annotation) and both example scripts; documented as a 7th failure mode ("Outage page silently parsed as data") plus two new rows in Common errors | ran: `examples/ortholog_table.py` end-to-end, exit 0, 4298 chr17 rows, 532 real 1:1 orthologs across mouse+zebrafish (e.g. DOC2B, VPS53, TIMM22, YWHAE, CRK — real chr17 genes) | |
| `examples/bulk_id_mapping.py` adds `entrezgene_id` (6th attribute), breaking live with "Too many attributes selected for External References" even after the filter fix | P2 | Dropped `entrezgene_id` from the example's attribute list to match SKILL.md's own 5-attribute inline pattern | ran (part of the same bulk_id_mapping.py run above): no "too many attributes" error, 5 attributes returned cleanly | |
| (found during verification, not in the audit) `examples/bulk_id_mapping.py`'s groupby-collapse step crashes with `TypeError: sequence item 2: expected str instance, float found` | not in report; fixed as a shipped-example defect per FIX_BRIEF | `filter(None, x)` does not drop `NaN` (NaN is truthy in Python), so the join over RefSeq/UniProt columns hit a float; replaced with an explicit `pd.notna()` filter | ran: same bulk_id_mapping.py end-to-end run above, "Collapse to one row per gene" section now completes and prints correctly for all 5 genes | only surfaced now that the P0 filter fix lets the script reach this line; the auditor's run never got this far |

**Redundancy pass (usage-guide.md):** deleted "What the Agent Will Do" (8 numbered points) and "Tips"
(8 bullets) in full — every point restated something already in SKILL.md (decision matrix, discovery
pattern, failure modes: row-multiplication, HGNC renames, version pinning, SNP-vs-gene mart, REST vs
BioMart). Two Tips bullets had content not found elsewhere in SKILL.md and were moved rather than
deleted: "R biomaRt is more mature/Bioconductor-supported, prefer it for R pipelines" -> merged into
SKILL.md's tool listing bullet for `biomaRt`; "non-vertebrate species use the Ensembl Genomes BioMart
host" -> added as a new bullet in the same tool listing (`Server(host='http://plants.ensembl.org')`).
Also trimmed usage-guide.md's "Prerequisites" `pip install` duplicate down to a pointer at SKILL.md's
existing "Installation" section. Kept Overview, Quick Start, Example Prompts, Related Skills (all
human-facing, not restated in SKILL.md). `SKILL.md` itself had no internal repetition to collapse.

Left unfixed: none of the audit's P0/P1/P2 findings. R-side live confirmation of the `gene_biotype`
attribute fix is the one item verified by schema-equivalence + docs rather than a completed live R
round trip, noted above and in the commit body — Ensembl BioMart's own live availability, not this
fix, is the blocker (already documented independently in `TOOLS.md`'s "Blocked or gated" section from
the tooling pass).

Needs Sam: nothing new. Live Ensembl BioMart remains intermittently unavailable to R's mirror-selection
logic specifically (Python succeeded every time against the same service, same session) — a pre-existing,
already-documented environment/service condition, not something this fix caused or can resolve.
