> **Audit record for `bio-single-cell-multimodal-integration`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@71a6862](https://github.com/mrsonord2240/bioSkills/tree/71a686293613d3e5e11c5e5b34aa792e923f552d/single-cell/multimodal-integration) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-multimodal-integration

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@71a686293613d3e5e11c5e5b34aa792e923f552d:single-cell/multimodal-integration`

## Final result

**80/100 numeric score; Reject; deployable: false.** The Research Veto is **FAIL** at M4: the shipped Python CITE-seq WNN example fails on valid input because it never makes the required modality-local neighbor graphs. This final-pass report deliberately uses `auditor_independent: false`; see the checkpoint.

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Canonical R CITE-seq DSB/WNN | Yes | 38 | 56 | 94 | 5/5 | Completed |
| 2 | totalVI determinism | Yes | 37 | 56 | 93 | 5/5 | Completed |
| 3 | Multiome WNN | Yes | 36 | 55 | 91 | 4/4 | Completed |
| 4 | Mosaic MultiVI | Yes | 34 | 50 | 84 | 5/5 | Completed |
| 5 | GLUE Windows boundary | Yes | 31 | 46 | 77 | 3/4 | Partial |
| 6 | Seurat v5 bridge CLI | Yes | 29 | 41 | 70 | 3/5 | Partial |
| 7 | Python CITE-seq example | Yes | 18 | 24 | 42 | 2/4 | Error |
| 8 | Scope boundary | Yes | 37 | 53 | 90 | 5/5 | Completed |

Execution average: **80.1/100**. Assertions: **32/37**. Static score: **79/100**. Weighted score: `79 × .4 + 80.1 × .6 = 79.7`, rounded to 80; veto overrides the grade.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Most core routes completed; failures were deterministic and diagnostic. |
| T2 Contract | PASS | Required frontmatter and referenced files exist. |
| T3 Determinism | PASS | totalVI latent arrays were byte-identical across two OS processes. |
| T4 Security | PASS | No secrets, destructive commands, or raw-user-code execution. |
| M1 Scientific integrity | PASS | All figures reported here come from fresh saved runs. |
| M2 Practice boundaries | PASS | The direct response declined individual lupus-risk assessment. |
| M3 Methodological ground | PASS | Depth/anchor/imputation cautions remain present and were exercised. |
| M4 Code usability | **FAIL** | The shipped Python WNN example errors before output on valid 10x CITE-seq data. |

## Detailed execution

### 1. Shipped R CITE-seq DSB plus WNN

`run/cite_regression/` contains a new 10x-format fixture generator and an audit-local copy of the exact shipped R example. It completed on 240 called cells plus 1,200 empty droplets, wrote `cite_seq_analyzed.rds`, and returned three perfectly pure planted clusters. The independent DSB guard run recorded a real-empty ratio of 0.066 (passes), cell-as-empty ratio 1.001 (stops), and boundary ratio 0.501 (stops). See `run/cite_regression.log` and `run/test_dsb_guard.log`.

### 2. totalVI

Fresh 240-by-150-by-12 MuData was generated with seed 777. Two distinct Python processes ran the shipped seeded totalVI pattern; both returned a `(240, 20)` latent and `(240, 12)` foreground matrix. `np.array_equal` was true and maximum absolute difference was `0.0`. See `run/totalvi_regression.log`.

### 3. Paired multiome WNN

The controlled 300-cell regression rerun measured LSI_1/depth correlation of `0.9830216` before excluding it and achieved 90.7% majority-label concordance after joint WNN. See `run/input4_regression.log`.

### 4. Mosaic MultiVI

The fresh 195-cell, three-type fixture trained 500 epochs. RNA-only cells had a same-type nearest paired neighbor in 58.7% of cases (33.3% chance); mean same-type distance was 0.182 versus 0.246 for different types. See `run/multivi_regression.log`.

### 5. GLUE Windows boundary

The exact prerequisite command was run as a dry run in the Windows audit environment. It accurately encountered the documented `pysam` build failure. The source caveat is adequate, but no supported scglue host was available, so the GLUE block itself is not live-evidenced. See `run/check_scglue_windows.log`.

### 6. Seurat bridge CLI

The copied script was invoked on a new three-object 150-cell fixture. The advertised bare command fails immediately because `Seurat` is not resolved from this environment's private R library. With diagnostic `R_LIBS` supplied, it wrote a mapped 150-cell object and the saved object had 0.733 label accuracy, but R exited 139 after output. This is partial, not clean command success. See `run/bridge_run.log`, `run/bridge_with_rlibs_final.log`, and `run/bridge_check_final.log`.

### 7. Shipped Python CITE-seq WNN example — M4 failure

The exact copied `examples/cite_seq_analysis.py` read a newly generated valid 10x-v3 CITE-seq H5 and completed RNA/ADT preprocessing. It then failed:

```text
ValueError: Did not find .uns["neighbors"] for modality "rna".
Run `sc.pp.neighbors` on all modalities first.
```

The source calls `mu.pp.neighbors(mdata, key_added='wnn')` but never calls `sc.pp.neighbors` on `rna` and `adt`. No output H5 is produced. See `run/python_example_regression.log`.

### 8. Scope boundary

The direct transcript at `run/mode_a_scope_response.md` classified CITE-seq plus independent scRNA-seq as mosaic, preserved the QC/imputation warnings, and refused an individual lupus-risk request.

## Required remediation

1. **P0:** repair the Python example by making per-modality neighbor graphs before `mu.pp.neighbors`, then execute it on a small committed CITE-seq fixture.
2. **P1:** make the bridge script's R-library/environment preflight explicit and prove a clean exit in the designated environment.
3. **P2:** live-run GLUE on a supported host with a truth-bearing fixture.

## Artifact map

- Fresh report: `eval_report_bio-single-cell-multimodal-integration_result.json`
- Fresh evidence and all executed scripts: `run/`
- Fresh fixture data: `data/`
- Prior canonical audit preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-multimodal-integration`
