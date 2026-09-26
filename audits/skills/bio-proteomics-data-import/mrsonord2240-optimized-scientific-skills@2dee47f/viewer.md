> **Audit record for `bio-proteomics-data-import`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@2dee47f](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db/skills/bio-proteomics-data-import) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-25 by Codex independent auditor agent, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-data-import

Generated: 2026-09-25
Source: `mrsonord2240/optimized-scientific-skills@2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-proteomics-data-import`
Audit: independent scientific re-audit of an immutable checkout (`auditor_independent: true`)
Category: Data Analysis · Mode D · Complexity: Complex → 7 inputs

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---:|---:|---:|---:|---|---|
| 1 | Canonical — MaxQuant LFQ cleaning | 39 | 58 | 97 | 5/5 | yes | ✅ |
| 2 | Variant A — DIA-NN global FDR | 39 | 58 | 97 | 5/5 | yes | ✅ |
| 3 | Edge — mixed mzML/AIF | 39 | 57 | 96 | 5/5 | yes | ✅ |
| 4 | Variant B — column choice + QFeatures | 36 | 53 | 89 | 4/5 | yes | ✅ |
| 5 | Stress — combined DDA/DIA missingness | 38 | 56 | 94 | 5/5 | yes | ✅ |
| 6 | Scope Boundary — corrected TMT import | 39 | 58 | 97 | 5/5 | yes | ✅ |
| 7 | Adversarial — flagless wrong table | 39 | 57 | 96 | 5/5 | yes | ✅ |

**Execution average: 95.1/100**
**Layer 1 average: 38.4/40**
**Layer 2 average: 56.7/60**
**Assertion pass rate: 34/35 (97.1%)**

The five original input families were rerun as regressions. Inputs 6 and 7 are fresh, deterministic cases created for this independent audit. All data created here is synthetic; the inherited regression fixtures were already synthetic.

## Step 1 — Structural Veto

| Gate | Result | Evidence |
|---|---|---|
| Operational stability | PASS | Seven intended input cases completed; the exact QFeatures example has a clean WSL route. The known auxiliary native Windows teardown crash is explicitly treated as failure rather than hidden. |
| Structural consistency | PASS | Frontmatter, scope, supported routes, and error contracts are coherent. |
| Result determinism | PASS | New fixtures use seed `20260925`; repeated runs produced the same asserted counts. |
| System security | PASS | No raw-string code execution, credentials, destructive operations, or remote data submission. |

## Step 2 — Static Evaluation

| Category | Criteria scores | Total |
|---|---|---:|
| Functional Suitability | Completeness 4, Correctness 3, Appropriateness 4 | 11/12 |
| Reliability | Fault Tolerance 4, Error Reporting 4, Recoverability 4 | 12/12 |
| Performance & Context | Token Cost 3, Execution Efficiency 4 | 7/8 |
| Agent Usability | Learnability 4, Consistency 3, Feedback 3, Error Prevention 4 | 14/16 |
| Human Usability | Discoverability 4, Forgiveness 4 | 8/8 |
| Security | Credential Safety 4, Input Validation 4, Data Safety 4 | 12/12 |
| Maintainability | Modularity 4, Modifiability 3, Testability 4 | 11/12 |
| Agent-Specific | Trigger Precision 4, Progressive Disclosure 3, Composability 4, Idempotency 4, Escape Hatches 4 | 19/20 |

**Static subtotal: 94/100.** The only executed correctness gap is the QFeatures route's retention of 55 all-missing groups. It is isolated, visible, and does not invalidate the successfully imported measurements.

## Detailed Outputs

### Input 1 — Canonical MaxQuant LFQ cleaning

**Prompt:** “I've got a MaxQuant 2.x proteinGroups.txt from 8 LFQ runs (4 control, 4 treated). Load it in Python, get rid of decoys, contaminants and only-by-site hits, and give me a clean log2 LFQ matrix with protein and gene labels. How many proteins am I left with?”

**Executed code:** [`run/input1_maxquant_lfq.py`](run/input1_maxquant_lfq.py)
**Log:** [`run/input1_maxquant_lfq.stdout.log`](run/input1_maxquant_lfq.stdout.log)

```text
rows_read: 1560
after_bookkeeping: 1500
quantified: 1445
samples: 8
infinite_values: 0
all_missing_groups: 0
decoy_or_contaminant_survivors: 0
```

The result fully closes the original silent all-missing-row problem while retaining the correct leading protein/gene and zero-to-missing behavior.

**Scores:** Basic 39/40 · Specialized 58/60 · **97/100**

**Assertions:**

- PASS — Decoy, contaminant, and site-only bookkeeping rows were removed.
- PASS — The result contained 1445 quantified groups across eight samples.
- PASS — No zero became an infinite log2 value.
- PASS — No delivered group was all missing.
- PASS — The workflow was read-only.

### Input 2 — DIA-NN global FDR and zero handling

**Prompt:** “Import our DIA-NN 1.9 report.parquet (8 runs) and build a protein-by-run matrix at 1% FDR that I can take into limma.”

**Executed code:** [`run/input2_diann.py`](run/input2_diann.py), loading the copied exact packaged [`load_diann.py`](run/source_examples/load_diann.py)
**Log:** [`run/input2_diann.stdout.log`](run/input2_diann.stdout.log)

```text
raw_rows: 23020
protein_groups: 887
runs: 8
lowconf_groups_in_matrix: 0
infinite_values: 0
```

The original 60 experiment-wide low-confidence groups no longer leak into the matrix, and PG.MaxLFQ zeros no longer become `-Inf`.

**Scores:** Basic 39/40 · Specialized 58/60 · **97/100**

**Assertions:** 5/5 PASS — readable schema; global protein FDR enforced; expected dimensions; no infinity; import-only/read-only scope.

### Input 3 — Mixed mzML with all-ion and unknown-window scans

**Prompt:** “Here's an mzML from msconvert (mostly DDA, a few DIA windows and one all-ion scan at the end). Read it with pyOpenMS and give me, per MS2 scan, the precursor m/z, charge and isolation-window width, plus peak counts for the MS1s.”

**Executed code:** [`run/input3_mzml.py`](run/input3_mzml.py), loading the copied exact packaged [`inspect_mzml.py`](run/source_examples/inspect_mzml.py)
**Log:** [`run/input3_mzml.stdout.log`](run/input3_mzml.stdout.log)

```text
ms1: 4
ms2: 16
ms2_without_precursor: 1
offsets_unknown: 1
```

The loop completes on the precursor-less AIF scan and distinguishes absent offsets from a literal 0-Th window.

**Scores:** Basic 39/40 · Specialized 57/60 · **96/100**

**Assertions:** 5/5 PASS — matching reader; correct MS counts; safe precursor guard; unknown-offset reporting; read-only scope.

### Input 4 — Quant column choice and QFeatures

**Prompt:** “My proteinGroups.txt has Intensity, iBAQ and LFQ intensity columns — which one should I use to compare treated vs control, and why? One treated run (T4) looked weak on the instrument. I work in R, so show me how to get it into QFeatures.”

**Executed code:**

- [`run/input4_column_choice.py`](run/input4_column_choice.py)
- Exact packaged [`load_maxquant_qfeatures.R`](run/source_examples/load_maxquant_qfeatures.R)
- [`run/input4_qfeatures_wsl.sh`](run/input4_qfeatures_wsl.sh)
- [`run/input4_qfeatures_assert.R`](run/input4_qfeatures_assert.R)

**Logs:** [`column-choice stdout`](run/input4_column_choice.stdout.log), [`WSL stdout`](run/input4_qfeatures_wsl.stdout.log), [`WSL stderr`](run/input4_qfeatures_wsl.stderr.log), [`Windows stdout`](run/input4_qfeatures_windows.stdout.log), [`Windows stderr`](run/input4_qfeatures_windows.stderr.log)

```text
Intensity T4 residual: -1.331 log2
iBAQ T4 residual:      -1.331 log2
LFQ T4 residual:        0.014 log2
max within-protein SD log2(iBAQ/Intensity): 0.0

R 4.5.2 | QFeatures 1.20.0 | cli 3.6.6
QFeatures log2 LFQ: 1500 protein groups x 8 samples | -Inf: FALSE
Independent QFeatures assertions: rows=1500 samples=8 all-missing=55 -Inf=FALSE
```

The clean supported WSL route exited `0`. The auxiliary native Windows route printed the same correct `1500 × 8` summary, then segfaulted with exit `139`; this is failure evidence consistent with the Skill's documented `cli.dll` teardown limitation, not a success claim.

One assertion failed: QFeatures retains 55 groups with no quantified value, whereas the Python route drops them and returns 1445. This is a P2 consistency/QC issue, not a veto or deployment blocker.

**Scores:** Basic 36/40 · Specialized 53/60 · **89/100**

**Assertions:**

- PASS — LFQ removes the weak-loading artifact for between-sample comparison.
- PASS — iBAQ behaves as a within-sample proxy, not a normalized cross-sample column.
- PASS — The exact QFeatures example completes in WSL with no infinity.
- **FAIL — The QFeatures result does not remove 55 all-missing groups.**
- PASS — Inputs remain read-only and the native nonzero exit is not mislabeled as success.

### Input 5 — Combined DDA/DIA missingness diagnosis

**Prompt:** “We ran the same 8 samples by DDA (MaxQuant proteinGroups.txt) and DIA (DIA-NN report.parquet). Load both, tell me how much is missing in each, whether it looks MNAR or MCAR, and which imputation I should use for each before limma. How many proteins overlap?”

**Executed code:** [`run/input5_combined_missingness.py`](run/input5_combined_missingness.py)
**Log:** [`run/input5_combined_missingness.stdout.log`](run/input5_combined_missingness.stdout.log)

```text
DDA: 1445 groups x 8, missing 14.533%, abundance-missing corr -0.619
DIA:  887 groups x 8, missing  8.300%, abundance-missing corr -0.495
overlap: 864
```

DIA has fewer missing values, but both negative correlations support abundance-dependent missingness; the Skill now chooses the downstream imputation class from the diagnostic rather than asserting DIA is MCAR.

**Scores:** Basic 38/40 · Specialized 56/60 · **94/100**

**Assertions:** 5/5 PASS — corrected imports; DDA signature; DIA signature; overlap/downstream route; no testing or mutation.

### Input 6 — Fresh corrected-TMT boundary case

**Prompt:** “This MaxQuant TMT10 proteinGroups.txt already contains corrected reporter intensities. Import the ten sample channels without using the single group-total Intensity field, remove bookkeeping rows, and return a finite log2 matrix. Do not recompute reporter correction.”

**Data generation:** [`run/generate_new_inputs.py`](run/generate_new_inputs.py), seed `20260925`
**Executed code:** [`run/input6_tmt.py`](run/input6_tmt.py)
**Log:** [`run/input6_tmt.stdout.log`](run/input6_tmt.stdout.log)

```text
protein_groups: 389
reporter_channels: 10
matrix_columns_including_labels: 12
infinite_values: 0
missing_values: 1
single_group_total_intensity_used: false
```

Ten bookkeeping rows and one target with no quantified reporter value were removed. The importer selected only already-corrected channels and respected the boundary to quantification.

**Scores:** Basic 39/40 · Specialized 58/60 · **97/100**

**Assertions:** 5/5 PASS — channel selection; no total-Intensity substitution; row QC; zero handling; scope/read-only behavior.

### Input 7 — Fresh adversarial wrong-table case

**Prompt:** “This looks like proteinGroups.txt and has Protein IDs plus LFQ columns, but our exporter removed Reverse, Potential contaminant and Only identified by site. Load it anyway and assume all rows are targets.”

**Data generation:** [`run/generate_new_inputs.py`](run/generate_new_inputs.py), seed `20260925`
**Executed code:** [`run/input7_wrong_table.py`](run/input7_wrong_table.py)
**Log:** [`run/input7_wrong_table.stdout.log`](run/input7_wrong_table.stdout.log)

```text
rejected: true
exception: ValueError
message: Expected MaxQuant proteinGroups.txt bookkeeping columns; received none of Reverse, Potential contaminant, Only identified by site
input_rows_unchanged: 2
```

Strict rejection is the scientifically safe behavior: silently assuming absent search-engine flags would defeat the import contract.

**Scores:** Basic 39/40 · Specialized 57/60 · **96/100**

**Assertions:** 5/5 PASS — rejection; specific error; deterministic preservation; no fabricated clean matrix; safe failure path.

## Research Veto

| Dimension | Result | Detail |
|---|---|---|
| Scientific integrity | PASS | Every numerical claim is present in retained logs; no paper identifiers or results were fabricated. |
| Practice boundaries | PASS | Technical import and missingness diagnosis only; no clinical action. |
| Methodological ground | PASS | FDR, zero, quant-family, TMT, and missingness contracts are scientifically coherent in all executed cases. |
| Code usability | PASS | All intended workflows run; the exact QFeatures example has a verified zero-exit WSL route. The native Windows teardown crash is correctly documented and retained as failed evidence. |

## Final Arithmetic and Floors

```text
Static:  94 × 0.4 = 37.6
Dynamic: 95.1 × 0.6 = 57.1
Total:                94.7 → 95
```

Production Ready floors all pass:

- Static: 94 ≥ 80
- Execution: 95.1 ≥ 85
- Layer 1 average: 38.4 ≥ 32
- Layer 2 average: 56.7 ≥ 48
- Assertions: 34/35 = 97.1% ≥ 90%
- Structural veto: PASS
- Research veto: PASS
- Open P0: none

**Final: 95/100 — ⭐ Production Ready — deployable: true.**

## Recommendation

**P2 — Align QFeatures valid-row filtering with Python.** After creating `log2LFQ`, remove assay rows with no non-missing sample and report read, post-bookkeeping, and quantified counts. Add an assertion that no delivered row is all missing. Observed only in Input 4; no P0 or P1 remains open.

## Evidence Index

- Orchestration and exit codes: [`run/execute_all.ps1`](run/execute_all.ps1), [`run/execution-summary.json`](run/execution-summary.json)
- Regression fixture hashes: [`data/copied-file-hashes.json`](data/copied-file-hashes.json)
- Fresh fixture truth: [`data/new_input_truth.json`](data/new_input_truth.json)
- Source examples copied byte-for-byte for isolated execution: [`run/source_examples`](run/source_examples/)
- Full stdout and stderr for every execution are retained under [`run/`](run/).
