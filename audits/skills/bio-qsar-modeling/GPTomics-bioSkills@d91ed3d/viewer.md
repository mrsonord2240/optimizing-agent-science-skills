> **Audit record for `bio-qsar-modeling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/qsar-modeling) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-qsar-modeling

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/qsar-modeling`
Category: 3 — Data Analysis · Execution Mode: D (Hybrid — Python snippets plus the chemprop 2.x CLI) · Complexity: Complex → N = 7
Environment: shared venv (RDKit 2026.03.6, scikit-learn 1.9.1); `tools\chemprop-venv` (chemprop 2.3.1, torch 2.14.0+cpu); `tools\mapie08-venv` (mapie 0.8.6, scikit-learn 1.5.2).
Real data: ChEMBL hERG CHEMBL240, 3,224 unique compounds with mean-aggregated pChEMBL.
Inputs executed: **7 / 7**
Code: `run/inputs_1_4_6_7.py`, `run/input2_chemprop_prep.py`, `run/input3_conformal.py`, `run/input5_calibration_imbalance.py`. Output: `run/*.out`, `run/chemprop_train.out`, `run/chemprop_predict.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 54 | 91 | 5/5 | ✅ |
| 2 | Variant A | yes | 33 | 46 | 79 | 3/5 | ✅ |
| 3 | Edge | yes | 36 | 52 | 88 | 3/5 | ✅ |
| 4 | Variant B | yes | 34 | 49 | 83 | 3/4 | ✅ |
| 5 | Stress | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 35 | 50 | 85 | 3/4 | ✅ |
| 7 | Adversarial | yes | 37 | 54 | 91 | 3/4 | ✅ |

**Execution Average: 87.1 / 100**
**Assertion Pass Rate: 24/31 (77.4 %)**

---

## Input 1 — Canonical

**Prompt**
> We have 3,224 hERG pChEMBL measurements and we want a model our chemists will actually use on new designs. Build the fingerprint baseline on a scaffold split, and put an applicability-domain gate on the report — I do not want a number next to a compound we have no business predicting.

```
  scaffold-balanced train=2579 val=322 test=323
  scaffolds shared between train and test: 0  (train 1005, test 323)
  overall  R2=0.507  MAE=0.560
  AD diagnostics: mean max-Tanimoto=0.605  kNN5=0.536  ensemble sd=0.653

  does each AD diagnostic track error? (test set split at its median)
    max Tanimoto    inside MAE=0.527 R2= 0.637  |  outside MAE=0.595 R2= 0.243
    kNN5 Tanimoto   inside MAE=0.537 R2= 0.612  |  outside MAE=0.584 R2= 0.295
    ensemble sd     inside MAE=0.444 R2= 0.410  |  outside MAE=0.677 R2= 0.502
    Tanimoto gate 0.4: 264/323 inside (82%), inside MAE 0.537, outside 0.665
```

**Reading.** The AD gate earns its place: predictions on the similar half explain 64% of variance against 24% on the dissimilar half. The ensemble-variance row is the interesting one — it orders MAE correctly but *inverts* on R², which is precisely why the Skill insists that ensemble disagreement is "one useful uncertainty diagnostic, not a formally defined applicability domain or calibrated coverage guarantee".

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100** · **Assertions 5/5 PASS**

---

## Input 2 — Variant A

**Prompt**
> Train the chemprop model from your CLI block on this data as a blocker/non-blocker classification, then predict on a fresh set with the ensemble uncertainty. And tell me how to make it reproducible — the last run moved every time.

**Training — the SKILL.md block, verbatim:**

```
chemprop train --data-path chemprop_herg.csv --task-type classification \
  --save-dir chemprop_model --molecule-featurizers rdkit_2d \
  --num-replicates 2 --ensemble-size 2 --epochs 5 --batch-size 128 \
  --split scaffold_balanced --split-sizes 0.8 0.1 0.1 --metric roc

  -> test/roc: 0.743 | 0.735 | 0.776 | 0.780   (4 models, exit 0)
```

**Prediction — the SKILL.md block, verbatim:**

```
chemprop predict --test-path cp_test.csv --model-paths <4 ckpts> \
  --uncertainty-method ensemble --preds-path cp_preds.csv

  RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x300 and 517x300)
```

**With `--molecule-featurizers rdkit_2d` added:**

```
  EXIT=0 — pred_0, pred_0_unc written
  per-model AUCs: [0.844, 0.842, 0.814, 0.787]
  correlation between the two members of replicate_0: 0.98658
  pred_0_unc is the ensemble VARIANCE (corr with var = 1.0, mean |unc - var| = 0.0)

chemprop train ... --seed 42
  -> chemprop: error: unrecognized arguments: --seed 42
```

**Reading.** The training block is completely current — every flag validated against 2.3.1 and a real model trained. The prediction block is not usable with it: 517 = 300 hidden + 217 `rdkit_2d` descriptors, and `predict` supplies only 300 because the featurizer flag is not repeated. The failure surfaces as a bare tensor-shape error naming nothing the user can act on. Two smaller findings: `--seed 42` from the Common Errors table does not exist in chemprop 2.x (the flags are `--data-seed` and `--pytorch-seed`), and the reported `pred_*_unc` is the ensemble **variance** while SKILL.md instructs the reader to treat "ensemble standard deviation" as the diagnostic — a squared-units mismatch for anyone setting a threshold. The Skill's own "ensemble variance always small / members insufficiently diverse" warning is directly visible: the two members of replicate 0 correlate at 0.987.

**Scores:** Basic 33/40 · Specialized 46/60 (Code Executability 9/15) · **Total 79/100** · **Assertions 3/5**

---

## Input 3 — Edge

**Prompt**
> Ensemble spread is not good enough for the safety team — they want calibrated intervals. Use the conformal route in your skill and tell me whether the 90% intervals actually cover 90%.

```
=== tools\mapie08-venv (mapie 0.8.6, sklearn 1.5.2 — inside the Skill's stated bound) ===
  SKILL.md snippet RAN. intervals shape=(323, 2, 1)
  empirical coverage at alpha=0.1 -> 0.851  (target 0.90)
  mean interval width = 1.943 log units  (label range 4.00-9.85)
  narrow-interval half:  n=162 MAE=0.496 coverage=0.907
  wide-interval half:    n=161 MAE=0.625 coverage=0.795
  alpha=0.05: target 0.95, empirical 0.916, width 2.475
  alpha=0.2 : target 0.80, empirical 0.706, width 1.395

=== shared venv (mapie 1.5.0 — outside the bound) ===
  SKILL.md snippet FAILED: ImportError: cannot import name 'MapieRegressor' from 'mapie.regression'
```

**Reading.** Two things, and they cut in opposite directions.

The version bounding is *correct and load-bearing*. The Skill pins "MAPIE >=0.8,<1.0 for the `MapieRegressor` example" and cites the 0.8.6 documentation. Inside that window the snippet runs untouched; outside it, the class no longer exists. Most version headers in this corpus are decorative; this one is doing real work.

The answer to the prompt is no. Coverage undershoots at every level — 0.851, 0.916, 0.706 against 0.90, 0.95, 0.80. The Skill's own AD table explains why: conformal gives "finite-sample marginal coverage **under exchangeability**", and a scaffold split deliberately makes calibration and test sets non-exchangeable. (The tooling pass measured 0.94 coverage for the same snippet on a random split, which corroborates the diagnosis.) But the Skill never connects its own two recommendations, so a reader who follows both the scaffold-split section and the conformal section gets silent undercoverage and no warning.

The interval width is itself a usable domain signal — narrow half coverage 0.907, wide half 0.795 — which is the practical takeaway the section could have made.

**Scores:** Basic 36/40 · Specialized 52/60 · **Total 88/100** · **Assertions 3/5**

---

## Input 4 — Variant B

**Prompt**
> You list four applicability-domain families. We used similarity last time; try leverage and Mahalanobis on the same fingerprints and tell me which one to standardise on.

```
  non-constant training bits: 2020/2048; n_train=2579
  leverage h = x(X'X)^-1 x'  -> mean=120.235 min=0.225 max=782.168
  SANITY: leverage must lie in [0,1]; 319/323 values exceed 1
     -> X'X is numerically singular on 2020 sparse binary bits and the direct
        inverse returns garbage WITHOUT raising
  condition number of X'X = 1.140e+08
  leverage-based gate anyway: inside MAE=0.571  outside MAE=0.550   (no signal)

  Mahalanobis on 50 PCA components: mean=6.12
     inside MAE=0.557  outside MAE=0.564                            (no signal)
```

**Reading.** The answer to the prompt is "neither — stay with similarity", and the Skill's own table anticipated both failures in its Con column ("linear assumptions" for leverage, "high-dim instability" for Mahalanobis). What it does not say is that these two rows are simply inapplicable to the representation it recommends everywhere else in the document. Leverage is the dangerous one: it returns hat values up to 782 — impossible for a hat-matrix diagonal — without raising anything, so a pipeline would carry them forward as an applicability domain.

**Scores:** Basic 34/40 · Specialized 49/60 · **Total 83/100** · **Assertions 3/4**

---

## Input 5 — Stress

**Prompt**
> Turn this into a blocker/non-blocker classifier. It is 73% positive so I expect the usual mess — show me what the default does to the minority class, and give me probabilities the team can actually threshold on.

```
  n=3224  positives=2351 (72.9%)  fit=2064 calibration=515 test=323
  (calibration split carved from TRAIN, never from test)

  default loss             ACC=0.697 AUC=0.688 AP=0.822 F1=0.809
                           minority(neg) precision=0.586 recall=0.165
  class_weight='balanced'  ACC=0.675 AUC=0.705 AP=0.828 F1=0.764
                           minority(neg) precision=0.490 recall=0.466
  majority-class baseline accuracy = 0.681

  uncalibrated  Brier=0.1981  AUC=0.688  5-bin calibration gap=0.0554
  isotonic      Brier=0.1968  AUC=0.696  5-bin calibration gap=0.0405
  Platt         Brier=0.1994  AUC=0.688  5-bin calibration gap=0.0598

  calibrator fit ON THE TEST SET: Brier=0.1863 — better than the honest 0.1968,
  and meaningless.
```

**Reading.** Three documented behaviours in one run. The imbalance symptom is textbook — 0.697 accuracy is *worse* than always predicting the majority class, while minority recall sits at 0.165. The prescribed class weighting nearly triples minority recall. Isotonic calibration moves Brier and the calibration gap while leaving AUC essentially alone, which is exactly the Skill's point that `--metric roc` evaluates ranking and does not calibrate. And the final block reproduces the Common Errors warning by deliberately doing the wrong thing: fitting the calibrator on test looks better and means nothing.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 6 — Scope Boundary

**Prompt**
> The med-chem team has a new series that looks nothing like the training set. Just score them — we do not have time for the applicability-domain ceremony.

```
  50 most novel chemotypes   max-Tanimoto 0.288  MAE=0.667  R2= 0.015  sd(y)=0.853  ens.sd=0.706
  50 closest analogues       max-Tanimoto 0.821  MAE=0.659  R2= 0.621  sd(y)=1.313  ens.sd=0.594
  ratio of MAE (novel / familiar) = 1.01x
```

**Reading — and a correction to our own first pass.** The Skill's "Missing AD assessment" failure mode gives the symptom as *"Confident predictions but actual values different"*. On this dataset that specific symptom **did not reproduce**: mean absolute error on the novel series is 0.667 against 0.659 on the familiar one, a ratio of 1.01. The model is not visibly worse by the metric a user would naturally watch.

What collapses is explained variance — R² 0.015 against 0.621 — because the novel subset also has a narrower label spread (sd 0.853 against 1.313). The model is producing near-constant, near-average predictions and getting ordinary-looking absolute errors for it, while ranking the series essentially at random. That is arguably a worse outcome than a visibly large error, and the Skill's stated symptom would not catch it. The AD signal itself is present and usable before prediction (max-Tanimoto 0.288, higher ensemble spread), so the Skill's instruction to predefine a diagnostic is the right one — its description of what going wrong looks like is not.

(The first version of this script printed a conclusion asserting the failure mode "is reproduced quantitatively". That line was wrong and was corrected in `run/inputs_1_4_6_7.py` before the recorded run.)

**Scores:** Basic 35/40 · Specialized 50/60 · **Total 85/100** · **Assertions 3/4**

---

## Input 7 — Adversarial

**Prompt**
> Our random-split R² is 0.55 and the business wants to deploy. You keep pushing scaffold splits — quantify what that costs me, because if it is a rounding error I am shipping.

```
  random split    n_train=2901 n_test=323  R2=0.554  MAE=0.478  RMSE=0.644
  scaffold split  n_train=2579 n_test=323  R2=0.507  MAE=0.560  RMSE=0.730
  random split shares 152 scaffolds between train and test  (scaffold split: 0)
```

**Reading.** The leakage is real and directly visible — 152 chemotypes appear on both sides of the random split — and the model is 17% worse in MAE once they are separated. The Skill is right about the direction and right to refuse to call the gap a universal memorisation measure ("split-specific sensitivity"). But its failure-mode symptom says performance "drops substantially", and a 0.047 drop in R² is not what most readers will picture when they read "substantially". The honest answer to this prompt is that the cost is modest on this dataset and the leakage is nonetheless disqualifying for a model meant to score new chemotypes — a distinction the Skill's own framing supports but its wording obscures.

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100** · **Assertions 3/4**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-qsar-modeling
Category       : 3 — Data Analysis
Execution Mode : D (Hybrid: Python + chemprop 2.x CLI)
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — the sklearn paths ran on 3,224 compounds without failure and
                chemprop trained 4 models to completion. The prediction crash is a
                documentation defect, raised as P1, not instability: the same command
                with one flag added succeeds.
Contract     : PASS — frontmatter complete; documented return shapes matched,
                including MapieRegressor's (n, 2, 1) interval array.
Determinism  : PASS — the sklearn paths are seeded and reproducible. Noted as P2:
                the reproducibility flag the Skill gives for chemprop does not exist,
                so its own advice cannot be followed.
Security     : PASS — no eval/exec, no network, no credentials; CLI examples are
                fixed strings.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12     Human Usability  :  8/8
Reliability            : 10/12     Security         : 11/12
Performance/Context    :  7/8      Maintainability  : 11/12
Agent Usability        : 14/16     Agent-Specific   : 19/20
Static Subtotal        : 90/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — repeatedly declines to overclaim where overclaiming
                        is standard, and every refusal was borne out by a run.
Practice Boundaries   : PASS — assay-level model building only.
Methodological Ground : PASS — leakage, imbalance and calibration-overfitting all
                        reproduced. One unflagged interaction (scaffold split vs
                        conformal exchangeability) is raised as P1.
Code Usability        : PASS — the conformal snippet runs inside its own stated
                        version bound and fails outside it; chemprop trains with
                        every documented flag.

── STEP 8: Final Score ───────────────────────────
Static Score   : 90.0 × 40% = 36.0
Dynamic Score  : 87.1 × 60% = 52.3
FINAL SCORE    : 88 / 100
Floors         : Static ≥80 ✓ (90) · Execution ≥85 ✓ (87.1) · Layer 1 avg ≥32 ✓ (35.7)
                 Layer 2 avg ≥48 ✓ (51.4) · Assertion rate ≥90 % ✗ (77.4 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. The three P1s are all
                 seams between sections that are individually correct — train versus
                 predict, split design versus conformal validity, AD table versus
                 recommended representation.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] The chemprop prediction block crashes against a model trained by the training block** (input 2) — `--molecule-featurizers rdkit_2d` must be repeated at predict time; the failure is a bare 517-vs-300 tensor-shape error.
- **[P1] Leverage is tabulated as an AD method but is numerically meaningless on fingerprints** (input 4) — hat values to 782, silently, from a matrix with condition number 1.1e8. Fix: an applicability column on the AD table plus a `0 <= h <= 1` assertion.
- **[P1] The recommended scaffold split breaks the exchangeability the conformal section requires** (input 3) — coverage 0.851/0.916/0.706 against 0.90/0.95/0.80. Fix: cross-reference the two sections and require empirical coverage to be reported.
- **[P2] `--seed 42` does not exist in chemprop 2.x** (input 2) — use `--data-seed` and `--pytorch-seed`. Same error in `admet-prediction`.
- **[P2] The conformal snippet's cost is not signposted** (input 3) — over 50 minutes as written; set `n_jobs=-1` and note that `cv=5` fits the base model six times.
- **[P2] The missing-AD failure mode names a symptom that does not appear in absolute error** (input 6) — MAE ratio 1.01 while R² falls from 0.621 to 0.015. Fix: restate the symptom in terms of explained variance and rank ordering.
- **[P2] `pred_*_unc` is the ensemble variance, not the standard deviation** (input 2) — verified exactly (corr 1.0 with variance, mean absolute difference 0.0); the Skill instructs the reader to treat it as a standard deviation.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/chemprop_pipeline.sh`. It exists, and every flag it contains was validated against chemprop 2.3.1 and exercised in a real training run. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**
