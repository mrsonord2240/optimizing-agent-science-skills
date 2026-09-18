> **Audit record for `bio-biomart-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@eb9a071](https://github.com/mrsonord2240/bioSkills/tree/eb9a071e28dec6fef79e277bd94aa8d41afd5695/database-access/biomart-queries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-biomart-queries (re-audit of fix)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@eb9a071:database-access/biomart-queries` (branch `fix/db-biomart`, worktree `F:\OpenScience\wt\db-biomart`)
Pre-fix report archived at: `F:\OpenScience\audits\_pre-fix-20260917d\bio-biomart-queries\` (score 60, Reject, Research Veto M4 FAIL)

This is an independent re-audit. The fix log (`F:\optimizing-agent-science-skills\fixes\bio-biomart-queries.md`) was read to know where to look; nothing in it was accepted as evidence without an independent run below.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (Bulk ID mapping) | 38 | 55 | 93 | 5/5 PASS | ✅ |
| 2 | Variant A (Coordinate table) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 3 | Edge (Discovery / root-cause re-check) | 38 | 53 | 91 | 4/4 PASS | ✅ |
| 4 | Variant B (Ortholog wide-table) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 5 | Stress (GO annotation + MARCH1 rename) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (Ensembl Genomes host-swap) | 25 | 37 | 62 | 3/4 PASS | ❌ |
| 7 | Adversarial (outage guard / escaping / scale / degenerate filters) | 28 | 40 | 68 | 2/5 PASS | ❌ |

**Execution Average: 84.4 / 100**
**Assertion Pass Rate: 26/30 (86.7%)**

**Static Score: 92/100** | **Final Score: 87/100** | **Grade: ✅ Limited Release** (downgraded one tier from the raw score's Production Ready bracket — the Execution Average floor for Production Ready is ≥85 and this run measured 84.4; see `scoring_rubric.md` §5)
**Skill Veto: PASS** | **Research Veto: PASS** (both original P0s confirmed fixed; see below) | **Deployable: true**

> **Note for reviewer:** check ⚠️/❌ rows first. Inputs 6 and 7 are new findings this session (not regressions of the pre-fix report) and are the reason this fix does not reach Production Ready.

---

## Method note

Per the audit brief, all fenced code blocks were extracted **programmatically** from the shipped `SKILL.md` (see `run/extract_blocks.py` → `run/block_*.txt`) and assembled into the scripts below by straight concatenation — the document itself was tested, not a transcription of it. The three copies of `query_raw()` (SKILL.md + both `examples/*.py`) were diffed byte-for-byte and are identical (`run/` diff check, not shown as a separate script — inline Python one-liner in the transcript).

Ensembl BioMart was live but intermittently 429/500/outage-flaky throughout this session, consistent with what the tooling pass documented independently. Every input was retried with backoff (`run/retry_run.sh`, 4 attempts, 5/15/30/60s delays) before being scored; failures attributable to live flakiness are called out explicitly below and distinguished from genuine code defects.

---

## Detailed Outputs

### Input 1 — Canonical: Bulk ID mapping

**Prompt (regression of pre-fix Input 1):** *"Convert 5 Ensembl Gene IDs (BRCA2, TP53, PTEN, EGFR, MYC) to HGNC symbol, RefSeq mRNA, and UniProt accessions in one query."*

**What ran:** `run/input1_bulk_id_mapping.py` (SKILL.md's inline pattern, assembled from `block_2` + `block_3`) and `run/input_shipped_bulk_id_mapping.py` (runs the actual shipped `examples/bulk_id_mapping.py` unmodified as a subprocess).

**Output (shipped example, abbreviated):**
```
=== Bulk ID mapping: Ensembl Gene -> HGNC + RefSeq + UniProt ===
  Rows: 54 (note: many-to-many cross-ref joins multiply rows)
...
=== Collapse to one row per gene (most common downstream pattern) ===
ENSG00000136997       MYC  HGNC:7553  NM_001354870;NM_002467                    P01106
ENSG00000139618     BRCA2  HGNC:1101  NM_000059;NM_001406719;...;NM_001432077   P51587
ENSG00000141510      TP53 HGNC:11998  NM_000546;...(25 transcripts)...          P04637
ENSG00000146648      EGFR  HGNC:3236  NM_001346897;...;NM_201284                P00533
ENSG00000171862      PTEN  HGNC:9588  NM_000314;NM_001304717;NM_001304718       P60484
```
This is the **flagship pattern that was the P0** pre-fix — it now runs end-to-end, real biology confirmed (BRCA2=HGNC:1101, TP53=HGNC:11998 — both independently verifiable ground truth), and the fixer's extra NaN/groupby fix works (the collapse step completes for all 5 genes without the `TypeError` the pre-fix `filter(None, x)` would have hit).

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] Code executes without unhandled exceptions — both variants exit 0
- [PASS] Returned HGNC IDs match known ground truth — all 5 correct
- [PASS] NaN/groupby collapse step completes without crashing — confirmed fixed
- [PASS] Row multiplication for multi-isoform genes documented and observed
- [PASS] No fabricated biological data

---

### Input 2 — Variant A: Coordinate table (gene_biotype fix)

**Prompt (regression of pre-fix Input 2):** *"Pull all protein-coding genes on chromosome 17 with coordinates, using SKILL.md's inline pattern verbatim."*

**What ran:** `run/input2_coordinate_table.py` (`setup_lite` + `block_2` + `block_4`).

**Output:**
```
1187 protein-coding genes on chr17
Gene stable ID   Gene name  Chromosome  Start    End     Strand  Gene type
ENSG00000268320  SCGB1C2    17          137569   139067  1       protein_coding
ENSG00000272636  DOC2B      17          142789   181691  -1      protein_coding
ENSG00000181031  RPH3AL     17          210130   386376  -1      protein_coding
...
```
This is the **P1 fix** (`biotype`→`gene_biotype` attribute name) — confirmed live, 1187 real chr17 protein-coding genes, all real known loci.

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 4/4 PASS (executes cleanly; correct attribute name; real known genes; no fabrication)

---

### Input 3 — Edge: Discovery / independent root-cause re-check

**Prompt:** *"Before trusting any filter/attribute name, discover what's really available — and check SKILL.md's own claims about what's missing."*

**What ran:** `run/input3_discover.py` (`block_1` + `block_8`, plus explicit membership assertions).

**Output:**
```
ensembl_gene_id in ds.filters: False
external_gene_name in ds.filters: False
gene_biotype in ds.attributes: True
biotype in ds.attributes: False
biotype in ds.filters: True
OK: SKILL.md Version Compatibility claims confirmed live against current pybiomart/Ensembl state.
```
Independently reproduces the exact root cause SKILL.md's "Version Compatibility" section now documents — this is not taken on the fixer's word, it was re-derived live.

**Scores:** Basic: 38/40 | Specialized: 53/60 | Total: 91/100
**Assertions:** 4/4 PASS

---

### Input 4 — Variant B: Ortholog wide-table

**Prompt (regression of pre-fix Input 4):** *"Build a wide ortholog table: human chr17 genes with mouse and zebrafish 1:1 orthologs."*

**What ran:** `run/input4_ortholog.py` (inline pattern) and `run/input_shipped_ortholog_table.py` (shipped example, subprocess).

**Output (shipped example, abbreviated):**
```
All chr17 genes with any ortholog row: 4298
1:1 in mouse AND zebrafish: 532
Gene stable ID  Gene name  Mouse gene stable ID  ... Zebrafish gene stable ID ...
ENSG00000272636 DOC2B      ENSMUSG00000020848        ENSDARG00000088293
ENSG00000183688 RFLNB      ENSMUSG00000020846        ENSDARG00000093931
ENSG00000108953 YWHAE      ENSMUSG00000020849        ENSDARG00000006399
ENSG00000167193 CRK        ENSMUSG00000017776        ENSDARG00000055635
```
532 real 1:1 orthologs, matching the fix log's own claimed count, independently reproduced with the shipped example (not just the inline pattern).

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 4/4 PASS

---

### Input 5 — Stress: GO annotation + MARCH1 HGNC-rename check

**Prompt (regression of pre-fix Input 5):** *"Get GO term annotations for TP53, BRCA1, MYC, EGFR, and MARCH1 (a pre-2020 HGNC symbol renamed MARCHF1)."*

**What ran:** `run/input5_go_and_rename.py` (`setup_lite` + `block_2` + GO pattern extended with MARCH1).

**Output:**
```
OK: 380 GO rows; gene symbols present: ['BRCA1', 'EGFR', 'MYC', 'TP53']
MARCH1 present (expected: NO, renamed to MARCHF1 post-2020): False
```
This is the **same filter bug as Input 1** (root cause fixed) plus an empirical confirmation — this session, unlike the pre-fix audit — of the HGNC-rename failure mode SKILL.md documents.

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 4/4 PASS

---

### Input 6 — Scope Boundary: Ensembl Genomes host-swap claim ❌

**Prompt (new, auditor's own):** *"I need gene coordinates for Arabidopsis thaliana on chr1 — SKILL.md says just swap the host to plants.ensembl.org."*

**What ran:** `run/input6_scope_boundary_plants.py`, `run/input6b_diagnose_virtual_schema.py`, `run/input6c_diagnose_host.py`.

**Output:**
```
Marts: ['plants_mart', 'plants_variations', 'plants_sequences']
Arabidopsis-matching dataset(s): ['athaliana_eg_gene']
RuntimeError: BioMart rejected the query: Query ERROR: caught BioMart::Exception::Usage:
WITHIN Virtual Schema : default, Dataset athaliana_eg_gene NOT FOUND
```
Follow-up diagnosis ruled out the obvious hypothesis (a `virtualSchemaName` mismatch — it genuinely is `'default'` per the server's own registry response) and confirmed **pybiomart's own high-level `ds.query()` fails identically** — so this is not a `query_raw()`-specific regression, but the SKILL.md/usage-guide.md claim ("swap the host, e.g. `Server(host='http://plants.ensembl.org')`") — newly promoted into SKILL.md's main tool listing by this fix — does not work as a simple one-line instruction for a real Ensembl Genomes dataset.

**Scores:** Basic: 25/40 | Specialized: 37/60 | Total: 62/100
**Assertions:** 3/4 PASS (fails: "host-swap produces a working query as documented")

---

### Input 7 — Adversarial: outage guard, escaping, realistic scale, degenerate filters ❌

**Prompt (new, auditor's own; four sub-probes):**
1. *Does the outage-page guard genuinely fire?* (offline unit test, monkeypatched `Dataset.get()`)
2. *Is the hand-built XML safe for values needing escaping?* (offline, captured outgoing bytes)
3. *Does bulk ID mapping work at the scale SKILL.md itself advertises (thousands of IDs)?*
4. *What happens with an unknown ID or an empty ID list?*

**What ran:** `run/input6_outage_guard.py`, `run/input7a_escaping_offline.py`, `run/input7b_scale_and_unknown_ids.py`, `run/input7c_unknown_and_empty.py` (x2), `run/input7d_raw_body_diagnosis.py`.

**Outage guard (offline unit test) — PASS, 5/5:**
```
outage_html_200      -> RuntimeError: BioMart returned a non-TSV response...
empty_200            -> RuntimeError: ...
whitespace_only_200  -> RuntimeError: ...
query_error_body     -> RuntimeError: BioMart rejected the query: Query ERROR...
genuine_tsv          -> NO EXCEPTION -- returned DataFrame shape (1, 2)
ALL GUARD ASSERTIONS PASSED
```
This directly answers the brief's central question: **the outage-page guard is real.** It fires on every non-TSV shape tested and does not false-positive on valid data, exercised against the actual `query_raw()` function via a monkeypatched `Dataset`, not a reimplementation.

**XML escaping (offline) — PASS:**
```
<Filter name="external_gene_name" value="TP53 &amp; BRCA1,A&lt;B&gt;C,quote&quot;inside,apostrophe's-name" />
Parsed back Filter value attribute: 'TP53 & BRCA1,A<B>C,quote"inside,apostrophe\'s-name'
OK: special characters round-trip safely through ElementTree escaping; XML is well-formed.
```

**Realistic scale (live) — FAIL, new defect:**
```
Got 2066 real chr1 protein-coding gene IDs
Approx filter-value length alone: 33056 chars
FAILED: HTTPError: 414 Client Error: Request-URI Too Large
```
`query_raw()` sends the whole query via HTTP **GET** (inherited unchanged from `pybiomart.ServerBase.get()`). At ~2000+ IDs this exceeds the server's URL-length limit. SKILL.md's own Goal text says "Convert **5,000** Ensembl Gene IDs"; usage-guide.md's Quick Start says "**8,000** Ensembl Gene IDs" — both would fail the same way, worse. This directly undermines the Skill's flagship advertised use case at real scale, even though it now works correctly at the small/example scale every regression input above tested.

**Unknown ID / empty list (live) — inconclusive, not a guard defect:**
```
=== RAW: unknown/fake ID mixed with a real one ===
HTTP status: 200
Body: '<html>...<title>Service unavailable</title>...' (2459 bytes)
=== RAW: empty list as filter value ===
HTTP status: 200
Body: identical outage page (2459 bytes)
=== CONTROL: known-good 2-real-gene query ===
HTTP status: 200
Body: 'Gene stable ID\tGene name\nENSG00000012048\tBRCA1\nENSG00000141510\tTP53\n'
```
Raw-body capture (bypassing the guard) proves these two sub-probes hit a **genuine live "Service unavailable" outage page**, byte-identical to the documented failure mode, on 4/4 isolated attempts — while a control query moments later succeeded. This is not a guard malfunction (the guard correctly raised `RuntimeError` instead of returning the HTML as data both times) but it also means normal-condition behavior for an unknown/empty filter was **not cleanly demonstrated** this session — scored as a FAIL on the specific assertion ("returns a clear, usable result") since success was never observed, while noting honestly that the guard itself behaved correctly throughout.

**Scores:** Basic: 28/40 | Specialized: 40/60 | Total: 68/100
**Assertions:** 2/5 PASS (fail: scale claim; unknown-ID clean result; empty-list clean result)

---

## Veto Gates

**Skill Veto:** PASS (T1 stability — no crashes/infinite loops from the Skill's own code; T2 contract — frontmatter complete; T3 determinism — deterministic given stable live data; T4 security — no eval/exec of raw strings, filter values confirmed safely XML-escaped)

**Research Veto (Category 3 — Data Analysis):**
- M1 Scientific Integrity: PASS — no fabricated values across any of the 7 inputs, all cross-checked against real biology
- M2 Practice Boundaries: PASS — population-level reference data only, no disclaimer needed
- M3 Methodological Ground: PASS — no principled methodological fallacy; new gaps found (Input 6, 7) are code-usability/documentation-accuracy defects, not methodological errors
- M4 Code Usability: PASS — both original P0s are genuinely fixed and reproduced independently; the new 414-at-scale defect is real but pattern-specific (small/chromosome-level scale works correctly everywhere tested) and fails cleanly rather than silently, so it does not meet the veto bar ("unrunnable... syntax errors, infinite loops, missing dependencies")

## Gate checks

- **Gate 8 (shipped-means-present):** PASS — `examples/bulk_id_mapping.py`, `examples/coordinate_table.sh`, `examples/ortholog_table.py` all present; SKILL.md/usage-guide.md do not name any file by path that is missing.
- **Gate 7 (research scope):** PASS — Data Analysis category, no diagnostic/prescriptive content, population-level genomic reference data only.

## Housekeeping

- `find F:/OpenScience/external/mrsonord2240__bioSkills -name __pycache__` → empty (no writes to the clone).
- `git status --short` in `F:\OpenScience\wt\db-biomart` → clean (no writes to the fix worktree).
- All scripts run from `F:\OpenScience\audits\bio-biomart-queries\run\` with the Skill's files copied into `run/skill_copy/`, never imported in place.
