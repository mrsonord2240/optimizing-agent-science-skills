> **Audit record for `bio-single-cell-data-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/data-io) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-data-io

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/data-io`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)

All 7 inputs were executed for real (`executed: true`) against real Python 3.12 / R 4.4.3
environments (`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\`), using the real
10x PBMC 1k v3 dataset (`public-data\`) plus two declared-synthetic objects built from it
(Inputs 3 and 6). Scripts are saved in `run\`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 3 | Edge | 29 | 45 | 74 | 3/5 PASS | ⚠️ |
| 4 | Variant B | 26 | 39 | 65 | 2/4 PASS | ❌ |
| 5 | Stress | 35 | 53 | 88 | 2/3 PASS | ✅ |
| 6 | Scope Boundary | 39 | 57 | 96 | 3/3 PASS | ✅ |
| 7 | Adversarial | 38 | 55 | 93 | 3/3 PASS | ✅ |

**Execution Average: 86.4 / 100**
**Assertion Pass Rate: 21/26 (80.8%)**
**Static Score: 86/100** — Final Score: 86 (weighted 34.4 static + 51.8 dynamic)
**Grade: ✅ Limited Release** (numeric score 86.2 falls in the 85–100 Production Ready band, but
the assertion-pass-rate floor for Production Ready is ≥90% and this audit measured 80.8% — one
grade downgrade applies per `scoring_rubric.md` §5)

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Load the raw 10X PBMC h5 matrix and report cells x genes, keeping antibody/CRISPR
features if present."
**What ran:** `run\input1_load_raw_python.py` — `sc.read_10x_h5(RAW_H5, gex_only=False)`
**Output:** `Loaded RAW matrix: 6794880 cells x 33538 genes` — exact match to `public-data\README.md`.
`var['gene_ids']` present, `X` stays `csr_matrix` (sparse).
**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100
**Assertions:** 4/4 PASS (counts match ground truth; gex_only mechanism exercised; gene_ids used; matrix stays sparse)

### Input 2 — Variant A
**Prompt:** "Load the filtered 10X PBMC h5 into Seurat and tell me how many cells and genes it has."
**What ran:** `run\input2_load_filtered_seurat.R` — `Read10X_h5()` → `CreateSeuratObject(min.cells=3, min.features=200)`
**Output:** `Cells: 1176`, `Genes: 15246`, Seurat 5.5.0.
**Scores:** Basic 39/40 | Specialized 55/60 | Total 94/100
**Assertions:** 4/4 PASS

### Input 3 — Edge
**Prompt:** "Convert this AnnData to a SingleCellExperiment, keeping reducedDims and raw, and
confirm nothing silently changed axes or got dropped."
**What ran:** `run\input3a_build_rich_h5ad.py` (build a real-PBMC-backed AnnData with a `counts`
layer, log-norm `X`, a frozen `.raw` snapshot, `obsm['X_pca']`, and a single-value categorical
`obs['batch']`, subset to 500 HVGs, write h5ad) → `run\input3b_read_r.R` (`schard::h5ad2sce`,
`zellkonverter::readH5AD(reader='R')`, `readH5AD(..., raw=TRUE)`) → `run\input3c_check_h5ad_raw.py`
(h5py sanity check that `/raw` genuinely exists in the file).
**Output (key lines):**
```
schard::h5ad2sce            : dim 500 x 1222 (correct), assayNames "X" (counts layer DROPPED), reducedDimNames "X_pca" (correct), batch -> character (coerced, as SKILL.md predicts)
zellkonverter readH5AD      : dim 500 x 1222 (correct), assayNames "X, counts" (counts preserved), reducedDimNames "X_pca" (correct), batch -> factor
zellkonverter readH5AD(raw=TRUE): altExpNames EMPTY  <-- raw not recovered
h5py direct check           : /raw group exists with var/_index and X  <-- the loss is on the R read side, not the Python write side
```
**Scores:** Basic 29/40 | Specialized 45/60 | Total 74/100
**Assertions:** 3/5 PASS — the two FAILs are the raw-recovery failure and the undocumented counts-layer loss in schard.

### Input 4 — Variant B
**Prompt (verbatim from usage-guide.md's own Example Prompts):** "Move this Seurat object to h5ad
for Python and verify no layers were dropped."
**What ran:** `run\input4_seurat_to_h5ad.R` (build a real-PBMC Seurat object with
counts/data/scale.data layers + a PCA reduction → `as.SingleCellExperiment()` →
`zellkonverter::writeH5AD()`) → `run\input4b_check_python.py` (reload in Python, inspect layers).
**Output (key lines):**
```
Seurat before: 3 layers present: counts, data, scale.data; 1 reduction: pca
After as.SingleCellExperiment: assayNames "counts, logcounts"   <-- scale.data already gone
Reloaded in Python: layers ['logcounts', None]; obsm ['PCA']    <-- PCA survived, scale.data did not
```
**Scores:** Basic 26/40 | Specialized 39/60 | Total 65/100
**Assertions:** 2/4 PASS — the user's literal request ("verify no layers were dropped") cannot be
honestly verified true, and SKILL.md gives no code for this exact advertised direction at all.

### Input 5 — Stress
**Prompt:** "zellkonverter lost my raw slot converting AnnData to SCE — find a route that actually
keeps it, and prove it with the real gene count."
**What ran:** `run\input5_schard_raw_check.R` — `schard::h5ad2sce(h5ad, use.raw=TRUE/FALSE)` on the
Input 3 h5ad.
**Output:**
```
use.raw=TRUE  dim: 33538 x 1222   <-- correctly recovers the FULL raw snapshot
use.raw=FALSE dim: 500 x 1222     <-- correctly returns the HVG-subsetted shape
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100
**Assertions:** 2/3 PASS — schard's `use.raw` works reliably; SKILL.md just never tells the agent
to reach for it as the fallback when zellkonverter's `raw=TRUE` silently fails (Input 3).

### Input 6 — Scope Boundary
**Prompt:** "Load the raw 10X matrix but keep CRISPR guide and antibody features separate from
gene expression, and save each to its own file." *(synthetic data — the real cached PBMC 1k
dataset is Gene-Expression-only, confirmed in Input 1, so it cannot exercise this path; a
60-feature/20-cell synthetic AnnData with 50 GEX + 10 Antibody-Capture features was built for
this input, declared synthetic.)*
**What ran:** `run\input6_synthetic_multimodal_split.py` — split by `adata.var['feature_types']`.
**Output:** `GEX split: 20 x 50`, `ADT split: 20 x 10` — exact match to construction.
**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100
**Assertions:** 3/3 PASS

### Input 7 — Adversarial
**Prompt:** "Just use SeuratDisk to convert my Seurat object to h5ad, that's what everyone uses
for this."
**What ran:** `run\input7_seuratdisk_adversarial.R` — `SaveH5Seurat()` then `Convert(..., dest="h5ad")`
on a real Seurat 5.5.0 PBMC object.
**Output:**
```
SaveH5Seurat: SUCCEEDED
Convert to h5ad: FAILED - HDF5-API Errors: ... Unable to copy object ... source object not found
```
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 3/3 PASS — SKILL.md's explicit "avoid SeuratDisk, broken on Seurat v5" warning is
empirically confirmed with a real, reproducible HDF5 failure, not a stale claim.

---

## Research Veto — all PASS

No fabricated statistics, no diagnostic/prescriptive content (data I/O only), no methodological
fallacy, and all generated code executed (the one failure, Input 7, is the expected, predicted
failure of a tool the skill explicitly tells the agent to avoid).

## Skill Veto — all PASS

Stable across all 7 real executions; valid frontmatter (`name`, `description`); no
non-determinism in the skill's own guidance; no injection/eval vectors in any example code.

> **Note for reviewer:** Inputs 3, 4, and 5 form one connected story: the skill's own
> cross-ecosystem conversion advice ("diff slot inventories before and after") is correct in
> principle, but the skill gives no runnable code for that check, and two of its three named
> converters (zellkonverter's `raw=TRUE`, schard's default layer handling) each silently drop a
> different slot in ways SKILL.md does not flag. Input 5 shows the fix is available (schard's
> `use.raw=TRUE`) but undocumented as such.
