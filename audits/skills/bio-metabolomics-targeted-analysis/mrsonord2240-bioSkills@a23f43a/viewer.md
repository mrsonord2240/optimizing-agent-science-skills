> **Audit record for `bio-metabolomics-targeted-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@a23f43a](https://github.com/mrsonord2240/bioSkills/tree/a23f43a7558a4ed755dea34196feaebc5affcfc1/metabolomics/targeted-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-targeted-analysis

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@a23f43a7558a4ed755dea34196feaebc5affcfc1:metabolomics/targeted-analysis`
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The previous active audit has been preserved without modification at `F:\OpenScience\audits\_pre-fix-20260923\bio-metabolomics-targeted-analysis\`. This fresh Phase 2 audit uses the current branch tip only. All fixtures are synthetic.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical regression | 37 | 56 | 93 | 4/4 | Yes |
| 2 | Variant A regression | 36 | 54 | 90 | 4/4 | Yes |
| 3 | Edge regression | 37 | 55 | 92 | 4/4 | Yes |
| 4 | Variant B regression | 38 | 56 | 94 | 4/4 | Yes |
| 5 | Stress regression | 38 | 58 | 96 | 4/4 | Yes |
| 6 | Fresh validation | 39 | 58 | 97 | 4/4 | Yes |
| 7 | Fresh validation | 38 | 58 | 96 | 4/4 | Yes |

Execution average: **94.0/100**. Assertions: **28/28**. Static score: **94/100**. Final score: **94/100 — Production Ready — deployable**.

Structural veto: PASS (stability, contract, determinism, security). Research veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability).

## Dynamic evidence

### 1. Weighted calibration and SIL-IS quantification

Ran `run/input1_canonical.R` via the environment's `rs.sh` wrapper against `data/input1_calibration_standards.csv` and `data/input1_unknown_samples.csv`.

```
LLOQ set to: 2 ng/mL
U1 14.84 vs 15 (-1.09%); U2 39.72 vs 40 (-0.71%)
U3 79.61 vs 80 (-0.48%); U4 300.43 vs 300 (0.14%)
U5 706.43 vs 700 (0.92%); U6 2.99 vs 3 (-0.22%)
All non-below-LLOQ samples within +-15% of planted truth: TRUE
```

The current bundled `examples/targeted_quantification.R` was also run twice. Both runs printed LLOQ=1 nM and `S5 ... FALSE` for the planted qualifier collapse, then returned status 2816 after output materialization. `run/runtime_exit_smoke.R` returned `BASE_R_SMOKE_OK` with status 0 through the same wrapper. The complete output is recorded in the execution transcript and this isolated issue is P2, not hidden as a success-by-exit-code claim.

### 2. Shared-IS strategy advisory

The fresh Mode A response is in `run/input2_variantA_phase2_response.md`. It correctly limits one global IS to exploratory or semi-quantitative work, explains why precision does not establish accuracy across distant analytes, and escalates to clustered SIL-IS for cross-study quantification or one co-eluting SIL-IS per analyte plus ICH M10 for regulated work.

### 3. LOD/LLOQ and forced single transition

Ran `run/input3_edge_lod_lloq.R` on synthetic blank replicates.

```
Mean blank ratio: 0.001068  SD: 8.758e-05
LOD: 1.329 ng/mL
LOD below stated 2 ng/mL calibrator: TRUE
```

The output treats a single transition as a named selectivity compromise requiring retention-time and selectivity evidence, not as equivalent to ion-ratio confirmation.

### 4. Ion ratio and matrix factor

Ran `run/input4_variantB_ion_ratio_matrix_factor.R` on six clean synthetic lots and one planted interferent.

```
Clean lots: all id_confirmed TRUE
Interferent ion ratio: 0.1667; id_confirmed FALSE
IS-normalized matrix-factor mean: 0.982
MF CV: 4.44%; threshold <=15%; PASS TRUE
```

### 5. Current ICH M10 stress pathway

Ran `run/input5_phase2_ich_m10_stress.ps1`, which invokes both current shipped helpers rather than the archived pre-fix pooled-SD logic.

```
LLOQ: intra-day d1 21.7%, d2 20.6%; nested-ANOVA inter-day 21.1% -> FAIL
LOW/MID/HIGH nested-ANOVA results -> PASS
blank response 0.00850 | LLOQ response 0.00196
analyte carryover 433.7% of LLOQ (limit 20%)
CARRYOVER PASS: FALSE
ASSERT regulated_assay_rejected_for_precision_and_carryover=TRUE
```

### 6. Fresh direct test of `precision_nested_anova.R`

Ran `run/input6_shipped_precision.ps1` exactly against the current source helper. It expected its protective exit 1 and verified the actual printed failure rather than treating an expected failure as an execution failure.

```
LLOQ ... naive pooled CV 18.9% (not valid) | nested-ANOVA inter-day CV 21.1% -> FAIL
ALL LEVELS PASS: FALSE
ASSERT precision_script_rejects_planted_LLOQ_failure=TRUE
```

### 7. Fresh direct test of all `matrix_recovery_carryover.R` modes

Ran `run/input7_shipped_matrix_recovery_carryover.ps1` on the current source helper and a newly created synthetic recovery fixture.

```
matrix factor: six lots, CV 4.44%, MATRIX FACTOR PASS: TRUE
recovery: LLOQ 85.00% (CV 1.18%), MID 70.17% (CV 0.50%)
carryover: analyte 15.0% of LLOQ; IS 0.3%; CARRYOVER PASS: TRUE
ASSERT matrix_recovery_carryover_all_modes_pass=TRUE
```

## Source and static checks

`run/static_parse_checks.ps1` parsed the current `examples/targeted_quantification.R`, `scripts/precision_nested_anova.R`, and `scripts/matrix_recovery_carryover.R` through the target R wrapper. It also confirmed all files referenced by the current workflow are present: `SKILL.md`, `usage-guide.md`, the example, and both scripts.

## Score and issue

All Production Ready floors pass: static 94 >= 80; execution 94.0 >= 85; Layer 1 average 37.6 >= 32; Layer 2 average 56.4 >= 48; assertions 100% >= 90%; no veto and no P0.

- P2 — The bundled ggplot2 example returns status 2816 after emitting correct complete output; reproduce in a clean target R/ggplot2 environment and fix or document the teardown behavior if it persists.
