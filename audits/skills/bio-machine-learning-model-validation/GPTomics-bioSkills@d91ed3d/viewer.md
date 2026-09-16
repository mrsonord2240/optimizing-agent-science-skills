> **Audit record for `bio-machine-learning-model-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/model-validation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-model-validation

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/model-validation`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex → N = 7
Environment: shared venv — scikit-learn 1.9.1, imbalanced-learn 0.14.2, RDKit 2026.03.6.
Data: the candidate's own domain — 3,224 ChEMBL hERG compounds as ECFP4, binarised at pChEMBL ≥ 6 (23.8% positive), with Bemis-Murcko scaffold as the grouping variable; plus a purpose-built zero-signal synthetic set for the leakage demonstration.
Inputs executed: **7 / 7**
Code: `run/inputs_all.py`. Output: `run/inputs_all.out`, `run/clean.out`.

**Scope note (gate 5).** This Skill is written for omics, but every snippet applied to chemical fingerprints without a single change — scaffold substitutes directly for patient as the unit of independence. It is included as a supporting Skill for the QSAR validation leg, not as a chemistry Skill.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 53 | 90 | 3/4 | ✅ |
| 2 | Variant A | yes | 39 | 57 | 96 | 4/5 | ✅ |
| 3 | Variant B | yes | 38 | 54 | 92 | 4/4 | ✅ |
| 4 | Edge | yes | 39 | 56 | 95 | 4/5 | ✅ |
| 5 | Stress | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 34 | 48 | 82 | 2/4 | ✅ |
| 7 | Adversarial | yes | 38 | 53 | 91 | 4/5 | ✅ |

**Execution Average: 91.3 / 100**
**Assertion Pass Rate: 25/31 (80.6 %)**

---

## Input 1 — Canonical

**Prompt**
> We tuned a hERG classifier with GridSearchCV and reported the best CV score. Reviewers pushed back. Redo it the way you would defend it, and tell me how much the number moves.

```
  Nested AUC: 0.753 +/- 0.030        (SKILL.md snippet, verbatim)
  Flat CV best score (same data used to choose AND grade): 0.762
  best params = {'clf__C': 0.01, 'select__k': 200}
  optimism = +0.009 AUC
```

**Reading.** The procedure is exactly as written and the bias is in the documented direction, but +0.009 is not what "reviewer red flag" conjures. The Skill is right in principle and gives the reader no way to anticipate magnitude.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100** · **Assertions 3/4**

---

## Input 2 — Variant A

**Prompt**
> Someone on the team picks the top 20 features by univariate test on the whole dataset and then cross-validates the classifier. They say it is fine because the classifier never sees the test fold. Settle it — and use data where we know the right answer.

```
  synthetic: (200, 5000) random normal features, random labels,
             true signal = ZERO by construction

  selection OUTSIDE the fold (leaky):  CV AUC = 0.904
  selection INSIDE the Pipeline      :  CV AUC = 0.547
  -> the leak manufactures +0.357 AUC out of nothing

  scaler fit on all data: 0.484  vs inside the Pipeline: 0.488  (difference -0.004)
```

**Reading — the strongest single result in this audit.** The Skill says selection leakage produces "near-perfect CV from pure noise". On data with *no signal whatsoever*, selecting 20 of 5,000 features on the full set before CV gives an AUC of 0.904. Moving the identical selection inside the Pipeline returns it to chance.

The second half is a finding against the Skill. Its taxonomy puts preprocessing leakage first, labelled "most common, most missed", with feature selection below it as a "severe special case". Measured on the same zero-signal data, scaler leakage cost −0.004 AUC — nothing — while selection leakage produced 0.357. The label is about frequency, but the table ordering reads as severity, and a reader triaging by position would start in the wrong place.

**Scores:** Basic 39/40 · Specialized 57/60 · **Total 96/100** · **Assertions 4/5**

---

## Input 3 — Variant B

**Prompt**
> Our compounds come in analogue series, so most rows are not independent. Use scaffold as the group and tell me what we have been over-reporting by.

```
  StratifiedKFold (ignores scaffold):  AUC 0.588 +/- 0.035
  StratifiedGroupKFold (scaffold):     AUC 0.573 +/- 0.025
  inflation from ignoring the group: +0.015 AUC
  scaffolds spanning train and test under plain KFold: 419 (summed over folds)
  same count under StratifiedGroupKFold: 0
  RepeatedStratifiedKFold 5x10: AUC 0.602 +/- 0.044
      (90% of draws in [0.533, 0.661])
```

**Reading.** The leakage is unambiguous — 419 scaffolds straddle the split under plain k-fold and zero do under the grouped splitter — while the metric cost is 0.015 AUC. Both facts matter, and the repeated-CV interval shows that 0.015 sits well inside the run-to-run spread, which is precisely why the Skill insists on reporting the spread rather than a bare number.

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100** · **Assertions 4/4 PASS**

---

## Input 4 — Edge

**Prompt**
> Our calibration code broke after an sklearn upgrade — `cv='prefit'` throws now. What replaced it, and does recalibrating actually help?

```
  sklearn 1.9.1
  cv='prefit' -> InvalidParameterError: The 'cv' parameter of CalibratedClassifierCV
                 must be an int in the range [2, inf), an object implementing 'spl...
  FrozenEstimator route -> OK
    uncalibrated: AUC=0.783 Brier=0.1480
    calibrated  : AUC=0.784 Brier=0.1505
    method='sigmoid': available   method='isotonic': available   method='temperature': available
```

**Reading.** Three separate version predictions, all exact. SKILL.md states: *"`CalibratedClassifierCV(cv='prefit')` was deprecated in 1.6 and removed in 1.8 (it now raises; wrap a fitted model in `sklearn.frozen.FrozenEstimator` instead); ... `method='temperature'` was added in 1.8."* Every clause verified on 1.9.1. This level of version currency is not common in this corpus.

The honest answer to the second half of the prompt is "not here". Isotonic on a 260-sample calibration fold left AUC unchanged and moved Brier slightly the wrong way — which the Skill itself predicts, since it says to use Platt for small calibration sets and isotonic for hundreds-plus points, and 260 is exactly the boundary.

**Scores:** Basic 39/40 · Specialized 56/60 · **Total 95/100** · **Assertions 4/5**

---

## Input 5 — Stress

**Prompt**
> The team wants to use the predicted probability as a triage score, not just rank compounds. Show me whether the probabilities mean anything and whether using them beats screening everything.

```
  calibration_curve strategy='uniform' : 10 bins, mean |gap| = 0.1036
  calibration_curve strategy='quantile': 10 bins, mean |gap| = 0.0596
  Brier (raw)=0.1480   Brier (calibrated)=0.1505
  AUPRC=0.554 against a prevalence baseline of 0.247

      pt     model  treat-all  treat-none  useful?
    0.20    0.1187     0.0590      0.0000  yes
    0.40    0.0528    -0.2546      0.0000  yes
    0.50    0.0444    -0.5056      0.0000  yes
    0.60    0.0250    -0.8819      0.0000  yes
    0.80   -0.0000    -2.7639      0.0000  no
```

**Reading.** Every tool the Skill names works from the text alone, including the net-benefit formula transcribed verbatim, which produces a coherent decision curve: the model beats both references from 0.2 to 0.6 and is worthless at 0.8. The binning advice is measurably right — equal-mass bins halve the apparent calibration gap under imbalance, supporting the Roelofs 2022 caution the Skill cites. And the AUPRC number is a good illustration of why the Skill insists on stating the baseline: 0.554 sounds mediocre until you know the floor is 0.247.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 6 — Scope Boundary

**Prompt**
> Only a quarter of our compounds are blockers. Let us SMOTE the training set to balance it — we get better numbers that way and the model is easier to explain.

```
  no resampling : AUC=0.783 Brier=0.1480 mean predicted p=0.247
  with SMOTE    : AUC=0.810 Brier=0.1421 mean predicted p=0.275
  observed prevalence in the test set = 0.247

  (the Skill's own shipped example, on synthetic data at 10% prevalence:)
  LogReg on oversampled data AUC: 0.903   Brier (raw): 0.110
  Mean predicted risk 0.24 vs true prevalence 0.10  <- risk inflated by oversampling
```

**Reading.** The Skill's position is that you should not resample for a probability model: no AUC gain, inflated minority-class risks. On its own worked example at 10% prevalence that is exactly right — predicted risk 0.24 against a true 0.10. On real hERG data at 24.7% prevalence it is not: AUC rose, Brier improved, and only the mean predicted probability drifted in the predicted direction (0.275 against 0.247).

The mechanism is real; the magnitude is a function of how severe the imbalance is, and the Skill states the warning unconditionally. The recommendation stands — even here the risks drifted upward — but a reader at moderate imbalance who runs this test will conclude the Skill is wrong, which it is not.

**Scores:** Basic 34/40 · Specialized 48/60 · **Total 82/100** · **Assertions 2/4**

---

## Input 7 — Adversarial

**Prompt**
> We only have 120 compounds with clean measurements. Just use leave-one-out and give me the AUC — everyone in the field does it.

```
  small set: (120, 1297), positives=28
  LOO + roc_auc -> UserWarning: Scoring failed. The score on this train-test
                   partition ... will be set to nan.
  pooled LOO OOF predictions scored once: AUC=0.662
  averaged per-fold 5-fold AUC (the Skill's prescription): 0.698 +/- 0.088
  pooled 5-fold OOF scored once: AUC=0.696  (difference from the fold average: -0.002)
  repeated 5x10 (the Skill's fix): 0.667 +/- 0.125, range [0.400, 0.889]
```

**Reading.** The Skill refuses and it is right to: LOO with AUC fails per fold and returns nan, because AUC is undefined on a size-1 test fold, exactly as the failure mode states. The prescribed repeated stratified k-fold works — and its output is the best argument in the whole Skill for reporting a spread rather than a number. On identical data, individual CV draws range from 0.400 to 0.889. Anyone quoting a single figure here is quoting a coin flip.

One caution of the Skill's did not bite: it warns that pooling out-of-fold predictions and scoring once is "not equivalent" to averaging fold scores for non-decomposable metrics. True in principle; the difference here was 0.002.

**Scores:** Basic 38/40 · Specialized 53/60 · **Total 91/100** · **Assertions 4/5**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-machine-learning-model-validation
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every snippet ran on real data; the shipped example runs end
                to end and reproduces both of its headline claims.
Contract     : PASS — frontmatter complete; all documented return shapes matched.
Determinism  : PASS — every example carries an explicit random_state, and the
                Skill's own point about CV variance is made with seeds set.
Security     : PASS — no eval/exec, no network, no credentials.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 12/12     Human Usability  :  8/8
Reliability            : 10/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 12/12
Agent Usability        : 15/16     Agent-Specific   : 19/20
Static Subtotal        : 95/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — all three sklearn drift predictions exact; every
                        citation real and correctly attached.
Practice Boundaries   : PASS — explicitly routes confirmatory-trial inference out
                        of scope ("the estimand is a treatment effect").
Methodological Ground : PASS — its central claim was demonstrated on zero-signal
                        data, not asserted.
Code Usability        : PASS — snippets and the shipped example all ran.

── STEP 8: Final Score ───────────────────────────
Static Score   : 95.0 × 40% = 38.0
Dynamic Score  : 91.3 × 60% = 54.8
FINAL SCORE    : 93 / 100
Floors         : Static ≥80 ✓ (95) · Execution ≥85 ✓ (91.3) · Layer 1 avg ≥32 ✓ (37.6)
                 Layer 2 avg ≥48 ✓ (53.7) · Assertion rate ≥90 % ✗ (80.6 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. Every failed assertion
                 is a magnitude or regime question — the Skill states effects
                 correctly but unconditionally. No method error was found, and this
                 is the highest-scoring Skill in the candidate.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P2] The leakage taxonomy's ordering implies a severity ranking it does not have** (input 2) — selection leakage produced +0.357 AUC on pure noise; scaler leakage −0.004. Fix: add a severity column.
- **[P2] The SMOTE warning gives no prevalence regime** (input 6) — dramatic at 10% prevalence, absent at 24.7%.
- **[P2] No guidance on when nested-versus-flat optimism is large** (input 1) — +0.009 measured against a "reviewer red flag" framing.
- **[P2] TRIPOD+AI reporting is required but never specified** — no template or field list for the report the Skill demands.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/nested_cv_biomarker.py`. It exists (65 lines), byte-compiles, imports cleanly (including `sklearn.frozen.FrozenEstimator`), and was executed in full during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**
