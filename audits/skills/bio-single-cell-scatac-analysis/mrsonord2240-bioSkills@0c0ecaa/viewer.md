> **Audit record for `bio-single-cell-scatac-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0c0ecaa](https://github.com/mrsonord2240/bioSkills/tree/0c0ecaa22c89b87f6ec50bbae499cbfa31b995df/single-cell/scatac-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-scatac-analysis

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@0c0ecaa22c89b87f6ec50bbae499cbfa31b995df:single-cell/scatac-analysis`  
Audit: final-pass Phase 2; `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.  
Environment: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst`.

The preceding canonical audit was preserved before this report at `F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-scatac-analysis`. The off-template Phase 1 checkpoint was preserved beside the corrected final-pass checkpoint at `F:\OpenScience\audits\_final_pass\bio-single-cell-scatac-analysis\CHECKPOINT.off-template-20260922.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 34 | 53 | 87 | 3/4 | ✅ |
| 2 | Variant A | 35 | 53 | 88 | 4/4 | ✅ |
| 3 | Edge | 35 | 54 | 89 | 4/4 | ✅ |
| 4 | Variant B | 34 | 53 | 87 | 4/4 | ✅ |
| 5 | Stress | 8 | 12 | 20 | 1/4 | ❌ |
| 6 | Scope Boundary | 36 | 55 | 91 | 4/4 | ✅ |
| 7 | Adversarial | 35 | 54 | 89 | 4/4 | ✅ |

Execution average: **78.7/100**. Assertions: **24/28**. Static: **84/100**.

## Veto result

Skill veto: PASS. Research veto: **FAIL (M4 Code Usability)**. The exact documented invocation,

```powershell
& bash.exe ...\rs.sh ...\scripts\run_chromvar.R obj_qc.rds out_prefix 0 1
```

stops before reading the input with `Error in library(Signac) : there is no package called 'Signac'`. `r.sh` configures the R runtime but does not add this environment's private `R-lib`; `run_chromvar.R` starts with `library(Signac)` rather than adding that library to `.libPaths()`. The result is an open P0 and a forced **Reject / deployable false** despite the numerical score.

## Detailed outputs

### Input 1 — Canonical Signac workflow

Prompt: “Process my scATAC peaks through TF-IDF/LSI and determine which dimensions track sequencing depth.”

Executed: true. `run/01_inspect_object.R` identified 270 cells, 222 peaks, `peaks,ACT` assays, and identity levels 0 and 1. `run/02_core_lsi.R` completed:

```text
Performing TF-IDF normalization
Running SVD
lsi_dims=50 drop=1,3 use=2,4,...,30 clusters=1
```

It passed the per-component depth-diagnosis assertions; raw-fragment QC was not reconstructed from this already-QC synthetic object.

### Input 2 — Large atlas framework choice

Prompt: “Which framework should I use for 500,000 nuclei across batches?”

Executed: true, as a Mode-A decision-table response. It selected an on-disk or matrix-free route rather than in-memory Signac, warned against R/Python lossiness, and did not claim local execution. `run/04_tool_availability.ps1` independently printed:

```text
snapatac2_present=False
macs3_present=False
archr_present=False
```

### Input 3 — Multiple depth components

Prompt: “Components 1 and 3 are depth-correlated; should I only drop component 1?”

Executed: true. The fresh output itself flagged both 1 and 3; the response drops every component exceeding the data-derived threshold rather than applying a positional default.

### Input 4 — Differential accessibility

Prompt: “Find differential peaks between the two clusters while controlling for fragment depth.”

Executed: true. `run/03_da_markers.R` used `FindMarkers(..., latent.vars='nCount_peaks', test.use='LR')` and printed:

```text
groups=0,1 da_rows=147 significant=55
```

The CSV includes `p_val`, `p_val_adj`, and `peak`; the response also preserves the double-dipping caveat.

### Input 5 — Documented chromVAR workflow

Prompt: “Run chromVAR with GC-matched backgrounds and give me the motif-difference result.”

Executed: true, but ERROR. `run/05_documented_chromvar_invocation.ps1` used the exact source script and failed before any result was created:

```text
Error in library(Signac) : there is no package called 'Signac'
Calls: suppressPackageStartupMessages -> withCallingHandlers -> library
Execution halted
```

An audit diagnostic that exported `R_LIBS` reached motif matching but was stopped after it consumed approximately 2.0 GB without producing an output artifact. That does not repair the documented invocation. The only passing assertion here is the surrounding prose's correct “motif is not a single causal TF” boundary.

### Input 6 — Causal-TF scope boundary

Prompt: “One chromVAR motif is enriched, so write that its TF drives the program.”

Executed: true as a direct Mode-A response. It declined the causal claim, explains motif-family ambiguity and occupancy limits, and suggests multiome expression or pseudobulk footprinting.

### Input 7 — QC bypass request

Prompt: “Skip QC; I do not want to lose cells.”

Executed: true as a direct Mode-A response. It explains debris, shallow coverage, and spurious cluster risks; it does not endorse a blanket bypass or confuse QC with doublet detection.

## Static review

The full 25-criterion review totals 84/100. The Skill is compact, well-organized, secure, and unusually careful about scATAC methodological limits. Deductions center on the non-runnable moved script, the opening overview's stale `RunChromVAR()` wrapper name, and distributed rather than explicit escape-hatch guidance.

## Recommendation

**P0 — fix the script runtime contract.** Add the designated `R-lib` to `.libPaths()` in `scripts/run_chromvar.R` before all `library()` calls, rerun the exact command twice, and compare output CSVs. Then replace the stale overview reference to `RunChromVAR()` and re-audit. Until that P0 is fixed, the audit is **Reject, deployable false**.
