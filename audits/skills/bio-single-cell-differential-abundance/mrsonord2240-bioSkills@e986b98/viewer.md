> **Audit record for `bio-single-cell-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e986b98](https://github.com/mrsonord2240/bioSkills/tree/e986b98c85b38b4ad31ee9289f5aa39f6bec212b/single-cell/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-differential-abundance

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@e986b98c85b38b4ad31ee9289f5aa39f6bec212b:single-cell/differential-abundance`
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Decision

**90/100, ⭐ Production Ready, deployable: true.** All 7 fresh inputs completed with 28/28 assertions. Both veto gates pass. In particular, the source-faithful Milo and scCODA paths now execute after the P0 import repair.

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|
| 1 | Canonical propeller | 37/40 | 56/60 | 93 | 4/4 | ✅ |
| 2 | Milo regression | 36/40 | 52/60 | 88 | 4/4 | ✅ |
| 3 | scCODA reference regression | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 4 | n=1 edge case | 37/40 | 55/60 | 92 | 4/4 | ✅ |
| 5 | DE/DA stress | 35/40 | 53/60 | 88 | 4/4 | ✅ |
| 6 | Exact Milo inline path | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 7 | Exact scCODA inline path | 39/40 | 57/60 | 96 | 4/4 | ✅ |

Execution average: **92.1/100**. Assertion pass rate: **28/28 (100%)**.

## Fresh execution evidence

All runnable scripts and logs are under [run/2026-09-23-final-reaudit](run/2026-09-23-final-reaudit).

### 1. Eight-donor propeller composition test

Prompt: Compare donor-level cell-type composition for four control and four treated samples with a planted NK expansion, and avoid interpreting simplex-induced changes as independent depletions.

`input1_propeller_regression.R` ran with speckle 1.6.0. The default logged the logit transformation and called **NK cells only** (FDR `9.25e-05`) for the planted 5.65% to 12.75% change. NK proportion versus the mean of all other types was `-1.000`.

### 2. Eight-donor Milo neighborhood regression

Prompt: Run Milo on the same synthetic donor-level SCE, including an adjusted design and k/prop sensitivity, and interpret a null without overclaiming no change.

`input2_milo_regression.R` made 284 neighborhoods and returned no SpatialFDR < 0.1 call for the planted NK change. All four k/prop checks also had zero calls. The adjusted `~ batch + condition` output was retained only as the Skill's caution: it changed the result to 16 neighborhoods, mostly unchanged CD14 monocytes. The R runtime returned Windows code 2816 after the checked `DONE` output; the materialized output, not exit code, is the evidence.

### 3. Seeded scCODA reference-model regression

Prompt: Test cluster composition with automatic reference selection on the same eight donors and confirm the planted NK change under a seeded HMC fit.

`input3_sccoda_reference_regression.py` in the isolated scCODA 0.1.9 environment completed 1,000 draws at 80.1% acceptance. Automatic reference was index 2 (CD4 T cells); NK alone had inclusion probability 1.0 and a positive log2 fold change.

### 4. One donor per condition

Prompt: Test the n=1 boundary and show whether a donor-confounded contrast produces a valid abundance conclusion.

`input4_n1_regression.R` correctly surfaced `No finite residual standard deviations` at n=1 per group. At n=2, n=3, and n=4, only NK was called, with FDR 0.01226, 0.0005968, and 0.0000925 respectively. Its checked output completed despite the same Windows code 2816 at teardown.

### 5. Joint DE and DA interpretation

Prompt: Pair pseudobulk DE with abundance testing and avoid claiming a CD4/CD8 mixing artifact unless the fixture demonstrates one.

`input5_de_da_regression.R` recovered 15 monocyte DE genes with precision 1.0. It found zero false DE calls in the forced CD4/CD8 mixing construction, and correctly described that fixture as inconclusive rather than proving the general mechanism.

### 6. Exact repaired Milo inline path

Prompt: Run the displayed Milo block exactly as currently printed, after constructing its documented `sce` input.

`input6_milo_inline_full_path.R` includes the exact source imports, notably `library(dplyr)`. It completed `distinct()`, created 8 donor designs, produced 306 neighborhoods and SpatialFDR output, then printed:

```
PASS_MILO_INLINE_FULL_PATH designs=8 neighbourhoods=306
```

This closes the prior M4 Milo import failure.

### 7. Exact repaired scCODA inline path

Prompt: Run the displayed scCODA block exactly as currently printed, including its default HMC settings, after constructing its documented `adata` input.

`input7_sccoda_inline_full_path.py` includes the exact source import `import tensorflow as tf`. Its default 20,000-draw HMC completed in 87.848 seconds at 73.9% acceptance, selected reference 2, and gave only NK a nonzero final parameter/credible effect:

```
PASS_SCCODA_INLINE_FULL_PATH samples=8 reference=2
```

This closes the prior M4 scCODA import failure.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All seven fresh inputs produced checked outputs. |
| T2 Contract | PASS | Required Skill files and examples are present; displayed primary blocks now complete. |
| T3 Determinism | PASS | Source documents seeds and fresh seeded Milo/scCODA paths completed. |
| T4 Security | PASS | No credentials, raw code execution, or destructive operation appears. |
| M1 Scientific integrity | PASS | Every numerical claim above is tied to a fresh log; inconclusive evidence remains qualified. |
| M2 Practice boundaries | PASS | Donor-group analyses only; no individual clinical decision. |
| M3 Methodological ground | PASS | Sample replication, simplex-aware testing, and n=1 refusal are preserved. |
| M4 Code usability | PASS | Exact repaired Milo and scCODA inline blocks completed end to end. |

## Static evaluation — 86/100

The direct source/example import drift is repaired. The remaining material limitation is **P1**: sccomp is still advertised, but its CmdStan/sccomp route has not been executed in this environment and the text records API drift. It does not fire a veto or block deployment, but needs a complete version-pinned execution proof (or a narrowed claim).

## Preservation and provenance

The preceding rejected 79-point M4 report and viewer are preserved in [rejected-phase2-9f69601](../_pre-fix-20260923/bio-single-cell-differential-abundance/rejected-phase2-9f69601). The current report is source-specific to commit `e986b98c85b38b4ad31ee9289f5aa39f6bec212b`; no source file was edited in Phase 2.
