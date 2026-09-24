> **Audit record for `bio-crispr-screens-batch-correction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f04f3c5](https://github.com/mrsonord2240/bioSkills/tree/f04f3c5168224974c7879822c33f364c5e4fd034/crispr-screens/batch-correction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-batch-correction

## Canonical final summary

**Final:** 96/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@f04f3c5168224974c7879822c33f364c5e4fd034:crispr-screens/batch-correction`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@f04f3c5168224974c7879822c33f364c5e4fd034:crispr-screens/batch-correction`
Category: Data Analysis | Execution mode: D (Hybrid) | Complexity: Complex (N=9)
Final-pass disclosure: `meta.auditor_independent: false`; fixed and audited under one brief, per `CHECKPOINT.md`.

The previous finished report and its complete prior run directory were preserved before replacement at `F:\OpenScience\audits\_pre-fix-20260922\bio-crispr-screens-batch-correction\`.

## Summary

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical: balanced ComBat CLI | yes | 38 | 58 | 96 | 3/3 | ✅ |
| 2 | Variant A: hidden batch RUVg | yes | 38 | 58 | 96 | 3/3 | ✅ |
| 3 | Edge: fully confounded design | yes | 38 | 57 | 95 | 3/3 | ✅ |
| 4 | Variant B: MAGeCK batch covariate | yes | 37 | 58 | 95 | 3/3 | ✅ |
| 5 | Stress: residual-RSS guard | yes | 39 | 59 | 98 | 3/3 | ✅ |
| 6 | Scope boundary: bulk RNA-seq | no* | 37 | 55 | 92 | 3/3 | ✅ |
| 7 | Adversarial: unnecessary correction | yes | 38 | 57 | 95 | 3/3 | ✅ |
| 8 | Fresh: standalone example | yes | 37 | 56 | 93 | 3/3 | ✅ |
| 9 | Fresh: SVA + NTC anchoring | yes | 38 | 58 | 96 | 3/3 | ✅ |

*Input 6 is a direct inspection of the Skill's scope response; no computation is applicable.

**Execution average:** 95.1/100. **Assertions:** 27/27. **Executed:** 8/9.
**Static:** 96/100. **Final:** 96/100, ⭐ Production Ready, deployable.
Skill Veto: PASS (T1–T4). Research Veto: PASS (M1–M4).

## Evidence and generated code

All audit code and stdout logs are in `run/phase2/`. `skill_copy/` is an audit-owned byte-copy of the source-tip runnable scripts; the source worktree stayed clean. The scripts that generated and asserted the results are:

- `phase2_core_regressions.py` — Inputs 1, 3, 5, 7; `phase2_core_regressions.log`
- `phase2_r_regressions.R` — Inputs 2, 9; `phase2_r_regressions.log`
- `phase2_mageck.py` and `phase2_postrun_assert.py` — Input 4; `phase2_postrun_assert.log`
- `phase2_example.ps1` — Input 8; `phase2_example.log`
- `phase2_static_assert.py` — parsed Python sources, checked split/file presence and MAGeCK control-normalization flag; `phase2_static_assert.log`

### Input 1 — canonical batch diagnosis and ComBat

Prompt: “I ran a two-batch CRISPR knockout screen; diagnose technical batch, correct it with condition protected, and verify the biological dropout signal.”

The copied diagnostic CLI found batch significant on PC2 (`p=0.013885`), which its current output explicitly calls out as needing inspection even though PC1 was condition-dominant. The copied ComBat CLI corrected all 600 guides, wrote no uncorrected rows, and produced a finite table. Assertions: PCA batch-centroid distance `12.500 -> 0.297`; essential-guide mean LFC `-1.645 -> -1.629`; output shape and finiteness passed.

### Input 2 — hidden batch through RUVg

Prompt: “My NTCs shift but I do not know the technical batch; use RUV controls.”

Fresh 1,000-guide/8-sample synthetic count data ran through the documented character-rowname `cIdx` call. `W` was `8x2`, corrected counts were `1000x8`, and no NA occurred. Replacing the documented rownames with the old integer `which()` pattern produced the expected S4 dispatch error, confirming that this is a regression test.

### Input 3 — fully confounded design

Prompt: “All drug samples were processed in batch 2 and all vehicle samples in batch 1; correct the batch.”

The copied wrapper raised `ConfoundingVariablesError: Covariate is confounded with batch. Try removing the covariates.` This is the scientifically safe outcome and agrees with the Skill’s decision tree: correction cannot separate batch from biology.

### Input 4 — batch-aware MAGeCK MLE

Prompt: “Use an explicit batch covariate in MAGeCK MLE rather than pre-correction.”

The exact current command, including `--permutation-round 10`, was run on the prior public HAP1 subset and completed. `phase2_batch_aware_mle.gene_summary.txt` contains 1,646 genes and two beta columns; both were fully finite. A separate completed-output parser asserted this and confirmed the option is listed by `mageck mle --help`.

### Input 5 — zero-residual feature stress test

Prompt: “Will the ComBat guard safely handle guides fully explained by batch and condition?”

On a fresh 120-guide balanced matrix, the planted `zero_residual` guide was the only returned raw row; it exactly matched original counts. A planted `one_batch_constant` guide was not over-filtered. The fitted output contained no NaN or Inf.

### Input 6 — scope boundary

Prompt: “Does this CRISPR-screen Skill apply to bulk RNA-seq?”

Not a compute task. The current `Related but out of scope` passage correctly states that ComBat/RUV/SVA methods generalize, while CRISPR-specific NTC requirements, CEGv2 validation, and MAGeCK/Chronos integration do not. It directs the user to replace those checks with assay-appropriate ones.

### Input 7 — force correction despite no detected batch

Prompt: “My across-batch replicates already agree; run ComBat anyway.”

The forced synthetic no-batch call completed with preserved `350x8` shape and no NaN/Inf. The result does not override the Skill’s guidance to decline unnecessary correction; it verifies that the residual-RSS filter and post-fit check do not return the historical silent-all-NaN failure.

### Input 8 — fresh standalone example

The copied `examples/batch_correct.py` ran in an audit-only directory. It wrote `qc_metrics.csv`; parsed results showed 15 detected planted hits and true-positive rate `1.0` (zero false positives).

### Input 9 — fresh SVA and NTC anchoring

The documented SVA pattern found one surrogate variable, yielding an `8x3` finite design matrix. The documented NTC-anchored scaling function set every sample’s median across 300 named NTC guides to exactly `1000` (tolerance `<1e-9`).

## Static assessment

The 231-line entry point uses references for individual methods and scripts for nontrivial Python. All shipped Python modules parsed, all four referenced method files existed, and MAGeCK control normalization was confirmed as a real option. The decision tree, failure modes, validation checklist, runtime note, reproducibility caveat, and scope boundary cover the main operational risks.

Minor recommendation: document a JACKS version/API expectation, or make it only a cross-reference to the dedicated JACKS Skill. This is P2 only and did not affect a tested primary workflow.
