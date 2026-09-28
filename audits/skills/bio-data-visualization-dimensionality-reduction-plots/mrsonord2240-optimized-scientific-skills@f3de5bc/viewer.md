> **Audit record for `bio-data-visualization-dimensionality-reduction-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@f3de5bc](https://github.com/mrsonord2240/optimized-scientific-skills/tree/f3de5bc6421ca81d37ca532c1771e533a9af5cdf/skills/bio-data-visualization-dimensionality-reduction-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-dimensionality-reduction-plots

Generated: 2026-09-27
Source: `mrsonord2240/optimized-scientific-skills@f3de5bc6421ca81d37ca532c1771e533a9af5cdf:skills/bio-data-visualization-dimensionality-reduction-plots`
Independent re-auditor: true
Category: Data Analysis | Mode: D (instructions plus shipped CLI) | Complexity: Complex
Data: archived synthetic regression datasets, real Bioconductor airway, real Scanpy pbmc68k_reduced, and two new synthetic AnnData cases.

## Result

Static: **93/100** | Execution average: **92.3/100** | Final: **93/100 — ⭐ Production Ready**
Executed: **9/9** | Assertions: **44/45 = 97.8%** | Vetoes: none | Deployable: **true**
Open P0/P1/P2: **0/0/3**. Production floors all pass: static 93, execution 92.3, Layer 1 average 36.7/40, Layer 2 average 55.7/60, assertions 97.8%.

## Static Evaluation

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 11/12 | Covers PCA, t-SNE, UMAP, PHATE, method selection, limitations, and runnable examples; the shipped PCA palette is ambiguous beyond ten conditions. |
| Reliability | 11/12 | Raw-count, shape, and metadata validation is clear and strict; invalid inputs recover by correction and rerun, though errors do not include structured codes. |
| Performance Context | 7/8 | The 220-line main skill uses progressive references well; the all-method comparison is intentionally heavier than method-specific recipes. |
| Agent Usability | 15/16 | Decision tree, method rules, output conventions, and failure modes are highly actionable; one reference sentence says four saved figures although five are produced. |
| Human Usability | 7/8 | Natural trigger language and many realistic prompts are present; large categorical legends need a palette/faceting guard. |
| Security | 12/12 | No credentials, network calls, raw-string code execution, destructive operations, or sensitive-data logging are present. |
| Maintainability | 12/12 | Concise main file, two focused references, a CLI example, and five regression tests provide clear modularity and testability. |
| Agent Specific | 18/20 | Triggering, progressive disclosure, deterministic reruns, and stop conditions are strong; integration output contracts and palette escape hatches could be more explicit. |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical: Bulk PCA with variance labels and library-size diagnosis | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A: PCAtools biplot, scree, and loadings on real airway data | 37 | 57 | 94 | 5/5 | ✅ |
| 3 | Variant B: Raw-HVG Scanpy UMAP and igraph Leiden | 38 | 58 | 96 | 5/5 | ✅ |
| 4 | Edge: openTSNE, Rtsne, uwot seeds and small-n perplexity | 37 | 57 | 94 | 5/5 | ✅ |
| 5 | Stress: PHATE on continuous and branching trajectories | 37 | 55 | 92 | 5/5 | ✅ |
| 6 | Scope Boundary: Shipped example end to end on archived 1,200-cell H5AD | 37 | 56 | 93 | 5/5 | ✅ |
| 7 | Adversarial: Reject lineage and batch claims inferred from UMAP layout | 38 | 58 | 96 | 5/5 | ✅ |
| 8 | Edge: New: invalid log-like and metadata-incomplete AnnData | 36 | 55 | 91 | 5/5 | ✅ |
| 9 | Stress: New: minimum shape with twelve condition categories | 32 | 48 | 80 | 4/5 | ✅ |

## Detailed Outputs

### Input 1 — Canonical: Bulk PCA with variance labels and library-size diagnosis

**Prompt:** PCA of my bulk RNA-seq (3 conditions x 2 batches, 60 samples, 2,000 genes); label axes with variance explained, color by condition, and determine whether library size drives PC1.

**Execution:** Executed run/input1_bulk_pca.py on archived synthetic counts and visually inspected figs/input1_bulk_pca.png.

**Checked output:** svd_solver=full; repeated scores bit-identical; max variance-ratio difference 1.11e-16; PC1 6.6%; raw/normalized library-factor correlations +0.960/+0.188; legend ctrl/trtA/trtB; five loading arrows.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] Library-size normalization precedes log transform and scaling — CPM normalization was applied before log2 and scaling.
- [PASS] PCA variance labels match an independent SVD — Maximum ratio difference was 1.11e-16; PC1 was 6.6% in both computations.
- [PASS] The PCA implementation is deterministic for identical input — Two full-SVD fits were bit-identical.
- [PASS] String condition groups receive a truthful categorical legend — Legend labels were ctrl, trtA, and trtB with one scatter per group.
- [PASS] The output contains both a scree view and loading arrows — Ten-component scree and five strongest loadings were rendered.

### Input 2 — Variant A: PCAtools biplot, scree, and loadings on real airway data

**Prompt:** Use PCAtools on VST-normalized airway bulk RNA-seq; color by treatment, shape by cell line, show loading arrows, and make a scree plot without requesting nonexistent components.

**Execution:** Executed run/input2_pcatools_airway.R through r.sh; output assertions completed despite the documented Windows wrapper status anomaly; opened all three PNGs.

**Checked output:** PCAtools 2.18.0; variance 41.94/21.97/16.20 equals prcomp; dynamic scree count 8; biplot 112,409 B, scree 51,062 B, loadings 64,821 B.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:**

- [PASS] Count data are variance-stabilized before PCA — DESeq2 vst(blind=FALSE) was applied before PCAtools.
- [PASS] PCAtools variance percentages match an independent implementation — All eight available component percentages matched prcomp at tolerance 1e-6.
- [PASS] The scree plot does not request nonexistent components — The component count was bounded to eight and no NA slot appeared.
- [PASS] Treatment, cell line, and loadings are visibly encoded — Opened biplot showed treatment color, four cell-line shapes, and loading arrows/labels.
- [PASS] All requested R figures are non-empty and interpretable — Biplot, scree, and loadings PNGs were 51-112 KB and visually inspected.

### Input 3 — Variant B: Raw-HVG Scanpy UMAP and igraph Leiden

**Prompt:** From raw-count AnnData, select seurat_v3 HVGs before normalization, compute PCA(50), neighbors(30), UMAP(min_dist=0.3, seed 42), igraph Leiden, and save the plot to an exact PDF path.

**Execution:** Executed run/input3_scanpy_umap.py on archived synthetic raw counts and opened the rendered PDF.

**Checked output:** Raw integer source true; 500 HVGs; four Leiden clusters; ARI 1.000; seeded UMAP bit-identical; 15-NN retention 0.216; exact PDF 19,501 B.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:**

- [PASS] seurat_v3 HVG selection runs on raw integer counts — Raw integer status was verified before the HVG call, which preceded normalization.
- [PASS] The documented igraph Leiden route works without leidenalg — flavor=igraph completed and produced four clusters.
- [PASS] The planted cluster structure is recovered — Adjusted Rand index was 1.000.
- [PASS] Seeded UMAP is reproducible — Repeated seed-42 embeddings were bit-identical.
- [PASS] The exact output path and quantitative retention are reported — The requested PDF existed and 15-NN retention was 0.216.

### Input 4 — Edge: openTSNE, Rtsne, uwot seeds and small-n perplexity

**Prompt:** Compare explicit openTSNE PCA/auto settings with Rtsne and uwot, prove the supported seed mechanisms, and explain behavior at n=60 with perplexity 30.

**Execution:** Executed run/i4_tsne.py, run/i4b_rtsne_uwot.R, and run/i4c_seedarg.R on the archived six-cluster hierarchy.

**Checked output:** openTSNE repeated fits identical and defaults pca/auto; Rtsne set.seed repeated fits identical while seed= is ignored; uwot seed= works; at n=60 Rtsne p=30 errors and openTSNE clamps to 19.67 with a warning.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:**

- [PASS] Explicit openTSNE PCA initialization and auto learning rate execute reproducibly — Two seed-42 fits were bit-identical.
- [PASS] The skill states openTSNE 1.0 defaults accurately — Runtime signature reported initialization=pca and learning_rate=auto.
- [PASS] Rtsne reproducibility uses set.seed rather than an ignored seed argument — set.seed reproduced exactly; seed=42 without set.seed did not.
- [PASS] uwot uses its supported seed argument — Two uwot seed-42 calls were identical.
- [PASS] Small-sample perplexity behavior is distinguished by implementation — Rtsne errored at 30 while openTSNE warned and clamped.

### Input 5 — Stress: PHATE on continuous and branching trajectories

**Prompt:** Use PHATE for a developmental continuum and a branching trajectory, compare it with UMAP, and validate ordering against planted pseudotime rather than inferring biology from layout alone.

**Execution:** Executed run/i5_phate.py and run/i5b_branching.py; opened PHATE and UMAP comparison figures.

**Checked output:** PHATE 800x2, t=8, bit-identical; |rho| with pseudotime 0.97; branching 10-NN pseudotime error 0.100 vs UMAP 0.124/0.130; cross-branch fraction 0.061 vs 0.101/0.142.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- [PASS] PHATE returns a seeded, reproducible two-dimensional embedding — Two seed-42 embeddings were bit-identical.
- [PASS] Continuous ordering is checked against known pseudotime — Absolute Spearman correlation was 0.97.
- [PASS] Branch preservation is compared quantitatively with UMAP — PHATE had lower pseudotime-neighbor and cross-branch errors in this planted case.
- [PASS] The output avoids claiming PHATE universally outperforms UMAP — The measured advantage was described as modest and dataset-specific.
- [PASS] Trajectory interpretation is not based on 2D geometry alone — All conclusions used planted pseudotime and branch labels.

### Input 6 — Scope Boundary: Shipped example end to end on archived 1,200-cell H5AD

**Prompt:** Run the shipped embedding_phd.py end to end on the archived 1,200-cell, 3,000-gene raw-count H5AD, save every promised figure, and independently reproduce its 15-neighbor retention statistic.

**Execution:** Executed the immutable example copy in run/example with task-local scikit-misc 0.5.2; checked via run/input6_check_full_example.py; rendered and opened five first pages.

**Checked output:** pca 265,455 B; scree 13,378 B; UMAP 17,665 B; t-SNE 68,776 B; PHATE 27,564 B; independent retention 0.164944; caption 16.5% and N=1200.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**

- [PASS] All five promised PDF figures are written and non-empty — PCA, scree, UMAP, t-SNE, and PHATE PDFs were 13-265 KB.
- [PASS] Every first page renders into a meaningful, nonblank plot — All five pages were rendered to PNG and visually opened.
- [PASS] The caption interpolates the true cell count — stdout contained N=1200, not a literal placeholder.
- [PASS] The printed 15-NN retention is independently reproducible — Independent computation yielded 0.164944, which rounds to 16.5%.
- [PASS] Raw-count HVG selection completes without the prior ordering warning — seurat_v3 ran before normalization and emitted no raw-count warning.

### Input 7 — Adversarial: Reject lineage and batch claims inferred from UMAP layout

**Prompt:** UMAP shows A closer to B than C, so they are lineage-related, and UMAP hid our batch. Confirm those conclusions from the plot.

**Execution:** Executed run/i3b_batch_hierarchy.py and run/i7_local_preservation.py on archived planted and real PBMC data.

**Checked output:** Batch R2 peaked on PC4 at 0.83; same-batch kNN fractions were PCA 0.798-0.829 and UMAP 0.940-0.964; PBMC 15-NN retention 0.39-0.41; UMAP/high-dimensional centroid-distance rho 0.22-0.33.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:**

- [PASS] Inter-cluster UMAP distance is not treated as lineage evidence — Planted equidistant clusters had seed-dependent UMAP distance ranks.
- [PASS] Local-neighborhood preservation is measured rather than asserted — 15-NN overlap was reported for real and synthetic data.
- [PASS] Batch association is screened beyond PC1 and PC2 — PC1-PC5 were tested and the planted effect appeared on PC4.
- [PASS] Batch mixing is quantified within biological groups — Same-batch kNN fractions were computed within cell type.
- [PASS] The response stays within research visualization boundaries — No individual diagnostic or treatment inference was made.

### Input 8 — Edge: New: invalid log-like and metadata-incomplete AnnData

**Prompt:** Can I run the shipped workflow on a fractional/log-normalized AnnData, and on another raw-count AnnData that lacks obs['condition']? Validate both before analysis.

**Execution:** Executed run/input8_invalid_contract.py against the fixed example's validator on two new synthetic invalid objects.

**Checked output:** Fractional case: ValueError adata.X must contain raw, non-negative integer counts. Missing metadata case: ValueError adata.obs['condition'] is required.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**

- [PASS] Fractional/log-like values are rejected — The validator raised a raw-count ValueError.
- [PASS] Missing condition metadata is rejected — The validator named obs['condition'] explicitly.
- [PASS] Invalid inputs are not silently coerced — Both checks hard-stopped as required for data integrity.
- [PASS] The errors identify the violated input contract — Messages specify raw integers and the required metadata column.
- [PASS] Re-running validation is side-effect free — The validator only reads the supplied AnnData and deterministically raises.

### Input 9 — Stress: New: minimum shape with twelve condition categories

**Prompt:** Run the shipped comparison at its exact minimum input size (100 cells, 2,000 genes) with 12 condition categories and no pseudotime; ensure the PCA legend uniquely distinguishes every condition.

**Execution:** Generated and executed a new synthetic 100x2,000 raw-count H5AD via run/input9_make_boundary.py; checked via run/input9_check_boundary.py; rendered and opened all five PDFs.

**Checked output:** Five PDFs 9,551-64,156 B; caption N=100; PHATE fallback plotted without pseudotime; 12 condition categories mapped to only 10 distinct tab10 colors, with categories 09-11 sharing the last color.

**Scores:** Basic 32/40 | Specialized 48/60 | Total 80/100

**Assertions:**

- [PASS] The documented minimum shape is accepted — The 100-cell by 2,000-gene raw-count object completed.
- [PASS] All five figures are written at the boundary — All expected PDFs existed and were non-empty.
- [PASS] The caption reports the boundary cell count — stdout contained N=100.
- [PASS] Missing pseudotime uses the documented neutral PHATE fallback — PHATE rendered as an uncolored scatter without failure.
- [FAIL] Every condition category receives a unique visual color — Twelve categories produced only ten colors; conditions 09, 10, and 11 share tab10's last color.

## Visual Inspection

Opened all five rendered pages from the archived full example and all five from the new boundary example, plus the bulk PCA, airway biplot/scree/loadings, Scanpy UMAP, t-SNE, and PHATE comparison PNGs. No plot was blank. The full example clearly shows five planted clusters; the boundary output exposed the duplicated condition colors and repeated loading-label congestion.

## Vetoes

- Skill veto T1-T4: PASS. Nine of nine inputs executed to their intended terminal state; frontmatter contract is valid; supported seeds are explicit; no injection or credential risk was found.
- Research veto M1-M4: PASS. Numerical claims are traceable to logs, no practice boundary was crossed, methodology remained valid, and valid workflows ran while invalid contracts failed intentionally.

## Recommendations

### [P2] Use a categorical palette beyond ten conditions

Observed in: 9

Problem: The shipped PCA code indexes tab10 with integer category positions. With 12 conditions, positions 9-11 all render with the final tab10 color, so the legend is not visually one-to-one.

Root cause: A fixed ten-color ListedColormap is used without a category-count guard or faceting fallback.

Fix: Select a palette with at least n_categories distinct colors (for example tab20 up to 20), and require faceting or a documented alternative when cardinality exceeds the safe palette size. Add a test asserting unique RGBA values per category.

### [P2] Correct the four-versus-five figure description

Observed in: static inspection

Problem: SKILL.md describes the runnable example as saving four figures, while the example and prerequisite checks correctly produce five: PCA, scree, UMAP, t-SNE, and PHATE.

Root cause: The reference summary was not updated when the scree output was added.

Fix: Change 'four saved figures' to 'five saved figures' and keep the explicit filename list in the regression test.

### [P2] Improve PCA loading-label collision handling

Observed in: 1, 6, 9

Problem: The five loading labels can remain congested near the origin, especially in the full and minimum-boundary examples, reducing publication readability even though the arrows are numerically correct.

Root cause: Labels use a fixed vertical offset pattern rather than collision-aware placement.

Fix: Use adjustText or a small deterministic collision-avoidance routine and add a visual-regression check for overlapping loading labels.

## Evidence Paths

- Full-example stdout and PDFs: `run/example/`
- Boundary stdout and PDFs: `run/boundary/`
- Independent 15-NN check: `run/input6_check_full_example.out`
- Regression and new-input logs: `run/*.out`
- Rendered/inspected plots: `figs/`
- Immutable source hashes and commit: `run/source_identity.out`
