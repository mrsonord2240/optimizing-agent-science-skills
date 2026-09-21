> **Audit record for `bio-data-visualization-oncoprint-mutation-matrices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/oncoprint-mutation-matrices) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-oncoprint-mutation-matrices

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/oncoprint-mutation-matrices` | Category: Data Analysis | Mode A | Complexity: Complex (7 inputs)

Method: every figure was rendered to SVG (svglite) and its rectangles, polygons and text labels were decoded and compared with counts computed independently from the raw MAF (pandas/scipy/base R). PNGs were opened with the Read tool and are non-blank. Data: real TCGA-LAML (maftools extdata, 193 samples) and SYNTHETIC cohorts with planted truth (`run/data`, generators `run/gen_synth_*.R`). Scripts are in `run/`, outputs in `run/out/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 48 | 80 | 4/5 PASS | ✅ |
| 2 | Variant A | 30 | 46 | 76 | 3/4 PASS | ✅ |
| 3 | Edge | 30 | 46 | 76 | 3/5 PASS | ✅ |
| 4 | Variant B | 24 | 34 | 58 | 2/5 PASS | ⚠️ |
| 5 | Stress | 33 | 47 | 80 | 3/6 PASS | ✅ |
| 6 | Scope Boundary | 34 | 50 | 84 | 4/5 PASS | ✅ |
| 7 | Adversarial | 28 | 42 | 70 | 1/4 PASS | ⚠️ |

**Execution Average: 74.9 / 100** | **Assertion Pass Rate: 20/34** | Static: 71/100 | **Final: 73 (Beta Only), deployable: false, veto: none**

Floors (Limited Release): static >= 70 met (71); execution avg >= 75 not met (74.9); assertion pass rate >= 80% not met (59%).

## Skill Veto and Research Veto
All PASS (see JSON). M4 note: the comut block fails verbatim, but the Skill's own version section instructs the agent to introspect and adapt on AttributeError/TypeError, so it is recorded as P1 and not a veto.

## Shipped-means-present (gate 8)
`SKILL.md` points at no scripts/references; `examples/oncoprint_phd.R` and `usage-guide.md` exist; the six Related Skills all exist in staging. The example ran from a copy (`run/ex_run.R`) once `mat`, `clinical` and `cohort.maf` were supplied (the example leaves them as comments; `cohort.maf` does not exist).

## SKILL.md code blocks
| Block | Result |
|---|---|
| ComplexHeatmap `oncoPrint` | ran after defining `mat` and `clinical` (not defined by the Skill); output verified (Input 1, 5) |
| maftools `read.maf` + `oncoplot` | ran only after adding `Tumor_Sample_Barcode` to clinical and giving numeric features a palette (Input 2) |
| `somaticInteractions` | ran; returns a data.table (Input 6) |
| comut Python block | FAILS verbatim: AttributeError (`comut.CoMut`), then ValueError (sample subset rule), then TypeError on pandas 3 (Input 4) |
| examples/oncoprint_phd.R | ran with supplied objects; `oncoprint.pdf` 41 KB (Input 5) |

## Detailed Outputs

### Input 1 - Canonical: ComplexHeatmap oncoPrint of the top 20 genes of real TCGA-LAML (193 samples), FAB + vital-status tracks

**Executed:** true. Executed. run/i1_complexheatmap_laml.R, i1b_memosort.R; ComplexHeatmap 2.22.0; figure opened (non-blank, out/i1.png).

**Result:** Skill block run with data adapted; drawn cells decoded from SVG equal the matrix (0/3860 mismatches), colours, 193 columns, 192/192 annotation strips correct; but row order is by alteration events, not by the mutated-sample percentages printed beside it.

Code: `run/i1_complexheatmap_laml.R`, `helpers.R` (Skill `alter_fun` block verbatim). Key printed output:
```
drawn gene order   : DNMT3A FLT3 NPM1 TET2 IDH2 TP53 IDH1 CEBPA RUNX1 NRAS WT1 PTPN11 KIT KRAS U2AF1 SMC3 PHF6 SMC1A STAG2 TTN
input (count desc) : FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 RUNX1 NRAS TP53 CEBPA WT1 ...
n columns drawn: 193  cohort N: 193
cell mismatches (drawn vs matrix in drawn order): 0 of 3860
Missense 225 / Splice 22 / Truncating 96 (matrix) == (drawing)
pct labels: 25% 27% 17% 9% 10% 8% 9% 7% ...  expected: identical
subtype strip mismatches: 0 of 192 (1 NA sample grey)
drawn order == descending alteration-EVENT count: TRUE ; == descending mutated SAMPLES: FALSE (DNMT3A FLT3 TET2 IDH2 TP53 IDH1 CEBPA RUNX1 NRAS out of order)
```
Figure: `run/out/i1.png` (opened: stacked cells, staircase, coloured tracks).

**Scores:** Basic 32/40 | Specialized 48/60 | Total 80/100

**Assertions:**
- [PASS] Every drawn cell (colour rectangles decoded from the SVG, in drawn row/column order) equals an independent gene x sample matrix built from the MAF - 0 of 3860 cells differ; class totals Missense 225 / Truncating 96 / Splice 22 identical in matrix and drawing; 20 multi-class cells drawn stacked
- [PASS] Variant-class to colour mapping is right (Missense #56B4E9, Truncating #000000, Splice #CC79A7) - Decoded rect fills map back to the expected class for every cell
- [PASS] All 193 cohort samples are drawn (remove_empty_columns = FALSE) and % labels equal independent n/193 - 193 columns; labels 25% 27% 17% ... 3% equal round(n/193*100) for all 20 rows
- [PASS] Annotation track colours map to the right samples - FAB strip 0 mismatches over 192 coloured columns; the one sample with NA FAB (TCGA-AB-2941) is grey
- [FAIL] Gene order follows descending mutated-sample frequency as the decision table says ('Gene frequency (default)') - DNMT3A (48 samples, 25%) is drawn above FLT3 (52, 27%); 9 of 20 rows are out of sample-frequency order. oncoPrint ranks by summed alteration types (drawn order == descending event count, verified)

### Input 2 - Variant A: maftools::oncoplot(top=20) with clinical features and sortByAnnotation on TCGA-LAML

**Executed:** true. Executed. run/i2_maftools_oncoplot.R, i2c_verify_colours.R; maftools 2.22.0; figures opened (out/i2.png, i2b.png).

**Result:** Gene order, percentages and per-class colours match an independent count (20/20 gene rows); the Skill's call as written fails (clinicalData needs Tumor_Sample_Barcode, numeric feature needs a palette) and its partial annotationColor greys out the other groups.

Code: `run/i2_maftools_oncoplot.R`, `i2c_verify_colours.R`. Key output:
```
naive numeric-feature call: ERROR: numeric annotation color for NA must be a sequential color palette!
drawn genes: FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 RUNX1 NRAS TP53 CEBPA ...  == independent sample counts 52 48 33 20 18 17 16 15 15 13 ...
drawn pct: 27% 25% 17% 10% 9% 9% 8% 8% 8% 7% ... == n/193
gene rows whose drawn colour counts equal independent per-class/Multi_Hit counts: 19 of 20 (TTN row confounded by the annotation strip; own tiles match)
read.maf with the Skill's clinical (no Tumor_Sample_Barcode): ERROR: Tumor_Sample_Barcode column not found
```
Figures: `run/out/i2.png`, `i2b.png` (partial annotationColor: only M1/M0 coloured, rest grey, legend lists two).

**Scores:** Basic 30/40 | Specialized 46/60 | Total 76/100

**Assertions:**
- [PASS] Gene order equals descending count of mutated samples from the raw MAF - FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 ... TTN identical; gene percentages 27% 25% 17% ... equal independent n/193
- [PASS] Drawn colour counts per gene equal independent per-class and Multi_Hit counts - 20/20 rows (19 exact, TTN row only confounded by the annotation strip below it; its own tiles match); 30 multi-hit gene-sample pairs shown as black Multi_Hit
- [PASS] Non-mutated samples kept (removeNonMutated = FALSE) so the denominator is the cohort - Title 'Altered in 159 (82.38%) of 193 samples'; 193 columns
- [FAIL] The maftools example call runs as written in SKILL.md - clinicalData must contain a Tumor_Sample_Barcode column (the Skill's clinical does not); a numeric feature without a palette raises 'numeric annotation color for NA must be a sequential color palette'; annotationColor with 2 of 3 subtypes silently draws the rest grey and unlabeled

### Input 3 - Edge: Synthetic 30-sample cohort: multi-class cell, two hits of the same class, CNV+SNV cell, empty gene, zero-mutation samples, one sample, all-empty

**Executed:** true. Executed. run/gen_synth_edge.R, i3_edge.R (SYNTHETIC data with planted truth). An all-empty matrix errors with 'subscript out of bounds' (ComplexHeatmap, unhelpful message).

**Result:** ComplexHeatmap stacking and collapsing are exact and the cohort denominator holds; maftools silently drops the 14 samples without a mutation (denominator 16, not 30) even with removeNonMutated = FALSE and clinicalData for all 30.

Code: `run/gen_synth_edge.R`, `i3_edge.R` (synthetic, planted). Key output:
```
matrix from MAF+CNV equals planted truth: TRUE ; multi-class cells 2 ; S02 TP53 two Missense hits -> Missense
[keepempty] columns 30 rows 6 order TP53 KRAS RB1 MYC PIK3CA EMPTYG ; cell mismatches 0 of 180 ; pct 27% 20% 10% 7% 7% 0%
[dropempty] columns 13 ; cell mismatches 0 of 78 ; pct 27% 20% 10% 7% 7% 0%   (unchanged)
one-sample: ok ; all-empty: ERROR subscript out of bounds ; remove_empty_rows=TRUE drops EMPTYG only
maftools sample count: 16 (cohort 30) ; clinical rows 16 ; pct 50/38/19/12 ; removeNonMutated TRUE == FALSE
```
Figures: `run/out/i3_keepempty.png`, `i3_one.png`, `i3_maftools.png`.

**Scores:** Basic 30/40 | Specialized 46/60 | Total 76/100

**Assertions:**
- [PASS] Stacked cells (Missense;Truncating, Amp;Missense) and a double same-class hit are drawn as planted - 0 of 180 cells differ from the planted truth; S02 TP53 two Missense hits collapses to one Missense rectangle
- [PASS] Empty gene row is kept at 0% and zero-mutation samples are kept with cohort denominator 30 - EMPTYG row present at 0%; 30 columns; TP53 27% = 8/30; remove_empty_rows = TRUE drops only EMPTYG
- [PASS] Single-sample matrix draws correctly - 1 column; TP53 stack Missense+Truncating, KRAS Missense, MYC Amp; PIK3CA/RB1/EMPTYG 0%
- [FAIL] maftools with removeNonMutated = FALSE preserves the cohort N (30) when clinicalData lists all 30 samples - maftools reports 16 samples; getClinicalData has 16 rows; percentages 50/38/19/12 are of 16. Samples absent from the MAF cannot be restored
- [FAIL] Percent labels differ between remove_empty_columns TRUE and FALSE, as the Reconciliation table says - ComplexHeatmap labels identical (27% 20% 10% 7% 7% 0%) with 13 or 30 columns; maftools identical too; the documented denominator effect does not exist

### Input 4 - Variant B: comut.py co-mutation plot from TCGA-LAML long-format data (Skill Python block)

**Executed:** true. Executed in main venv (pandas 3.0.6) and venv-pd2 (pandas 2.3.3): run/i4_comut.py, outputs out/i4_pd3.log, i4_pd2.log. Verbatim block failed in both (with the import shim).

**Result:** The Skill block does not run verbatim: comut.CoMut is not exposed by 'import comut'; after adapting, the first dataset must hold every sample; pandas 3 breaks add_continuous_data. With fixes cells match (0/1930) but the top gene is drawn at the bottom and samples are unsorted.

Code: `run/i4_comut.py`. Key output:
```
import comut; hasattr(comut,'CoMut') = False
verbatim block (with import shim) ERROR: ValueError Unknown samples {...}
pandas 3.0.6: TypeError: Invalid value '[0.3 0.43 ...]' for dtype 'int64' (LossySetitemError)
y tick order (bottom->top): FLT3 DNMT3A NPM1 ... CEBPA   (top gene at the bottom)
cells checked 1930 | mismatches 0 | 2-class triangle cells 20
TMB values above the Skill's 30: 1 of 192 ; normalised keys for 10,20,30 over (10,30): 0, 0.333, 0.667
```
Figure: `run/out/i4_comut.png` (opened: unsorted samples, overlapping x labels, no legend).

**Scores:** Basic 24/40 | Specialized 34/60 | Total 58/100

**Assertions:**
- [FAIL] The Skill's comut code block runs as written - AttributeError: module 'comut' has no attribute 'CoMut' (comut 0.0.3; correct is from comut import comut); with that fixed, ValueError 'Unknown samples' because clinical/TMB samples are not in the mutation frame (zero-mutation samples); pandas 3.0.6: TypeError LossySetitemError in add_continuous_data (pandas 2.3.3 only warns)
- [PASS] After adaptation every cell equals an independent groupby (single class = colour, two classes = two triangles) - 0 of 1930 cells mismatched; 20 two-class triangle cells; no 3+ class cells in this data
- [PASS] Annotation track maps to the right samples - Subtype 0 mismatches for annotated samples; sample without annotation left white
- [FAIL] Top-frequency gene is drawn at the top and samples ordered by burden as the description promises - category_order=top_genes puts FLT3 at the bottom (y tick order bottom-to-top); samples are in first-seen/list order, unsorted, no staircase
- [FAIL] TMB colour scale is valid for the data - value_range=(0,30) hard-coded; max TMB 34 saturates; comut normalises as (x-min)/max, so any range with min>0 is mis-scaled (10,20,30 over (10,30) -> 0, .33, .67)

### Input 5 - Stress: Synthetic 600-sample cohort (subtypes, 3 hypermutators to 3000 mutations, multi-hit TP53): shipped example script + column_split + log10 TMB

**Executed:** true. Executed. run/gen_synth_cohort.R, i5_stress.R, i5b_tmb.R, ex_run.R (SYNTHETIC cohort, seed 7); figures opened (out/i5_C_split.png).

**Result:** Shipped example runs once mat/clinical are defined; log10 TMB bars are exact (r = 1.0, tallest/median 2.6 vs 143 linear) and split panels are right; clinical order not matching mat columns silently mislabels 391/600 samples and the Skill never warns.

Code: `run/gen_synth_cohort.R`, `i5_stress.R`, `i5b_tmb.R`, `ex_run.R`. Key output:
```
MAF rows 24326 ; hypermutator TMBs 3000 2500 1800 ; median 21
[A unaligned] annotation strip vs TRUE subtype: mismatches 391 of 600 (no warning)
[B aligned]   mismatches 0 of 600 ; cells 0/7200
[C split] Basal 180 | HER2 120 | Luminal 300 ; every column in the right panel ; pct labels cohort-wide (39% TP53)
TMB bars 600: cor(height, log10(TMB+1)) = 1.0000 ; tallest/median 2.59 (linear 142.9)
read.maf(clinicalData = Skill-shaped clinical): ERROR Tumor_Sample_Barcode column not found
example: pdf exists TRUE size 41029 ; class(si) data.table ; dim 190x12
```
Figure: `run/out/i5_C_split.png`.

**Scores:** Basic 33/40 | Specialized 47/60 | Total 80/100

**Assertions:**
- [PASS] examples/oncoprint_phd.R runs from a clean copy once mat, clinical and cohort.maf exist - oncoprint.pdf 41 KB written; somaticInteractions returns 190 pairs; script leaves mat, clinical and cohort.maf undefined (comments only)
- [PASS] TMB bar height is proportional to log10(true TMB + 1) per column and hypermutators do not dominate - 600 bars; cor(height, log10(TMB+1)) = 1.0000; tallest/median = 2.59 (log expectation 2.59; linear would be 143)
- [PASS] column_split by subtype puts each sample in the panel of its true subtype - Basal 180 / HER2 120 / Luminal 300; every column matches; annotation 0/600 mismatches; cells 0/7200 mismatches
- [FAIL] Annotation tracks map to the right samples even when the clinical table is in MAF order and the matrix columns are sorted - 391 of 600 subtype strips wrong, no error or warning: HeatmapAnnotation is positional and the Skill never says to reorder clinical by colnames(mat)
- [FAIL] Per-panel gene frequency right bar as the usage guide promises for split layouts - One cohort-wide right bar and cohort-wide % (39% TP53), no per-panel frequencies
- [FAIL] The Skill's step 6 read.maf(clinicalData = clinical) works with the clinical data frame defined in the Skill - Error: Tumor_Sample_Barcode column not found in provided clinical data (works after adding it)

### Input 6 - Scope Boundary: Mutual exclusivity / co-occurrence: somaticInteractions on LAML, on a planted N=600 cohort and on an N=20 subset, plus small-cohort CI recipe

**Executed:** true. Executed. run/i6_somatic_interactions.R, i6_verify_fisher.py. Haldane-Anscombe OR for BRAF/NRAS (0/2/1/17) is 2.33 (>1) although zero co-occurrences were observed: the recommended correction reverses the apparent direction at these counts (P2).

**Result:** All 263 pairwise Fisher results equal an independent scipy computation; planted pairs are recovered at N=600 and correctly non-significant at N=20; the documented return value is wrong.

Code: `run/i6_somatic_interactions.R`, `i6_verify_fisher.py`. Key output:
```
[LAML top20, N=193] pairs=190 | 2x2 count mismatches=0 | p mismatches=0 | max rel diff 2.6e-13
[synthetic N=600]   pairs=45  | 0 | 0 | 3.6e-14
[synthetic N=20]    pairs=28  | 0 | 0 | 3.2e-15
TP53-MYC (planted co-occur) N=600 p=7.65e-46 OR=23.7 ; N=20 p=0.141
BRAF-NRAS (planted mutex)   N=600 p=3.07e-06 OR=0 (0/166) ; N=20 p=1.0
return class data.table 190x12: gene1,gene2,pValue,oddsRatio,00,01,11,10,pAdj,Event,pair,event_ratio
Clopper-Pearson max |R - scipy| 3e-16 ; BRAF/NRAS N=20 table 0/2/1/17 Haldane-Anscombe OR 2.33
```
Figure: `run/out/i6_synth.png` (opened; the significance legend overlaps one heat-map cell).

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**
- [PASS] somaticInteractions p-values and 2x2 counts equal an independent two-sided Fisher computed from the raw MAF - LAML 190/190 pairs (N=193), synthetic N=600 45/45, N=20 28/28; max relative p difference 2.6e-13; direction agrees for all p<0.05
- [PASS] Planted co-occurrence (TP53-MYC) and mutual exclusivity (BRAF-NRAS) are detected at N=600 - TP53-MYC p=7.6e-46 OR=23.7 Co_Occurence; BRAF-NRAS p=3.1e-06 OR=0, 0 of 166 co-mutated
- [PASS] At N=20 the same pairs are not significant, supporting the Skill's small-cohort warning - TP53-MYC p=0.141 (adj 0.75); BRAF-NRAS p=1.0; KRAS-EGFR p=1.0
- [PASS] Clopper-Pearson intervals from binom.test agree with an independent exact method - max |R - scipy exact| 3e-16 over 8 genes
- [FAIL] somaticInteractions returns 'a matrix of -log10(p) with sign by direction' as the Skill states - Returns a 12-column data.table (gene1, gene2, pValue, oddsRatio, 00/01/11/10, pAdj, Event, pair, event_ratio); the signed -log10 matrix exists only in the plot

### Input 7 - Adversarial: MAF barcodes differ from clinical barcodes; MAF classes outside the six Skill classes; request to drop non-mutated samples so frequencies look higher

**Executed:** true. Executed. run/i7_adversarial.R on TCGA-LAML. No scope or safety problem arises; the Skill correctly advises keeping all samples.

**Result:** Unmapped alteration strings fail loudly, but ID mismatch produces an all-NA annotation with no warning in both tools, the Skill gives no Variant_Classification mapping, and its claim that dropping empty columns changes the percentages is false.

Code: `run/i7_adversarial.R`. Key output:
```
annotation values matched by ID: 0 of 193 ; oncoPrint: ok, warnings: none
read.maf with non-matching clinical IDs: ok, warnings: none ; clinical rows kept 0
unmapped 'Silent' cells: ERROR You should define graphic function for: Silent
LAML classes not covered by the Skill classes: 5'Flank IGR Intron RNA Silent
remove_empty_columns FALSE: 193 columns pct 25% 27% 17% 9% 10% 9% 8% 8% ; TRUE: 126 columns, same pct; altered-only would be 41% 38% 26% ...
```

**Scores:** Basic 28/40 | Specialized 42/60 | Total 70/100

**Assertions:**
- [PASS] An alteration string with no alter_fun/col entry fails loudly - 'You should define graphic function for: Silent' (and for a case mismatch 'missense')
- [FAIL] A clinical/MAF sample-ID mismatch is reported - oncoPrint draws an all-grey annotation with no warning; read.maf(clinicalData = non-matching IDs) returns 0 clinical rows with no warning
- [FAIL] The Skill maps MAF Variant_Classification values to its alteration classes - SKILL.md/usage guide only say 'map per-row Variant_Classification to alteration class'; 5 of the 12 LAML classes (Silent, Intron, RNA, IGR, 5'Flank) plus In_Frame_* and Nonstop have no stated rule
- [FAIL] Dropping empty columns changes the percentage denominator as the Skill states, so the request would inflate frequencies - remove_empty_columns TRUE: 126 columns but labels unchanged (25% 27% 17% ...); an altered-only denominator would give 41% 38% 26%; the Skill's denominator warning describes behaviour that does not occur

## Static scores

- functional_suitability: 9/12 - Completeness 3, correctness 2, appropriateness 4. Central pieces are only comments (MAF to matrix pivot, Variant_Classification map, CNV merge, TMB definition). Several stated behaviours are wrong: % labels change with remove_empty_columns, somaticInteractions returns a signed matrix, default gene order is by frequency, comut example imports.
- reliability: 7/12 - Fault tolerance 2, error reporting 3, recoverability 2. Silent failure modes an agent will hit: clinical order not aligned to matrix columns (391/600 wrong strips), ID mismatch gives all-NA annotation, maftools drops samples absent from the MAF; no guard or check is described. The Common Errors table is useful but misses these.
- performance_context: 6/8 - SKILL.md about 240 lines with no references layer; usage-guide adds a second copy of several tips; example repeats the alter_fun block verbatim.
- agent_usability: 10/16 - Learnability 3, consistency 2, feedback 3, error prevention 2. Clear Goal/Approach and decision table, but usage-guide prompt colours/heights (green Missense, quarter-height Truncating) contradict SKILL.md (#56B4E9, 0.33), and the 'sort by gene 1' failure mode contradicts its own fix line.
- human_usability: 5/8 - Discoverability 3, forgiveness 2. Example prompts are natural; numeric errors from maftools/comut surface with no Skill-side hint.
- security: 11/12 - No credentials, network, eval or shell. Example writes oncoprint.pdf and reads cohort.maf in cwd.
- maintainability: 8/12 - Version-stamped and cited (Cerami 2012, Canisius 2016, Gu 2016, Mayakonda 2018 are correct references), but the example cannot run without objects the reader must invent and nothing is testable as shipped; comut instructions drifted from the package API.
- agent_specific: 15/20 - Trigger precise; all six related Skills exist; safe re-runs; escape hatch for AttributeError present in the version block; no references/ layer and no MAF loader helper.

Subtotal 71/100. Final = 28.4 + 44.9 = 73.

## Recommendations

**[P1] comut block cannot run as written** (inputs [4])
- Problem: import comut then comut.CoMut() raises AttributeError (class lives in comut.comut); later datasets must have samples inside the first dataset's set, so zero-mutation and unannotated samples raise ValueError; add_continuous_data raises TypeError on pandas 3; category_order draws the top gene at the bottom; no sample sorting; TMB range (0,30) saturates.
- Root cause: Python equivalent was written from memory of the API and never executed.
- Fix: Use from comut import comut, set toy_comut.samples to the full cohort first, reverse category_order, pre-sort samples by burden, note pandas<3, derive value_range from the data.

**[P1] Denominator claims contradict tool behaviour** (inputs [3, 7])
- Problem: The Skill says percentages differ with remove_empty_columns and that removeNonMutated = FALSE preserves cohort N. ComplexHeatmap % is always over the input matrix; maftools drops samples that are absent from the MAF (16 of 30) regardless of the flag and of clinicalData.
- Root cause: Behaviour asserted without running it.
- Fix: State the true denominators, and tell the agent to build the matrix from the explicit cohort sample list (or add zero-mutation samples to the MAF/clinical merge) before plotting.

**[P1] Matrix and annotation construction left as comments** (inputs [1, 5, 7])
- Problem: mat, clinical and the Variant_Classification-to-class map are undefined; clinical rows not ordered like colnames(mat) silently mislabel samples (391/600 wrong), non-matching IDs give an all-NA track with no warning, and the maftools example needs a Tumor_Sample_Barcode column.
- Root cause: The hardest correctness step is the one the Skill does not show.
- Fix: Ship a short verified MAF-to-matrix function with the class map, and require clinical <- clinical[match(colnames(mat), clinical$Tumor_Sample_Barcode), ] plus a stopifnot on NA matches.

**[P1] Row order is not sample frequency; somaticInteractions return misdescribed** (inputs [1, 6])
- Problem: oncoPrint ranks genes by alteration events, so a gene with fewer mutated samples can sit above one with more (DNMT3A 25% above FLT3 27%). somaticInteractions returns a data.table, not a signed -log10 matrix.
- Root cause: Both descriptions were written from the plot appearance.
- Fix: Say the default order counts alteration types and pass row_order = order(-rowSums(mat != '')) when sample frequency is wanted; document the data.table columns (pValue, oddsRatio, Event, pAdj).

**[P2] usage-guide and SKILL.md disagree; smaller gaps** (inputs [3, 5, 6])
- Problem: Usage-guide prompt gives green Missense and quarter-height Truncating versus SKILL.md; the 'sort by gene 1' failure mode contradicts its own fix; per-panel right bar and 'rasterize the cell layer' / 'side annotation' have no code and are not what oncoPrint does; Haldane-Anscombe OR flips to >1 for a 0-cell mutex pair; an all-empty matrix errors with 'subscript out of bounds'; maftools Multi_Hit black clashes with the Skill's black Truncating; partial annotationColor greys unlisted groups.
- Root cause: Two documents maintained separately.
- Fix: Align the two files, delete or implement the unsupported claims, and add one line per gotcha.

> Reviewer: check the failing assertions in Inputs 3, 4, 5 and 7 first; the recurring pattern is that the Skill states denominator and return-value behaviour it never ran, and leaves the matrix/annotation construction (where the silent errors live) as comments.
