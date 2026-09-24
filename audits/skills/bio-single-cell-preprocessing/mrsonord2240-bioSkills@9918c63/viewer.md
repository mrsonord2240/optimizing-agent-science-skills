> **Audit record for `bio-single-cell-preprocessing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9918c63](https://github.com/mrsonord2240/bioSkills/tree/9918c631d94f81dd418cf71d5c40be59f4850677/single-cell/preprocessing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-preprocessing

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@9918c631d94f81dd418cf71d5c40be59f4850677:single-cell/preprocessing`
Audit type: final-pass exact-commit corrective re-audit
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 9 · Executed: 8/9

## What the Skill claims to do

Quality control, ambient-RNA handling, normalization, and feature selection for single-cell RNA-seq using Scanpy (Python) and Seurat (R). Use when filtering low-quality cells with MAD-adaptive thresholds, setting tissue-aware mito cutoffs, removing ambient RNA (SoupX/CellBender/DecontX), choosing a normalization (shifted-log vs scran vs sctransform vs Pearson residuals), selecting highly variable genes, or deciding whether to scale and regress out covariates.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | **92** | 4/4 | yes | ✅ |
| 2 | Variant A | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 4 | Variant B | 37 | 55 | **92** | 4/4 | yes | ✅ |
| 5 | Stress | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 6 | Scope Boundary | 33 | 49 | **82** | 4/4 | no | ✅ |
| 7 | Adversarial | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 8 | Fresh Variant A | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 9 | Fresh Variant B | 38 | 57 | **95** | 4/4 | yes | ✅ |

**Execution Average: 92.9 / 100** · **Assertion Pass Rate: 36/36**

**Static: 92/100** · Static weighted 36.8 + dynamic weighted 55.7 = **93/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All quantitative statements in this re-audit are from recorded local synthetic or public-fixture runs. |
| practice boundaries | PASS | The Skill remains a preprocessing workflow and makes no individual diagnostic or treatment claim. |
| methodological ground | PASS | The re-run confirms normalization-composition, high-mito, simple-cell-type, and batch-depth caveats; correction branches now address the demonstrated failure modes. |
| code usability | PASS | SoupX now completes when clusters are absent, the QC guard stops zero-MAD filtering, and per-batch seurat_v3 HVG selection completes on the shallow-batch fixture. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Core QC, ambient-correction, normalization, and feature-selection routes are present; the audited Scanpy, Seurat, SoupX, and batch-HVG paths execute on the saved fixtures. |
| reliability | 12/12 | The prior SoupX, zero-MAD, shallow-batch, and high-mito failure modes now have prevention or explicit recovery guidance. |
| performance context | 7/8 | The workflow is concise for its breadth; quick clustering and per-batch HVG filtering add necessary, bounded work. |
| agent usability | 15/16 | Pipeline order and failure modes are explicit; the spatial scope boundary remains intentionally narrow. |
| human usability | 7/8 | Scenario prompts and decision tables are discoverable, with strict data-integrity stops where needed. |
| security | 10/12 | No secret or destructive-operation path; input files are researcher-provided matrices without PHI-specific handling. |
| maintainability | 11/12 | Python and R routes are separated and both packaged examples now share the documented adaptive-QC policy; the repository still has no general automated test harness. |
| agent specific | 18/20 | Accurate trigger, version bounds, progressive sections, and explicit stop conditions; adjacent spatial preprocessing is still delegated. |

## Input 1 — Canonical: 8-donor PBMC drug study, QC through PCA with per-sample MAD

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: Canonical synthetic eight-sample QC run completed: per-sample MAD flags 555/6,524 cells and exposes 28.8% megakaryocyte removal for the required per-cluster review.
- Finding: Canonical synthetic eight-sample QC run completed: per-sample MAD flags 555/6,524 cells and exposes 28.8% megakaryocyte removal for the required per-cluster review.

| Assertion | Result | Evidence |
|---|---|---|
| MAD thresholds are computed per sample, not globally, as the Skill requires for multi-sample designs | PASS | Per-sample medians and MADs printed for all eight samples; the SKILL.md:81-86 block executed verbatim and its output matched the explicit loop. |
| Raw counts are stashed before normalization and seurat_v3 HVG selection reads them | PASS | layers['counts'] written before normalize_total; highly_variable_genes called with layer='counts', 2000 HVGs selected. |
| The response names which real cell types were lost to QC rather than reporting only a survivor count | PASS | Loss-by-true-type table printed: megakaryocytes 28.8%, FCGR3A+ monocytes 9.6%, CD8 T 5.5%. |
| No claim is made that a clean post-QC object proves the filtering was correct | PASS | Precision 0.523 against the synthetic truth labels is reported alongside the survivor count; the Skill's 'a beautiful UMAP proves nothing' principle is honoured. |

## Input 2 — Variant A: SoupX ambient removal on Cell Ranger raw+filtered, 8 samples + real PBMC 1k

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: The archived eight-sample and real-PBMC regression reran, and the exact corrected SoupX route completed on 707 cells with rho 0.085 and 8.5% of counts removed.
- Finding: The archived eight-sample and real-PBMC regression reran, and the exact corrected SoupX route completed on 707 cells with rho 0.085 and 8.5% of counts removed.

| Assertion | Result | Evidence |
|---|---|---|
| The SoupX code the Skill prescribes runs on the input the Skill names (Cell Ranger raw+filtered) | PASS | Exact corrected route rerun from the saved audit harness against Cell Ranger raw and filtered matrices; clustering was supplied before autoEstCont. |
| A contamination fraction is reported per sample rather than pooled | PASS | Eight per-sample rho values reported (0.085-0.153) against the synthetic truth (0.042-0.098); mean absolute error 0.052, rank order broadly preserved. |
| A lineage-specific marker is checked for survival after adjustment, as the Skill instructs | PASS | CD3D/CD3E: 1,849 -> 1,670 counts, cells expressing 472 -> 412. The loss is reported, not hidden. |
| Only one ambient tool is applied; no stacking of SoupX with DecontX or CellBender | PASS | SoupX only, per the Skill's 'do not stack tools; double-correction compounds over-removal'. |

## Input 3 — Edge: 120-nucleus low-complexity capture where MAD collapses to zero

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: The archived fixture reproduced its former 70% survivor result; the exact corrected guard separately stopped on zero MAD before subsetting, and nuclei now use MAD-only mito policy.
- Finding: The archived fixture reproduced its former 70% survivor result; the exact corrected guard separately stopped on zero MAD before subsetting, and nuclei now use MAD-only mito policy.

| Assertion | Result | Evidence |
|---|---|---|
| The MAD collapse is surfaced explicitly rather than the filtered object being returned silently | PASS | Median and MAD printed for all four QC metrics; MAD = 0.000000 for log1p_total_counts and pct_counts_mt. |
| The guard the Skill prescribes fires and triggers its fixed-cutoff fallback | PASS | The c3ca7ea exact-path check raised the documented MAD-collapse ValueError before subsetting. |
| The mito rule is correctly identified as inert on nuclei instead of being applied as written | PASS | pct_counts_mt all zero -> 0 cells flagged; response states the nuclei guidance the Skill gives (lean on counts/genes outliers). |
| No quality conclusion is asserted that this 120-cell capture cannot support | PASS | Response reports the collapse and stops short of declaring cells good or bad. |

## Input 4 — Variant B: Normalization choice for a set containing a composition-divergent population

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: Real synthetic normalization comparison completed: scran and library-size factors differ by cell type and SCTransform v2 completed.
- Finding: Real synthetic normalization comparison completed: scran and library-size factors differ by cell type and SCTransform v2 completed.

| Assertion | Result | Evidence |
|---|---|---|
| A default is recommended and the assumption it encodes is stated | PASS | Shifted-log recommended with the constant-total-mRNA assumption named, per SKILL.md's Governing Principle. |
| scran size factors are checked for non-positive values, the failure the Skill names | PASS | min 0.1153, none <= 0; the Skill's 'factors can go negative' caveat was tested rather than repeated. |
| The response states that the result is relative, not absolute, expression | PASS | The per-type size-factor ratios are used to qualify the shifted-log deltas instead of presenting them as absolute abundances. |
| Normalization is applied exactly once per route and routes are not chained | PASS | Three independent objects; no route receives another route's output. |

## Input 5 — Stress: Depth-imbalanced 8-sample design: per-sample QC, batch HVG, regression decision

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: The archived stress regression reproduced the former singular loess failure; the exact corrected per-batch filter retained 7,846 genes and selected 2,000 HVGs successfully.
- Finding: The archived stress regression reproduced the former singular loess failure; the exact corrected per-batch filter retained 7,846 genes and selected 2,000 HVGs successfully.

| Assertion | Result | Evidence |
|---|---|---|
| Per-sample MAD thresholds outperform global thresholds on a depth-imbalanced design | PASS | Recall 1.000 for both; precision 0.478 (global) -> 0.510 (per-sample), and the 14.6% over-cut of S5 disappeared. |
| The Skill's HVG batch_key instruction executes on the design it is prescribed for | PASS | The c3ca7ea per-batch helper retained 7,846/12,521 genes and seurat_v3 selected 2,000 HVGs. |
| regress_out is not applied reflexively before its effect is measured | PASS | Run as a comparison only; cell-type silhouette 0.2372 -> 0.2412 and batch silhouette 0.0877 -> 0.0301, i.e. no harm on this dataset, which is reported as such. |
| The Skill's predicted failure direction is verified before being repeated to the user | PASS | The claim 'global MAD over-cuts the shallow batch' was tested and found not to hold here; the response says so instead of asserting it. |

## Input 6 — Scope Boundary: 10x Visium spatial slides - same QC recipe?

- Status: ✅ COMPLETED · Basic 33/40 · Specialized 49/60 · **Total 82/100**
- Execution: Text-only scope boundary: the Skill remains limited to scRNA-seq and redirects spatial-specific preprocessing rather than fabricating a workflow.
- Finding: Text-only scope boundary: the Skill remains limited to scRNA-seq and redirects spatial-specific preprocessing rather than fabricating a workflow.

| Assertion | Result | Evidence |
|---|---|---|
| The response states that the Skill does not cover spatial-specific QC | PASS | Stated explicitly, with the reason: barcodes are spots containing several cells, so the droplet/empty-droplet and doublet framing does not apply. |
| No Visium-specific threshold is invented from the Skill's droplet QC table | PASS | The 200-gene and 8% mito reference values are explicitly withheld as droplet-specific. |
| The transferable part is separated from the non-transferable part rather than the whole recipe being applied | PASS | MAD machinery and mito-as-biology reasoning carried over; ambient/empty-droplet/doublet steps declared out of scope. |
| A handoff is offered rather than the request being silently attempted | PASS | Deferred to a spatial-specific workflow; note that this escape hatch came from the agent, not from the Skill, which is scored as a static deduction. |

## Input 7 — Adversarial: Keep the flat 5% mito cutoff because the UMAP looks great, re-normalize, regress everything out

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: Adversarial high-mito and re-normalization regression completed: old >8% behavior deletes all 374 simulated high-mito cells; a second normalization compresses total X to 0.662x and emits Scanpy's warning.
- Finding: Adversarial high-mito and re-normalization regression completed: old >8% behavior deletes all 374 simulated high-mito cells; a second normalization compresses total X to 0.662x and emits Scanpy's warning.

| Assertion | Result | Evidence |
|---|---|---|
| The request to keep the flat mito cutoff is refused with evidence, not with an appeal to authority | PASS | Flat >5% deleted 374/374 of the high-mito population; the loss-by-type table is the evidence. |
| The 'the UMAP looks great' argument is rejected | PASS | After the deletion the survivors still gave 16 Leiden clusters at silhouette 0.211; the response uses this to show the embedding cannot detect the loss. |
| The request to re-normalize already-normalized data is refused | PASS | Refused. Measured: sum(X) went to 0.662x, not the ~2x the Skill's Common Errors row claims, and scanpy 1.12 emits its own warning - reported as a correction to the Skill. |
| The request to regress out total_counts and cell cycle is refused or explicitly qualified | PASS | Refused for cell cycle on the Skill's confounding argument; for total_counts the measured effect on this dataset (input 5) is given rather than asserted. |

## Input 8 — Fresh Variant A: Packaged Scanpy example on a 707-cell PBMC fixture

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: The example shipped at c3ca7ea ran end to end: 707 raw cells, 657 retained cells, 11,109 genes, 2,000 HVGs, PCA, and an h5ad output.
- Finding: The example shipped at c3ca7ea ran end to end: 707 raw cells, 657 retained cells, 11,109 genes, 2,000 HVGs, PCA, and an h5ad output.

| Assertion | Result | Evidence |
|---|---|---|
| The packaged Scanpy example executes without modification | PASS | Ran the exact source file from c3ca7ea; exit 0 and preprocessed.h5ad was written. |
| Adaptive QC replaces the former flat mitochondrial cutoff | PASS | Four medians/MADs printed and unknown tissue used no hard mitochondrial cap. |
| The survival guard permits this plausible fixture | PASS | 657/707 cells survived, above the documented 80% stop boundary. |
| Raw counts feed seurat_v3 HVG selection | PASS | The example stored layers['counts'] and selected exactly 2,000 HVGs from that layer. |

## Input 9 — Fresh Variant B: Packaged Seurat example on the same PBMC fixture

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: The exact packaged R example ran through the audit library wrapper: 707 raw cells, 658 retained cells, 3,000 variable features, and an RDS output.
- Finding: The exact packaged R example ran through the audit library wrapper: 707 raw cells, 658 retained cells, 3,000 variable features, and an RDS output.

| Assertion | Result | Evidence |
|---|---|---|
| The packaged Seurat example executes without source modification | PASS | The saved wrapper only prepended the private audit library and sourced the exact c3ca7ea example. |
| Adaptive QC replaces the former fixed percent.mt filter | PASS | Counts, features, and mitochondrial MADs printed; no flat percent.mt < 20 filter remains. |
| The survival guard permits this plausible fixture | PASS | 658/707 cells survived, above the documented 80% stop boundary. |
| The normalization route produces its declared artifact | PASS | SCTransform completed with 3,000 variable features and preprocessed.rds passed the wrapper checks. |

## Key strengths

- Both packaged preprocessing examples now implement the same MAD-adaptive, tissue-aware QC policy as the main Skill and execute end to end.
- The corrected SoupX path creates clusters before autoEstCont and completes on both synthetic and real Cell Ranger outputs.
- Zero-MAD and low-survival guards stop unsafe filtering, while nuclei and unknown tissues avoid copied mitochondrial hard caps.
- Per-batch gene filtering prevents the reproduced seurat_v3 shallow-batch loess failure and preserves 2,000 HVGs.
