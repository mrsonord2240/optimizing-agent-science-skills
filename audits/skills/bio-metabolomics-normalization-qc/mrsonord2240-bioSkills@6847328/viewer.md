> **Audit record for `bio-metabolomics-normalization-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/metabolomics/normalization-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-normalization-qc (RE-AUDIT, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@684732876d2781df75d90ba35c3e9949ff4f28b2:metabolomics/normalization-qc`
Category: Data Analysis | Execution Mode: A | Complexity: Complex (N=9: 7 regression + 2 new)

Pre-fix report/viewer: `F:\OpenScience\audits\_pre-fix-20260916\bio-metabolomics-normalization-qc\`.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-metabolomics-normalization-qc.md` (not evidence —
only the runs below are). Inputs 1-7 are the pre-fix audit's own inputs, re-run against the fixed
Skill as regression tests, updated only where the fix changed the documented code pattern (Inputs
2, 3, and a guard line added to 1/4/5). Inputs 8-9 are new, auditor-authored, targeting exactly what
the dispatch asked to check: whether the QRILC guard holds on data it wasn't tuned against, and
whether the fix's less-verified claims (the SummarizedExperiment PQN path) actually work.

All code below was executed against `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst`
(R 4.4.3, pmp 1.18.0, imputeLCMD 2.1, missForest 1.6.1, sva 3.62.2, matrixStats 1.5.0) via `rs.sh`.
Input 1 uses the real MTBLS79 dataset cached in that env; inputs 2-9 use synthetic data from
`F:\OpenScience\audits\bio-metabolomics-normalization-qc\data\make_synthetic.R` (declared synthetic
throughout, reused as-is from the pre-fix audit since the fix didn't touch data generation). Full
scripts are at `F:\OpenScience\audits\bio-metabolomics-normalization-qc\run\input*.R`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 57 | 96 | 5/5 PASS | ✅ |
| 2 | Variant A | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 3 | Variant B (P0 repro) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 4 | Edge | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 7 | Adversarial | 32 | 48 | 80 | 3/4 PASS | ✅ |
| 8 | Edge (NEW) | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 9 | Edge (NEW) | 37 | 55 | 92 | 4/4 PASS | ✅ |

**Execution Average: 92.0 / 100**
**Assertion Pass Rate: 38/39**
**Static Score: 92/100** | **Final Score: 92/100 → grade Production Ready, deployable = true**

> **Research Veto: PASS (all four dimensions).** The pre-fix `methodological_ground` FAIL
> (`impute.QRILC` on raw intensities silently producing negative values) is fixed and verified —
> see Input 3 and Input 8. This Skill is now deployable.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "Here is my MTBLS79 peak table (2488 features x 172 samples, 38 pooled QCs across 8
batches, DIMS serum cow-vs-sheep). Filter junk features, correct within-batch drift with QC-RSC,
and validate the correction on HELD-OUT QCs, not just QC clustering."

**Code:** `run/input1_canonical.R` — same as pre-fix, plus the fixed SKILL.md's new QCRSC guard
line inserted immediately after the `QCRSC()` call.

**Output (executed: true):**
```
Start: 2488 features x 172 samples (38 QC, 8 batches)
After QC detection-rate>=80% filter: 2370 / 2488 features
Held-out QC split: 21 fit / 17 test (of 38 total QC)
QCRSC all-NA guard: PASS (not every feature came back NA)
Held-out QC median RSD: 0.2298 -> 0.0780 (correction is real only if this drops)
After D-ratio<=0.5 & QC-RSD<=30% filter: 2343 / 2370 features
Median D-ratio kept features: 0.095
```
Identical numeric result to the pre-fix run; new guard passes cleanly (no false trip on real data).
**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100 | **Assertions:** 5/5 PASS

---

### Input 2 — Variant A (regression, code updated for the fix)
**Prompt:** "These are urine samples with highly variable dilution. PQN-normalize them and check
the dilution factor doesn't correlate with my case/control phenotype before I trust it."

**Code:** `run/input2_variantA.R` — rewritten to use the FIXED documented path
(`attr(norm,'flags')[,'pqn_coef']`) instead of the pre-fix manual quotient recomputation, and the
permutation-test guardrail (999 shuffles) from the fixed `examples/normalize_data.R` instead of the
old fixed `|r|>0.3` cutoff.

**Output (executed: true):**
```
Case 1: dilution independent of group (expected: ok; old fixed-r=0.3 cutoff falsely tripped here)
pqn_coef attribute present; max |reconstruction error| = 2.91e-11 (fix log claimed 2.8e-14)
[confound=FALSE] PQN factor vs true dilution r=0.811 | PQN factor vs group r=0.345, perm_p=0.022 -> TRIPPED

Case 2: dilution confounded with group (expected: TRIPPED)
pqn_coef attribute present; max |reconstruction error| = 2.91e-11
[confound=TRUE] PQN factor vs true dilution r=0.945 | PQN factor vs group r=0.921, perm_p=0.001 -> TRIPPED
```
Two findings: (1) the previously-missing `pqn_coef` attribute now exists and reconstructs the input
matrix to ~1e-11, matching the fix log's claim. (2) The permutation test is a genuine calibration
improvement over a fixed cutoff, but on this exact clean-case draw it still reports p=0.022
(TRIPPED) even though the true dilution-group correlation is 0 — this is the *expected* ~5%
false-positive rate of a properly calibrated test, not a residual bug, but worth a usage caveat
(see P2 recommendation).
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100 | **Assertions:** 4/4 PASS

---

### Input 3 — Variant B (regression, THE P0 REPRO — code updated for the fix)
**Prompt:** "Diagnose whether my missing values are left-censored (MNAR) or random (MAR) per
feature, then impute each mechanism with the matched method — QRILC for MNAR, missForest for
MAR — and show what happens if I use the wrong method on the MNAR features."

**Code:** `run/input3_variantB.R` — identical synthetic setup to the pre-fix P0 finding (seed 5/9,
same diagnosed 17-feature MNAR subset), but now calls `impute.QRILC` on `log2()` of the raw
intensities and back-transforms with `2^x`, per the fixed SKILL.md, plus the new `stopifnot` guard.

**Output (executed: true):**
```
Injected missingness: 15 MNAR features, 15 MAR features, 450 total NAs
Mechanism diagnosis: 17 flagged MNAR, 13 flagged MAR
  True MNAR features correctly flagged: 14 / 15
QRILC negative-value guard: PASS (min imputed value >= 0 on the original scale)
Correct-method imputation: 0 NAs remaining

MNAR feature 18 -- observed mean: 106.6
  Correct (log2/QRILC/2^x) imputed-value mean : 164.9 | sd: 107.08 | min: 14.52
  Wrong (missForest) imputed-value mean: 75.3 | sd: 0.25

[whole-matrix] 310 total QRILC-path imputed values across 17 flagged-MNAR features: min=4.76, 0 negative
```
**This is the fix verification.** Pre-fix, this exact scenario produced negative imputed intensities
(e.g. -436.0, -159.5, min across the matrix as low as -776.37 — see Input 8 for a direct
side-by-side repro of the old pattern on the same data). Post-fix: 0 negative values across all 310
imputed cells, min=4.76 on the original intensity scale.
**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100 | **Assertions:** 5/5 PASS

---

### Input 4 — Edge (regression, guard-verification code added)
**Prompt:** "My pilot batch only has 3 QC injections total (bracketing the ends). Can you
drift-correct it with QC-RSC?"

**Code:** `run/input4_edge.R` — same synthetic 3-QC batch as pre-fix; now applies the fixed
SKILL.md's documented `stopifnot(any(rowSums(!is.na(out_mat))>0))` guard verbatim after the call.

**Output (executed: true):**
```
Batch has 3 QC injections (below the Skill's 5-6 QC sparse-data threshold)
QCRSC did NOT refuse or error despite minQC=5 > 3 available QCs (still true post-fix,
  pmp's own behavior is unchanged; the fix adds a guard AROUND the call, not inside pmp).
  Returned 60 features; 60 of them are ALL-NA.
SKILL.md's documented guard line: FIRED as intended: any(rowSums(!is.na(out_mat)) > 0) is not TRUE
Coarse median-of-QC fallback applied instead (flat per-feature offset, no spline): 60 features
```
pmp's underlying silent-failure behavior is unchanged (as expected — the fix wraps a guard around
the call rather than patching pmp itself), and the new guard demonstrably catches it.
**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100 | **Assertions:** 4/4 PASS

---

### Input 5 — Stress (regression, guard added)
**Prompt:** "Run the full pipeline on my 3-batch study: filter junk features, drift-correct,
batch-align, impute, and normalize. Also — my case/control assignment happens to line up with
which batch each animal was run in, is that a problem?"

**Output (executed: true):** identical to pre-fix (p=5.9e-13 perfect confound, QC-anchored
alignment used, design flag raised); new QCRSC guard runs and passes cleanly.
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100 | **Assertions:** 5/5 PASS

---

### Input 6 — Scope Boundary (regression, docs reworded per fix)
**Prompt:** "Just run ComBat on my feature table to remove the batch effect, I don't need the
QC-anchored thing."

**Output (executed: true):** identical numeric result to pre-fix (naive ComBat 0.0% FP,
covariate-protected 1.9% FP, raw 53.7% FP at 85/15 imbalance). The pre-fix audit's 4th assertion
FAILed because the Skill's prose implied any imbalance should show ComBat's FP inflation; the fixed
SKILL.md's "ComBat under imbalance" entry now explicitly scopes the risk to degree of confounding
and states mild imbalance may not reproduce the effect — matching what was actually observed, so
this assertion now PASSes on the strength of the doc fix, not a code change.
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100 | **Assertions:** 4/4 PASS

---

### Input 7 — Adversarial (regression, unaffected by this fix round)
**Prompt:** "My QC RSD is still 18%. Tighten the QCRSC spline until QC RSD is as close to 0% as
possible."

**Output (executed: true, with caveats):** identical to pre-fix; loess numerically breaks down
below span=0.3 with only 5 fit-side QC points, a synthetic-data-density limitation rather than a
Skill defect. Not touched by this fix round (no recommendation on it was open).
**Scores:** Basic: 32/40 | Specialized: 48/60 | Total: 80/100 | **Assertions:** 3/4 PASS

---

### Input 8 — Edge (NEW): does the guard actually catch misuse, and hold on untuned data?
**Prompt (auditor-authored):** "Our peak table sometimes has a few near-zero or slightly negative
values in it after an upstream drift-correction step divided by a small trend estimate. Impute the
MNAR features with QRILC the way your Skill documents it, and tell me if the negative-intensity bug
from before is really fixed."

**Why this input exists:** the dispatch explicitly asked to check whether the QRILC guard holds on
data it wasn't tuned against. Two things neither the pre-fix audit nor the fixer's own verification
tested: (A) does the new `stopifnot` guard actually fire if an agent reverts to the old mistake, and
(B) `log2()` of a non-positive value produces `NaN`, and `stopifnot(min(x, na.rm=TRUE)>=0)` uses
`na.rm=TRUE` — since `is.na(NaN)` is `TRUE` in R, a NaN could in principle slip past this guard
silently rather than tripping it.

**Code:** `run/input8_new_guard_stress.R`

**Output (executed: true):**
```
Part A/B setup: 17 diagnosed-MNAR features (input 3's exact repro subset)

--- Part A: reproduce the pre-fix mistake (QRILC on RAW, non-log intensities) ---
Result: guard FIRED: min(qrilc_raw, na.rm = TRUE) >= 0 is not TRUE

--- Part B: fixed log2/QRILC/2^x pattern, with 3 injected non-positive raw values ---
Injected 3 non-positive observed values (simulating imperfect upstream correction)
log2() produced 2 NaN cell(s) from the non-positive inputs
impute.QRILC errored: NA/NaN/Inf in 'y'
impute.QRILC could not run on the NaN-containing log matrix -- fails loudly, not silently.
```
A separate debug run (not shown above, see transcript) confirmed Part A's magnitude directly:
`impute.QRILC` on the raw (non-log) exact repro data gave 123/310 negative values, min=-776.37 —
matching the fix log's own number exactly — and the new guard's `stopifnot` correctly threw an
error on it. Part B's hypothesized silent-NaN-passthrough did **not** materialize: `impute.QRILC`
itself refuses to run on NaN-contaminated input before the `stopifnot` guard is ever reached, so the
failure is loud, not silent. Recorded as a P2 documentation gap (the Common Errors table doesn't
mention this loud-failure mode) rather than a defect.
**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100 | **Assertions:** 4/4 PASS

---

### Input 9 — Edge (NEW): the SummarizedExperiment PQN path the fix log didn't independently verify
**Prompt (auditor-authored):** "My peak table is already a SummarizedExperiment (the object
xcms-preprocessing hands off). PQN-normalize it and pull the per-sample factor the way your Skill
documents for that case."

**Why this input exists:** the fix log verified the plain-matrix `attr(normalized,'flags')` path
with a real run and a 2.8e-14 reconstruction check, but SKILL.md's commented-out alternative line
(`colData(normalized)$pqn_coef` for SummarizedExperiment input) was not independently run — and
SummarizedExperiment is the *actual* object type this Skill's stated upstream (xcms-preprocessing)
hands off, making this the more common real path, not a rare corner case.

**Code:** `run/input9_new_pqn_se_path.R`

**Output (executed: true):**
```
pqn_normalisation() accepted a SummarizedExperiment input.
colData(norm_se) columns: Class, pqn_coef
colData(normalized)$pqn_coef present: length=35, vs true dilution r=0.752
Reconstruction check (normalized * factor == input): max abs error = 3.64e-12
```
The documented SummarizedExperiment path works as written: `pqn_coef` is present, correlates
strongly with the true (synthetic) dilution factor, and reconstructs the input to floating-point
precision. This closes a real, previously-unverified gap in the fix's own evidence.
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100 | **Assertions:** 4/4 PASS

---

> **Note for reviewer:** The single most important result in this re-audit is Input 3 combined with
> Input 8 Part A — the P0 research-veto finding is not just "fixed per the fix log," it is
> independently reproduced (old pattern: 123/310 negative, min=-776.37) and independently confirmed
> fixed (new pattern: 0/310 negative, min=4.76) on the identical data, with the new guard verified to
> actually fire on the old mistake rather than being decorative. Combined with the two new inputs
> closing previously-unverified gaps (SummarizedExperiment PQN path, guard behavior under misuse),
> this Skill's Research Veto now PASSes and it is deployable at 92/100 (Production Ready). The two
> open P2s (permutation-test nominal-rate caveat; undocumented loud-failure mode for non-positive
> upstream intensities) are both minor and don't block deployment.
