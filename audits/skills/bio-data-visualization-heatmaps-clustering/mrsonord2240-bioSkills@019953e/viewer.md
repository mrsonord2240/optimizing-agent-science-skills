> **Audit record for `bio-data-visualization-heatmaps-clustering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@019953e](https://github.com/mrsonord2240/bioSkills/tree/019953e9ca90f6f6f69e3f5a9cd19a5c1b9dc6be/data-visualization/heatmaps-clustering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-heatmaps-clustering (FIRST AUDIT)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@019953e9ca90f6f6f69e3f5a9cd19a5c1b9dc6be:data-visualization/heatmaps-clustering` (unmodified upstream GPTomics/bioSkills; read from a `git archive` copy in `run\skill\`, nothing written in the staging clone).
Category: Data Analysis | Mode: A (code-writing Skill, every block and both shipped examples run) | Complexity: Complex, 7 inputs
Env: `F:\OpenScience\audit-envs\data-visualization` (R 4.4.3 through `r.sh`: ComplexHeatmap 2.22.0, pheatmap 1.0.13, seriation 1.5.8, circlize 0.4.18; `py.sh`: seaborn 0.13.2, scipy 1.18.1, scanpy 1.12.4). Every output PNG was opened with the Read tool; numbers behind each plot were checked against the input matrix.

## Result

| | |
|---|---|
| Static | **79** |
| Execution average | **77.0** |
| Final | **78** (31.6 + 46.2 = 77.8) |
| Assertions | 28/33 (84.8%) |
| Floors (Limited Release) | all met: static 79 >= 70, exec 77.0 >= 75, L1 31.1 >= 28, L2 45.9 >= 42, assertions 84.8% >= 80% |
| Skill veto | PASS |
| Research veto | **FAIL: M4 Code Usability** (`examples/heatmap_phd.R` crashes on every input) |
| Grade | **Reject** (forced by the veto; numerically 78 = Limited Release) |
| Deployable | **false**, veto_override true |
| Open P0 / P1 / P2 | 1 / 3 / 4 |

The one open P0 is a one-line repair (drop `row_split` or make it a number), so a fix pass should clear the veto; the seaborn colour-bound defect and the missing circular-selection guard are the P1s a fixer should take with it.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: shipped examples, SKILL.md OLO/annotation blocks, real ALL | 30 | 46 | 76 | 3/5 | pass |
| 2 | Variant A: seaborn clustermap block | 31 | 44 | 75 | 4/5 | pass |
| 3 | Edge: failure-mode and reconciliation claims | 31 | 48 | 79 | 4/5 | pass |
| 4 | Variant B: correlation QC + concatenated heatmaps, real airway | 33 | 47 | 80 | 5/5 | pass |
| 5 | Stress: 5,000 x 60, OLO, raster, cairo_pdf | 34 | 50 | 84 | 5/5 | pass |
| 6 | Scope Boundary: oncoPrint (real TCGA-LAML) + scanpy heatmap | 32 | 46 | 78 | 4/4 | pass |
| 7 | Adversarial: circular gene selection on pure noise | 27 | 40 | 67 | 3/4 | warn |

**Executed 7/7.** Scripts and raw outputs are in `run\` (`i<N>*.R|py` with matching `.out`). Data: real (Bioconductor ALL, airway + `public-data` DESeq2 results, TCGA-LAML MAF from maftools) and labelled synthetic with planted structure everywhere else.

## Detailed Outputs

### Input 1 - Canonical: annotated ComplexHeatmap, pathway split, OLO
**Prompt:** "Build a publication-quality annotated heatmap of the top variable genes, row-z-scored, ward.D2, condition/batch tracks, pathway row split, optimal leaf ordering." Ran both shipped examples, the SKILL.md annotation and OLO blocks verbatim, then the recipe on real ALL leukaemia.

`examples/heatmap_phd.R` with the objects it assumes supplied (`run\scratch\ex2`, `i1b_phd_verbatim.out`):
```
Error: When `cluster_rows` is a dendrogram, `row_split` can only be a single number.
Execution halted
```
Deterministic: any `row_split` vector with `cluster_rows = as.dendrogram(olo[[1]])` fails (`t_split.R`: hclust object also fails; numeric `row_split = 3` works). Diagnostic run with `row_split = NULL` (everything else verbatim) ran and passed: `row_order(ht) == OLO order`, adjacent-distance sum 431.4 vs 466.1 default, `cutree(k=4)` names aligned with rownames, planted up/down modules pure (40/40) (`i1b_phd.out`; PNG opened: orange up block, blue down block, batch colours as declared).

`examples/expression_heatmap.R` ran unmodified (PDF 26,515 B); PNG copy opened: slices 10/10 columns, 20/60/20 rows; drawn Control-slice dendrogram is cophenetic-identical to an independent `hclust(complete)`. But the legend says "Z-score" on a matrix that is not z-scored (row means -0.22..1.06, sd 0.30..1.19; 3.6% of cells saturate the fixed +-2 range) and pathway labels do not match the simulated gene blocks (`i1a.out`).

SKILL.md annotation block, verbatim (`i1c.out`): OK with two pathway levels; with a third level not in the `col` list: `Pathway: cannot map colors to some of the levels: Immune`.

Real ALL, 200 top-variance genes x 126 samples (`i1.out`):
```
row mean max abs 7e-16, row sd 1; bounds 2.523; row_order == OLO order TRUE
adjacent-row distance: default hclust 2014.2, OLO 1893.3
column slices 32 / 94: slice 1 = 32 T-cell, slice 2 = 94 B-cell, 0 mixed
CD3D (38319_at) B 4.84, T 9.52; col_fun(-bounds) == vik[1] TRUE; col_fun(10) == col_fun(bounds) TRUE
```
PNG opened: T-cell block left, sub-clusters ALL1/AF4 and E2A/PBX1 visible in the annotation. Note the legend ticks run to +-4 while colours saturate at 2.52 (ComplexHeatmap derives legend `at` from the data range).

Scores 30 + 46 = 76; assertions 3/5 (flagship example crashes; 'Z-score' mislabel).

### Input 2 - Variant A: seaborn.clustermap
The SKILL.md block runs verbatim (`i2_seaborn.py`, synthetic log-expression, baseline ~8, planted up/down modules):
```
vmax computed on RAW df: 13.173
plotted data range: -2.81 2.38 | fraction of cells with |z| > 0.5*vmax: 0.0
plotted == row z-score of input (rows reordered): True ; rows mean 0, sd 1: True True
row tree cophenetic identical to independent scipy ward: True
cluster vs truth: 30 up / 30 down / 29+1 flat ; columns 9 Control | 9 Treatment
z_score + standard_scale -> ValueError Cannot perform both z-scoring and standard-scaling on data
```
The clustering is right and annotations map to the right samples, but the figure I opened is uniformly pale (colourbar +-13, data within +-2.8): `vmax` is computed from the un-scaled frame and applied to the z-scored plot, the exact failure the Skill warns about elsewhere. Scores 31 + 44 = 75; assertions 4/5.

### Input 3 - Edge: the failure-mode claims
`i3.out`, `i3b.out`, `i1e.out`. Reproduced: ward.D vs ward.D2 merge tables differ; R ward.D2 heights equal scipy `ward` to 1.4e-14 (ward.D differs by 209); Euclid(z)^2 / (1-r) = 22 = 2(n-1); outlier 60 renders at the extreme colour with no error while a typical value goes from `#FFFAF8` (naive) to `#FF8E6F` (99% bound); pheatmap `gaps_col` ignored under `cluster_cols=TRUE`; raster auto-on above 2000 rows; time course: `cluster_columns=TRUE` gives `0h 1h 2h 4h 8h 48h 24h 12h`, `FALSE` keeps `0h..48h` (with `column_split` too). Wrong or overstated:
- "Rscript ... a bare `Heatmap()` produces no output": at top level in Rscript it draws (PDF 6,862 B); only for/function/lapply give the blank 3,448 B page.
- Reconciliation row "ComplexHeatmap and pheatmap give different dendrograms": at defaults the trees are identical.
- Sparse-row z-scores "explode": a one-non-zero row reaches only (n-1)/sqrt(n) = 2.85; the ">=3 non-zero" threshold has no source.
- "use column_split or column_order" alone does not preserve order (default clustering still reorders slices: `4h 8h 12h 48h 24h 1h 2h 0h`); usage-guide wording (with `cluster_columns = FALSE`) is right.

Scores 31 + 48 = 79; assertions 4/5.

### Input 4 - Variant B: correlation QC and concatenated heatmaps (real airway)
No code in SKILL.md for either usage-guide prompt (`i4_airway_qc_concat.R`, `i4.out`): vst of 22,369 genes x 8 samples, top-500 variable genes, Pearson r range 0.5995..0.882, symmetric, diag 1, `row_order == column_order == hclust(1-r, ward.D2)`. Colour scale set to the observed range with reversed batlow, not 0-1. Concatenated `h1 + h2` (40 top-padj DE genes from `public-data\...airway_dex_deseq2_results.csv`): shared order is a permutation of 40, log2FC panel rows aligned by rowname, `sign(log2FC) == sign(mean z trt - untrt)` for 40/40. Both PNGs opened, non-blank, annotation matches colData. Samples cluster mostly by dex with N080611 apart (real airway structure). Scores 33 + 47 = 80; assertions 5/5; the missing code/colour guidance is a P1 completeness gap.

### Input 5 - Stress: 5,000 x 60
`i5_stress.R`, `i5.out` (synthetic, 5 planted row modules, 3 column groups, one outlier at z = 7.09):
```
dist+hclust ward.D2 5000 rows: 3.7-4.9 s ; OLO (seriation) 5000 rows: 125.9 / 120.2 / 121.9 s
row order == OLO order TRUE ; cutree(k=5) vs planted: ARI 0.992 ; column slices 20/20/20, each one group
PDF: raster_quality=5 761,672 B ; raster_quality=1 265,034 B ; vector cells 2,408,920 B ; raster_device='CairoPNG' 775,142 B
use_raster auto message: 'automatically set to TRUE for a matrix with more than 2000 rows'
```
PNG opened: five clear blocks, outlier clipped, no wash-out. Environment note (not scored against the Skill): on this Windows R, `cairo_pdf()` failed with "unable to load winCairo.dll" once the Cairo package DLL had loaded (it loads at `Heatmap(use_raster = TRUE)`); it worked after opening `cairo_pdf` once first. Scores 34 + 50 = 84; assertions 5/5.

### Input 6 - Scope boundary: OncoPrint and single-cell
Real TCGA-LAML MAF (2,207 rows, 193 samples), 12 genes (`i6.out`): matrix altered-sample counts `48/52/33/17/20/15/13/18/16/15/12/9` equal the MAF unique-sample counts; `column_order` argument honoured; first 10 drawn columns all carry DNMT3A; PNG opened (missense/truncating/inframe overlays). Default row order is by sample x type count (DNMT3A 25% drawn above FLT3 27%), which the Skill does not mention. scanpy `pl.heatmap` on synthetic markers shows the planted 3-block structure. The Skill correctly defers oncoPrint detail to `oncoprint-mutation-matrices` (exists). Scores 32 + 46 = 78; assertions 4/4.

### Input 7 - Adversarial: circular selection
`i7_adversarial.R` (iid-normal noise, 10,000 genes x 20 samples, random labels):
```
genes p<0.05: 480 (expected ~500); min p 1.8e-4; BH padj<0.05: 0
top-100 by p, ward.D2, row z: column slices Control 10/0, 0/10 Treatment (perfect separation)
100 unselected random genes: 2 clusters 7/7 and 3/3 (no separation)
```
The rendering is exactly what the Skill prescribes and looks convincing. Neither SKILL.md nor usage-guide says anything about selecting features on the grouping variable (grep for circular / selection / double-dip / cherry: none); the only guard is the generic "verify against orthogonal evidence" line 34. Recorded as P1, not a veto (the Skill never instructs the fallacy). Scores 27 + 40 = 67; assertions 3/4.

## Shipped-means-present (gate 8)
Every file `SKILL.md` and `usage-guide.md` point at exists: the two `examples/*.R` files ship; the six Related Skills (`color-palettes`, `oncoprint-mutation-matrices`, `multipanel-figures`, `dimensionality-reduction-plots`, `differential-expression/de-visualization`, `single-cell/markers-annotation`) exist at the commit. There is no `references/` or `scripts/` directory. Research scope (gate 7): plotting only, no diagnostic content.

## Recommendations
P0 heatmap_phd.R crash. P1: seaborn `vmax` from raw data; no circular-selection guard; no code/colour guidance for correlation QC, concatenation and pseudobulk. P2: inaccurate failure-mode statements (Rscript top level, pheatmap defaults, sparse z, column_split wording); `expression_heatmap.R` 'Z-score' mislabel and pathway/block mismatch; pathway colour list omits levels and legend ticks exceed the colour bounds; second `draw()` leaves `Rplots.pdf` and the description over-claims a column-scaling decision. Full text with fixes is in the JSON report.

## Run order
`v0_versions.R`, `i1a_check_example1.R` (needs `scratch\ex1` copy of the example), `scratch\ex2\{run_phd_syn.R,check_phd.R,t_split.R}`, `i1c_skillmd_annotation_block.R`, `i1_all_real.R`, `i1d_legend_range.R`, `i1e_olo_verbatim_pheatmap.R`, `i2_seaborn.py`, `i3_edge_claims.R`, `i3_scipy_check.py` then `i3_cmp.R`, `i3b_timecourse.R`, `i4_airway_qc_concat.R`, `i5_stress.R` (first run builds `i5_olo.rds`), `i5b_png.R`, `i6_oncoprint_scanpy.R`, `i6b_scanpy.py`, `i7_adversarial.R`, `finalize_report.py`. R scripts run with `bash F:\OpenScience\audit-envs\data-visualization\r.sh <script>` from `run\`, Python with `py.sh`.
