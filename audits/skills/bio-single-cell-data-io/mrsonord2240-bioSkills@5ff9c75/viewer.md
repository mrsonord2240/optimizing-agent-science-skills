> **Audit record for `bio-single-cell-data-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5ff9c75](https://github.com/mrsonord2240/bioSkills/tree/5ff9c75dc947fa7c7292315ae64198769d067faf/single-cell/data-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-data-io

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23
Phase: Final pass, Phase 2 only
Source audited: `mrsonord2240/bioSkills@5ff9c75dc947fa7c7292315ae64198769d067faf:single-cell/data-io`
Environment: `single-cell-transcriptomics-analyst`
Auditor independent: **false** — final pass: fixed and audited under one brief, see CHECKPOINT.md.

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Result

**94/100 — Production Ready — deployable: true — veto: none.**

Static: 93/100. Dynamic execution: 95.1/100. Assertions: 32/33 (97.0%).
All nine required dynamic inputs were freshly executed. The prior report is preserved at
`F:/OpenScience/audits/_pre-fix-20260919/bio-single-cell-data-io/`.

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical raw 10x H5 | 39 | 57 | 96 | 4/4 | yes |
| 2 | Variant A Seurat load | 39 | 56 | 95 | 4/4 | yes |
| 3 | Edge rich h5ad conversion | 37 | 55 | 92 | 3/4 | yes |
| 4 | Variant B Seurat to h5ad | 39 | 56 | 95 | 4/4 | yes |
| 5 | Stress raw and counts tradeoff | 39 | 56 | 95 | 3/3 | yes |
| 6 | Scope boundary GEX+ADT | 39 | 58 | 97 | 3/3 | yes |
| 7 | Adversarial SeuratDisk | 38 | 57 | 95 | 3/3 | yes |
| 8 | New synthetic 10x MEX | 39 | 58 | 97 | 4/4 | yes |
| 9 | New source-code syntax check | 38 | 56 | 94 | 4/4 | yes |

## Fresh execution evidence

All commands were saved beneath [run](run/). Python used the shared audit venv; R used
`run/fp2_run_r.sh`, which delegates to the environment's required `tools/rs.sh` wrapper.
The expected SeuratDisk failure and one R nonzero exit after a completed assertion were scored
from their verified output, not exit status alone.

### Input 1 — real raw Cell Ranger H5

Prompt: “Load the raw Cell Ranger matrix with Ensembl IDs, retain all feature types, and confirm it remains sparse.”

Generated test code: [fp2_input1_raw_load.py](run/fp2_input1_raw_load.py)

```text
shape (6794880, 33538)
sparse True
gene_ids True
feature_types ['Gene Expression']
PASS input1
```

### Input 2 — real filtered H5 to Seurat v5

Prompt: “Create a Seurat v5 object from filtered Cell Ranger H5 and report orientation and storage.”

Generated test code: [fp2_input2_seurat_load.R](run/fp2_input2_seurat_load.R)

```text
counts_dim genes_x_cells 15246 1176
sparse TRUE
PASS input2
```

The wrapper emitted `PASS input2` after all assertions; its process status was nonzero without an
additional R error. The measured object and assertions are the evidence.

### Input 3 — rich AnnData to SCE with raw recovery

Prompt: “Convert a rich h5ad to R, retain counts and embeddings, and recover the full raw snapshot.”

Generated test code: [fixture builder](run/fp2_input3_build_rich.py) and
[conversion test](run/fp2_input3_conversion.R).

```text
hvg_shape (1222, 700) raw_shape (1222, 33538) obsm ['X_pca']
zell_dim 700x1222 zell_altExp_length 0 zell_assays X,counts
schard_raw_dim 33538x1222 schard_hvg_dim 700x1222
schard_raw_nonzero TRUE schard_raw_has_na FALSE
PASS input3
```

The current skill correctly routes raw recovery through `schard::h5ad2sce(use.raw=TRUE)`.
One assertion failed: its displayed `altExpNames(sce_hvg)` check cannot diagnose the separate
zellkonverter object. This is the sole P2.

### Input 4 — Seurat to h5ad plus scale-data sidecar

Prompt: “Move a Seurat object with PCA and UMAP to h5ad; preserve scale.data for later use and verify the Python result.”

Generated test code: [R exporter](run/fp2_input4_seurat_to_h5ad.R) and
[Python verifier](run/fp2_input4_check_h5ad.py).

```text
seurat_layers counts,data,scale.data sce_assays counts,logcounts reductions PCA,UMAP
scale_sidecar_dim 500x1176
PASS input4_R
shape (1176, 15246) layers ['logcounts', None] obsm ['PCA', 'UMAP']
obsm_shapes {'PCA': (1176, 10), 'UMAP': (1176, 2)}
scale_trace False nonzero 2491554
PASS input4_Python
```

### Input 5 — raw recovery versus counts retention

Prompt: “Choose the reliable raw route for an HVG-subsetted h5ad and state whether counts come along.”

Generated test code: [fp2_input5_raw_and_counts.R](run/fp2_input5_raw_and_counts.R)

```text
raw_dim 33538x1222 hvg_dim 700x1222 hvg_assays X
PASS input5
```

### Input 6 — multimodal feature split

Prompt: “Keep antibody-capture features on load and split a 20-cell GEX+ADT object without loss.”

Generated test code: [fp2_input6_multimodal.py](run/fp2_input6_multimodal.py)

```text
original (20, 60) gex (20, 50) adt (20, 10) sum_features 60
PASS input6
```

### Input 7 — legacy SeuratDisk request

Prompt: “Use SeuratDisk to convert my Seurat v5 object to h5ad.”

Generated test code: [fp2_input7_seuratdisk.R](run/fp2_input7_seuratdisk.R)

```text
Creating h5Seurat file for version 3.1.5.9900
SeuratDisk_result FAILED HDF5-API Errors: unable to copy object
PASS input7
```

The expected legacy conversion error was observed live, supporting the Skill's instruction to avoid
this route. Its process status was nonzero after the expected failure was caught and asserted.

### Input 8 — synthetic 10x MEX

Prompt: “Read this MEX using stable IDs, retain ADT and guide features, and avoid ambiguous symbols.”

Generated test code: [fp2_input8_mex.py](run/fp2_input8_mex.py)

```text
shape (3, 4) names ['ENSG1', 'ENSG2', 'ADT1', 'GUIDE1']
types ['Antibody Capture', 'CRISPR Guide Capture', 'Gene Expression']
PASS input8
```

### Input 9 — shipped-code parse test

Prompt: “Validate the shipped data-I/O examples before I use them in a workflow.”

Generated test code: [Python extraction/parser](run/fp2_input9_code_blocks.py) and
[R parser](run/fp2_input9_parse_r.R).

```text
python_blocks 2 r_blocks 7 PASS input9_python
r_blocks_parsed 7
PASS input9_R
```

## Veto gates

- Structural veto (T1–T4): PASS.
- Research veto (M1–M4): PASS. This is a data-analysis Skill; it made no medical conclusion,
  fabricated no measurement, preserved methodological boundaries, and supplied executable code.

## Static score

| Category | Score |
|---|---:|
| Functional suitability | 12/12 |
| Reliability | 10/12 |
| Performance/context | 8/8 |
| Agent usability | 15/16 |
| Human usability | 8/8 |
| Security | 12/12 |
| Maintainability | 12/12 |
| Agent-specific | 16/20 |

## Issue

**P2 — Correct the zellkonverter raw diagnostic variable.** In the “Recovering `.raw`” code
block, replace `length(SingleCellExperiment::altExpNames(sce_hvg))` with a check on the object
returned by `readH5AD(..., raw=TRUE)`, e.g. `sce_zk`. The current recovery route itself works.

## Artifacts

- [JSON report](eval_report_bio-single-cell-data-io_result.json)
- [Phase-2 scripts](run/)
- [Fresh generated data](data/)
- [Final-pass checkpoint](../_final_pass/bio-single-cell-data-io/CHECKPOINT.md)
