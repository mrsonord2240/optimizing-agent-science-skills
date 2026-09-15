> **Audit record for `bio-proteomics-proteomics-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/proteomics-qc) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-proteomics-qc
Generated: 2026-09-11 (sub-audit for `mass-spec-proteomics-analyst`, round 2, run 2)
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/proteomics-qc` (read-only)
Role in candidate: CORE (validation / QC gate)

All data used here is **SYNTHETIC**. It is copied from `audits/bio-workflows-proteomics-pipeline/data/` (generator `make_synthetic.py`, seed 20260911) into `data/`. `data/ptxqc_txt/` holds a copy of the two MaxQuant tables plus the PTXQC outputs. No real data was used and nothing was pip-installed.
Scripts and their captured stdout/stderr are in `runs/`. The SKILL.md functions are copied **verbatim** into `runs/skill_funcs.py`, which every Python input imports.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical: MaxQuant LFQ QC before limma | 30 | 44 | 74 | 3/5 | yes | ⚠️ |
| 2 | Variant A: DIA-NN report per-run IDs / global q | 32 | 48 | 80 | 4/5 | yes | ✅ |
| 3 | Edge: failed-loading T4 hidden by MaxLFQ | 30 | 42 | 72 | 3/5 | yes | ⚠️ |
| 4 | Variant B: TMT channel balance, 2 plexes | 29 | 42 | 71 | 4/5 | yes | ⚠️ |
| 5 | Stress: batch-dominated PCA + exclusion + sensitivity | 31 | 46 | 77 | 3/5 | yes | ✅ |

**Execution Average: 74.8 / 100** (374 / 5)
**Assertion Pass Rate: 17/25 (68%)**
**Executed: 5/5**

---

## Step 1 — Skill Veto

| Dimension | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | `examples/qc_analysis.py` exits 0. All SKILL.md functions run. The failures are input-dependent crashes, not random ones. |
| T2 Contract | PASS | Frontmatter has `name` and `description` (plus `tool_type`, `primary_tool`). The functions return DataFrames or tuples consistently. |
| T3 Determinism | PASS | Everything is deterministic (the PCA uses the full SVD). The example is seeded (`default_rng(0)`). Re-running gives identical output. |
| T4 Security | PASS | No `eval`/`exec`, no shell-outs, no network access. The example writes nothing to disk. |

## Step 2 — Static breakdown (25 criteria)

| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 2 | The description promises three levels. Code exists only for Level 3 matrix QC and contaminant stripping. Levels 1 and 2, TMT balance, DIA q-values and the contaminant fraction are prose or threshold rows only. |
| 1.2 | Correctness | 2 | `raw_sample_qc` silently reports 0% missing on MaxQuant zeros. The ">1% PTXQC" contaminant claim is misattributed. The MSstatsTMT "RAW" claim is false under default arguments. The "~14x" claim is scale-dependent. |
| 1.3 | Appropriateness | 3 | Inspect-before-normalize and the funnel framing are the right approach. Level 1 is over-promised given there is no raw-file tooling path. |
| 2.1 | Fault tolerance | 2 | `pca_batch_check` has three crash paths (RangeIndex annotation, all-NaN rows, n<5). None is caught or explained. |
| 2.2 | Error reporting | 2 | The Common Errors table maps symptoms to fixes for 7 cases. The code emits no messages of its own; the crash text is cryptic ("At least two samples are required; got 1"). |
| 2.3 | Recoverability | 3 | Pure, read-only analyses; re-running with fixed inputs is safe. |
| 3.1 | Token cost | 2 | The 276-line, 25.7 KB SKILL.md is loaded whole, including Level-1 prose and 13 references. There is no references/ split. |
| 3.2 | Execution efficiency | 3 | Linear workflow. Minor waste: StandardScaler is fitted twice, and `abundance_bins` is computed and discarded. |
| 4.1 | Learnability | 3 | The funnel, the ordering and the decision tree are very clear. Mapping "un-normalized" to real columns needs outside knowledge. |
| 4.2 | Consistency | 3 | The "2-3x below its group median" rule does not match the example's `total_signal < 0.5x`. "Never let batch dominate" conflicts with "batch in design". |
| 4.3 | Feedback design | 2 | No QC-report or exclusion-decision template; the functions print or return ad hoc. |
| 4.4 | Error prevention | 3 | A strong failure-mode section (7 modes). It misses the two most common MaxQuant pitfalls: 0 = missing, and LFQ is already normalised. |
| 5.1 | Discoverability | 4 | Natural trigger language: "assessing data quality, diagnosing outlier samples, deciding which samples to exclude". |
| 5.2 | Forgiveness | 2 | Input requirements (NaN for missing, sample-indexed annotation) are not stated, so wrong input is computed silently instead of rejected (Category 3 Override 2 applied). |
| 6.1 | Credential safety | 4 | No credentials involved. |
| 6.2 | Input validation | 2 | None, as in the shared template; no injection surface. |
| 6.3 | Data safety | 4 | Read-only; the example writes nothing. |
| 7.1 | Modularity | 3 | Small single-purpose functions, but everything sits inline in SKILL.md. |
| 7.2 | Modifiability | 3 | Thresholds are centralised in one table; the functions are independent. |
| 7.3 | Testability | 3 | One seeded, self-contained example; no per-function tests. |
| 8.1 | Trigger precision | 4 | The description itself routes normalisation, testing and DIA internals to sibling Skills. |
| 8.2 | Progressive disclosure | 2 | Under 500 lines, but no references/ folder; everything is in SKILL.md. |
| 8.3 | Composability | 3 | DataFrame in, DataFrame out; all six related Skills exist. |
| 8.4 | Idempotency | 4 | Stateless and read-only. |
| 8.5 | Escape hatches | 2 | Routing lines only. No stop conditions (n<5, no raw column available, exclusion needs human sign-off). |

**Static subtotal: 7 + 7 + 5 + 11 + 6 + 10 + 9 + 15 = 70 / 100**

## Gate 8 — shipped-means-present

- SKILL.md and usage-guide.md contain **no** pointers to `references/` or `scripts/`, and none exist, which confirms the lead's finding. The only path-like token is "PTXQC `createYaml.R`", a file in the upstream PTXQC package. Its 20/35% ID-rate bins were confirmed in the YAML that PTXQC 1.1.5 wrote (`IDRate: Thresh_bad_num: 20.0, Thresh_great_num: 35.0`).
- Related Skills all exist at the pinned commit: `proteomics/{data-import, quantification, differential-abundance, dia-analysis}`, `data-visualization/dimensionality-reduction-plots`, `workflows/proteomics-pipeline`.
- `examples/qc_analysis.py` exists. SKILL.md does not reference it.
- **No missing primary file, so no P0.**

## Step 3 — Classification

- Category 3 **Data Analysis**, execution **Mode A** (no scripts; the agent writes code from the SKILL.md patterns).
- Complexity **Moderate → N = 5**. There are three QC levels, but only one executable code path (matrix-level pandas/sklearn), 1 example, and no reference files. Branching (MaxQuant / DIA / TMT) is described in the decision tree without dedicated code, so N = 7 is not warranted.

## Example smoke test

`python examples/qc_analysis.py` → exit 0 (`runs/example_smoke.out`). It flags `ctrl_3` (0.30x total signal), reports contaminants at 4.4%, within-group r 0.973-0.975, CV 14.0% / 17.3%, present fraction 0.86 → 1.00, and PC1 ~ condition p = 0.0001. The example is internally consistent with the Skill's principles.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Attached is proteinGroups.txt from MaxQuant 2.x (LFQ, match-between-runs on) for 4 control and 4 treated samples. We ran them over two days; sample_annotation.csv has the day as `batch`. Before I run limma, can you QC it — contaminants, whether any sample is off, how well replicates agree, CVs, missing values, and whether the batch is going to be a problem?"

**Code:** `runs/in1_canonical.py` (SKILL.md functions verbatim), `runs/in1_ptxqc.R` (Decision Tree row 1). **Executed:** yes.

**What it printed (trimmed, `runs/in1_canonical.out`):**
```
rows 1560 | flags: {'Potential contaminant': 20, 'Reverse': 25, 'Only identified by site': 15}
Contaminant % of summed raw Intensity per sample: C1 4.70 C2 6.52 C3 4.19 C4 5.01 T1 4.97 T2 4.22 T3 5.53 T4 4.81
After strip_contaminant_rows: 1500 rows (removed 60 )
raw_sample_qc AS WRITTEN (zeros left in):   n_quantified 1500 for all 8, missing_pct 0.0 for all 8
raw_sample_qc with 0->NaN: n_quantified 1207-1329, missing 11.4-19.5%, fold_vs_group_median_total 0.770-1.184
Samples >=2x below group median (total or median): []
Within-group Pearson r (log2 LFQ): 0.956-0.966; no sample correlates better with the other group
median_cv_linear: Control 24.27  Treatment 23.57
  Control: geometric CV from log2 = 25.00% | base formula on log2 = 1.44% | linear/log ratio = 16.9x | mean log2 = 24.7
Present fraction by mean-abundance quintile: 0.539, 0.887, 0.935, 0.953, 0.960   (rising = MNAR)
completeness_filter(0.7): 1500 -> 1323 rows; all-NaN rows before filter: 55
[G1] pca_batch_check(filt, info) with info as read_csv returns it: ERROR: TypeError At least two samples are required; got 1.
[G2] pca_batch_check on the UNFILTERED matrix: ERROR: ValueError Input X contains NaN.
[G3] PC1 ~ batch: p=0.0000 | explained [0.251 0.167 0.125 ...] | PC1 ~ condition p=0.9484, PC2 ~ condition p=0.0000
```
**PTXQC** (`runs/in1_ptxqc.out`): `createReport(txt_folder=...)` on a folder holding only proteinGroups.txt and evidence.txt **ran** in 0.6 min. It computed 37 metrics and wrote a PDF, heatmap, yaml and mzQC. It skipped summary.txt, parameters.txt, msms.txt, msmsScans.txt and mqpar.xml with warnings. The HTML report was not built because pandoc is absent. The EVD Contaminants score was NA because the synthetic evidence has no CON rows. It needs nothing beyond the txt folder.

**Answer to the researcher (as Claude-with-Skill):** 60 bookkeeping rows were removed before any transform. Contaminants are 4-6.5% of raw signal, uniform across groups. No sample is a loading or injection failure. Replicate r of about 0.96 and a linear CV of about 24% are in the biological range. Missingness is left-censored (MNAR), so impute low rather than kNN, and filter to 70% valid in at least one condition first. Batch (day) is PC1 and condition is PC2. The design is balanced, so put `batch` in the limma design.

**Scores:** Basic 30/40 (FC 7: three adaptations needed; Rel 6: two crash paths plus one silent-wrong; Eff 8; Scope 9) | Specialized 44/60 (Method 16, Code 9, Data QC 8, Repro 6, Security 5) | **Total 74**

**Assertions:**
- [PASS] Contaminant, reverse and site-only rows removed before log/normalise — 1560 → 1500
- [FAIL] raw_sample_qc as written reports differing per-sample ID counts on MaxQuant input — 1500 and 0.0% for all
- [FAIL] pca_batch_check runs on sample_info as loaded — TypeError from the `.join` on a RangeIndex
- [PASS] Batch detected as the dominant axis, with a design-level remedy — PC1 p<1e-4
- [PASS] Scope: stays at QC and routes the test out

### Input 2 — Variant A
**Prompt:** "Here's the DIA-NN 1.9 report.parquet for the same 8 samples. How many protein groups do I actually have at 1% FDR, per run and overall? Do any runs look weak before I build the protein matrix and do stats?"

**Code:** `runs/in2_dia.py`. The Skill has no DIA code; the filter follows Decision Tree row 7 and the Thresholds row "DIA precursor + protein q both <= 0.01, GLOBAL q". **Executed:** yes.

**Printed (trimmed):**
```
rows 23020 runs 8 protein groups 947
Protein groups, run-level q only : 947  (LOWCONF: 60)
Protein groups, + global q <= 0.01: 887  (LOWCONF: 0)
Per-run: precursors 2458-2562, protein_groups 798-839 (0.970-1.020x), raw Precursor.Quantity 0.737-1.263x
PG.MaxLFQ matrix (887, 8); exact zeros: 61
[as written, zeros in] r 0.983-0.990 ; median_cv_linear Control 17.78 Treatment 17.24
[0 -> NaN]            r 0.983-0.990 ; median_cv_linear Control 17.43 Treatment 16.89
PC1 ~ batch p=0.0000 (39.9%)
```
**Answer:** 887 protein groups at 1% global precursor and protein q. Run-level q alone would admit 60 extra single-hit groups. No weak run: IDs fall within ±3%, and C2 has the lowest raw signal at 0.74x, which is a watch item and not a failure. Batch again dominates PC1.

**Scores:** Basic 32 (FC 8, Rel 7, Eff 8, Scope 9) | Specialized 48 (Method 17, Code 11, Data QC 8, Repro 7, Security 5) | **Total 80**

**Assertions:**
- [PASS] Global q filters remove every group that passes only run-level q (60 → 0)
- [PASS] Per-run precursor and protein-group counts reported
- [PASS] Raw per-run signal taken from a non-normalised quantity (Precursor.Quantity; the Skill does not name it)
- [FAIL] The Skill warns that PG.MaxLFQ zeros are missing — not mentioned; CV 17.78% versus 17.43%
- [PASS] Scope: q internals routed to dia-analysis

### Input 3 — Edge
**Prompt:** "Same experiment, but this is the re-searched table (proteinGroups_failed.txt). The LFQ intensity boxplots all line up nicely, so I think every sample is fine. Can you just confirm nothing needs excluding before I run limma?"

**Code:** `runs/in3_failed_sample.py`, `runs/in3_aswritten.py`. **Executed:** yes.

Following the Skill: Decision Tree row "Boxplots flat but a sample feels wrong → Re-plot the RAW matrix", then the l.103 rule "a sample shifted >=2-3x below its group median is a loading/injection failure".

**Printed (T4 rows; other samples 0.72-1.20x):**
```
                       column          n_quant  missing%  fold_total  fold_median  ids_vs_group  flag_2x
proteinGroups.txt      LFQ / Intensity  1278/1303  14.8/13.1  1.08/1.11   1.03/1.07    1.04/1.03     no/no
proteinGroups_failed   LFQ intensity    1004       33.1       1.021       1.414        0.817         no
proteinGroups_failed   Intensity        1031       31.3       0.409       0.621        0.814         YES
AS WRITTEN (zeros kept), failed file:  LFQ -> T4 1500 IDs, 0.0% missing, total 1.021x, median 0.994x
                                       Intensity -> T4 total 0.390x, median 0.372x
after median normalisation: all log2 medians 0.00; T4 within-group r 0.952-0.956 (above the 0.8 floor)
```
**Lead's question answered:** the Skill steers only to "the un-normalized matrix". It never says that MaxQuant's `LFQ intensity` is already MaxLFQ-normalised, or that `Intensity` is the raw column. On the column this user is looking at (LFQ), T4 is **not** flagged by the Skill's rule. With zeros left in, it is not visible at all. On `Intensity`, T4 is flagged by total signal (2.4x low). Its boxplot median is only 1.6x low, because left-censoring removed its low values, so a reader applying "2-3x" to the boxplot would miss it. On the clean `proteinGroups.txt` nothing is flagged on either column. As Claude-with-Skill I re-plotted raw Intensity and recommended excluding T4.

**Scores:** Basic 30 (FC 7, Rel 6, Eff 8, Scope 9) | Specialized 42 (Method 15, Code 9, Data QC 7, Repro 6, Security 5) | **Total 72**

**Assertions:**
- [PASS] T4 flagged from raw signal — total 0.409x, IDs 0.81x
- [FAIL] The Skill identifies which MaxQuant column is un-normalised
- [FAIL] raw_sample_qc as written exposes T4's ID/missing drop
- [PASS] Shows that normalisation erases the evidence
- [PASS] Safety: exclusion documented and left to the researcher

### Input 4 — Variant B
**Prompt:** "We ran two TMT10plex batches (plex A and B), each with a pooled reference in 131. Attached are the protein-level reporter intensities from PD and the channel design. Is any channel under- or over-loaded enough to drop before we normalise, and can we compare samples across the two plexes?"

**Code:** `runs/in4_tmt.py` (agent-written; the Skill has no TMT Python), `runs/in4_msstatstmt.R` and `runs/in4_msstatstmt_nonorm.R` (MSstatsTMT 2.14.2; the protein-level table was converted to one pseudo-PSM per protein, since `dataProcessPlotsTMT` needs `proteinSummarization` output). **Executed:** yes.

**Printed (trimmed):**
```
fold_total_within_plex: A 0.921-1.322, B 0.892-1.208  -> Within-plex flags: []
Plex B / plex A median total ratio: 2.08
PCA raw log2 reporters: PC1 ~ plex p=0.0000 (61.2%), PC1 ~ condition p=0.959
PCA log2 ratio to 131:  PC1 ~ plex p=0.936, PC1 ~ condition p=0.0000
Observed vs true log2FC slope on 51 true DA proteins: 0.60
MSstatsTMT default (global_norm=TRUE): FeatureLevelData median log2 = 24.73 in all 20 channels  -> QCPlot shows normalised data
MSstatsTMT global_norm=FALSE:          channel medians 23.96-24.52 (A), 24.93-25.39 (B)
```
**Answer:** no channel deviates by more than 1.32x within its plex, so there is nothing to drop. The 2x plex offset is an elution-sampling effect, so compare across plexes only through the 131 ratio. The ratio view makes condition PC1. Expect compression (fold changes about 0.6 of true).

**Scores:** Basic 29 (FC 7, Rel 6, Eff 7, Scope 9) | Specialized 42 (Method 15, Code 8, Data QC 7, Repro 7, Security 5) | **Total 71**

**Assertions:**
- [PASS] Within-plex channel totals, none above 2x
- [FAIL] The Skill's named tool shows raw imbalance with its defaults — global_norm=TRUE equalises channels
- [PASS] Plex offset handled via the reference channel, not flagged as a channel failure (agent judgement)
- [PASS] Ratio compression quantified (slope 0.60)
- [PASS] Scope: normalisation mechanics routed to quantification

### Input 5 — Stress
**Prompt:** "PCA on our LFQ data is dominated by processing day, not treatment, and T4 is a bit suspicious. I need a defensible, documented call for the methods section: (1) do we exclude T4, (2) how do we deal with the batch before limma, and (3) show me that the result doesn't hinge on the T4 decision."

**Code:** `runs/in5_stress.py`, `runs/in5_limma_sensitivity.R` (limma 3.62.2; the test is used only to measure how the QC decisions move the hit list, per the usage-guide Tip on sensitivity checks). **Executed:** yes.

**Printed (trimmed):**
```
[all 8] PC1 ~ batch p=0.0005 (23.8%) ; T4 PC1 = 2.27 (B1 samples about -16, B2 about +20)
distance to own-group centroid: T4 10.9 (smallest), others 16.7-39.2
[batch-centred view, plots only] PC1 ~ batch p=0.99, PC1 ~ condition p=0.0001
[4-sample pilot] ValueError n_components=5 must be between 0 and min(n_samples, n_features)=4
 samples batch_in_design n_sig true_pos false_pos sens
   all 8           FALSE    81       81         0 0.862
   all 8            TRUE    84       82         2 0.872
 drop T4           FALSE    78       78         0 0.830
 drop T4            TRUE    84       83         1 0.883
Overlap (batch in design): shared 82, Jaccard 0.95
```
**Answer:** (1) Exclude T4 as a loading failure: raw total 0.41x, IDs -19%, 31% missing (Input 3). The PCA does not isolate T4, because the Skill's row-median fill makes its many missing values look average. (2) The layout is balanced, so model `~ condition + batch`. Use a batch-centred matrix for PCA plots only. (3) The hit lists with and without T4 share 82 of 86 proteins, so the decision does not drive the result.

**Scores:** Basic 31 (FC 8, Rel 7, Eff 7, Scope 9) | Specialized 46 (Method 15, Code 10, Data QC 8, Repro 8, Security 5) | **Total 77**

**Assertions:**
- [PASS] Exclusion documented with raw evidence plus a sensitivity check
- [PASS] Batch added to the design rather than ComBat-then-test
- [FAIL] pca_batch_check shows the failed sample isolated — T4 is closest to its group centroid
- [FAIL] pca_batch_check runs at small n — n=4 ValueError
- [PASS] Safety: research QC only; the final call is left to the researcher

---

## Lead's leads — confirmed or refuted

1. **Column steering / T4:** **CONFIRMED.** The Skill never names the raw column. On `LFQ intensity`, T4 is not flagged (1.02x total, 1.41x median). On `Intensity` it is flagged by total signal (0.41x) but only borderline by median (0.62x). The verbatim `raw_sample_qc` with MaxQuant zeros hides the ID drop entirely. `proteinGroups.txt`: nothing flagged, correctly.
2. **pca_batch_check:** **CONFIRMED on all three points.** (a) All-NaN rows stay NaN → `ValueError: Input X contains NaN` (from PCA, after StandardScaler RuntimeWarnings). (b) `.join` with a RangeIndex annotation → `TypeError: At least two samples are required; got 1.` (c) Batch association is real: PC1 ~ batch p<1e-4, condition on PC2. New finding: `n_components=5` fails at n<5, and the median fill pulls a high-missing sample to the centre.
3. **missingness_profile / CV:** `abundance_bins` is dead code (**confirmed**). `completeness_filter` works (1500 → 1323). Linear CV 24.3% and geometric CV 25.0% agree. The base formula on log2 gives 1.44%, a compression of **16.9-17.1x** at mean log2 24.7. The "~14x" claim roughly holds but is scale-dependent (about ln2 × mean log2).
4. **PTXQC:** **RUNS.** It needs only the txt folder. Missing tables and mqpar.xml are skipped with warnings. PDF/yaml/heatmap/mzQC are written; the HTML needs pandoc.
5. **Contaminants:** 20 CON__ rows, 4.2-6.5% of raw Intensity, uniform across groups. `strip_contaminant_rows` removes them correctly. The Skill has no code for the fraction. Its "PTXQC default flags >1%" is PTXQC's user-defined MYCOPLASMA threshold; the general contaminant metric is a continuous score (confirmed from PTXQC 1.1.5 help text and YAML). **Misattribution confirmed.**

## Research Veto

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated values or identifiers. PTXQC ID-rate bins verified. The PTXQC 1% attribution is wrong (P2), not fabricated. |
| M2 Practice boundaries | PASS | No individual-level diagnosis or triage. |
| M3 Methodological ground | PASS | Core methods verified by running them. The batch wording is inconsistent (P2). |
| M4 Code usability | PASS | All functions parse and run on current pandas/sklearn; the example exits 0; PTXQC and MSstatsTMT calls ran. The crash paths are input-dependent (P1). |

## Final arithmetic

- Static 70 × 0.4 = **28.0**
- Execution average (74 + 80 + 72 + 71 + 77) / 5 = 74.8; × 0.6 = **44.9**
- Final = 72.9 → **73** → band **⚠️ Beta Only**
- Floors (for information; already Beta): static 70 (Limited-Release floor 70 met); exec 74.8 (< 75); L1 30.4 (met); L2 44.4 (met); assertions 68% (< 80%)
- Safety/scope assertion FAILs: 0 → no safety downgrade
- **Deployable: false.** Veto override: false.

## Recommendations
- **[P1] raw_sample_qc counts MaxQuant zeros as quantified** (Inputs 1, 3). Add `.replace(0, np.nan)` and state that 0 = missing.
- **[P1] Name the un-normalised column per tool** (Inputs 2, 3). MaxQuant `Intensity`, not `LFQ intensity`; DIA-NN `Precursor.Quantity`. Apply the 2x rule to total signal, and add an ID-count drop threshold.
- **[P1] pca_batch_check brittleness** (Inputs 1, 5). Assert a sample-indexed annotation, `dropna(how='all')`, use `n_components=min(5, n-1)`, and avoid the row-median fill for high-missing samples.
- **[P1] MSstatsTMT QC plot is post-normalisation by default** (Input 4). Document `global_norm=FALSE` and the PSM-level input requirement, and add pandas within-plex balance code.
- **[P2] PTXQC ">1%" contaminant claim misattributed** (Input 1). Add contaminant-fraction code.
- **[P2] Dead `abundance_bins`; the "~14x" claim is scale-dependent** (Input 1).
- **[P2] Batch guidance inconsistent; no QC-report template or stop conditions** (Inputs 2, 4, 5).

## Unverified
- The DIA-NN claim that "High precision silently median-normalizes, halving median CV vs High accuracy" (no DIA-NN build here).
- Level-1 tools (RawTools, RawBeans, rawrr, rawDiag, QuaMeter, Panorama AutoQC) were not run: no vendor raw files, no Windows builds installed.
- The literature references were not checked online. They are plausible citations with no DOIs given.
