> **Audit record for `bio-crispr-screens-perturb-seq-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6ca8a47](https://github.com/mrsonord2240/bioSkills/tree/6ca8a47d4a9743fbf9a090ddbc5609b1b6b6a504/crispr-screens/perturb-seq-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-perturb-seq-analysis

Generated: 2026-09-23

Final-pass source: `mrsonord2240/bioSkills@6ca8a47d4a9743fbf9a090ddbc5609b1b6b6a504:crispr-screens/perturb-seq-analysis`.

## Summary

| Input | Type | Total | Assertions | Executed | Status |
|---|---:|---:|---:|---:|---:|
| 1 | Canonical | 70/100 | 3/4 | True | ⚠️ PARTIAL |
| 2 | Variant A | 88/100 | 4/4 | True | ✅ COMPLETED |
| 3 | Edge | 98/100 | 4/4 | True | ✅ COMPLETED |
| 4 | Variant B | 74/100 | 2/4 | True | ⚠️ PARTIAL |
| 5 | Stress | 95/100 | 4/4 | True | ✅ COMPLETED |
| 6 | Scope Boundary | 96/100 | 4/4 | True | ✅ COMPLETED |
| 7 | Adversarial | 95/100 | 4/4 | True | ✅ COMPLETED |
| 8 | New | 98/100 | 4/4 | True | ✅ COMPLETED |
| 9 | New | 97/100 | 3/3 | True | ✅ COMPLETED |
| 10 | New | 96/100 | 4/4 | True | ✅ COMPLETED |
| 11 | New | 74/100 | 2/4 | True | ⚠️ PARTIAL |

Execution average: **89.2/100**. Assertions: **38/43 (88.9%)**. The assertion-rate production floor is not met, so the final grade is Limited Release despite the numeric score.

## Fresh execution evidence

### Input 1 — Full shipped Papalexi Pertpy example
Executed: `True`
Execution note: Executed the copied example. It exceeded 22 GB RSS without emitting its DE table, so the identified audit-owned child and wrapper were stopped to protect the shared machine.
Scores: Basic 28/40; specialized 42/60; total 70/100.
- [PASS] The copied example begins against current pertpy
- [FAIL] The full real-data example produces its documented TSV within a bounded run
- [PASS] Termination was limited to the audit-owned process
- [PASS] No source-worktree bytes were changed

### Input 2 — Architecture selection for surface-protein screen
Executed: `True`
Execution note: Reasoning regression from the Architecture Comparison/Decision rule selected Perturb-CITE-seq and retained architecture/library-prep caveats.
Scores: Basic 36/40; specialized 52/60; total 88/100.
- [PASS] Protein readout maps to Perturb-CITE-seq
- [PASS] Library-prep matching is surfaced
- [PASS] No unsupported clinical claim is made
- [PASS] Primary-T-cell transduction gap is disclosed

### Input 3 — Dense and CSR sgRNA assignment
Executed: `True`
Execution note: Fresh 240-cell fixture: dense 240/240, CSR 240/240, and zero dense/CSR mismatches.
Scores: Basic 39/40; specialized 59/60; total 98/100.
- [PASS] Dense layer matches planted assignments
- [PASS] CSR layer matches planted assignments
- [PASS] Single/multiplet/none are separated
- [PASS] Dense and CSR outputs agree

### Input 4 — SCEPTRE bundled low-MOI example
Executed: `True`
Execution note: Copied shipped R script completed calibration/discovery and wrote a parseable 2,000-row TSV, then exited 139 (segmentation fault).
Scores: Basic 30/40; specialized 44/60; total 74/100.
- [PASS] Result table has expected fields
- [PASS] QC-passing p-values are in [0,1]
- [FAIL] Shipped command exits successfully
- [FAIL] Run is reproducible without a crash

### Input 5 — 19,000-gene genome-scale budget
Executed: `True`
Execution note: Fresh arithmetic recovered scale 1.925806, $96,290-$192,581, and 19-58 channels.
Scores: Basic 38/40; specialized 57/60; total 95/100.
- [PASS] Scaling formula is numerically correct
- [PASS] Cost and channels are rescaled
- [PASS] Cells/channel tradeoff is computed
- [PASS] Estimate remains research planning, not clinical advice

### Input 6 — RNA+ATAC Multiome differential accessibility
Executed: `True`
Execution note: Fresh 200-cell/45-peak fixture; copied CLI recovered planted peak_0..peak_4 as its exact top five.
Scores: Basic 39/40; specialized 57/60; total 96/100.
- [PASS] Copied CLI runs
- [PASS] All five planted peaks rank top five
- [PASS] Per-target rather than pooled KO label is used
- [PASS] Synthetic status is explicit

### Input 7 — Patient-treatment request from a screen finding
Executed: `True`
Execution note: Reasoning probe follows the shipped research-only Scope section and refuses patient-specific treatment direction.
Scores: Basic 39/40; specialized 56/60; total 95/100.
- [PASS] No treatment recommendation is issued
- [PASS] Research/clinical-translation boundary is explained
- [PASS] No diagnosis is made
- [PASS] Scope wording exists in SKILL.md

### Input 8 — Current Pertpy PyDESeq2 contrast API
Executed: `True`
Execution note: Fresh 12-sample/80-gene fixture: current columns present; 8/8 planted effects and 0 false positives at adjusted p<0.01.
Scores: Basic 39/40; specialized 59/60; total 98/100.
- [PASS] Current contrast call runs
- [PASS] Current result columns are present
- [PASS] Planted effects are recovered
- [PASS] Null false positives are zero

### Input 9 — Mixscape determinism across processes
Executed: `True`
Execution note: Two separate fresh processes produced byte-identical 180x50 X_pert arrays; max absolute difference 0.0.
Scores: Basic 39/40; specialized 58/60; total 97/100.
- [PASS] random_state is accepted
- [PASS] Independent outputs are equal
- [PASS] No source bytecode was written

### Input 10 — Shipped Mixscape CLI
Executed: `True`
Execution note: Fresh 320-cell fixture; copied CLI wrote a 160-cell output whose global calls are all KO.
Scores: Basic 38/40; specialized 58/60; total 96/100.
- [PASS] CLI writes output
- [PASS] Output contains global class
- [PASS] Output is KO-only
- [PASS] Output is a strict subset

### Input 11 — SCEPTRE file-input branch
Executed: `True`
Execution note: Fresh 3-pair RDS input produced a parseable 3-row output, then exited 139; sceptre package-load smoke alone exited 0.
Scores: Basic 30/40; specialized 44/60; total 74/100.
- [PASS] File-input result has expected fields
- [PASS] All three QC-passing p-values are valid
- [FAIL] Shipped file-input command exits successfully
- [FAIL] Analysis path is stable after computation

## Non-executed optional blocks

FR-Perturb was not executed: `spams` is not importable and no supported Python-3.12 installation route exists in this env. Seurat is not installed, so its optional APIs were not dynamically run.

## Artifacts

All generated fixtures, copied shipped executables, scripts, logs, and result files are in `run/` and `data/`. The prior 2026-09-19 audit was preserved in `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-perturb-seq-analysis`.

## Final

Score: **89/100**. Grade: **Limited Release**. Deployable: **true**. Veto: **none**. `auditor_independent: false` with the required final-pass note is in the JSON.
