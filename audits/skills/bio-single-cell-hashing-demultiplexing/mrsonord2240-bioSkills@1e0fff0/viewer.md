> **Audit record for `bio-single-cell-hashing-demultiplexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1e0fff0](https://github.com/mrsonord2240/bioSkills/tree/1e0fff03e588881b92d9fe67da31a5f3ffdc4b18/single-cell/hashing-demultiplexing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-hashing-demultiplexing

Generated: 2026-09-23

Final-pass Phase 2 audit of `mrsonord2240/bioSkills@1e0fff03e588881b92d9fe67da31a5f3ffdc4b18:single-cell/hashing-demultiplexing`. The source worktree was clean before and after the audit. All data used below are seeded synthetic HTO/GEX fixtures described in [data/README.md](data/README.md).

## Summary

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | Yes | 38 | 57 | 95 | 4/4 | ✅ |
| 2 | Variant A | Yes | 38 | 58 | 96 | 4/4 | ✅ |
| 3 | Edge | Yes | 36 | 53 | 89 | 4/4 | ✅ |
| 4 | Variant B | Yes | 38 | 57 | 95 | 4/4 | ✅ |
| 5 | Stress | Yes | 35 | 55 | 90 | 4/4 | ✅ |

Execution average: **93.0/100**. Assertion pass rate: **20/20**.

## Detailed outputs

### 1. Canonical — four clean CITE-seq HTO pools

**Prompt:** “I pooled four CITE-seq antibody-hashed samples. Normalize their HTO assay, assign each cell to its sample, call cross-sample doublets, and also show the MULTI-seq alternative.”

**Response used:** Create a Seurat HTO assay, apply CLR with `margin=2`, use `HTODemux(..., positive.quantile=0.99)`, inspect `HTO_classification.global` and `hash.ID`, and use `MULTIseqDemux(..., autoThresh=TRUE)` for the lipid-tag route. These are the skill’s documented patterns.

**Execution:** `input1_htodemux_multiseq.R` completed. HTODemux reported 677 singlets, 83 doublets, and 40 negatives; global-class agreement was 0.996 and singlet-ID agreement 1.000. MULTIseqDemux returned complete `MULTI_ID` calls. Evidence: `run/phase2_20260923/input1.log`.

**Scores:** 38/40 + 57/60 = **95**. Assertions: global class PASS; singlet identity PASS; complete MULTIseq calls PASS; computational-only scope PASS.

### 2. Variant A — exactly two hashtags in scanpy

**Prompt:** “I have exactly two HTOs in `adata.obs`; use hashsolo without silently turning the whole pool Negative.”

**Response used:** Follow the shipped example: call `sce.pp.hashsolo` with `priors=(0.01, 0.8, 0.19)` and `number_of_noise_barcodes=1`, then stop and diagnose if `Negative > 90%`.

**Execution:** `input2_hashsolo.py` completed on 700 synthetic cells. Calls: HTO_A 319, HTO_B 283, Doublet 61, Negative 37; global and singlet-ID accuracy were each 1.000, Negative fraction 0.053, and two runs were identical. Evidence: `run/phase2_20260923/input2.log`.

**Scores:** 38/40 + 58/60 = **96**. Assertions: two-tag safeguard PASS; installed API PASS; truth accuracy PASS; determinism PASS.

### 3. Edge — weak or underdispersed HTO background

**Prompt:** “My HTO background is poorly separated and `demuxmix()` can crash. Show the robust route and tell me when not to trust it.”

**Response used:** Use `demuxmix(as.matrix(hto_counts), rna=num_detected_genes)`. If it errors, retry `model='naive'`, then treat the `dmmClassify()` non-convergence warning as a stop condition rather than a valid result.

**Execution:** `input3_demuxmix.R` completed. The regular three-tag fixture had 1.000 class agreement but emitted `Not all models converged. Do not use the classification results.` The 600-cell near-constant fixture reproduced `missing value where TRUE/FALSE needed`; the documented naive fallback returned `FALLBACK_OK_600`. Evidence: `run/phase2_20260923/input3.log`.

**Scores:** 36/40 + 53/60 = **89**. Assertions: normal route PASS; explicit failure reproduced PASS; fallback completed PASS; convergence warning retained PASS.

### 4. Variant B — explicit multiplet accounting with GMM-Demux

**Prompt:** “Use a four-tag float CSV with GMM-Demux and give me a reproducible multiplet-classification report.”

**Response used:** Use `GMM-demux -c hto_counts.csv HTO_A,HTO_B,HTO_C,HTO_D -f gmm_out`; verify `GMM_full.csv` and its config rather than relying only on exit status.

**Execution:** `input4_gmm_generate.py` generated 1,000 float-typed cells. GMM-Demux completed twice with exit code 0. Both reports had 1,000 rows and `barcode`, `Cluster_id`, and `Confidence`; `Cluster_id` was identical. Evidence: `run/phase2_20260923/input4.log`, `input4_rerun.log`, `input4_check.log`, and `gmm_out/`.

**Scores:** 38/40 + 57/60 = **95**. Assertions: CSV route PASS; report fields PASS; dtype compatibility PASS; determinism PASS.

### 5. Stress — unequal CMO pooling and a 5% minority tag

**Prompt:** “One of four CellPlex CMO pools is only 5%. Check whether it is a real minority rather than a failed tag, estimate the hashing blind spot, and say what additional doublet method is needed.”

**Response used:** Apply the HTODemux workflow, inspect actual singlet tag counts, and retain expression-based doublet detection for within-sample doublets. For a four-pool experiment, the skill correctly explains that the within-sample share of doublets is about `1/k = 0.25`.

**Execution:** `input5_unequal_pooling.R` completed. It returned 768 singlets, 66 doublets, and 66 negatives. After dropping unused factor levels, CMO-4 was 36/768 = 0.047 of singlets, consistent with the planted minority. The initial factor-level behavior is preserved in `input5_initial_factor_levels.log`; the factor-safe agent response is in `input5.log`.

**Scores:** 35/40 + 55/60 = **90**. Assertions: rare tag retained PASS; `1/k` blind-spot statement PASS; orthogonal doublet method PASS; factor-safe inspection PASS.

## Veto and static review

Skill Veto: **PASS** — no structural failure, unstable route, determinism defect, or unsafe execution instruction was found. Shipped means present: both referenced examples exist, and both parse (`source_python_parse.log`, `source_r_parse.log`).

Research Veto: **PASS**. The audit makes no clinical conclusion (M2); all numerical claims trace to retained synthetic executions (M1); method choices and limits are stated without substituting HTO calls for expression doublet detection (M3); code parsed and the tested paths executed (M4).

Static score: **91/100**. Main deductions: no bundled deterministic HTO fixture, caller-side convergence review remains necessary, and the rare-tag stress check lacks a factor-safe example.

## Final

`91 × 0.4 + 93.0 × 0.6 = 92.2`, rounded to **92/100 — Production Ready**. All Production Ready floors hold: static ≥80, execution ≥85, mean basic ≥32, mean specialized ≥48, and assertions ≥90%. Deployable: **true**. Veto override: **false**.

Recommendations:

- **P2:** Add a `droplevels()`-safe per-tag singlet inspection snippet before applying a rare-tag threshold.
- **P2:** Bundle a small deterministic HTO fixture with expected call counts for regression smoke tests.
