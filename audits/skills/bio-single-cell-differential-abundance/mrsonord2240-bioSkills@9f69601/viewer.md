> **Audit record for `bio-single-cell-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9f69601](https://github.com/mrsonord2240/bioSkills/tree/9f696015114bfcdd053a5a7b4425db5014b40761/single-cell/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-differential-abundance

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@9f696015114bfcdd053a5a7b4425db5014b40761:single-cell/differential-abundance`  
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Decision

**79/100 by weighted score, ❌ Reject, deployable: false.** The Research Veto M4 is **FAIL**: the two direct inline method blocks fail as printed. This overrides the otherwise useful live method evidence.

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical propeller | 37/40 | 56/60 | 93 | 4/4 | ✅ |
| 2 | Milo regression | 34/40 | 48/60 | 82 | 3/4 | ✅ |
| 3 | scCODA reference regression | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 4 | n=1 edge case | 37/40 | 55/60 | 92 | 4/4 | ✅ |
| 5 | DE/DA stress | 35/40 | 53/60 | 88 | 4/4 | ✅ |
| 6 | Milo inline dependency | 23/40 | 27/60 | 50 | 2/4 | ❌ |
| 7 | scCODA inline dependency | 23/40 | 27/60 | 50 | 2/4 | ❌ |

Execution average: **78.4/100**. Assertion pass rate: **23/28 (82.1%)**.

## What ran

All fresh scripts and complete logs are in [`run/phase2_20260923`](run/phase2_20260923).

### Input 1 — canonical propeller

`input1_propeller_regression.R` ran on the synthetic 8-donor fixture. speckle 1.6.0 printed `Performing logit transformation of proportions`; NK cells were the only FDR < 0.05 call (FDR `9.25e-05`) for the planted 5.66% to 12.75% shift. The NK-versus-all-other-proportions correlation was `-1.000`.

### Input 2 — Milo regression

`input2_milo_regression.R` produced 284 neighborhoods. No neighborhood met SpatialFDR < 0.1 for the planted NK shift. The adjusted `~ batch + condition` run produced 16 significant neighborhoods: 15 CD14+ monocyte and one NK; the sensitivity sweep at k 15/30 and prop 0.05/0.10 also had zero calls. This confirms the Skill's documented power/adjustment caution. It also exposes a separate source-fidelity issue: this regression had to load `dplyr`, which the inline block does not declare.

### Input 3 — scCODA reference regression

`input3_sccoda_reference_regression.py` ran a seeded 1,000-draw HMC fit on the eight-sample synthetic fixture. It selected automatic reference `2` (the CD4 T-cell column) and recovered NK cells alone with inclusion probability `1.000`; all other final parameters were zero. The log records 80.1% HMC acceptance. This validates the method when the required TensorFlow import is supplied.

### Input 7 — scCODA source fidelity

The isolated scCODA 0.1.9 environment successfully imported `sccoda` and accepted a count table as `AnnData`, but `input7_sccoda_inline_dependency_check.py` stopped at the source line:

```
EXPECTED_SOURCE_FAILURE=name 'tf' is not defined
COUNTS_ROWS=4 DATA_TYPE=AnnData
```

`SKILL.md` calls `tf.random.set_seed(42)` without `import tensorflow as tf`. Its shipped `examples/sccoda_composition.py` has the import and compiles, so the defect is source/example drift, not a missing environment package.

### Input 4 — one donor per condition

`input4_n1_regression.R` correctly produced `No finite residual standard deviations` rather than a p-value at n=1. At n=2, n=3, and n=4, it called NK only, with FDR `0.01226`, `0.0005968`, and `9.25e-05` respectively.

### Input 5 — DE/DA stress

`input5_de_da_regression.R` recovered 15 monocyte DE genes, all from the planted set (precision 1.0), and no false calls in merged T cells. The constructed CD4/CD8 mixture shift gave zero false DE calls and was accurately reported as inconclusive for that particular fixture.

### Input 6 — Milo inline dependency

With exactly the libraries printed in the Milo code block, fresh execution produced:

```
miloR=2.2.0
dplyr attached before source-faithful call=FALSE
EXPECTED_SOURCE_FAILURE=could not find function "distinct"
```

The inline Milo block needs `library(dplyr)` or must use `dplyr::distinct`.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Completed substantive propeller, Milo, and DE/DA runs produced checked outputs. |
| T2 Contract | PASS | Referenced examples exist and parse/compile. |
| T3 Determinism | PASS | Revised prose includes seed guidance; primary fresh regressions are reproducible fixtures. |
| T4 Security | PASS | No credentials, raw-code execution, or destructive operations. |
| M1 Scientific integrity | PASS | Logged measurements only; inconclusive constructed result was not overclaimed. |
| M2 Practice boundaries | PASS | Group-level analysis only. |
| M3 Methodological ground | PASS | Sample-level replication and composition safeguards were retained. |
| M4 Code usability | **FAIL** | Inline Milo and scCODA blocks terminate with undeclared dependencies. |

## Static score — 81/100

The current version materially improves the prior audit: corrected propeller default, seed documentation, replicate error guidance, and frank Milo power limits all matched fresh outputs. The direct executable contract remains broken because inline snippets do not carry the imports their own examples require. sccomp is still unexecuted with CmdStan absent.

## Required fix

**P0 — repair direct blocks before deployment.** Add `library(dplyr)` to the inline Milo block and `import tensorflow as tf` to the inline scCODA block, then execute those exact inline blocks on the saved synthetic fixture. This should resolve the M4 veto if their full paths complete.

**P1 — sccomp executable proof.** Add and test a complete version-pinned CmdStan/sccomp route, or reduce the advertised sccomp execution claim.

## Artifact notes

The prior 2026-09-16 audit was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-differential-abundance`. The current report and evidence occupy the canonical audit root. Source was not modified.
