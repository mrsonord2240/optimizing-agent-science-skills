> **Audit record for `bio-data-visualization-dimensionality-reduction-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@228b1ca](https://github.com/mrsonord2240/optimized-scientific-skills/tree/228b1caf42f42053a16db2dfe0f67fcb2005a413/skills/bio-data-visualization-dimensionality-reduction-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-dimensionality-reduction-plots

Generated: 2026-09-27  
Source: `mrsonord2240/optimized-scientific-skills@228b1caf42f42053a16db2dfe0f67fcb2005a413:skills/bio-data-visualization-dimensionality-reduction-plots`  
Independent round-2 re-auditor: true  
Category: Data Analysis | Mode: D (instructions plus shipped CLI) | Complexity: Complex  
Data: archived synthetic regressions, real Bioconductor airway, real Scanpy PBMC, and new seeded 20-category synthetic AnnData.

## Result

Static: **96/100** | Execution average: **94.5/100** | Final: **95/100 — ⭐ Production Ready**  
Executed: **11/11** | Assertions: **55/55 = 100%** | Vetoes: **none** | Deployable: **true**  
Open P0/P1/P2: **0/0/0**. Production floors all pass: static 96, execution 94.5, Layer 1 average 37.5/40, Layer 2 average 57.0/60, assertions 100%.

The eleven inputs comprise all nine archived regressions plus two genuinely new cases. The count exceeds the ordinary complexity cap because this re-audit was required to preserve the prior regression set and add new adversarial coverage.

## Static Evaluation

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 12/12 | Covers PCA, t-SNE, UMAP, PHATE, preprocessing, method choice, quantitative checks, exact outputs, palettes through 20 categories, and interpretation limits. |
| Reliability | 11/12 | Strict input checks and deterministic reruns are strong; errors are specific but not machine-coded. |
| Performance Context | 7/8 | Progressive references keep the 220-line main skill focused; the all-method comparison is intentionally compute-heavy. |
| Agent Usability | 16/16 | Decision flow, five-file contract, palette guard, label collision routine, and failure modes are explicit. |
| Human Usability | 8/8 | Natural prompts, truthful legends, and the >20 escape hatch are directly usable. |
| Security | 12/12 | No credentials, network calls, raw-string execution, destructive operations, or sensitive-data logging. |
| Maintainability | 12/12 | Two references, one CLI, and seven focused tests cleanly separate and verify behavior. |
| Agent Specific | 18/20 | Triggering, disclosure, determinism, and stop conditions are strong; the mixed advisory/CLI surface is broader than a narrow API. |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical: bulk PCA | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A: PCAtools airway | 37 | 57 | 94 | 5/5 | ✅ |
| 3 | Variant B: Scanpy UMAP/Leiden | 38 | 58 | 96 | 5/5 | ✅ |
| 4 | Edge: t-SNE/UMAP seed semantics | 37 | 57 | 94 | 5/5 | ✅ |
| 5 | Stress: PHATE trajectories | 37 | 55 | 92 | 5/5 | ✅ |
| 6 | Scope Boundary: 1,200-cell shipped example | 38 | 57 | 95 | 5/5 | ✅ |
| 7 | Adversarial: reject UMAP storytelling | 38 | 58 | 96 | 5/5 | ✅ |
| 8 | Edge: invalid AnnData contracts | 36 | 55 | 91 | 5/5 | ✅ |
| 9 | Stress: 12-category minimum shape | 38 | 57 | 95 | 5/5 | ✅ |
| 10 | Edge: exhaustive 1-20 palette and >20 guard | 38 | 58 | 96 | 5/5 | ✅ |
| 11 | Stress: 20-category end-to-end and loading labels | 38 | 58 | 96 | 5/5 | ✅ |

## Detailed Outputs

### Input 1 — Bulk PCA with variance labels and library-size diagnosis

**Prompt:** PCA of bulk RNA-seq with three conditions, two batches, 60 samples, and 2,000 genes; label axes with variance explained, color by condition, and test whether library size drives PC1.

**Execution:** `run/input1_bulk_pca.py` on archived synthetic counts. Full-SVD fits were bit-identical; variance ratios matched independent SVD within `1.11e-16`; PC1 was 6.6%; raw versus normalized library-factor correlations were +0.960 versus +0.188; three truthful legend groups and five loading arrows rendered.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:** PASS — normalization before transform/scale; independent variance match; deterministic PCA; truthful string-group legend; scree and loading arrows present.

### Input 2 — PCAtools biplot, scree, and loadings on airway data

**Prompt:** Use PCAtools on VST-normalized airway RNA-seq, color by treatment, shape by cell line, show loadings, and bound the scree to available components.

**Execution:** `run/input2_pcatools_airway.R` through `r.sh`. PCAtools 2.18.0 matched `prcomp` for all eight components; biplot, scree, and loadings PNGs were 51-112 KB and visually inspected.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:** PASS — VST precedes PCA; variance matches independent implementation; scree is bounded; treatment/cell/loadings are encoded; all figures are meaningful.

### Input 3 — Raw-HVG Scanpy UMAP and igraph Leiden

**Prompt:** From raw AnnData, select `seurat_v3` HVGs before normalization, compute PCA/neighbors/UMAP, run igraph Leiden, and save to an exact path.

**Execution:** `run/input3_scanpy_umap.py`. Raw integer input was verified; 500 HVGs retained; four planted clusters recovered at ARI 1.000; repeated UMAP was bit-identical; 15-neighbor retention was 0.216; exact PDF was written and rendered.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:** PASS — raw-count HVG order; igraph route; planted clusters; seeded reproducibility; exact path plus retention.

### Input 4 — openTSNE, Rtsne, uwot seeds and small-n perplexity

**Prompt:** Compare seed mechanisms and small-sample perplexity behavior across openTSNE, Rtsne, and uwot.

**Execution:** `run/i4_tsne.py`, `run/i4b_rtsne_uwot.R`, and `run/i4c_seedarg.R`. openTSNE confirmed PCA/auto defaults and deterministic seed-42 fits; Rtsne required `set.seed`; uwot's `seed=` reproduced; Rtsne rejected invalid small-n perplexity while openTSNE emitted clamp messages and ran.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:** PASS — openTSNE provenance; accurate defaults; Rtsne seed semantics; uwot seed semantics; implementation-specific perplexity behavior.

### Input 5 — PHATE on continuous and branching trajectories

**Prompt:** Compare PHATE with UMAP on continuous and branching planted trajectories, validating against known pseudotime rather than layout alone.

**Execution:** `run/i5_phate.py` and `run/i5b_branching.py`. Seeded PHATE was identical across runs; absolute pseudotime correlation was 0.97; branch-neighborhood and cross-branch errors were quantified; convergence warnings were preserved.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:** PASS — deterministic embedding; known-pseudotime validation; quantitative UMAP comparison; no universal superiority claim; no 2D-only trajectory inference.

### Input 6 — Shipped example on the archived 1,200-cell H5AD

**Prompt:** Run the shipped CLI end to end, save every promised figure, and reproduce its 15-neighbor retention statistic independently.

**Execution:** Current immutable example copied to `run/example/`. It produced PCA, scree, UMAP, t-SNE, and PHATE PDFs (13-255 KB); all rendered nonblank; stdout reported N=1200; independent retention was 0.164944 and matched the printed 16.5%.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:** PASS — five outputs; meaningful renders; true cell count; independent retention; raw-count HVG ordering.

### Input 7 — Reject lineage and batch claims inferred from UMAP layout

**Prompt:** "UMAP shows A closer to B than C, so they are lineage-related, and UMAP hid our batch. Confirm those conclusions."

**Execution:** `run/i3b_batch_hierarchy.py` and `run/i7_local_preservation.py`. UMAP centroid ranks varied by seed; PBMC 15-neighbor retention was 0.39-0.41; planted batch association peaked on PC4 at R2 0.83; within-cell-type batch mixing was quantified.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:** PASS — no lineage inference from inter-cluster distance; retention measured; PC1-PC5 batch screen; biology-stratified mixing; research scope respected.

### Input 8 — Invalid log-like and metadata-incomplete AnnData

**Prompt:** Validate a fractional/log-normalized AnnData and another raw-count object missing `obs['condition']` before analysis.

**Execution:** `run/input8_invalid_contract.py`. Both inputs stopped with specific deterministic `ValueError`s; no coercion or analysis occurred.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:** PASS — fractional values rejected; missing metadata rejected; no silent coercion; contract identified; validation is side-effect free.

### Input 9 — Minimum shape with twelve conditions

**Prompt:** Run the exact 100-cell by 2,000-gene minimum with 12 conditions and no pseudotime; require one visual color per condition.

**Execution:** `run/input9_make_boundary.py`, current CLI, and `run/input9_check_boundary.py`. Five PDFs were written; caption contained N=100; neutral PHATE fallback rendered; 12 categories produced 12 distinct RGBA values. All five pages were opened.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:** PASS — minimum shape; five figures; true caption count; pseudotime fallback; unique category colors.

### Input 10 — New exhaustive palette and guard probe

**Prompt:** Prove that every supported category cardinality through 20 receives deterministic one-to-one colors and that unsupported cardinalities stop with a usable fallback.

**Execution:** `run/input10_palette_guard.py`. Counts 1-20 each returned exactly that many distinct RGBA rows, identically across two calls. Counts 0, 21, 25, and 50 raised the documented `ValueError` directing the caller to facet or use an alternative encoding.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:** PASS — requested shapes; one-to-one uniqueness; determinism; no recycling above 20; actionable fallback.

### Input 11 — New 20-category end-to-end and loading-label determinism

**Prompt:** Run the shipped CLI on an exact-boundary 20-condition object; require the five-file contract, twenty distinct condition colors, and deterministic non-overlapping loading labels.

**Execution:** `run/input11_make_twenty.py`, current CLI, and `run/input11_check_twenty.py`. Exactly the five documented PDF names existed and parsed as PDFs; all rendered nonblank; 20 unique RGBA colors were present. Actual strongest-loading endpoints produced pairwise non-overlapping rendered text boxes. Two independent placement passes selected identical offsets. `figs/input11_loading_labels.png` was opened and confirmed readable.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:** PASS — exact five names; valid non-empty PDFs; twenty unique colors; actual label boxes do not overlap; placement is deterministic.

## Visual Inspection

Opened the bulk PCA, airway biplot, Scanpy UMAP, t-SNE, PHATE comparison, full-example PCA, 12-category PCA, all five 20-category pages, and the actual-loading-label proof. No output was blank. The 12- and 20-category legends were one-to-one. The five example loading labels were separated; the direct bounding-box check confirmed pairwise non-overlap on actual 20-category PCA loadings.

## Vetoes

- Skill veto T1-T4: **PASS**. Eleven of eleven inputs reached their intended terminal state; the frontmatter and output contracts are coherent; supported seeds are explicit; no injection or credential risk was found.
- Research veto M1-M4: **PASS**. Numerical claims are traceable to evidence, no practice boundary was crossed, methodology remained valid, and all valid code paths ran while invalid contracts failed intentionally.

## Recommendations

No open P0, P1, or P2 findings. The three prior P2 findings are closed by executed evidence: unique colors through 20 with a >20 guard, an accurate five-figure contract, and deterministic rendered-box collision avoidance for PCA loading labels.

## Evidence Paths

- Full example: `run/example/`
- Twelve-category boundary: `run/boundary/`
- New twenty-category boundary: `run/twenty/`
- Exhaustive palette/guard: `run/input10_palette_guard.out`
- Actual loading-label check: `run/input11_check_twenty.out` and `figs/input11_loading_labels.png`
- Provider focused tests: `run/provider_tests.out`
- Source commit, hashes, and clean status: `run/source_identity_round2.out`
- All runnable audit scripts: `run/`
