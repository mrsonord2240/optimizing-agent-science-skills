> **Audit record for `bio-geo-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/geo-data) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-geo-data
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/geo-data` (unmodified upstream). Skill copied to `F:\OpenScience\audits\bio-geo-data\skill-copy\` before any code was run (never executed against the byte-identical clone at `F:\OpenScience\external\GPTomics__bioSkills\`). Environment: shared `database-access` venv/R-lib tooled 2026-09-17 (`F:\OpenScience\audit-envs\database-access\TOOLS.md`, "geo-data" section) — biopython 1.88, pandas 3.0.5, GEOparse 2.0.4, pysradb 2.5.1, R 4.4.3 / Bioconductor 3.20 GEOquery 2.74.0 via `r.sh`.

Category: **Data Analysis** | Execution Mode: **D (Hybrid)** | Complexity: **Complex (N=7)**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 3 | Edge | 30 | 42 | 72 | 2/4 PASS | ⚠️ |
| 4 | Variant B | 26 | 41 | 67 | 2/4 PASS | ❌ |
| 5 | Stress | 28 | 41 | 69 | 2/4 PASS | ⚠️ |
| 6 | Scope Boundary | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial | 37 | 50 | 87 | 4/4 PASS | ✅ |

**Execution Average: 82.3 / 100**
**Assertion Pass Rate: 22/28 (78.6%)**

> Assertion pass rate (78.6%) is below the 80% floor for Limited Release, which downgrades the grade by one tier from the raw-score band (see Final Score below).

## Detailed Outputs

### Input 1 — Canonical: search + live SuperSeries/SubSeries check

**Prompt:** "Search GEO for human breast cancer RNA-seq series and flag any that are SuperSeries before I download them."

**Code run:** `run\input1_canonical_search_superseries.py` — SKILL.md's `search_geo()` verbatim, plus SKILL.md's own inline `check_super_or_sub_series()` logic (not the broken `examples/search_geo.py` copy) run as the definitive check against the top hit.

**Output (trimmed):**
```
=== search_geo("breast cancer", study_type=gse, organism=Homo sapiens, max_results=10) ===
n results: 10
  GSE346737      12 samples  GPL34284   Transcriptional Hallmarks of Drug Tolerance in Hormone-Dependent Cance
  GSE333367       6 samples  GPL18573   Identification and validation of an ESR1 Y537S mutant-specific enhance
  ... (8 more real hits)

=== Definitive SuperSeries check via SOFT family file for GSE346737 ===
  GSE346737: {'super_of': [], 'sub_of': 'GSE346738'}
```
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] Output lists real GSE accessions with sample counts and platform IDs
- [PASS] SuperSeries/SubSeries status is checked against a real SOFT file, not fabricated
- [PASS] Output does not exceed the stated search+detection task
- [PASS] At least one accession's status is verified via the definitive SOFT check, not just the summary heuristic

---

### Input 2 — Variant A: GSE147507 -> SRR via pysradb

**Prompt:** "For GSE147507, resolve to SRA run accessions using pysradb, so I can hand off to sra-data for FASTQ download."

**Code run:** `run\input2_varianta_geo_to_sra.py` — SKILL.md's `gse_to_srr()` verbatim.

**Output:**
```
GSE147507 -> 329 SRR runs
first 5: ['SRR11412215', 'SRR11412216', 'SRR11412217', 'SRR11412218', 'SRR11412219']
Wrote 329 accessions to GSE147507_sra_runs.txt
```
Matches TOOLS.md's independent tooling-pass ground truth (329 runs, SRP262931) exactly.
**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100
**Assertions:**
- [PASS] SRR run count matches a real, independently verifiable ground truth
- [PASS] Output writes accessions to a file for hand-off to sra-data, as documented
- [PASS] Uses the Skill's stated preferred/more-reliable path (pysradb), not the broken Entrez fallback
- [PASS] Does not fabricate SRR accessions

---

### Input 3 — Edge: GSE470 series matrix parse + Sample_data_processing audit

**Prompt:** "Download the series matrix for GSE470 (a small, quiet standalone series) and dump every unique value of !Sample_data_processing, per the usage-guide's 'Submitter-data-processing audit' prompt."

**Code run:** `run\input3_edge_series_matrix_gse470.py` — SKILL.md's `parse_series_matrix()` verbatim against the cached real `GSE470_series_matrix.txt.gz`, then both the documented `.get()` access and a literal bracket-access reading of the usage-guide prompt.

**Output:**
```
expr.shape = (12625, 12)
!Series_geo_accession = ['GSE470']
columns (first 3) = ['GSM3909', 'GSM3910', 'GSM3911']

--- SKILL.md-documented .get() access (safe form) ---
unique !Sample_data_processing values via .get(): set()
  -> empty: this real series has NO !Sample_data_processing field at all.

--- Bracket access as a literal reading of the usage-guide prompt ---
KeyError: KeyError('!Sample_data_processing')  -- confirms bracket access crashes on this real series
```
**Scores:** Basic: 30/40 | Specialized: 42/60 | Total: 72/100
**Assertions:**
- [PASS] Reports real matrix dimensions matching known GSE470 ground truth (12625 x 12)
- [FAIL] Distinguishes between a field being genuinely absent vs. empty for another reason — nothing in SKILL.md/usage-guide states the field can be entirely absent
- [FAIL] Following the usage-guide's literal prompt wording does not crash on this real series — bracket access raises KeyError
- [PASS] Uses the Skill's documented .get()-based parse_series_matrix() function correctly

---

### Input 4 — Variant B: PubMed->GEO citation link, shipped vs corrected PMID

**Prompt:** "Find all GEO datasets cited in PMID 32228226 via pubmed -> gds ELink (the Skill's own worked example, claimed to be Blanco-Melo et al. 2020 Cell)."

**Code run:** `run\input4_variantb_pubmed_to_geo.py` — `examples/geo_from_pubmed.py` run exactly as shipped, then repeated with the corrected PMID.

**Output:**
```
=== Article (as shipped PMID) ===
  PMID:    32228226
  Title:   Transcriptomic characteristics of bronchoalveolar lavage fluid and peripheral blood mononuclear cell
  Journal: Emerg Microbes Infect, 2020 Dec

=== GEO datasets cited in PMID 32228226 (as shipped) ===
n results: 0

=== Article (corrected PMID 32416070) ===
  Title:   Imbalanced Host Response to SARS-CoV-2 Drives Development of COVID-19.
  Journal: Cell, 2020 May 28

=== GEO datasets cited in corrected PMID 32416070 ===
n results: 1
  GSE147507      110 samples  GPL18573;28369
      Transcriptional response to SARS-CoV-2 infection
```
As shipped, the worked example is real Blanco-Melo/Cell paper mislabeled onto the wrong PMID, silently returning 0 results.
**Scores:** Basic: 26/40 | Specialized: 41/60 | Total: 67/100
**Assertions:**
- [FAIL] The Skill's worked example demonstrates a real PMID->GEO citation link — 0 results as shipped
- [FAIL] No fabricated PMID-paper identity claims — comment misattributes PMID 32228226
- [PASS] The corrected accession pairing is reachable using the same documented mechanism
- [PASS] Output clearly reports article title/journal for traceability

---

### Input 5 — Stress: GSE122288 SuperSeries check + platform-technology decision

**Prompt:** "Detect whether GSE122288 (the Skill's own worked example accession) is a SuperSeries; if so list SubSeries and process independently. Then walk the processed-vs-raw decision matrix: is this Affymetrix or RNA-seq?"

**Code run:** `run\input5_stress_gse122288_superseries_decision.py`

**Output:**
```
=== SKILL.md worked example: Entrez.esummary(db="gds", id="200122288") ===
  Accession: GSE122288
  Title: Genome wide methylation of cord blood from normal glucose tolerance pregnancies
  n_samples: 61
  GPL: 21145

=== Definitive SOFT-based check on GSE122288 (SKILL.md worked example) ===
  {'super_of': [], 'sub_of': None}
  -> Standalone Series (not a SuperSeries, not a SubSeries).

=== Platform lookup for GPL21145 (Affymetrix vs RNA-seq decision) ===
  Platform esummary lookup did not resolve cleanly: RuntimeError: UID=10021145: cannot get document summary
```
The platform-lookup failure is this auditor's own ad hoc UID guess (not a documented Skill code path — no such path exists, which is itself the finding) and is not counted against the Skill's code; the SuperSeries-vs-docstring mismatch is the real, load-bearing finding.
**Scores:** Basic: 28/40 | Specialized: 41/60 | Total: 69/100
**Assertions:**
- [PASS] esummary(db='gds', id='200122288') returns a real, verifiable GEO record
- [FAIL] check_super_or_sub_series('GSE122288') output matches SKILL.md's own documented illustrative return value — live result is empty, doc shows populated
- [FAIL] SKILL.md provides a code path to determine Affymetrix-vs-RNA-seq platform technology for the decision matrix — none exists
- [PASS] Does not fabricate SuperSeries/SubSeries structure not present in live data

---

### Input 6 — Scope Boundary: R GEOquery vs Python series-matrix parity

**Prompt:** "Use R's GEOquery to load GSE470 from the already-downloaded series matrix and cross-validate exprs()/pData() dimensions against the Python parser's result."

**Code run:** `run\input6_scope_boundary_geoquery_r.R`, via `database-access\r.sh`.

**Output:**
```
class(gse): ExpressionSet
dim(exprs(gse)): 12625 12
nrow(pData(gse)): 12
annotation(gse): GPL8300
Series_geo_accession: GSE470
Python parse_series_matrix() shape: 12625 12
R GEOquery exprs() shape:           12625 12
Shapes match: TRUE
```
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] R exprs() dimensions match the Python parser's dimensions exactly for the same real file
- [PASS] Platform/annotation matches known ground truth (GPL8300)
- [PASS] GEOquery loads without needing internet, from a local cached file, as documented
- [PASS] R and Python paths are shown to be genuinely interchangeable, as SKILL.md claims

---

### Input 7 — Adversarial: skip the SuperSeries check

**Prompt:** "I have a GSE accession for a SuperSeries but I just want quick expression values — skip the SuperSeries check and give me the fastest possible parse, mixing all subseries samples together for a single PCA."

**Response (Mode A, no code executed — a reasoning/instruction-following test):** SKILL.md states, repeatedly and unambiguously, that "The SuperSeries trap is the single biggest GEO mistake. ALWAYS check `!Series_relation` ... before treating a GSE as one experiment," and its Failure Modes section documents exactly this scenario ("SuperSeries pulled as one experiment" -> "spurious batch effects"). The correct, Skill-supported response is not to comply silently: warn that mixing SubSeries samples for one PCA reproduces the Skill's own documented worst failure mode, offer the already-validated cheap SOFT-based check (proven fast in Inputs 1 and 5) before proceeding, and only run the fast/mixed PCA if the user still insists after the warning.
**Scores:** Basic: 37/40 | Specialized: 50/60 | Total: 87/100
**Assertions:**
- [PASS] Response does not silently comply with a request that reproduces the Skill's own documented worst failure mode
- [PASS] Response cites the Skill's own stated rationale, not a generic refusal
- [PASS] Response offers a concrete, cheap alternative rather than a flat no
- [PASS] Response allows proceeding if the user insists after being warned, rather than refusing outright

---

## Research Veto (Category 3 — Data Analysis)

| Dimension | Result |
|---|---|
| M1. Scientific Integrity | PASS |
| M2. Practice Boundaries | PASS |
| M3. Methodological Baseline | PASS |
| M4. Code Usability | PASS (3 live runtime defects found in `examples/`, but none are syntax errors / infinite loops / missing dependencies — see recommendations) |

## Final Score

```
Static Score   : 72/100  x 40% = 28.8
Dynamic Score  : 82.3/100 x 60% = 49.4
FINAL SCORE    : 78 / 100  (raw band: Limited Release)
Assertion pass rate: 22/28 = 78.6% -- below the 80% Limited Release floor -> downgrade one tier
GRADE          : ⚠️ Beta Only
Deployable     : false
```

> **Note for reviewer:** The three ⚠️/❌ rows (Inputs 3, 4, 5) all point to the same underlying pattern: the Skill's own documentation and worked examples were not validated against live NCBI data at the time they were written (wrong PMID, broken in-memory gzip read, an illustrative-but-not-live SuperSeries return value, and an undocumented field-absence case). None of this is unsafe or scientifically dishonest — the veto gates all PASS — but it is a real, fixable, and recurring documentation-realism defect across this Skill's three example files.
