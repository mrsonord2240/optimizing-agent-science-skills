> **Audit record for `bio-biomart-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@581dcd8](https://github.com/mrsonord2240/bioSkills/tree/581dcd89a7450785c2451a0543ee822049fbf934/database-access/biomart-queries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-biomart-queries
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@581dcd89a7450785c2451a0543ee822049fbf934:database-access/biomart-queries`
Category: Data Analysis (3) | Execution Mode: D (Hybrid — runnable `examples/` scripts + SKILL.md
inline patterns an agent adapts) | Complexity: Moderate → N=5

All 5 inputs were **actually executed** against the shared venv
(`F:\OpenScience\audit-envs\database-access\Scripts\python.exe`, pybiomart 0.2.0) and, where the
high-level client failed, cross-checked against the live martservice XML endpoint directly via
`requests`. Every script run is saved under `run/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 14 | 25 | 39 | 2/4 PASS | ❌ |
| 2 | Variant A | 17 | 29 | 46 | 2/4 PASS | ❌ |
| 3 | Edge | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 4 | Variant B | 16 | 30 | 46 | 2/4 PASS | ❌ |
| 5 | Stress | 13 | 25 | 38 | 1/4 PASS | ❌ |

**Execution Average: 51.8 / 100**
**Assertion Pass Rate: 11/20 (55%)**

> Reviewer note: 3 of 5 inputs fail deterministically — not due to live Ensembl flakiness — because
> SKILL.md's own documented Python code patterns call `pybiomart`'s high-level
> `Dataset.query(filters={...})` with filter names (`ensembl_gene_id`, `external_gene_name`) that
> `pybiomart` 0.2.0 (the only real PyPI release; SKILL.md's claimed "0.9+" does not exist) never
> exposes as valid, because it does not recurse into nested `<Option>` filter definitions. This is
> the Skill's own flagship, most-advertised use case (bulk ID mapping) failing on its own canonical
> example, unmodified.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a list of Ensembl Gene IDs (BRCA2, TP53, PTEN, EGFR, MYC) and need HGNC symbol,
RefSeq mRNA, UniProt accession for each, in one BioMart query."

**What ran:** `run/bulk_id_mapping.py` — the Skill's own shipped `examples/bulk_id_mapping.py`,
copied verbatim (byte-identical) into the run folder, executed unmodified.

**Output (`run/input1_canonical_output.txt`):**
```
=== Bulk ID mapping: Ensembl Gene -> HGNC + RefSeq + UniProt ===
Traceback (most recent call last):
  File ".../pybiomart/dataset.py", line 254, in query
    filter_ = self.filters[name]
KeyError: 'ensembl_gene_id'
...
pybiomart.base.BiomartException: Unknown filter ensembl_gene_id, check dataset filters for a
list of valid filters.
```
**Scores:** Basic: 14/40 | Specialized: 25/60 | Total: 39/100
**Assertions:**
- [FAIL] Code executes without unhandled exceptions — `BiomartException` raised on the exact
  filter the Skill's flagship example uses.
- [FAIL] Output contains one row per (gene, cross-ref) pair as documented — zero rows produced.
- [PASS] No fabricated biological data in output — clean error, no silently-wrong data.
- [PASS] Error message clearly identifies the cause — names the exact unknown filter.

### Input 2 — Variant A
**Prompt:** "Pull all protein-coding genes on chromosome 21 with coordinates and biotype in one
BioMart query."

**What ran:** `run/input2_coordinate_table.py` — SKILL.md's inline "Pull gene coordinate table for
a chromosome" pattern, copied verbatim except chr17→chr21 (smaller/faster). Followed by
`run/input2b_coordinate_table_corrected.py`, the same query with `biotype`→`gene_biotype` in the
attribute list (filter usage of `biotype` is correct and unchanged).

**Output (`run/input2_output.txt`):**
```
pybiomart.base.BiomartException: Unknown attribute biotype, check dataset attributes for a
list of valid attributes.
```
**Output, corrected (`run/input2b_output.txt`):**
```
221 protein-coding genes on chr21
 Gene stable ID Gene name  Chromosome/scaffold name  Gene start (bp)  Gene end (bp)  Strand  Gene type
ENSG00000274391      TPTE                        21         10521553       10606140       1 protein_coding
ENSG00000166351     POTED                        21         13609777       13645823       1 protein_coding
...
```
(Full 221-row result archived at `data/input2_chr21_protein_coding_LIVE.tsv`.)

**Scores:** Basic: 17/40 | Specialized: 29/60 | Total: 46/100
**Assertions:**
- [FAIL] Code executes without unhandled exceptions — as literally documented, it does not.
- [FAIL] Attribute list matches real, queryable BioMart attribute names — `biotype` is a *filter*
  name, not an *attribute* name; the real attribute is `gene_biotype` (confirmed against a live
  attribute dump, see Input 3).
- [PASS] Corrected version returns real, plausible chr21 gene coordinates — 221 rows, real genes
  (TPTE, LIPI, CXADR, BTG3 are genuine chr21 loci).
- [PASS] No fabricated biological data.

### Input 3 — Edge
**Prompt:** "Before I trust the field names, list the real attributes and filters available on the
human gene dataset so I don't hallucinate field names."

**What ran:** `run/input3_discover.py` — SKILL.md's "Discover attributes / filters
programmatically" pattern, run verbatim, plus explicit membership checks for the exact names that
broke Inputs 1, 2 and 5.

**Output (`run/input3_output.txt`):**
```
2769 ortholog attributes; first 5: ['homologs_ensembl_gene_id', ...]
2 chromosome-related filters: ['chromosome_name', 'chromosomal_region']

Total filters enumerated by ds.filters: 45
Is 'ensembl_gene_id' in ds.filters? False
Is 'biotype' in ds.attributes (as an ATTRIBUTE, not filter)? False
Is 'gene_biotype' in ds.attributes? True
```
This is the diagnostic result that explains Inputs 1, 2 and 5: `ds.filters` only ever enumerates 45
top-level filters; `ensembl_gene_id` (and `external_gene_name`, confirmed separately in Input 5) is
a real, valid BioMart filter but is nested inside an `id_list` filter collection that pybiomart's
`Dataset.filters` never recurses into — so it can never appear as a key `ds.query()` will accept,
no matter how carefully you "discover before you guess," which is exactly what SKILL.md itself
recommends as the defensive pattern.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:**
- [PASS] `ds.attributes` / `ds.filters` execute without error.
- [PASS] Output correctly enumerates real attribute/filter counts (cross-checked against the
  cached live dump in `audit-envs/database-access/public-data/biomart-queries/`).
- [PASS] Confirms whether SKILL.md's own filter names are actually discoverable this way — and
  correctly shows they are not, root-causing the other failures.
- [PASS] No fabricated data.

### Input 4 — Variant B
**Prompt:** "Build an ortholog wide-table: human chr17 genes with mouse and zebrafish orthologs,
filtered to 1:1 only."

**What ran:** `run/ortholog_table.py` — the Skill's own shipped `examples/ortholog_table.py`,
copied verbatim, executed 3 times (initial + 2 backoff retries at 20s/35s) plus a smaller 4-gene
variant (`run/input4b_ortholog_small.py`, which independently hit the pybiomart filter bug from
Input 1 on `external_gene_name`).

**Output (`run/input4_output.txt`, `input4_output_retry.txt`, `input4_output_retry2.txt` — all
identical across 3 attempts):**
```
All chr17 genes with any ortholog row: 104
                                  <html>
                                  <head>
      <title>Service unavailable</title>
...
Traceback (most recent call last):
  ...
    mouse_col = next(c for c in df.columns if 'Mouse' in c and 'type' in c)
StopIteration
```
Ensembl returned its `status.ensembl.org` "Service unavailable" HTML page with HTTP 200 (not an
error code); pybiomart's TSV parser accepted this as valid data (a second, independent
confirmation of the response-shape-validation gap already logged in this environment's
`TOOLS.md`), producing a corrupted `df` that then crashed the script's column-matching logic with
no diagnostic context. Separately confirmed (`run/input3b_ortholog_attr_check.txt`) that all 4
ortholog attribute names the script uses are valid — the query design itself is correct.

**Scores:** Basic: 16/40 | Specialized: 30/60 | Total: 46/100
**Assertions:**
- [FAIL] Code executes without unhandled exceptions.
- [PASS] Ortholog attribute names used are valid BioMart attributes (independently verified).
- [FAIL] Script validates server response before using it — no check exists; malformed HTML is
  silently treated as data.
- [PASS] No fabricated ortholog calls produced — the script crashed rather than reporting wrong
  orthology, a safe (if unhelpful) failure.

### Input 5 — Stress
**Prompt:** "Get GO term annotations for TP53, BRCA1, MYC, EGFR, and also MARCH1 (older gene
symbol) — flag if any symbol returns nothing."

**What ran:** `run/input5_go_and_rename.py` — SKILL.md's "GO term annotation for a gene set"
pattern, run verbatim, with MARCH1 added to exercise the Skill's own documented "Symbol-based
filter misses HGNC renames" failure mode. Followed by `run/input5b_raw_xml_march1.py`, a raw
martservice XML query bypassing pybiomart entirely, to isolate client bug from server truth.

**Output (`run/input5_output.txt`):**
```
pybiomart.base.BiomartException: Unknown filter external_gene_name, check dataset filters for
a list of valid filters.
```
**Raw-XML control (`run/input5b_output.txt`, `input5c_march1_retry.txt`):**
```
--- TP53 (control, current symbol) ---
HTTP 200, body: 'Gene stable ID\tGene name\nENSG00000141510\tTP53'
--- MARCH1 (renamed to MARCHF1 in 2020) ---
HTTP 200, body: '<html>...Service unavailable...'
```
`external_gene_name` is confirmed valid server-side (TP53 returned the correct real answer via raw
XML), isolating the defect to pybiomart's client-side filter validation — the same root cause as
Input 1. The MARCH1-specific rename check itself hit the same live Ensembl outage seen in Input 4,
twice (15s apart), and could not be confirmed or denied this session — recorded honestly as
inconclusive rather than assumed.

**Scores:** Basic: 13/40 | Specialized: 25/60 | Total: 38/100
**Assertions:**
- [FAIL] Code executes without unhandled exceptions.
- [FAIL] Output distinguishes found vs. not-found gene symbols — never reached that stage.
- [PASS] Raw-XML control confirms `external_gene_name` is a valid server-side filter, isolating
  the defect to the pybiomart client.
- [FAIL] MARCH1-rename failure mode empirically confirmed this session — blocked twice by a live
  Ensembl outage; inconclusive.

---

## Research Veto Note

**M4 (Code Usability) — FAIL.** This is not attributable to live-service flakiness: Inputs 1, 2 and
5 fail with a `KeyError`/`BiomartException` raised entirely client-side, before any query is sent
to Ensembl, 100% reproducibly, on the Skill's own unmodified example code and inline patterns. The
Skill's single most central, most-advertised use case (bulk Ensembl-ID mapping, named first in its
own frontmatter `description`) does not run as documented against the only pybiomart version that
has ever existed on PyPI. See `eval_report_bio-biomart-queries_result.json` for the full veto
report.
