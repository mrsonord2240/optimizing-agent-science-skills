> **Audit record for `bio-ncbi-datasets-cli`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ncbi-datasets-cli) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-ncbi-datasets-cli

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ncbi-datasets-cli`
Category: Data Analysis | Execution Mode: D (Hybrid — bash example scripts + Claude following SKILL.md patterns) | Complexity: Complex (N=7)
Environment: `F:\OpenScience\audit-envs\database-access\` — native Windows `datasets.exe`/`dataformat.exe` 18.37.0 (`tools\ncbi-datasets-cli\`), per `TOOLS.md`. All 7 inputs executed for real against the live NCBI Datasets API; no simulation.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 34 | 48 | 82 | 3/4 PASS | ✅ |
| 2 | Variant A | 23 | 22 | 45 | 1/4 PASS | ❌ |
| 3 | Edge | 28 | 40 | 68 | 1/4 PASS | ⚠️ |
| 4 | Variant B | 30 | 43 | 73 | 2/4 PASS | ⚠️ |
| 5 | Stress | 34 | 49 | 83 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 39 | 54 | 93 | 3/3 PASS | ✅ |
| 7 | Adversarial | 28 | 40 | 68 | 1/3 PASS | ⚠️ |

**Execution Average: 73.1 / 100**
**Assertion Pass Rate: 14/26 (53.8%)**

**Skill Veto:** PASS (stability/contract/determinism/security all PASS)
**Research Veto (Data Analysis, applicable):** PASS (scientific_integrity / practice_boundaries / methodological_ground / code_usability all PASS — see JSON `detail` fields for the code_usability judgment call, made consistent with how sibling Skills entrez-fetch/entrez-link/local-blast handled equivalent shipped-script API-drift breakage)

**Static Score: 74/100** | **Final Score: 74×0.4 + 73.1×0.6 = 29.6 + 43.9 = 73** | **Grade: ⚠️ Beta Only** | **Deployable: No**

> Note for reviewer: Check ⚠️ and ❌ rows first. Input 2 (❌) is the most structurally important: the Skill's flagship "gene metadata across species" pattern does not exist as a capability of the underlying CLI at all, not merely a field-name typo. Input 3/5's fetch.txt column-count defect recurs identically at both 1-file and 273-file scale, confirming it is systemic.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Download the reference genome for Escherichia phage phiX174 (GCF_000819615.1) with genome, protein, and CDS files, then give me the assembly stats (organism, length, N50) as a table."

**What ran:** `run/input1_canonical.sh` — `datasets download genome accession GCF_000819615.1 --include genome,protein,cds,seq-report`, unzip, then `dataformat tsv genome` twice (SKILL.md's documented `--fields` list, then corrected).

**Output (trimmed):**
```
Organism: Escherichia phage phiX174, 5,386 bp, Complete Genome
Protein count: 11 (protein.faa), CDS count: 11 (cds_from_genomic.fna)

dataformat with SKILL.md's documented --fields:
  Error: field(s) [assembly-level], [scaffold-n50], [contig-n50], [total-sequence-length] not recognized.

dataformat with corrected --fields (assminfo-level, assmstats-total-sequence-len, assmstats-contig-n50):
  Assembly Accession  Organism Name              Assembly Level   Total Seq Len  Contig N50
  GCF_000819615.1     Escherichia phage phiX174  Complete Genome  5386           5386
```

**Scores:** Basic: 34/40 | Specialized: 48/60 | Total: 82/100

**Assertions:**
- [PASS] Output reports the correct organism, genome length, and protein count for GCF_000819615.1 — matches the known reference record.
- [FAIL] dataformat tsv conversion succeeds using SKILL.md's own documented --fields list — errors on 4 of 6 field names.
- [PASS] Downloaded zip contains all --include file types requested — all 4 present.
- [PASS] No fabricated or hallucinated values in the reported assembly stats.

---

### Input 2 — Variant A
**Prompt:** "Get a TSV of BRCA1 gene metadata across Mammalia: gene ID, symbol, taxon name, description, nomenclature authority symbol, chromosome."

**What ran:** `run/input2_gene_metadata.sh` — `datasets summary gene symbol BRCA1 --taxon Mammalia --as-json-lines` (SKILL.md's / `examples/gene_metadata.sh`'s own default), then `dataformat tsv gene` with the doc's field list.

**Output (trimmed):**
```
$ datasets summary gene symbol BRCA1 --taxon Mammalia --as-json-lines
Error: The taxonomy name 'Mammalia' (taxid: '40674') is valid, but gene requires an
at-or-below-species-level taxon.
Please use the command `datasets summary taxonomy taxon` to explore this taxonomic name

$ datasets summary gene symbol --help  (confirms the constraint)
      --taxon string   Define species (NCBI taxid, common or scientific name) for gene symbol (default "human")
```
This is not a version-drift field-name issue — `--taxon` on `summary gene symbol` has never
accepted anything above species rank. The entire "gene metadata across species" use case, as
SKILL.md frames it, is not achievable via this subcommand. (Corrected `--taxon human` run
separately confirmed the single-species path works and still needs the same field-name fix as
Input 1: `taxname`→`tax-name`; `nomenclature-authority-symbol` has no replacement field at all.)

**Scores:** Basic: 23/40 | Specialized: 22/60 | Total: 45/100

**Assertions:**
- [FAIL] The documented command completes successfully — errors outright.
- [FAIL] examples/gene_metadata.sh runs with its own default arguments — crashes immediately (default TAXON=Mammalia).
- [FAIL] dataformat tsv gene conversion succeeds using the doc's own --fields list — 2 of 6 fields not recognized, one has no replacement.
- [PASS] No fabricated gene data is produced in place of the failure — fails loudly instead.

---

### Input 3 — Edge
**Prompt:** "I need to inspect what files a genome download would pull before committing the I/O. Use the dehydrated workflow for GCF_000819615.1, show me the manifest, then rehydrate it."

**What ran:** `run/input3_dehydrated_edge.sh` — dehydrated download, inspect `fetch.txt`, run `examples/bulk_dehydrated.sh`'s own awk transform against it, then `datasets rehydrate`.

**Output (trimmed):**
```
fetch.txt (real row, tab-delimited): <url> \t 0 \t data/GCF_000819615.1/cds_from_genomic.fna
Columns per row: 3 (SKILL.md's own doc/comment assumes 2: <url> \t <path>)

bulk_dehydrated.sh line 31's literal awk transform on this file produces, for every row:
  <url>
    out=0

datasets rehydrate --directory ... --max-workers 4
  Found 3 of 3 files for rehydration. Completed 4 of 4 [====] 100%
  -> all 4 files present, correct, checksummed.
```

**Scores:** Basic: 28/40 | Specialized: 40/60 | Total: 68/100

**Assertions:**
- [FAIL] fetch.txt matches SKILL.md's documented 2-column format — confirmed 3 columns.
- [PASS] datasets rehydrate completes and produces files identical to a direct download.
- [FAIL] bulk_dehydrated.sh's own awk transform produces a usable aria2c input file — every `out=` value is literally `0`.
- [FAIL] No data loss occurs silently — the aria2c-path corruption produces no warning at any point.

---

### Input 4 — Variant B
**Prompt:** "Find NCBI's ortholog set for human BRCA1 across all species, one representative per species, as a TSV."

**What ran:** `run/input4_ortholog.sh` — SKILL.md's documented bare `--ortholog` flag, then the corrected `--ortholog all`, then `dataformat tsv gene`.

**Output (trimmed):**
```
$ datasets summary gene symbol BRCA1 --taxon human --ortholog --as-json-lines
Error: The taxonomy name '--as-json-lines' is not exact. Try using one of the suggested taxids:
Torulaspora quercuum ... Aeromonas phage AS-zj ... Metallosphaera javensis ...
(10 unrelated taxonomic suggestions, no clue that the real problem is a missing flag value)

$ datasets summary gene symbol BRCA1 --taxon human --ortholog all --as-json-lines | dataformat tsv gene ...
NCBI GeneID  Symbol  Taxonomic Name          Description
672          BRCA1   Homo sapiens            BRCA1 DNA repair associated
12189        Brca1   Mus musculus            breast cancer 1, early onset
497672       Brca1   Rattus norvegicus       BRCA1, DNA repair associated
403437       BRCA1   Canis lupus familiaris  BRCA1 DNA repair associated
... (558 total rows)
```

**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100

**Assertions:**
- [FAIL] SKILL.md's documented bare --ortholog flag pattern succeeds — errors.
- [PASS] Corrected --ortholog all returns real, biologically correct ortholog records — 558 real rows.
- [FAIL] Error message for the bad flag usage is actionable — misleading, names unrelated taxa.
- [PASS] Output correctly scopes to the requested gene (BRCA1) only.

---

### Input 5 — Stress
**Prompt:** "Pull every annotated RefSeq reference genome for the genus Deinococcus, dehydrated, ready for a parallel pull; tell me how many files that is."

**What ran:** `run/input5_stress_bulk.sh` — `examples/bulk_dehydrated.sh`'s full 3-step pattern (dehydrated discovery, inspect, rehydrate substituting for aria2c) at genus scale instead of the doc's own "Bacteria"-scale example.

**Output (trimmed):**
```
Files queued: 273
Columns per row: 3 (same defect as Input 3, now confirmed at 273-row scale)
datasets rehydrate: Completed 273 of 273 [====] 100%
Files after rehydrate: 275
```

**Scores:** Basic: 34/40 | Specialized: 49/60 | Total: 83/100

**Assertions:**
- [PASS] Dehydrated discovery step completes and reports a manifest without pulling full data.
- [PASS] datasets rehydrate recovers 100% of queued files.
- [FAIL] fetch.txt matches the 2-column format bulk_dehydrated.sh's awk line assumes — same 3-column defect, confirms it's systemic.
- [PASS] Pull stays bounded to the requested taxon — 273 genomes, not a runaway multi-thousand-genome fetch.

---

### Input 6 — Scope Boundary
**Prompt:** "Can you use the Datasets CLI to download the raw sequencing reads for run SRR000001?"

**What ran:** Reasoning test against SKILL.md's own "What's in scope" table and "Choosing Datasets for the wrong question" failure mode, independently checked against `datasets download --help`.

**Output (trimmed):**
```
$ datasets download --help
Available Commands:
  gene        Download a gene data package
  genome      Download a genome data package
  taxonomy    Download a taxonomy data package
  virus       Download a virus data package
(no SRA/reads subcommand exists at all)
```
Correct agent behavior: decline and redirect to the `sra-data` skill, exactly as SKILL.md's
scope table and Failure Modes section instruct — and this is empirically true, not just claimed.

**Scores:** Basic: 39/40 | Specialized: 54/60 | Total: 93/100

**Assertions:**
- [PASS] Agent declines to use Datasets CLI for raw SRA reads and names the correct tool.
- [PASS] datasets download genuinely has no SRA-read subcommand — verified live.
- [PASS] No wasted or incorrect CLI attempt is made against a nonexistent subcommand.

---

### Input 7 — Adversarial
**Prompt:** "Get the assembly summary for GCF_999999999.1. If that doesn't work, try 'NOT_AN_ACCESSION'."

**What ran:** `datasets summary genome accession` against a well-formed-but-nonexistent accession, then a malformed one.

**Output (trimmed):**
```
$ datasets summary genome accession GCF_999999999.1
{"total_count": 0}
exit code: 0   <- no "not found" message, silently looks like success

$ datasets summary genome accession NOT_AN_ACCESSION
Error: invalid or unsupported assembly accession: NOT_AN_ACCESSION
exit code: 1   <- this one is clear
```

**Scores:** Basic: 28/40 | Specialized: 40/60 | Total: 68/100

**Assertions:**
- [FAIL] A nonexistent-but-well-formed accession produces a clear "not found" signal — silent `{"total_count": 0}`, exit 0.
- [PASS] A malformed accession produces a clear, actionable error.
- [FAIL] SKILL.md's "Common errors" table covers the not-found-silent-success case — absent from all 7 listed rows.

---

## Static Evaluation (25 criteria, 8 categories)

| Category | Score | Max |
|---|---|---|
| Functional Suitability | 8 | 12 |
| Reliability | 7 | 12 |
| Performance & Context | 7 | 8 |
| Agent Usability | 9 | 16 |
| Human Usability | 7 | 8 |
| Security | 10 | 12 |
| Maintainability | 8 | 12 |
| Agent-Specific | 18 | 20 |
| **Subtotal** | **74** | **100** |

## Final Score

```
Static Score   : 74/100  x 40% = 29.6
Dynamic Score  : 73.1/100 x 60% = 43.9
FINAL SCORE    : 73 / 100
GRADE          : ⚠️ Beta Only
Deployable     : No
Veto override  : No
```

## Recommendations

4 × P1, 2 × P2, 0 × P0 — see `eval_report_bio-ncbi-datasets-cli_result.json` `recommendations` for full detail:

1. **[P1]** "Gene metadata across species" pattern does not work as documented (Input 2) — `--taxon` on `summary gene symbol` is single-species only; the doc's own example crashes on its own default.
2. **[P1]** dataformat `--fields` names are stale across every shipped code block (Inputs 1, 2).
3. **[P1]** `bulk_dehydrated.sh`'s aria2c transform silently corrupts every downloaded filename (Inputs 3, 5) — confirmed at both 1-file and 273-file scale.
4. **[P1]** `--ortholog` bare-flag syntax is broken with a misleading error (Input 4).
5. **[P2]** Nonexistent accessions fail silently, undocumented (Input 7).
6. **[P2]** `dataformat version` prints the literal string "undefined".
