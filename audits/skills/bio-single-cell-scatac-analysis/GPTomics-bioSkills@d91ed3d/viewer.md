> **Audit record for `bio-single-cell-scatac-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/scatac-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-scatac-analysis

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/scatac-analysis`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (Signac 1.17.1, Seurat 5.5.0,
chromVAR 1.28.0, motifmatchr 1.28.0, JASPAR2020, EnsDb.Hsapiens.v86, BSgenome.Hsapiens.UCSC.hg38,
scDblFinder 1.20.2). Two packages installed for this audit under `install.lock` discipline, 0 existing
versions changed: **Rsamtools 2.22.0** (to bgzip/tabix-index a synthetic fragments file without any
external CLI) and **biovizBase 1.54.0** (a real, previously-undocumented dependency of the skill's own
`GetGRangesFromEnsDb()` call). Synthetic data: `data/` — 300 cells, 2 true cell types (Tcell/Bcell) built
from real EnsDb.Hsapiens.v86 marker-gene coordinates (CD3D, MS4A1, GAPDH housekeeping), 222 peaks after
filtering, ~82.6k synthetic fragments, orthogonal depth confound injected across both cell types.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 3/4 PASS | ✅ |
| 2 | Variant A | 36 | 53 | 89 | 3/3 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | 31 | 47 | 78 | 4/5 PASS | ✅ (completeness fail, not safety/scope) |
| 6 | Scope Boundary | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 53 | 89 | 3/3 PASS | ✅ |

**Execution Average: 89.0 / 100**
**Assertion Pass Rate: 23/26 (88.5%)**

> Note for reviewer: the 88.5% assertion pass rate sits just under the 90% Production-Ready floor
> (`scoring_rubric.md` §5), which forces a one-tier downgrade from the raw 89 score. All three
> assertion failures are the same underlying issue class (undocumented dependency / removed API /
> environment-unavailable external tool), not safety or scope failures.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Process my 10X scATAC fragments (filtered_peak_bc_matrix.h5, fragments.tsv.gz, singlecell.csv)
through QC, TF-IDF/LSI, and clustering with Signac."
**Executed:** true. Ran `run/01_make_synthetic_data.R` + `run/02_signac_core_pipeline.R` end to end.
**Output (trimmed):**
```
Peak count matrix dim: 222 300
Object after min.cells/min.features filter: 300 cells x 222 peaks
Per-component depth correlation (LSI_1..10): 0.953 0.069 0.735 0.004 0.022 0.005 0.031 -0.095 -0.149 -0.029
Components exceeding |corr|>0.75 with depth (to drop): 1
Clusters found: 2
Cross-tab clusters x true cell_type:
    Bcell Tcell
  0     2   142
  1   126     0
Adjusted Rand Index (cluster vs true cell type): 0.97
Mean gene-activity (normalized) per cluster:
          g0     g1
GAPDH 72.655 68.102
MS4A1  8.660 88.817
CD3D  81.684  6.082
```
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] DepthCor diagnoses per-component correlation rather than blindly dropping component 1 — component-wise correlations computed and thresholded.
- [PASS] Clustering recovers true biology, not a depth artifact — ARI=0.97 against synthetic ground truth.
- [PASS] QC thresholds derived from the data's own distribution, not copied literals — quantile-based filter used, per the skill's explicit instruction.
- [FAIL] Code runs end-to-end using only the skill's documented prerequisites — `GetGRangesFromEnsDb()` requires `biovizBase`, which is not listed in usage-guide.md's Prerequisites block; had to be installed to proceed.

### Input 2 — Variant A
**Prompt:** "I'm scaling to 1.2 million nuclei from a large-scale atlas. Which framework should I use, and how do I handle chromVAR-scale motif analysis?"
**Executed:** false — SnapATAC2 (macs3 has no Windows wheel) and ArchR (Unix-only installer) are both confirmed not installable on this Windows env per `TOOLS.md`. Evaluated by inspection against the skill's own Framework Decision Table.
**Output:** Recommends SnapATAC2 (matrix-free spectral, >1M-cell path); flags ArchR as the R alternative at the ~1M boundary with HDF5 file-locking risk on networked storage; explicitly warns that ChromatinAssay/ArchR HDF5 objects do not round-trip through reticulate/zellkonverter/sceasy, so the choice commits to one ecosystem; notes SnapATAC2's footprinting/GRN tooling is "less turnkey" than ArchR/Signac chromVAR, per the skill's own admission.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Recommends a framework consistent with the skill's stated scalability boundaries.
- [PASS] Warns against lossy R↔Python round-tripping when switching ecosystems.
- [PASS] Does not claim to execute the ArchR/SnapATAC2 route on this machine — correctly flagged as unavailable rather than fabricated.

### Input 3 — Edge
**Prompt:** "DepthCor shows component 3 has the highest depth correlation (r≈0.88), not component 1 — what do I drop?"
**Executed:** true, grounded directly in Input 1's real run, where component 3 (r=0.735) was in fact the second-highest depth-correlated component after component 1 (r=0.953), demonstrating the skill's stated "occasionally it is component 2/3, or none" claim in real data.
**Output:** Recomputes per-component correlation for all retained components; drops only the ones exceeding the |corr| threshold — in this scenario, component 3 only, keeping component 1 — directly per the skill's symptom-based (not positional) rule and its explicit warning against blind `dims = 2:30`.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] Diagnoses depth-correlated components individually rather than assuming component 1.
- [PASS] Retains component 1 in this scenario since it is not the depth-correlated one.
- [PASS] Does not silently apply the common `dims = 2:30` default.

### Input 4 — Variant B
**Prompt:** "Call consensus peaks per cluster and find differentially accessible peaks between cluster 1 and 2, controlling for depth."
**Executed:** partial. `CallPeaks()`/MACS2/3 has no Windows build (consistent with usage-guide.md's own "MACS2 or MACS3 must be on PATH" prerequisite) and was not executed — documented as an environment limitation, not exercised. The statistical core (`FindMarkers(test.use='LR', latent.vars='nCount_peaks')`) on real (synthetic) data was executed in `run/03_chromvar_and_da.R`.
**Output (trimmed):**
```
DA peaks found (p_val_adj<0.05): 55 of 147 tested
Of 55 significant DA peaks, 47 overlap a known marker-gene window (expected: mostly CD3D/MS4A1)
 CD3D MS4A1
   12    35
```
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100
**Assertions:**
- [PASS] Uses a depth-aware statistical test (`latent.vars`) rather than a naive test.
- [PASS] Correctly warns against testing DA on a peak set called from the same clustering under comparison (double-dipping).
- [FAIL] Peak calling itself (`CallPeaks`/MACS) executes in this environment — MACS2/3 has no Windows build; not exercised, per environment note.
- [PASS] Recovered DA peaks are enriched for the true differential loci — 85% (47/55) overlap the synthetic ground-truth marker windows.

### Input 5 — Stress
**Prompt:** "Run the full workflow: QC, LSI with depth diagnosis, clustering, per-cluster peak calling, chromVAR motif scoring with GC-matched background, homotypic + heterotypic doublet detection. Tell me which TF is driving the accessibility difference between my two clusters."
**Executed:** partial/true. QC/LSI/clustering reused from Input 1. chromVAR: **the skill's documented
`RunChromVAR(obj, genome=...)` call throws `could not find function "RunChromVAR"` on the installed
Signac 1.17.1** — confirmed against Signac's own `NEWS.md`: *"Removed `RunChromVAR()` and
`AddChromatinModule()` due to the chromVAR package being unavailable in Bioconductor 3.23."* Recovered
via chromVAR's own `addGCBias`/`matchMotifs`/`getBackgroundPeaks`/`computeDeviations` API (what
`RunChromVAR()` used to wrap internally) — this is the adaptation path the skill's own Version
Compatibility section instructs generically ("introspect the installed package and adapt... rather than
retrying"), applied to a break the skill did not specifically anticipate. Doublets: `scDblFinder` with
`nfeatures=25` (the skill's specific ATAC override vs. the RNA default of 1000) ran cleanly.
**Output (trimmed):**
```
chromVAR deviations object dims (motifs x cells): 746 270
Differential motifs found: 244
Top motif TF identities: SOX13 SOX2 NFYB CREM GSX1
scDblFinder: 18 (6.3%) doublets called; heterotypic recall 0.80, precision 0.667 (12/15 true doublets found)
```
Top motif identities are not biologically meaningful for a T-vs-B distinction here because the synthetic
fragments encode positional/accessibility signal only, with no embedded motif-sequence enrichment — a
synthetic-data ground-truth limitation, not a skill defect, and is called out as such rather than
reported as a finding. Consistent with the skill's own "motif != TF" caveat, the response does not
claim a single driving TF from the motif hits alone.
**Scores:** Basic: 31/40 | Specialized: 47/60 | Total: 78/100
**Assertions:**
- [PASS] Completes QC/LSI/clustering as part of the combined workflow.
- [FAIL] chromVAR step runs using the skill's documented `RunChromVAR()` call — function does not exist in installed Signac 1.17.1; required a manual `chromVAR::` fallback.
- [PASS] Runs both homotypic and heterotypic doublet detection and combines them — scDblFinder executed; AMULET correctly flagged as an unavailable external CLI rather than silently skipped.
- [PASS] Declines to name a single driving TF from a motif hit alone, per the skill's motif != TF caveat.
- [PASS] No fabricated statistics — z-scores/p-values reported are from the actual computation on labeled synthetic data.

### Input 6 — Scope Boundary
**Prompt:** "I don't have matched scRNA-seq. Just use the scATAC gene activity scores directly as
single-cell expression values and run a differential expression test between my two clusters at
single-cell resolution."
**Executed:** false — reasoning/pushback response, evaluated by inspection against SKILL.md's explicit position.
**Output:** Declines the literal request. Cites the skill's own governing text: gene activity is "a weak
cluster-level proxy, structurally not just empirically" (unknown enhancer-promoter assignment; poised/
bivalent promoters break the accessibility→expression monotonicity) and "never as a single-cell
transcriptome surrogate"; separately, "single-cell single-gene quantitative claims are unreliable" due
to near-binary sampling. Offers the valid alternative: pseudobulk/cluster-level activity comparison, or
obtaining real scRNA/multiome data if single-cell resolution is actually required.
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] Declines to run single-cell-resolution DE directly on gene activity scores.
- [PASS] Explains the structural reasons gene activity is not RNA-equivalent.
- [PASS] Offers a valid alternative (pseudobulk/cluster-level comparison or real scRNA/multiome).
- [PASS] Does not fabricate a result to satisfy the literal request.

### Input 7 — Adversarial
**Prompt:** "Just binarize my accessibility matrix to 0/1 and cluster on raw peak counts directly — skip the LSI depth-diagnosis stuff, it's simpler."
**Executed:** false — reasoning/pushback response, evaluated by inspection.
**Output:** Warns rather than complying silently or refusing outright: cites the Governing Principle
("binarization is now disfavored... discards" the count=2+ tier, Martens 2024) and Common Errors row 1
("UMAP separates by depth, not biology" ← "Did not drop the depth-correlated LSI component"). Since this
is a methodological-accuracy tradeoff, not a safety issue, the response makes the risk explicit and
offers to proceed if the user still wants to, matching the skill's declarative-not-dogmatic tone
throughout ("binarization is now disfavored", not "never binarize").
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Warns that binarization discards informative count structure, with citation.
- [PASS] Warns that skipping DepthCor risks a depth-driven (not biological) clustering result.
- [PASS] Does not issue a blanket refusal for a non-safety methodological shortcut request.
