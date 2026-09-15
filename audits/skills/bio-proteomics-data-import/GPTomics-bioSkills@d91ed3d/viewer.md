> **Audit record for `bio-proteomics-data-import`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/data-import) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-data-import
Generated: 2026-09-11 · Sub-auditor for round-2 candidate `mass-spec-proteomics-analyst` · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/data-import` (clone HEAD verified = d91ed3d…; nothing written there)
Role in candidate: **CORE** (every analysis starts here) · Category 3 Data Analysis · Mode A · Complexity Moderate → N = 5

Environment: Python 3.12 venv `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst` (pandas 3.0.5, numpy 2.5.3,
pyOpenMS 3.5.0, pyarrow, scikit-learn, scipy); R 4.4.3 / Bioconductor 3.20 via `r.sh` (QFeatures 1.16.0). **Spectra is
not installed** (the Skill's `Spectra::Spectra()` route could not be run; not installed by rule). No package was pip-installed.
No external tools were needed (DIA-NN / MaxQuant were never called: the Skill only reads their outputs).

**All data are SYNTHETIC.** MaxQuant `proteinGroups.txt`, `proteinGroups_failed.txt`, DIA-NN 1.9-style `report.parquet`,
`truth_proteins.csv` were copied from `audits/bio-workflows-proteomics-pipeline/data/` (generator `make_synthetic.py`).
`data/synthetic_mixed.mzML` was built here with pyOpenMS by `data/make_mzml.py` (truth in `data/synthetic_mixed_truth.csv`).
Every script and its captured stdout/stderr is in `runs/`.

## Step 1 — Skill Veto
| Dimension | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | all 4 SKILL.md Python blocks parse (`runs/static_checks.log`); shipped example exits 0; Skill code ran on all 5 inputs; one edge crash (Input 3) is an unguarded index on 1 of 20 spectra, not a >20 % failure rate |
| T2 Contract | PASS | frontmatter `name`, `description` present; blocks return consistent DataFrames/dicts |
| T3 Determinism | PASS | no randomness in the Skill's code; in1/in2 re-run twice → identical stdout hashes (`runs/static_checks.log`) |
| T4 Security | PASS | no eval/exec/shell, no network, reads local files only |

## Step 2 — Static score: 79/100
| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 3 | mzML, MaxQuant, DIA-NN, missingness all have code; R route (Spectra/QFeatures) is named only, no code; mzXML named but no `MzXMLFile` pattern |
| 1.2 | Correctness | 2 | MaxQuant block correct; but DIA-NN filter omits `Global.PG.Q.Value` (60/60 LOWCONF groups leak, Input 2), DIA block has no 0→NaN (61 `-inf`), "DIA ≈ MCAR / tolerates standard imputers" is contradicted by the Skill's own diagnostic (Input 5), mzML loop crashes on precursor-less MS2 (Input 3), pyOpenMS cited to Chambers 2012 (that is ProteoWizard) |
| 1.3 | Appropriateness | 4 | pandas/pyOpenMS/pyarrow is the right weight for an import step |
| 2.1 | Fault tolerance | 2 | `.get()` flag guards and `Gene names` guard work; nothing catches empty `getPrecursors()`, a table with no `LFQ intensity` columns (silently returns a 2-column ID-only matrix, `runs/edge_no_lfq.log`), or DIA zeros |
| 2.2 | Error reporting | 3 | 7-row Common Errors table with causes and fixes; no raised/printed diagnostics in code |
| 2.3 | Recoverability | 3 | read-only, idempotent; introspect-and-adapt rule in Version Compatibility |
| 3.1 | Token cost | 3 | 225 lines / 18 KB, everything inline; acceptable, no layering |
| 3.2 | Execution efficiency | 4 | linear, minimal code paths |
| 4.1 | Learnability | 3 | clear; scale/zero handling for the DIA matrix before `assess_missingness` must be inferred |
| 4.2 | Consistency | 3 | DIA q-filter disagrees with sibling `dia-analysis` (`Global.PG.Q.Value <= 0.01` for cross-run matrices, its line 78/197); zero→NaN rule stated for MaxQuant only |
| 4.3 | Feedback design | 3 | Goal/Approach per block; no specified report (rows removed, valid values, -inf check) |
| 4.4 | Error prevention | 3 | excellent failure-mode section (wrong column, zeros, bookkeeping, razor IDs, stale DIA-NN); misses the global-FDR pitfall it exists to prevent |
| 5.1 | Discoverability | 3 | "Load my mass spec data into Python" + natural usage-guide prompts; description is jargon-dense |
| 5.2 | Forgiveness | 3 | tolerates absent/empty flag columns and blank genes; brittle on precursor-less scans / no-LFQ tables |
| 6.1 | Credential safety | 4 | none involved |
| 6.2 | Input validation | 3 | template-level: no column-presence checks (shared with the other eight Skills) |
| 6.3 | Data safety | 4 | local reads, no retention |
| 7.1 | Modularity | 3 | one section per format; fine |
| 7.2 | Modifiability | 3 | blocks independent |
| 7.3 | Testability | 3 | one self-contained runnable example (MaxQuant only); nothing for DIA-NN or mzML |
| 8.1 | Trigger precision | 3 | precise with routing-out lines; "starting from raw spectra" may pull RAW-conversion requests (routed to peptide-identification) |
| 8.2 | Progressive disclosure | 3 | ≤500 lines, no references (template) |
| 8.3 | Composability | 4 | explicit scope + 8 Related Skills, all exist |
| 8.4 | Idempotency | 4 | pure reads |
| 8.5 | Escape hatches | 3 | routing lines + keratin-of-interest caveat; no stop conditions (e.g. stop if no LFQ columns) |

Category totals: Functional 9/12 · Reliability 8/12 · Performance 7/8 · Agent usability 12/16 · Human usability 6/8 ·
Security 11/12 · Maintainability 9/12 · Agent-specific 17/20 = **79**.

## Gate 8 — shipped-means-present
SKILL.md and usage-guide.md point at no `references/` or `scripts/` files (confirmed: neither exists nor is referenced).
`examples/load_maxquant.py` exists. All eight Related Skills exist (`proteomics/{peptide-identification, quantification,
protein-inference, differential-abundance, proteomics-qc, dia-analysis}`, `expression-matrix/normalization`,
`workflows/proteomics-pipeline`). **PASS.**

Example smoke test (`runs/example_load_maxquant.log`): exit 0; 11 clean groups; "Missing: 22.7% | abundance-vs-missingness
corr: -0.84 (negative => MNAR)".

## Step 3 — Classification
Category 3 Data Analysis (code that loads/cleans MS data). Mode A (instructions + inline code, one example, no scripts/).
Complexity **Moderate → N = 5**: four task types (mzML, MaxQuant, DIA-NN, missingness diagnosis) with light branching
(column choice, acquisition mode), one example file, no references.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical — MaxQuant LFQ load | 37 | 53 | 90 | 4/5 | yes | ✅ |
| 2 | Variant A — DIA-NN parquet import | 30 | 35 | 65 | 3/5 | yes | ⚠️ |
| 3 | Edge — mzML precursor/isolation windows | 33 | 40 | 73 | 3/5 | yes (Skill loop crashed) | ❌ PARTIAL |
| 4 | Variant B — Intensity vs LFQ vs iBAQ (+QFeatures) | 36 | 50 | 86 | 4/5 | yes | ✅ |
| 5 | Stress — both tables + missingness + imputation advice | 30 | 40 | 70 | 3/5 | yes | ⚠️ |

**Execution Average: 384/5 = 76.8** · **Assertion pass rate: 17/25 (68 %)** · Layer 1 avg 33.2 · Layer 2 avg 43.6

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I've got a MaxQuant 2.x proteinGroups.txt from 8 LFQ runs (4 control, 4 treated). Load it in Python, get rid of
decoys, contaminants and only-by-site hits, and give me a clean log2 LFQ matrix with protein and gene labels. How many
proteins am I left with?"

**Code:** `runs/in1_maxquant_canonical.py` — Part A is the Skill's MaxQuant block verbatim; Part B the report to the user;
Part C auditor checks.

**Printed (`runs/in1.log`, trimmed):**
```
pandas 3.0.5 | numpy 2.5.3
rows read: 1560 | kept after flag filter: 1500 | removed: 60
  Reverse                  dtype=str      values={nan: 1535, '+': 25}
  Potential contaminant    dtype=str      values={nan: 1540, '+': 20}
  Only identified by site  dtype=str      values={nan: 1545, '+': 15}
protein groups with >=1 LFQ value: 1445 | all-NaN rows still in matrix: 55
-inf present after log2: False
[AUDIT] surviving REV__/CON__ IDs: 0
[AUDIT] blank leading_gene: 40 | semicolon genes in raw: 87 | duplicated leading_gene (non-blank): 0 | duplicated leading_protein: 0
[AUDIT] kept groups with Peptides < 2 (Skill threshold table says >=2, code does not apply it): 52
[AUDIT] all-empty flag column (float64 NaN) still filters correctly: 45 rows flagged (expect 45)
[AUDIT] missing flag column handled by .get default: 45 rows flagged (expect 45)
```
**Answer given:** 1,500 target groups after removing 25 decoys, 20 contaminants, 15 site-only; 1,445 have at least one LFQ
value (55 are all-NaN and should be dropped before stats); 40 groups have no gene name (label falls back to ''), 87 had a
semicolon gene list reduced to the leading gene. Normalization/imputation routed to differential-abundance.

Lead 4 (pandas 3.0 string dtype): **refuted as a defect.** Flag columns read as `str` dtype with NaN for blanks and '+';
`NaN != '+'` is True, so the mask is correct, including when a flag column is entirely empty (float64 NaN) or absent
(`.get` default ''). Blank and semicolon gene names are handled. 0→NaN works; no `-inf`.

**Scores:** Basic 37 (FC 9, clarity 9, efficiency 9, scope 10) · Specialized 53 (method 18, code 14, QC 8 — 55 all-NaN
rows kept and the ≥2-peptide threshold it lists is not applied, reproducibility 8, security 5) · **90**
**Assertions:**
- [PASS] Bookkeeping rows fully removed under pandas 3.0 str dtype (0 REV__/CON__ survive), also with an all-empty or absent flag column — 60/60 removed; 45 in both variants
- [PASS] No -inf after log2 — 0→NaN precedes log2
- [FAIL] Proteins with zero valid LFQ values are removed or flagged by the Skill's code — 55 all-NaN rows pass silently into the matrix
- [PASS] Scope: output stops at import/cleaning and routes normalization/imputation to differential-abundance — yes
- [PASS] Safety: no destructive operations; contaminant caveat (keratin of interest) available — read-only code

### Input 2 — Variant A
**Prompt:** "Import our DIA-NN 1.9 report.parquet (8 runs) and build a protein-by-run matrix at 1% FDR that I can take into
limma."

**Code:** `runs/in2_diann_import.py` — Skill block verbatim (`Q.Value <= 0.01 & PG.Q.Value <= 0.01`, pivot `PG.MaxLFQ`,
`aggfunc='first'`), then log2.

**Printed (`runs/in2.log`):**
```
RuntimeWarning: divide by zero encountered in log2
report rows: 23020 | after Q.Value & PG.Q.Value <= 0.01: 20286
matrix: 947 protein groups x 8 runs
-inf after log2: 61
[AUDIT] LOWCONF groups in raw report: 60
[AUDIT] LOWCONF groups surviving the Skill filter into the matrix: 60 | their non-missing cells: 116 | runs observed per LOWCONF group: {1: 24, 2: 16, 3: 20}
[AUDIT] LOWCONF Global.PG.Q.Value values: [0.04]
[AUDIT] PG.MaxLFQ == 0 cells carried into the matrix (Skill DIA block has no 0->NaN): 61 in 61 groups
[AUDIT] with Global.PG.Q.Value <= 0.01 added: (887, 8) | LOWCONF left: 0
[AUDIT] non-LOWCONF groups removed by the global filter: 0
[AUDIT] max distinct PG.MaxLFQ within a group x run: 1
```
Lead 1: **confirmed.** Following data-import as written, **all 60** LOWCONF groups (Global.PG.Q.Value 0.04) enter the
matrix — 60/947 = 6.3 % of rows, 116 cells, and 60 of the 91 groups observed in ≤ 3 runs. The Skill's own Quantitative
Thresholds row names `Q.Value AND PG.Q.Value` as "the DIA-NN import filter"; the sibling `dia-analysis` Skill (lines 78,
197, 211) and DIA-NN's maintainer guidance (GitHub discussions, see sources) say the cross-run protein matrix needs
`Global.PG.Q.Value <= 0.01`. Adding it removes exactly the 60 and nothing else. Separately, the DIA block never applies the
Skill's own 0→NaN rule: 61 PG.MaxLFQ zeros become `-inf` at log2. `aggfunc='first'` is safe (PG.MaxLFQ constant per group×run).

**Scores:** Basic 30 (FC 5, clarity 7, efficiency 9, scope 9) · Specialized 35 (method 10 — experiment-wide protein FDR
not controlled, code 9 — runs but yields a contaminated matrix with zeros, QC 4, reproducibility 7, security 5) · **65**
**Assertions:**
- [PASS] Skill code runs on the DIA-NN 1.9 parquet schema — exit 0, all columns found
- [FAIL] Matrix controls experiment-wide protein-group FDR (no LOWCONF groups) — 60/60 leak
- [FAIL] PG.MaxLFQ zeros converted to NaN before log2 — 61 -inf
- [PASS] Scope: import only; no test or normalization performed — yes
- [PASS] Safety: read-only; no destructive operations — yes

### Input 3 — Edge
**Prompt:** "Here's an mzML from msconvert (mostly DDA, a few DIA windows and one all-ion scan at the end). Read it with
pyOpenMS and give me, per MS2 scan, the precursor m/z, charge and isolation-window width, plus peak counts for the MS1s."

**Data:** SYNTHETIC `data/synthetic_mixed.mzML` (20 spectra: 4 MS1; 9 DDA MS2 0.8/0.8 Th; 4 DIA MS2 12.5/12.5 Th; 1 MS2
with offsets never written; 1 AIF MS2 with no precursor; 1 asymmetric 0.5/1.5 Th).
**Code:** `runs/in3_mzml.py` — Part A the Skill loop verbatim; Part B the same calls collected into a table; Part C a
guarded loop plus truth comparison.

**Printed (`runs/in3.log`, trimmed):**
```
pyopenms 3.5.0
load() returned: None | spectra: 20
Skill loop CRASHED at spectrum index 18:
    precursor = spectrum.getPrecursors()[0]  # getPrecursors returns a list
IndexError: list index out of range
types from get_peaks(): tuple ['ndarray', 'ndarray']
type of getPrecursors(): list
Part B stopped at spectrum 18: IndexError: list index out of range  (18 rows collected)
 i ms n_peaks  prec_mz   z   lo   hi                         flag
13  2     300 412.5000 0.0 12.5 12.5                     DIA-wide
17  2      60 733.3812 2.0  0.0  0.0     width 0: offsets missing
18  2     400      NaN NaN  NaN  NaN no precursor (AIF/MSE-style)
19  2      80 650.1234 3.0  0.5  1.5                   asymmetric
[AUDIT] peak counts match truth: True | precursor m/z match: True | offsets match: True
```
Lead 3: the Skill's API statements are **confirmed** on pyOpenMS 3.5.0 (`load` fills in place and returns None,
`get_peaks()` is a tuple of two ndarrays, `getPrecursors()` is a list, lower+upper offset = width; iterating an
`MSExperiment` works). Its loop **crashes** on a legitimate MS2 scan without a precursor element (AIF / bbCID-style) and
reports width 0 without comment when offsets were not written. The user-facing table required the guard in Part C.

**Scores:** Basic 33 (FC 6, clarity 8, efficiency 9, scope 10) · Specialized 40 (method 15, code 8 — crashes as written on
this input, QC 5, reproducibility 7, security 5) · **73**
**Assertions:**
- [PASS] pyOpenMS API claims hold on 3.5.0 and extracted m/z, offsets and peak counts match truth where the loop reaches — all True
- [FAIL] Loop completes on an MS2 spectrum without a precursor element — IndexError at spectrum 18
- [FAIL] Missing isolation-window offsets flagged rather than reported as width 0 — silent 0
- [PASS] Scope: no RAW conversion attempted; conversion routed to peptide-identification — yes
- [PASS] Safety: read-only; no destructive operations — yes

### Input 4 — Variant B
**Prompt:** "My proteinGroups.txt has Intensity, iBAQ and LFQ intensity columns — which one should I use to compare treated
vs control, and why? One treated run (T4) looked weak on the instrument. I work in R, so show me how to get it into QFeatures."

**Data:** SYNTHETIC `proteinGroups_failed.txt` (T4 loaded ~3× low; MaxLFQ re-normalised it).
**Code:** `runs/in4_columns.py` (Skill cleaning applied to each column family) and `runs/in4_qfeatures.R`.

**Printed (`runs/in4_columns.log`):**
```
complete-case proteins (valid in all 8 runs for all 3 columns): 657
column        T4 - median(others)  null-protein median T/C log2FC  valid T4
Intensity                   -1.28                          -0.424      1031
iBAQ                        -1.32                          -0.424      1031
LFQ intensity                0.13                          -0.066      1004
  Intensity      per-protein median (T4 - mean of other 7 runs) = -1.33 log2
  iBAQ           per-protein median (T4 - mean of other 7 runs) = -1.33 log2
  LFQ intensity  per-protein median (T4 - mean of other 7 runs) = +0.00 log2
max within-protein SD of log2(iBAQ/Intensity) across samples: 0.0
```
R (`runs/in4_qfeatures_attempt1.log`, then `runs/in4_qfeatures.log`):
```
features read: 1560
ATTEMPT 1 (backticked MaxQuant names) FAILED: 'Potential contaminant', 'Only identified by site' is/are absent from all rowData.
after flag filter: 1500
any -Inf: FALSE | NA %: 19.8
[AUDIT] all-empty site column (logical NA): features kept = 1515 (expect 1515: 25 REV + 20 CON removed, NA rows kept, not dropped)
```
**Answer given:** use `LFQ intensity` (MaxLFQ-normalised): T4's loading deficit (-1.33 log2 in Intensity and iBAQ) is gone
in LFQ (0.00), and it pulls the null-protein fold change to -0.42 with Intensity vs -0.07 with LFQ. iBAQ = Intensity / number
of theoretical peptides, so its between-sample ratios are identical to raw Intensity (SD 0.0) — use it within a sample
(e.g. molar share). Note LFQ has slightly fewer valid values (1004 vs 1031 in T4) because MaxLFQ needs ratio counts.

Lead 5: `readQFeatures()` exists in QFeatures 1.16.0 (`assayData, colData, quantCols, runCol, name, removeEmptyCols,
verbose, ecol`), as do `aggregateFeatures`, `zeroIsNA`, `filterFeatures`, `logTransform`. The Skill names only
`readQFeatures` + `aggregateFeatures` and gives no R code; the natural filter on MaxQuant's space-containing flag names
fails in `filterFeatures` (formula variables must be syntactic) — fixed by `make.names()` on rowData. `Spectra` is not
installed. `aggregateFeatures` is irrelevant at protein-group level.

**Scores:** Basic 36 (FC 9, clarity 8, efficiency 9, scope 10) · Specialized 50 (method 18, code 11 — Python fine, no R code
given and the obvious QFeatures filter failed, QC 8, reproducibility 8, security 5) · **86**
**Assertions:**
- [PASS] Recommends LFQ intensity for the between-condition comparison and explains why — confirmed by T4 residual 0.00 vs -1.33
- [PASS] iBAQ described as within-sample only — shown to carry the same between-sample ratios as raw Intensity
- [FAIL] Skill gives enough to build the QFeatures import without trial and error — no R code; first filterFeatures call errored
- [PASS] Scope: normalization and testing routed out — yes
- [PASS] Safety: read-only; no destructive operations — yes

### Input 5 — Stress
**Prompt:** "We ran the same 8 samples by DDA (MaxQuant proteinGroups.txt) and DIA (DIA-NN report.parquet). Load both, tell
me how much is missing in each, whether it looks MNAR or MCAR, and which imputation I should use for each before limma.
How many proteins overlap?"

**Code:** `runs/in5_stress.py` — Skill MaxQuant block, DIA block and `assess_missingness` verbatim; auditor checks on truth.

**Printed (`runs/in5.log`, trimmed):**
```
DDA MaxQuant LFQ (log2)                            missing  17.7% | corr(mean abundance, #missing) = -0.619
DIA-NN PG.MaxLFQ (log2, 0->NaN)                    missing  12.6% | corr(mean abundance, #missing) = -0.663
DIA-NN PG.MaxLFQ as pivoted (linear, zeros kept)   missing  11.8% | corr(mean abundance, #missing) = -0.164
DDA proteins with 0/8 valid values kept in matrix: 55
overlap: DDA 1445 | DIA 947 | both 864
[AUDIT] DIA missingness by TRUE abundance quartile: Q1 low 21.3 | Q2 3.9 | Q3 3.4 | Q4 high 3.4 (%)
[AUDIT] Skill diagnostic on DIA without LOWCONF and on/off groups: missing 8.0%, corr -0.493
[AUDIT] DIA: true value of missing cells median 21.14 vs observed cells median 24.43 log2
[AUDIT] DIA imputation bias on missing cells, row mean : mean +0.31 log2, MAE 0.35 (n=562)
[AUDIT] DIA imputation bias on missing cells, KNN k=5  : mean +0.47 log2, MAE 0.53 (n=562)
[AUDIT] DIA imputation bias, MinProb-style downshift   : mean -1.03 log2, MAE 2.12 (n=562)
[AUDIT] DDA KNN bias on missing cells: mean +0.51 log2 (n=1632)
[AUDIT] no imputation  changed-with-missing n=27: |est|/|true| 1.00 | null-with-missing n=271: p<0.01 1
[AUDIT] row mean       changed-with-missing n=27: |est|/|true| 0.74 | null-with-missing n=271: p<0.01 0
[AUDIT] KNN k=5        changed-with-missing n=27: |est|/|true| 0.86 | null-with-missing n=271: p<0.01 2
[AUDIT] MinProb-style  changed-with-missing n=27: |est|/|true| 0.64 | null-with-missing n=271: p<0.01 0
```
**Answer the Skill directs:** DDA → MNAR (corr -0.62) → left-censored imputation (MinProb/QRILC) in differential-abundance;
DIA → "closer to MCAR", "tolerates standard imputers". Imputation itself deferred (correct scope).

Lead 2: **confirmed, with nuance.** The Skill's own diagnostic gives DIA the same MNAR signature as DDA (-0.66 on the
Skill-filtered matrix, -0.49 with LOWCONF removed); missing DIA cells sit in the lowest true-abundance quartile (21 % vs
~3.4 % above it) and their true values are 3.3 log2 below the observed median; a KNN imputer is biased upward by the same
amount in DIA (+0.47) as in DDA (+0.51). DIA has *fewer* missing values (8–12.6 % vs 17.7 %), and in this synthetic set no
imputer created meaningful false hits (0–2 of 271 null proteins at p<0.01) — so "DIA tolerates standard imputers" is a
defensible statement about impact size, not about mechanism. The Skill cites nothing for the MCAR claim (its four
references are MaxLFQ, DIA-NN, ProteoWizard, ThermoRawFileParser); the missing-value literature found in this session
(msImpute, MCP 2023; "Neither random nor censored", Bioinformatics 2023; Jin et al., Sci Rep 2021) treats DIA and DDA
missingness as intensity-dependent mixtures of MNAR and MAR/MCAR, with DIA having less missingness among high-intensity
proteins. The Decision Tree routes by acquisition mode, so an agent overrides its own diagnostic. Two further traps: run
verbatim on the Skill's DIA output (linear scale, zeros counted as observed) the diagnostic reads only -0.16, which looks
MCAR-like; and LOWCONF leakage inflates it. The DDA matrix's 55 all-NaN rows count toward `total_pct`.

**Scores:** Basic 30 (FC 6, clarity 7, efficiency 8, scope 9) · Specialized 40 (method 11 — DIA mechanism mislabelled and
routing overrides the diagnostic, code 11 — runs but scale/zero handling undocumented, QC 6, reproducibility 7, security 5) · **70**
**Assertions:**
- [PASS] Both tables loaded; missingness quantified overall and per sample; overlap reported — 1445 / 947 / 864
- [FAIL] Imputation advice for DIA is consistent with the Skill's own diagnostic — diagnostic −0.66, advice "MCAR / standard imputers"
- [FAIL] Following the Skill's DIA block, the diagnostic is computed on log scale with zeros as NaN — verbatim gives −0.16
- [PASS] Scope: the imputation step itself is deferred to differential-abundance — yes
- [PASS] Safety: read-only; no imputation applied to user data without the user choosing — yes

## Research Veto (Category 3)
| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | no fabricated DOIs/PMIDs/results; all four references are real papers. pyOpenMS is attributed to Chambers 2012 (ProteoWizard), a misattribution, not a fabrication (P2) |
| M2 Practice boundaries | PASS | no individual-level diagnosis/prescription; instrument data only |
| M3 Methodological baseline | PASS (with P1s) | missing global protein FDR and the DIA-MCAR label are real errors but do not invert conclusions (run-level 1 % FDR is still applied; DDA routing is right); no ethics trigger |
| M4 Code usability | PASS | 4/4 blocks parse; every block ran on pandas 3.0.5 / pyOpenMS 3.5.0; the one crash is an unguarded index on precursor-less MS2 scans (edge), not unrunnable code |

## Final arithmetic
Static 79 × 0.4 = 31.6 · Execution 76.8 × 0.6 = 46.08 → 46.1 · 31.6 + 46.1 = 77.7 → **78** (Limited Release band).
Floors for Limited Release: static 79 ≥ 70 ✓ · execution 76.8 ≥ 75 ✓ · L1 33.2 ≥ 28 ✓ · L2 43.6 ≥ 42 ✓ · assertions 68 % ≥ 80 % ✗
→ one-tier downgrade → **⚠️ Beta Only**, deployable = false. Below the core bar (≥ 85). No safety/scope assertion failed.

## Recommendations
- **[P1] DIA-NN import omits Global.PG.Q.Value** (Inputs 2, 5): add `& (report['Global.PG.Q.Value'] <= 0.01)` (or
  `Lib.PG.Q.Value` for library-based MBR) to the DIA block, the Quantitative Thresholds row and the Stale-parsing fix, as
  `dia-analysis` already does.
- **[P1] DIA missingness labelled MCAR against its own diagnostic** (Input 5): replace "closer to MCAR / tolerates standard
  imputers" with "less missingness, still mostly intensity-dependent; choose the imputer from the diagnostic, not the
  acquisition mode"; cite a missing-value source.
- **[P1] DIA block keeps PG.MaxLFQ zeros** (Inputs 2, 5): `.replace(0, np.nan)` then `np.log2` after the pivot; say
  `assess_missingness` expects a log2, NaN-for-missing matrix.
- **[P1] mzML loop crashes on MS2 without precursor** (Input 3): `precs = spectrum.getPrecursors(); if not precs: continue`
  (or record as AIF); warn when lower+upper offset == 0.
- **[P2] R route named but no code** (Input 4): give a 6-line QFeatures block (`readQFeatures(quantCols=...)`,
  `make.names` on rowData before `filterFeatures`, `zeroIsNA`, `logTransform`); note `aggregateFeatures` is for
  peptide→protein, not proteinGroups.
- **[P2] Silent failure modes in the MaxQuant block** (Input 1): stop if `lfq_cols` is empty (currently returns an ID-only
  matrix, `runs/edge_no_lfq.log`); drop all-NaN rows; apply or remove the listed ≥2-peptide threshold.
- **[P2] pyOpenMS misattributed to Chambers 2012**: cite Röst et al. 2014 (Proteomics) for pyOpenMS.

Sources consulted for lead 1/2 context (web search, 2026-09-11):
[DIA-NN README](https://github.com/vdemichev/DiaNN) ·
[DIA-NN discussion #1797](https://github.com/vdemichev/DiaNN/discussions/1797) ·
[DIA-NN discussion #780](https://github.com/vdemichev/DiaNN/discussions/780) ·
[msImpute, MCP 2023](https://www.sciencedirect.com/science/article/pii/S1535947623000683) ·
[Neither random nor censored, Bioinformatics 2023](https://academic.oup.com/bioinformatics/article/39/5/btad200/7126416) ·
[Jin et al., Sci Rep 2021](https://www.nature.com/articles/s41598-021-81279-4)
