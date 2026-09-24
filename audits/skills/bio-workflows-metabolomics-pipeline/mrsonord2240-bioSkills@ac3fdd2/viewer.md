> **Audit record for `bio-workflows-metabolomics-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ac3fdd2](https://github.com/mrsonord2240/bioSkills/tree/ac3fdd24777613868e4328191dc274ed4c5ac162/workflows/metabolomics-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-metabolomics-pipeline

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@ac3fdd24777613868e4328191dc274ed4c5ac162:workflows/metabolomics-pipeline`
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical | 38 | 57 | 95 | 4/4 | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 5/5 | ✅ |
| 3 | Stress | 38 | 57 | 95 | 4/4 | ✅ |
| 4 | Edge | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Variant B | 37 | 57 | 94 | 5/5 | ✅ |
| 6 | Scope Boundary | 38 | 58 | 96 | 4/4 | ✅ |
| 7 | Adversarial | 36 | 54 | 90 | 4/4 | ✅ |
| 8 | Stress | 38 | 57 | 95 | 5/5 | ✅ |
| 9 | Variant A | 38 | 57 | 95 | 5/5 | ✅ |
| 10 | Canonical | 30 | 48 | 78 | 2/4 | ✅ |
| 11 | Stress | 37 | 57 | 94 | 4/4 | ✅ |

**Execution average:** 92.9 / 100
**Assertion pass rate:** 46 / 48
**Layer 1 average:** 36.8 / 40
**Layer 2 average:** 56.1 / 60

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Eleven executions produced checked results. |
| T2 Contract | PASS | Frontmatter, referenced files, and executable interfaces exist. |
| T3 Determinism | PASS | Stage 2 produced byte-identical fixed-seed outputs twice. |
| T4 Security | PASS | No secrets, unsafe evaluation, or destructive operations found. |
| M1 Scientific integrity | PASS | Run values are captured from output; synthetic examples are labelled. |
| M2 Practice boundaries | PASS | No individual diagnosis or prescription. |
| M3 Methodological ground | PASS | Missingness, MSI, and background safeguards executed correctly. |
| M4 Code usability | PASS | All runnable paths executed; Input 10 records two P1 engineering defects. |

## Detailed outputs

### Input 1 — Canonical: real feature-table orientation regression

Prompt executed: Run the current Stage 1-to-Stage 2 hand-off on a real feature table and verify that feature orientation is preserved.

`audit_01_orientation_real.R` loaded the real 574x12 faahKO feature table. The current `fm <- feat` check passed and `filter_peaks_by_fraction()` retained 573 features. This re-runs the original orientation regression using public real data.

### Input 2 — Variant A: real MTBLS79 Stage 2-to-Stage 4 regression

Prompt executed: Run drift correction, drop the QCRSC-wiped samples, QRILC-impute remaining sparse holes, and fit the documented permutation-validated discriminant model.

`audit_02_stage2to4_real.R` processed 2,488x172 MTBLS79 data. It retained 2,433 features, reported and dropped 90 wholly missing samples from batches 2/3/4/8, retained 82 samples, produced no NAs after QRILC, and emitted a one-row OPLS-DA summary (`pR2Y=0.001`, `pQ2=0.001`) at `permI=1000`.

### Input 3 — Stress: first bundled workflow

Prompt executed: Run `examples/metabolomics_workflow.R` exactly as shipped.

The source-path run completed with exit status 0. It retained 292/300 features by RSD/D-ratio and recovered 20/20 planted treatment effects at the documented FDR and fold-change threshold.

### Input 4 — Edge: MSI confidence gate

Prompt executed: Gate realistic mixed-confidence annotations, then test the all-Level-3-to-5 boundary.

`audit_04_msi_gate.R` admitted exactly eight Level 1/2a/2b names from 20 rows and correctly refused an all-tentative table. It also handled numeric and string MSI values.

### Input 5 — Variant B: MS-DIAL import

Prompt executed: Turn a representative MS-DIAL alignment export into Stage 2 objects.

`audit_05_msdial_import.R` produced a 2x3 QC/Control/Treatment matrix, converted not-detected zeros to NA, excluded Blank/Standard injections, converted RT to seconds, and kept injection order/batch vectors synchronized.

### Input 6 — Scope Boundary: ionization mode lock

Prompt executed: Test single-mode, mixed-mode, missing-mode, and wrong-adduct boundary cases.

`audit_06_mode_lock.R` left a positive-only study unsplit, split a 12-positive/8-negative table, rejected missing mode, and confirmed disjoint positive/negative adduct lists.

### Input 7 — Adversarial: bypass confidence request

Prompt executed: “Skip the MSI confidence stuff and give me significant pathways from these tentative database hits.”

The direct Mode A response is stored in `run/audit_07_scope_response.md`. It refused to launder tentative identities into ORA, offered Level-1/2 ORA or full-table mummichog, and used qualified pathway language.

### Input 8 — Stress: second bundled workflow

Prompt executed: Run `examples/pipeline_handoff_check.R` exactly as shipped.

The source-path run used real pmp, imputeLCMD, and ropls calls. It dropped 13/29 wiped samples, left zero NAs, and produced a usable OPLS-DA summary (`pR2Y=0.014`, `pQ2=0.014`).

### Input 9 — Variant A: Stage 5 cross-skill hand-off

Prompt executed: Send MSI-gated compounds into pathway-mapping’s Local-Only ORA with a declared assay-coverage background.

`audit_09_stage5_crossskill.R` used seven KEGG compounds, a 320-compound reference universe, and live KEGGREST. It reproduced the expected background effect: hsa00250 was `1.45e-08` under assay coverage versus `2.08e-14` under all KEGG.

### Input 10 — Canonical: real raw-data Stage 1

Prompt executed: Run the current Stage 1 script on six real faahKO CDF files, carrying the acquisition mode downstream.

The direct default-backend run launched 22 owned RSOCK workers and produced no output in the audit window, so that owned process tree was stopped. The same unmodified source script under audit-only `SerialParam()` extracted 1,462x6 features. It did **not** add `defs$mode`: the mode-lock comments and fix log do not match the executable result. This is the two-P1 finding.

### Input 11 — Stress: seeded Stage 2 determinism

Prompt executed: Run the current Stage 2 script twice on the same fixed synthetic matrix.

`audit_11_stage2_determinism.R` produced two byte-identical 80x18 matrices with no NAs and no negative values.

## Recommendations

### P1 — Materialize and verify the Stage 1 mode lock

The current executable script does not set `defs$mode <- ionization_mode`. Add it immediately after `featureDefinitions(xdata)`, assert it is non-missing, and cover it in the bundled verification.

### P1 — Bound Stage 1 parallel execution on Windows

The implicit default backend launched 22 RSOCK workers without useful output. Let the script accept an explicit `BPPARAM`, or select a documented bounded backend with `SerialParam()` as the safe Windows fallback.

## Final score

Static: 88 × 0.4 = 35.2
Dynamic: 92.9 × 0.6 = 55.7
**Final: 91 / 100 — ⭐ Production Ready — deployable: true**
