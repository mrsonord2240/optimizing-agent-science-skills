> **Audit record for `bio-machine-learning-omics-classifiers`**
> - Audited working candidate `1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/omics-classifiers), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-machine-learning-omics-classifiers

Generated: 2026-10-03  
Phase: bounded diagnostic initial audit (lane 3a)  
Exact candidate: `1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047` (files=5, bytes=29444)

## Outcome

Diagnostic score is **77/100**; the numeric band is Limited Release but two floors (execution average 73.9 < 75, assertion pass rate 62.1% < 80%) force a one-tier downgrade to **Beta Only**. Both veto gates pass. The SMOTE/leakage guidance and scripts are sound and reproduce. Four P1 findings are silent-failure risks in the examples: class weights that inflate predicted risk, a batch check that returns NaN or raises on most real designs, a scoring choice that removes the advertised sparsity, and isotonic calibration that collapses to 0/1 at the sample sizes the Skill targets. No safety assertion (fabrication, PHI, destructive action) failed. This is an initial diagnostic audit, not certification: route six open findings to `fix-scientific-skill`, then independently re-audit.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 34 | 48 | 82 | 3/4 | ✅ |
| 2 | Variant A | 28 | 40 | 68 | 2/4 | ⚠️ |
| 3 | Variant B | 36 | 53 | 89 | 4/4 | ✅ |
| 4 | Variant B | 33 | 47 | 80 | 3/4 | ✅ |
| 5 | Scope Boundary | 28 | 40 | 68 | 1/4 | ⚠️ |
| 6 | Edge | 24 | 30 | 54 | 1/4 | ❌ |
| 7 | Stress | 31 | 45 | 76 | 4/5 | ✅ |

**Execution average:** 73.9/100  
**Assertion pass rate:** 18/29 (62.1%)  
**Static score:** 81/100  
**Arithmetic:** 81 x 0.4 = 32.4; 73.9 x 0.6 = 44.3; 32.4 + 44.3 = 76.7 -> **77/100**  
**Grade:** Beta Only (score band Limited Release; one-tier downgrade for missed floors: execution_avg>=75(LR)/85(PR), assertion_rate>=80%(LR)/90%(PR))

## Veto gates

Skill veto: **PASS**. Research veto: **PASS**.

- T1 stability: PASS. Both bundled scripts and every SKILL.md snippet ran on sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2; no crash or dependency conflict.
- T2 contract: PASS. No structured API contract; documented shapes held (coef_ (1, p) with use_legacy_attributes=False; early_stopping_rounds accepted in the XGBClassifier constructor).
- T3 determinism: PASS. Both scripts are seeded and byte-identical across two runs; snippet fits use random_state.
- T4 security: PASS. No code execution of user strings, no network, no credentials, no destructive operations.
- M1 scientific integrity: PASS. Citations (Dudoit 2002, Statnikov 2008, Soneson 2014, Niculescu-Mizil 2005, van den Goorbergh 2022, Van Calster 2019, Chicco 2020) match their titles and venues; no invented numbers. The sklearn drift statements (cv=prefit removal, penalty= deprecation, scoring/use_legacy_attributes warnings) match installed 1.9.1 behaviour.
- M2 practice boundaries: PASS. Research-use modelling guidance; it defers unbiased evaluation to model-validation and states the probability is the product. No diagnostic or treatment claims.
- M3 methodological ground: PASS. SMOTE-before-split leakage reproduced (noise-label CV AUC 0.994 vs 0.549 in an imblearn Pipeline) and the "SMOTE gives no AUC gain / inflates risk" claim reproduced (mean AUC gain -0.006, mean predicted risk roughly doubled). The class_weight contradiction (OC-001) is an internal inconsistency in a recommendation, not a principled inversion of a conclusion; it is filed P1.
- M4 code usability: PASS. All snippets executed on Golub or synthetic data; the batch snippet fails by design limits (OC-002) rather than by syntax, so it is scored under reliability and the P1 ledger, not as non-runnable code.

## Inputs

### Input 1 (Canonical): Core Workflow snippet (StandardScaler + LogisticRegressionCV elastic net) on real Golub ALL/AML, 70/30 held-out split, 2,000 label-free high-variance probes

Status COMPLETED. Runs clean (no FutureWarning/ConvergenceWarning). Held-out AUC 1.0, Brier 0.0004, mean predicted risk 0.369 vs test prevalence 0.364. Chosen C=545, l1_ratio 0.9, 1,998 of 2,000 coefficients non-zero. Golub is near-separable: the AUC is an executability check, not evidence of skill.

Specialized dimensions: methodological_validity 15, code_executability 13, data_quality_control 7, reproducibility 8, security 5.

- PASS: Snippet runs on sklearn 1.9.1 with no FutureWarning or ConvergenceWarning (evidence/o1.json warnings {})
- PASS: Performance is measured on a split disjoint from tuning, scaler inside the Pipeline (train/test split; scaler fitted in pipe.fit)
- PASS: Quick-reference LogisticRegression(solver=saga, l1_ratio=0.5) runs unchanged (held-out AUC 1.0, no warnings)
- FAIL: "The L1 component yields a sparse signature" holds under the shipped scoring (1,998/2,000 non-zero under neg_log_loss; 83-160 under accuracy, 160-508 under roc_auc (evidence/o8.json))

### Input 2 (Variant A): class_weight=balanced vs probability calibration on a risk model (known linear generative model, 8% prevalence, 20,000-sample test sets, 3 seeds)

Status COMPLETED. Logistic: AUC identical with and without class_weight (0.70 vs 0.71) but mean predicted risk 0.119-0.133 vs prevalence 0.078-0.081, Brier 0.090-0.099 vs 0.073-0.077. RF balanced: mean risk 0.19-0.21, Brier 0.084-0.087 vs 0.071-0.074 unweighted.

Specialized dimensions: methodological_validity 8, code_executability 12, data_quality_control 7, reproducibility 8, security 5.

- FAIL: class_weight=balanced preserves calibrated risk for a probability model (predicted risk 1.5-2.6x the true prevalence (evidence/o2.json))
- FAIL: The imbalance advice is consistent with the XGBoost note that reweighting the prior distorts calibration (core snippet and decision tree recommend class_weight=balanced; XGBoost snippet omits scale_pos_weight for that reason)
- PASS: AUC is unaffected by class weighting (the Skill premise that discrimination and calibration are separable) (logistic AUC 0.709 vs 0.708)
- PASS: Estimates come from a large held-out set drawn from the same generative model (20,000 test samples per seed)

### Input 3 (Variant B): SMOTE placement and "no AUC gain" claim (imblearn Pipeline vs resample-before-CV; known linear model, 8 draws)

Status COMPLETED. Pure-noise labels: SMOTE-before-CV AUC 0.994 vs 0.549 inside ImbPipeline. Held-out: mean AUC gain from SMOTE -0.006 over 8 draws, mean predicted risk 0.063-0.116 -> 0.129-0.216 (about 2x).

Specialized dimensions: methodological_validity 17, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Resampling before the split leaks (near-perfect CV AUC on noise) (0.994)
- PASS: imblearn Pipeline placement removes the leak (0.549, chance)
- PASS: SMOTE gives no AUC gain on held-out data in this regime (mean -0.006)
- PASS: SMOTE inflates predicted minority risk (mean predicted risk roughly doubled)

### Input 4 (Variant B): Probability Calibration snippet (FrozenEstimator + isotonic) on Golub (tiny calibration fold) and on a 1,500-sample synthetic set

Status COMPLETED. API runs clean. Golub, n_cal=20: isotonic outputs only two distinct probabilities (exactly 0 or 1), test Brier 0.000 (raw RF 0.073); sigmoid gives 22 distinct values, Brier 0.010. Synthetic n_cal=600: Brier raw 0.187, isotonic 0.168, sigmoid 0.166.

Specialized dimensions: methodological_validity 15, code_executability 13, data_quality_control 6, reproducibility 8, security 5.

- PASS: FrozenEstimator snippet runs with no warnings on sklearn 1.9.1 (evidence/o4.json warnings {})
- PASS: The calibration set is disjoint from the training and test sets (three-way split)
- FAIL: Recalibrated probabilities are usable at the tens-of-samples scale the Skill targets (isotonic at n_cal=20 returns exactly 0 or 1 for every test sample (silent Brier 0.000))
- PASS: Calibration improves Brier when the calibration set is adequate (0.187 -> 0.166-0.168)

### Input 5 (Scope Boundary): XGBoost snippet (constructor early stopping, eval_set) on Golub, 5 splits

Status COMPLETED. Accepted by xgboost 3.4.1 with no warnings. With a 15-sample validation set the metric saturates immediately: best_iteration 0-18 (seed 3: 0), validation aucpr 1.0 every split, test AUC 1.0, 0.969, 1.0, 0.830, 1.0.

Specialized dimensions: methodological_validity 12, code_executability 10, data_quality_control 6, reproducibility 7, security 5.

- PASS: early_stopping_rounds and eval_metric in the constructor run on xgboost 3.4.1 (no TypeError or warning)
- FAIL: The snippet or text separates the early-stopping validation set from the performance estimate (only eval_set=[(X_val, y_val)] is shown; validation aucpr 1.0 vs test AUC as low as 0.83)
- FAIL: Early stopping is meaningful at the tiny n the Skill cites as its reason (metric saturates at iteration 0-18 on 15 validation samples)
- FAIL: The bundled script exercises the early-stopping recommendation (rf_xgboost_classifier.py uses fixed n_estimators=300, no early stopping)

### Input 6 (Edge): Batch-shortcut snippet verbatim with 6, 3 and 2 synthetic batches, label confounded with batch (no public multi-batch set staged)

Status PARTIAL. Batch-predictability step: NaN for 6 and 3 batches (roc_auc rejects multiclass, FitFailedWarning), 1.00 for 2 batches. StratifiedGroupKFold(n_splits=5) works for 6 batches (AUC 0.53) but raises ValueError for 3 and 2; it is not leave-one-batch-out. LeaveOneGroupOut AUC 0.47 / 0.34 / 0.52 vs random-split 0.82 / 0.76 / 0.79.

Specialized dimensions: methodological_validity 8, code_executability 5, data_quality_control 6, reproducibility 6, security 5.

- FAIL: The batch-predictability step returns a number for more than two batches (NaN for 6 and 3 batches)
- FAIL: The batch-aware split runs with n_splits=5 for the batch counts typical of a study (ValueError for 3 and 2 batches)
- FAIL: The step described as leave-one-batch-out (SKILL.md comment, usage-guide, failure-modes) is leave-one-batch-out (StratifiedGroupKFold(5) is group K-fold)
- PASS: The label-vs-batch association test flags the confounded design (chi-square p 3e-20, 3e-9, 2e-8)

### Input 7 (Stress): Both bundled scripts twice under -W default; correctness of their narrative

Status COMPLETED. logistic_regression.py: elastic net keeps 101/500; zero-signal batch data CV AUC 0.83, batch predictability 1.00; no batch-aware split is run although the docstring says one exposes it. rf_xgboost_classifier.py: EN AUC 0.749 / Brier 0.203, RF 0.545 / 0.249, XGB 0.625 / 0.247; captions "compressed toward 0.5" and "pushed toward extremes" are static strings. Both byte-identical across runs, no warnings.

Specialized dimensions: methodological_validity 13, code_executability 12, data_quality_control 6, reproducibility 9, security 5.

- PASS: Both scripts exit 0 with no warnings under -W default (evidence/*.err empty)
- PASS: Outputs are byte-identical across two runs (cmp identical)
- PASS: Performance numbers come from a held-out split (rf_xgboost_classifier.py scores X_te)
- FAIL: Docstrings and captions match what the script computes, and agree with SKILL.md (no batch-aware split despite docstring; fixed direction captions vs SKILL.md "direction depends on learner"; usage-guide tip repeats the fixed directions)
- PASS: The script shows the Skill headline finding (batch artifact) through its own metrics (CV AUC 0.83 on zero-signal data, batch predictability 1.00)

## Finding ledger (fixer order)

| ID | Sev | Fix touches | Summary |
|---|---|---|---|
| OC-001 | P1 | SKILL.md snippet + prose, usage-guide.md, references/failure-modes.md; scripts/ unchanged | Balanced class weights inflate predicted risk 1.5-2.6x for the models the Skill calls calibrated. |
| OC-002 | P1 | SKILL.md snippet; text in failure-modes.md/usage-guide.md already says LOBO; scripts/ unchanged (script can optionally add the LOBO step, see OC-006) | NaN / ValueError on 2-6 batch designs; step labelled LOBO is not. |
| OC-003 | P1 | SKILL.md snippet comment + prose; scripts/ unchanged | "Sparse signature" claim fails on Golub: 99.9% of coefficients non-zero under the shipped scoring. |
| OC-004 | P1 | SKILL.md snippet + one sentence; scripts/ unchanged | Isotonic at n_cal=20 returns only 0/1 probabilities with a silent Brier of 0. |
| OC-005 | P2 | SKILL.md prose + snippet comment; optional scripts/rf_xgboost_classifier.py (runnable bytes) | Validation set doubles as score; saturates on 15 samples. |
| OC-006 | P2 | scripts/logistic_regression.py and scripts/rf_xgboost_classifier.py (runnable bytes) + usage-guide.md | Docstring promises an unrun batch-aware split; static direction captions. |

## Lead verification

- **neg_log_loss / use_legacy_attributes=False**: behaviourally different from the origin default (accuracy). Correct per sklearn (1.9.1 warns for both old defaults and names neg_log_loss as the 1.11 default), stated in Version Compatibility here, and consistent between SKILL.md and rf_xgboost_classifier.py (logistic_regression.py uses plain LogisticRegression). It removes sparsity on Golub (OC-003).
- **Selection, scaling, SMOTE and tuning inside the fold**: SMOTE reproduced both ways; scaler is in every Pipeline; the Core Workflow scores on a held-out split. No bundled script or snippet reports an estimate from the data it was tuned on, apart from the early-stopping validation score (OC-005).
- **Tooling Golub AUC 1.000**: not used as evidence. Golub is near-separable (held-out AUC 1.0 for most settings), so Golub inputs here test executability, behavioural properties (sparsity, calibration extremes) and API; discrimination claims use synthetic data with a known generative model.
- **Batch snippets**: no public multi-batch expression set is staged; synthetic batch labels were used. A tooling-delta pass could stage one, but the OC-002 failures are API-level and do not depend on it.

## Coverage and evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6. Inputs: Golub 1999 ALL/AML from staging `public-data` (label-free variance filter to 2,000 probes) and generator-defined synthetic sets in `scripts/run_cases.py`. Executed: elastic-net Core Workflow, quick-reference LogisticRegression, XGBoost constructor early stopping, SMOTE pipeline, calibration (FrozenEstimator), batch snippet, both bundled scripts. Static-only: LightGBM, CatBoost, SVM, DLDA, ColumnTransformer and encoding bullets (prose, no code in the Skill). No blocked surface. Scripts: `scripts/run_cases.py` (cases o1-o8), builders. No audit-local repair; candidate bytes unmodified (identity re-verified after execution).
