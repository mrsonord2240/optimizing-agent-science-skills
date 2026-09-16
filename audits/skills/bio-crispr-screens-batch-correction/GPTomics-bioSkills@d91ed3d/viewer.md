> **Audit record for `bio-crispr-screens-batch-correction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/batch-correction) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-batch-correction
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/batch-correction`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 45 | 77 | 4/5 PASS | ✅ |
| 2 | Variant A | 32 | 45 | 77 | 3/4 PASS | ✅ |
| 3 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B | 37 | 53 | 90 | 4/5 PASS | ✅ |
| 5 | Stress | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 25 | 37 | 62 | 3/4 PASS | ⚠️ |
| 7 | Adversarial | 22 | 32 | 54 | 3/5 PASS | ❌ |

**Execution Average: 78.6 / 100**
**Assertion Pass Rate: 25/31**
**Static Score: 78/100 | Final Score: 78/100 | Grade: ✅ Limited Release | Deployable: true**

> Reviewer note: check Input 7 (❌) first — a safety-relevant, previously undocumented failure mode.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I ran my HAP1 knockout screen across two processing batches — diagnose the batch effect, apply ComBat with condition as the biological covariate, and verify the correction removes the batch shift without erasing true essential-gene dropout signal."

**Executed:** true — `run/input1_canonical.py`, real `HAP1_TKOv3_reads.txt` (hart-lab/bagel, 71,090 sgRNAs), planted 0.5x multiplicative + 150 additive batch2 shift (known ground truth).

**Output (key excerpts):**
```
=== Reproducing SKILL.md's combat_correct() verbatim (expected to crash) ===
CONFIRMED BUG: AttributeError: 'numpy.ndarray' object has no attribute 'columns'

[after fix: data as DataFrame, mod=list(condition_vector)]
ComBat correction applied (with condition covariate). Output shape: (71090, 8)
Post-correction PC1 batch_F / cond_F = 0.00 (was 0.01)
Batch centroid distance in PC1/PC2: raw=233.83 -> corrected=0.98 (99.6% reduction)

=== Essential-gene signal check (CEGv2 vs NEGv1 dropout AUC) ===
Pre-correction:  AUC = 0.9947  (n=1443 labeled genes)
Post-correction: AUC = 0.9966  (n=1443 labeled genes)
```

**Bug found:** SKILL.md's `combat_correct()` passes `data` as a raw numpy array (pycombat needs a DataFrame — it accesses `.columns`/`.index`) and passes `mod` as a one-hot-encoded numpy array via `pd.get_dummies(...).values` (pycombat's `treat_covariates()` does `if mod == []:`, which raises `ValueError: operands could not be broadcast together` for any non-empty ndarray — the docstring says `mod` must be a plain **list**, one-hot-encoded internally). Fixed with a 1-line change; the corrected function then ran cleanly on all 71,090 real guides.

**Scores:** Basic: 32/40 | Specialized: 45/60 | Total: 77/100
**Assertions:**
- [FAIL] SKILL.md's own combat_correct() code runs without modification — TypeError/ValueError as above.
- [PASS] Batch effect is measurably reduced after correction — 99.6% centroid-distance reduction.
- [PASS] Essential-gene dropout signal (CEGv2 vs NEGv1) preserved or improved — AUC 0.9947 → 0.9966.
- [PASS] Biological covariate supplied — mod=list(condition_vector) after fix.
- [PASS] Output stays within stated scope.

---

### Input 2 — Variant A
**Prompt:** "I don't know where my technical batch is coming from, but my NTCs look shifted across samples. Use RUV with the NTC sgRNAs as negative controls to remove it."

**Executed:** true — `run/input2_ruv.R` (RUVSeq 1.40.0), synthetic 2500-guide/8-sample dataset with a HIDDEN (analyst-invisible) true batch and 500 NTC controls.

**Output (key excerpts):**
```
Error: unable to find an inherited method for function 'RUVg' for signature
'x = "SeqExpressionSet", cIdx = "integer", k = "numeric"'

[after fix: cIdx as character rownames]
RUVg ran successfully. k=2 unwanted factors estimated.
NTC median counts (raw):       deep=800.0  shallow=519.0  ratio=0.649
NTC median counts (corrected):  deep=644.0  shallow=644.0  ratio=1.000
Essential-gene guides: mean raw LFC=-1.986, mean RUV-corrected LFC=-1.980
```

**Bug found:** `ntc_indices <- which(rownames(counts_df) %in% ntc_sgrna_names)` returns integer positions, but `RUVg`'s S4 method for `x="SeqExpressionSet"` only has a registered signature for `cIdx="character"` — dispatch fails outright. Fixed by using character rownames instead of `which()` positions.

**Scores:** Basic: 32/40 | Specialized: 45/60 | Total: 77/100
**Assertions:**
- [FAIL] SKILL.md's own RUV code runs without modification — S4 dispatch error as above.
- [PASS] RUV removes the hidden true batch shift in NTC medians — ratio 0.649 → 1.000.
- [PASS] Essential-gene dropout signal survives correction — LFC -1.986 → -1.980.
- [PASS] Correction used only NTC identity, not disclosed batch labels.

---

### Input 3 — Edge
**Prompt:** "All my drug-arm samples were processed in batch 2 (arrived late) and all vehicle-arm samples in batch 1. Can I still use ComBat to remove the batch effect?"

**Executed:** true — `run/input3_confounded.py`, real HAP1 data arranged so batch and condition are perfectly collinear.

**Output (key excerpts):**
```
Before any correction: CEGv2-vs-NEGv1 essentiality AUC = 0.9450 (n=1443)

ComBat WITHOUT mod (batch==condition, uncorrected mistake):
  Essentiality AUC after = 0.8312 (was 0.9450)
  Mean |LFC| for CEGv2 genes: before=2.070, after=0.017
  SKILL.md's claim ('correction will destroy biology') CONFIRMED by this run.

ComBat WITH mod=condition_vector (condition is fully collinear with batch):
  pycombat correctly REFUSED: ConfoundingVariablesError: Covariate is
  confounded with batch. Try removing the covariates.
```

**Finding:** No bugs — this input validates that SKILL.md's stated failure mode is real (essential-gene signal is nearly erased, AUC drops 11 points, mean |LFC| collapses 99%) and that pycombat's own confound detector correctly refuses rather than silently returning a wrong answer when a collinear covariate is supplied.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS (failure mode reproduced; tool refusal confirmed; correct recommendation; no fabrication).

---

### Input 4 — Variant B
**Prompt:** "I have a 2-batch HAP1 screen with vehicle/treatment arms in each batch. Add batch as a covariate to my MAGeCK MLE design matrix instead of pre-correcting, and tell me if the treatment beta still recovers known essential genes."

**Executed:** true — real `mageck mle` (0.5.9.5), 1646-gene / 6460-guide real HAP1 subset (646 CEGv2 genes + 1000 random genes), 2 batches × 2 conditions × 2 replicates, ~80s runtime.

**Output (key excerpts):**
```
Most negative treatment betas (should be essential genes):
   POLR2L  -1.6851   True
   POLR3H  -1.6101   True
   RPL31   -1.5918   False
   PCNA    -1.5620   True
   MRPL53  -1.5397   True
   RRM1    -1.4981   True
Essentiality AUC from batch-aware MLE treatment beta: 0.9685
```

**Finding:** No bugs — `mageck mle --count-table --design-matrix --output-prefix` ran exactly as SKILL.md documents. Top hits (POLR2L, POLR3H, PCNA, MRPL53, RRM1) match this environment's independent MAGeCK/BAGEL2/drugZ smoke tests on the same real dataset (see TOOLS.md), despite the planted batch shift — strong external validation of the "preferred" covariate-modeling approach.

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100
**Assertions:** 4/5 PASS (1 FAIL: SKILL.md doesn't disclose that full-genome-scale MLE is a multi-hour job — only the environment's own TOOLS.md notes this).

---

### Input 5 — Stress
**Prompt:** "My screen has clear essentiality signal, but a small hit set is barely significant. I suspect a hidden confounder I haven't identified. Use SVA to find latent surrogate variables and add them to my MAGeCK MLE design matrix."

**Executed:** true — `run/input5_sva.R` (sva 3.54.0), synthetic 4000-guide × 12-sample matrix with a hidden multiplicative confound orthogonal to condition (r=0.070 with condition).

**Output (key excerpts):**
```
Number of significant surrogate variables is:  1
sva() found n.sv = 1 surrogate variable(s)
SV1 correlation with the TRUE hidden confound: r = 0.998
Recovered the planted confound: YES
```

**Finding:** No bugs — SKILL.md's SVA snippet (`mod`, `mod0`, `sva()`) ran completely unmodified and recovered the hidden confound almost perfectly.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary
**Prompt:** "I have a bulk RNA-seq differential expression experiment (not a CRISPR screen) with 2 batches — should I use ComBat here, and does this Skill apply?"

**Executed:** false — reasoning-only; no computation needed to answer the scope question. Assessed against SKILL.md/usage-guide.md text directly.

**Response summary:** The underlying methods (ComBat, RUV, SVA) are general statistical techniques — notably, SKILL.md's own References section cites Johnson 2007, Leek 2012, and Risso 2014, which are microarray/RNA-seq papers, not CRISPR papers — so they do transfer to bulk RNA-seq. However, this Skill's quantitative thresholds and QC (≥500 NTCs, CEGv2 PR-AUC, MAGeCK MLE / Chronos integration) are CRISPR-screen-specific and do not transfer. SKILL.md has no explicit section stating this boundary; an agent must infer it from the CRISPR-specific frontmatter description alone.

**Scores:** Basic: 25/40 | Specialized: 37/60 | Total: 62/100
**Assertions:** 3/4 PASS (1 FAIL: no explicit out-of-domain escape hatch exists in the Skill text).

---

### Input 7 — Adversarial
**Prompt:** "My replicate correlations are already 0.97+ within and across batches, but let's run ComBat anyway just to be safe."

**Executed:** true — `run/input7_unnecessary_correction.py`, real HAP1 data resampled into 2 "batches" with **no** planted batch effect (both batches are independent Poisson draws of the same real distributions).

**Output (key excerpts):**
```
=== Replicate Pearson correlations (no planted batch effect) ===
  B1_day0_r1 vs B2_day0_r1 (cross-batch): r = 0.9981
  ... all pairs r >= 0.9974

Per SKILL.md 'When NOT to Correct': replicate r>0.95 within AND across
batches => 'No batch effect to correct'. Correction should be DECLINED here.

=== Replicate Pearson correlations AFTER forcing ComBat on clean data ===
  ... r_after=nan  (delta=+nan)   [all four pairs]
```
Follow-up check: **568,720 / 568,720 output values were NaN (100%)** — `pycombat` completed with exit code 0 and only a buried `RuntimeWarning: invalid value encountered in divide`, no exception.

**Finding — the audit's most important result:** exactly the scenario SKILL.md's own "When NOT to Correct" table calls out (replicate r>0.95 within and across batches) is also the scenario where `pycombat`'s empirical-Bayes variance step divides by a near-zero pooled variance and returns **100% NaN** with no error. Neither `combat_correct()` nor the usage-guide's Validation Checklist (PCA overlap, replicate Pearson, PR-AUC, NTC stability) includes a basic NaN/Inf sanity check — a user who overrides the "decline" guidance gets silent total data loss, not "wasted effort," and nothing in the Skill would catch it before it propagates into hit calling.

**Scores:** Basic: 22/40 | Specialized: 32/60 | Total: 54/100
**Assertions:** 3/5 PASS (2 FAIL, including a safety-flavored assertion — output not checked for NaN, and the Skill doesn't warn this can happen).

---

## Cross-Cutting Notes

- **3 real, reproducible bugs found** in SKILL.md's own documented code, none previously flagged in `TOOLS.md`: (1) `combat_correct()`'s `mod`/`data` type mismatch (Input 1), (2) RUV's `cIdx` type mismatch against `SeqExpressionSet` (Input 2), (3) silent 100%-NaN ComBat output on batch-free data (Input 7). All three are 1-line fixes once diagnosed; none are exotic dependency-version issues — pyComBat 0.3.3 and RUVSeq 1.40.0 are exactly the versions this Skill targets.
- **2 patterns ran perfectly out-of-the-box** on real data: MAGeCK MLE with a batch covariate (Input 4) and SVA latent-confounder discovery (Input 5) — both recovered real, independently-verifiable biological signal.
- The install for `pyComBat` (`combat` on PyPI) was missing from this candidate's `TOOLS.md` prior to this audit (flagged in `SELECTION.md`); it has been installed under the install lock with zero existing-package version changes and added to `TOOLS.md`.
