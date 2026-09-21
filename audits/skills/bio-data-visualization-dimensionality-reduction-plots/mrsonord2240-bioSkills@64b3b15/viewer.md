> **Audit record for `bio-data-visualization-dimensionality-reduction-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/dimensionality-reduction-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-dimensionality-reduction-plots (first audit)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/dimensionality-reduction-plots` (unmodified upstream GPTomics/bioSkills; `run\skill\` is a `git archive` copy, nothing written into the repo)
Category: Data Analysis | Mode: A (SKILL.md blocks + shipped example run from copies) | Complexity: Complex, 7 inputs, 7/7 executed
Env: `F:\OpenScience\audit-envs\data-visualization\` (`py.sh`, `r.sh`; scanpy 1.12.4, umap-learn 0.5.12, openTSNE 1.0.4, phate 2.0.0, scikit-learn 1.9.1, PCAtools 2.18.0, Rtsne 0.17, uwot 0.2.4). Data: **synthetic** planted clusters / batch / trajectories (`run\common.py`, seeded) plus **real** Bioconductor `airway` and scanpy `pbmc68k_reduced`.

## Result

| | |
|---|---|
| Static | **71** / 100 |
| Execution average | **77.3** / 100 |
| Final | **75** (28.4 + 46.4 = 74.8) |
| Assertions | **21/33 = 63.6%** |
| Grade | **Beta Only, not deployable** (numeric 75 = Limited Release, dropped one tier: assertion pass rate below the 80% floor) |
| Vetoes | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | **0** / 6 / 6 |

Floors (scoring_rubric section 5) for Limited Release: static 71 >= 70 ok, execution 77.3 >= 75 ok, Layer 1 avg 31.9 >= 28 ok, Layer 2 avg 45.4 >= 42 ok, **assertions 63.6% < 80% miss** -> one tier down.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: sklearn PCA, variance labels, batch/library size (synthetic) | 32 | 46 | 78 | 3/5 PASS | ✅ |
| 2 | Variant A: PCAtools biplot/scree/loadings, real airway (R) | 33 | 49 | 82 | 4/5 PASS | ✅ |
| 3 | Variant B: scanpy PCA-neighbors-UMAP-Leiden-save, synthetic + real pbmc68k_reduced | 31 | 44 | 75 | 3/5 PASS | ✅ |
| 4 | Edge: openTSNE / Rtsne / uwot, seeds, small-n perplexity | 31 | 43 | 74 | 3/5 PASS | ⚠️ |
| 5 | Stress: PHATE vs UMAP on continuous and branching trajectories | 34 | 50 | 84 | 4/4 PASS | ✅ |
| 6 | Scope boundary: shipped `examples/embedding_phd.py` end to end | 28 | 37 | 65 | 2/5 PASS | ❌ (PARTIAL) |
| 7 | Adversarial: "read UMAP distances / UMAP hides batch" against measurement | 34 | 49 | 83 | 2/4 PASS | ✅ |

**Execution Average: 77.3 / 100** | **Assertion Pass Rate: 21/33** | Shipped-means-present: PASS (SKILL.md and usage-guide point at no local files; all six Related Skills paths exist at the commit; the one example ships).

## Detailed Outputs

Scripts are in `run\`, raw stdout in `run\i*.out`, figures in `figs\` (each opened with the Read tool, none blank).

### Input 1 - Canonical: SKILL.md Python PCA block on bulk counts
**Prompt:** "PCA of my bulk RNA-seq (3 conditions x 2 batches, 60 samples, 2000 genes); label axes with variance explained, colour by condition; is the library size behind PC1?"
**Ran:** `run\i1_pca_python.py` (block verbatim), `run\i1b_pca_determinism.py`. Ground truth: numpy SVD of the centred matrix.
```
label PC1/PC2 = 32.0 10.3 | SVD truth = 32.0 10.3          solver randomized, max |ratio diff| 0.0005-0.0007
A2 colour-by-group mapping correct: True                    (facecolors == viridis(norm(code)))
PC2 R2 condition=0.99 ; PC3 R2 batch=0.94 ; PC1 corr(libfactor)=+0.99 (unnormalised log2)
string labels c=labels FAILS: ValueError 'c' argument must be a color ... not <StringArray>
RAW counts PC1 corr libfactor +0.96 | log+scale +0.99 | CPM+log+scale +0.19 (batch PC1 R2 0.97, condition PC2 R2 0.98)
i1b: PCA(n_components=10) run twice -> identical False, max|score diff| 15.3; svd_solver='full' True; random_state=42 True
```
`figs\i1_pca_skillblock.png`: three condition bands, PC1 (32.0%) / PC2 (10.3%), scree with elbow at PC4. **Scores:** 32 / 46 / 78.
- [PASS] Axis-label percentages equal independent SVD.
- [PASS] Colour-by-group mapping correct.
- [FAIL] Block accepts string condition labels and identifies groups (no category step, no legend).
- [FAIL] "log + scale" removes library-size PC1 (r stays 0.99; needs size-factor normalisation).
- [PASS] Warning that unnormalised PCA is library-size driven is accurate.
Also found: the "PCA is deterministic" claim fails for this exact block (randomized solver, sign/rotation changes between runs).

### Input 2 - Variant A: PCAtools on real airway (R)
**Ran:** `run\i2_pcatools_airway.R` via `r.sh`: `DESeqDataSet(airway, ~cell+dex)`, `vst(blind=FALSE)`, SKILL.md block (dex/cell substituted for condition/batch).
```
PCAtools 2.18.0 | p$variance[1:3] 41.94 21.97 16.2 == prcomp 41.94 21.97 16.2 (percent, all.equal 1e-6, PC1 cor +1)
biplot ok (dex colour, cell shape); biplot(colby='condition') on airway: undefined columns (data adaptation)
screeplot(components = 1:10) ok ; plotloadings(components = 1, rangeRetain = 0.05) ok (ENSG00000101347, ENSG00000211445 ...)
biplot(showLoadings=TRUE) ok (Skill gives no code for it)
PC1 R2 dex=0.95 ; PC2 R2 cell=0.98 ; raw counts: PC1 51.1%, top-10 genes = 65% of PC1 loading^2
```
`figs\i2_biplot.png`, `i2_scree.png`, `i2_loadings.png`, `i2_biplot_loadings.png` opened; trt right / untrt left on PC1, title "PC1 (41.9%)". **Scores:** 33 / 49 / 82.
- [PASS] p$variance is percent = prcomp. [PASS] biplot mapping correct. [PASS] scree/loadings run verbatim (with 8 samples the hard-coded `components = 1:10` draws an empty `NA` slot in the scree).
- [FAIL] "Show loadings as arrows" is promised (usage-guide) but no code/argument given. [PASS] raw-count dominance warning accurate.

### Input 3 - Variant B: scanpy workflow, synthetic 4 clusters + real pbmc68k_reduced
**Ran:** `run\i3_scanpy_umap.py`.
```
leiden FAILED as called: ModuleNotFoundError No module named 'leidenalg'
leiden flavor=igraph OK; n clusters 4 ARI vs planted 1.0
save='_clusters.pdf' -> figures\umap_clusters.pdf ; save='myplot.pdf' -> figures\umapmyplot.pdf ; cwd empty
scanpy umap seed 42 twice identical: True | seed 7: False | WITHOUT random_state twice identical: True (default random_state=0)
umap-learn seed=42 twice identical: True (warning: n_jobs overridden to 1) | WITHOUT random_state: False
UMAP colours == cluster_true palette: True ; kNN purity PCA 0.999 UMAP 1.0
pbmc68k_reduced (700 cells): kNN purity UMAP 0.729 vs PCA 0.703
```
`figs\i3_umap_true.png`, `i3_pbmc.png` opened. **Scores:** 31 / 44 / 75.
- [PASS] save-path trap accurate. [PASS] seeded UMAP reproducible. [FAIL] "without seed results vary" (false for scanpy). [FAIL] `sc.tl.leiden` as written needs leidenalg (not in pip line). [PASS] colour mapping and clusters right.

### Input 4 - Edge: t-SNE and uwot, seeds, perplexity
**Ran:** `run\i4_tsne.py` (openTSNE block verbatim, 1500 cells, 6 clusters in 3 super-groups), `run\i4b_rtsne_uwot.R`, `run\i4c_seedarg.R`.
```
openTSNE seed 42, n_jobs=-1 twice identical True | default learning_rate 'auto' (=n/12=125), initialization 'pca'
Spearman(centroid dists) KB 0.61/0.66/0.52/0.63 | random init lr=200 0.39/0.30/0.13/0.59 | openTSNE defaults 0.68/0.66/0.51/0.67
Rtsne formals: seed FALSE, Y_init TRUE, max_iter TRUE ; Rtsne set.seed(42) twice identical TRUE
Rtsne(seed=42) twice (no set.seed) identical: FALSE   uwot umap(seed=42) twice identical: TRUE
n=60: Rtsne perplexity 30 ERROR 'perplexity is too large'; 19, 5 run. openTSNE: 'Perplexity value 30 is too high. Using perplexity 19.67 instead'
kNN purity Rtsne 0.903, uwot 0.999
```
`figs\i4_tsne.png`, `i4b_r_embeddings.png` opened. **Scores:** 31 / 43 / 74.
- [PASS] openTSNE block runs, reproducible. [PASS] PCA init helps global structure. [FAIL] "lr n/12 not default 200 / init pca NOT random" (openTSNE defaults already). [FAIL] "seed=42 (Rtsne)" silently ignored. [PASS] small-n perplexity rule.

### Input 5 - Stress: PHATE
**Ran:** `run\i5_phate.py`, `run\i5b_branching.py`.
```
PHATE (knn=10, decay=40, t='auto', random_state=42): 800x2, t=8, twice identical True; colour == viridis(pseudotime) True
|Spearman| pseudotime vs principal axis: PHATE 0.97, UMAP 0.98, PCA 0.88 ; knn=3/10/40 rho 0.97/0.97/0.96
Branching: mean |d pseudotime| in 10-NN  high-dim 0.159 | PHATE 0.100 | UMAP nn30 0.124 | UMAP nn15 0.130
discrete 4 clusters kNN purity PHATE 0.998, UMAP 1.000
```
`figs\i5_phate.png`, `i5_umap_vs_phate.png` opened. **Scores:** 34 / 50 / 84. All 4 assertions PASS (margin over UMAP is modest; SGD-MDS convergence warnings not mentioned).

### Input 6 - Scope boundary: shipped `examples/embedding_phd.py`
**Ran:** copy in `run\ex`, synthetic `processed.h5ad` (1200 cells x 3000 genes, 5 clusters, `obs['condition']`, made by `run\mk_h5ad.py`; the example's file is not shipped). `run\i6_example_checks.py`, `i6b.py`, `i6c_colors.py`, `render_pdf.sh` (Ghostscript in WSL renders the PDFs).
```
As shipped: ModuleNotFoundError: No module named 'skmisc'  (after installing scikit-misc 0.5.2 + leidenalg 0.12.0 via pip --target run\pylib: runs to the end)
warning: flavor='seurat_v3' expects raw count data, but non-integers were found.
HVG overlap raw-vs-logged 1749/2000 ; planted markers captured raw 295/300, logged (example order) 288/300
scanpy variance_ratio[:3] = 1.10 1.05 0.99 == independent SVD ; PC1..5 sum 4.7% while leiden ARI vs planted = 1.000
caption node: Constant (not f-string) -> prints literal 'N={n}' ; savefig calls 2 for 4 figures (scree, PHATE never saved)
cmap='tab10' on 2 condition codes -> blue (0.12,0.47,0.71) and cyan (0.09,0.75,0.81); UMAP/t-SNE cluster colours identical across panels (True)
```
`figs\i6_pca.png` (PC1 (1.1%) / PC2 (1.1%), three clusters), `i6_tsne.png` (5 clusters), `i6_umap_clusters.png` opened. **Scores:** 28 / 37 / 65.
- [FAIL] runs as shipped. [PASS] with deps: labels equal independent computation, outputs non-blank. [FAIL] HVG step sound. [FAIL] every figure/caption usable. [PASS] example encodes the listed traps.

### Input 7 - Adversarial: "UMAP shows A closer to B than C, so they are lineage-related; and UMAP hid our batch"
**Ran:** `run\i3b_batch_hierarchy.py` (3 planted equidistant cell types + batch on 100 genes), `run\i7_local_preservation.py` (real pbmc68k_reduced).
```
PC R2 batch: PC1 0.00 PC2 0.00 PC3 0.04 PC4 0.83 | PC R2 celltype: 0.98 0.98 0 0 0
same-batch kNN fraction within cell type (0.5 = mixed): PCA 0.83/0.80/0.80 | UMAP 0.96/0.94/0.95
PCA centroid distances 13.5 13.9 13.3 (equidistant) ; UMAP (normalised, 5 seeds) e.g. 0.99 1.00 0.81 / 0.70 0.80 1.00 / 1.00 0.58 0.86 ...
pbmc68k_reduced 15-NN kept in 2-D: UMAP 0.41 / 0.39 / 0.39 ; synthetic 1500 cells UMAP 0.14, t-SNE 0.23
pbmc centroid-distance Spearman high-dim vs UMAP: 0.32 0.28 0.22 0.31 0.33 ; between seeds 0.87-0.98
```
**Scores:** 34 / 49 / 83.
- [PASS] "Do not read inter-cluster distance; check in high-dim" is right (equidistant clusters get arbitrary UMAP distances). [FAIL] "local neighborhoods preserved by construction" (kept 0.14-0.41). [FAIL] batch on PC1/PC2 / "UMAP can hide batch" (batch on PC4; UMAP exposed it more). [PASS] scope: research-only, caption asks for limits.

## Vetoes
- Skill veto: stability, contract (frontmatter name/description present), determinism (seeds documented; P1 for PCA), security (no exec of user strings, no credentials) all PASS.
- Research veto: M1 PASS (references verified), M2 PASS (no individual clinical content), M3 PASS (core guidance sound, errors recorded P1/P2), M4 PASS (all blocks executed; the omitted pip packages are explicit ImportErrors, recorded P1).

## Environment notes
- `scikit-misc` 0.5.2 and `leidenalg` 0.12.0 installed with `pip --target F:\OpenScience\audits\...\run\pylib` only (PYTHONPATH for the example); no shared env changed, no install.lock needed. Not used for inputs 1-5.
- `run\render_pdf.sh` runs Ghostscript in WSL `dv-cli` (`/mnt/openscience` mount only).
- Never killed any process by name.

## Recommendations (0 P0, 6 P1, 6 P2)
P1: Rtsne `seed=` ignored; "PCA is deterministic" but sklearn block is not (randomized solver, no random_state); shipped example not runnable as shipped (skmisc, leidenalg, placeholder h5ad, pip line); seurat_v3 HVG on log data; batch/library-size guidance (log+scale insufficient, PC1/PC2-only, "UMAP hides batch" contradicted); example drops figures and prints literal `{n}`.
P2: openTSNE defaults; "local neighborhoods preserved by construction"; "PC1=5% may be noise"; perplexity heading; no Python loadings/legend code and scanpy seed/save notes; usage-guide duplicates SKILL.md. Full text in the JSON.
