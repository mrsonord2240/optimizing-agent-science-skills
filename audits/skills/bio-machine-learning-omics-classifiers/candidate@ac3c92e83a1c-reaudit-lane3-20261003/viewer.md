> **Audit record for `bio-machine-learning-omics-classifiers`**
> - Audited working candidate `ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/omics-classifiers), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-machine-learning-omics-classifiers

Generated: 2026-10-03  
Phase: final re-audit, full mode (lane 3a-2), independent of the fixer and the initial auditor  
Exact candidate: `ac3c92e83a1c6946b20bc052a5443f1ab99e8e97c2dd902360b5a465a263732c` (files=7, bytes=48515; `tools/skill_preflight.py --offline` PASS before and after)

## Outcome

**Not candidate-ready.** Score 85/100 (static 85, execution average 85.6, Layer 1 average 34.3/40, Layer 2 average 51.3/60) falls in the Production Ready band, but the assertion pass rate is 29/33 = 87.9%, below the 90% floor, so the grade drops one tier to **Limited Release** and the readiness gate is not met. Both veto gates pass and there is no open P0 or P1. All six corrected findings (OC-001 to OC-006) hold under independent retest. Four of the five remaining findings are text-only P2s; one (the bundled XGBoost demo) needs a few script lines. Route to `fix-scientific-skill`, then a delta-mode re-audit.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 35 | 52 | 87 | 5/5 | ✅ |
| 2 | Variant A | 33 | 50 | 83 | 4/5 | ✅ |
| 3 | Variant B | 36 | 53 | 89 | 4/4 | ✅ |
| 4 | Edge | 35 | 52 | 87 | 5/5 | ✅ |
| 5 | Scope Boundary | 33 | 49 | 82 | 3/4 | ✅ |
| 6 | Adversarial | 37 | 55 | 92 | 5/5 | ✅ |
| 7 | Stress | 31 | 48 | 79 | 3/5 | ❌ |

**Execution average:** 85.6/100  
**Assertion pass rate:** 29/33 (87.9%)  
**Static score:** 85/100  
**Arithmetic:** 85 x 0.4 = 34.0; 85.6 x 0.6 = 51.4; sum -> **85/100**  
**Grade:** Limited Release (score band Production Ready; one-tier downgrade for the assertion floor)

## Veto gates

Skill veto: **PASS**. Research veto: **PASS**.

- scientific_integrity: PASS. Citations match titles and venues; every measured number in SKILL.md traced to a rerun (calibration_check.py, early-stopping, Golub scoring, 1-SE, batch self-test) or an independent generator; no invented values.
- practice_boundaries: PASS. Research-use modelling guidance; defers unbiased evaluation to model-validation; no diagnostic or treatment claims.
- methodological_ground: PASS. No selection, scaling, SMOTE, calibration or tuning sees held-out data (by construction and by a test-split perturbation test with negative controls). The RF ranking overclaim is a scoped generalization error, filed P2, and does not invert the recommendation.
- code_usability: PASS. All four scripts and seven SKILL.md blocks run under -W error::FutureWarning on Golub and synthetic data; the cwd-relative import fails loudly off the Skill directory (P2).
- Skill veto T1-T4: PASS. All scripts and blocks run under `-W error::FutureWarning`; outputs reproduce across reruns apart from saga noise (non-zero counts differ by one); no network, credentials or execution of user strings.

## Finding verdicts

| ID | Verdict | Measured |
|---|---|---|
| OC-001 | resolved | Guidance consistent across SKILL.md, usage-guide, failure-modes, decision tree and hyperparameter table. Own generator: logistic 0.99x unweighted, 3.24x balanced, 0.98x balanced + recalibrated; RF 1.11x vs 2.43x. Skill's setup: 0.988 / 4.193 / 1.106. T-1: each number is attributed to its setup (4.2x to `calibration_check.py`, 2.6x/1.16x to the 300-feature RF run); the 1.60x logistic figure of the latter is not stated. Residual: OC-007. |
| OC-002 | resolved | Real leave-one-batch-out (matches a manual loop to 0.0). Batch-only signal: per-batch 0.48 / 0.48 / 0.52 vs random-split 0.72 / 0.66 / 0.81 for 2 / 3 / 6 batches; real signal 0.83 / 0.82 / 0.89. One-class held-out batch shows NaN with a note; one-class training fold is skipped and listed. SD of a single estimate 0.09-0.10 at every batch count. |
| OC-003 | resolved | `neg_log_loss` pinned; dense elastic net 1,004 / 1,199 / 2,000 of 2,000 (own splits), no sparsity claim; 1-SE recomputed independently, identical C on 3/3 splits, training data only; 51 / 80 / 166 non-zero, AUC 1.00. |
| OC-004 | resolved | Rule boundaries 999 / 1000-99 sigmoid, 1000-100 isotonic. The shipped `recalibrate()` warns on a degenerate isotonic (2 distinct values, n=1000); the rule holds on own RF and logistic bases (isotonic wins at most 17% of repeats to n=1,000). Prose scopes the derivation to RF/XGBoost. T-4 confirmed: demo 2 prints `warnings raised: 0` for the sigmoid branch; the warning branch ran only in this audit and the staged check. |
| OC-005 | resolved | Three-way split; replacing the test split with garbage leaves XGBoost early stopping, 1-SE and calibration outputs identical, with negative controls that change. Early-stopping numbers identical to the fix run. Residual: OC-010 (demo). |
| OC-006 | resolved | Docstrings, captions and printed values match what runs (0.54 / 0.70 / 0.45 per-batch; spread line labelled). |

## New findings (all P2)

| ID | Fix | Summary |
|---|---|---|
| OC-007 | text-only | 'Reweighting changes scale, not ranking' and 'no AUC gain' are false for random forest: AUC 0.776 -> 0.812 with balanced weights in 6/6 seeds (staged run 0.648 -> 0.720). True for logistic. |
| OC-008 | text-only | T-2/T-3: snippets use `sys.path.insert(0, 'scripts')`; `ModuleNotFoundError` from any other cwd; the text does not say where to run. Scripts themselves run from any cwd. |
| OC-009 | text-only | LightGBM, CatBoost, linear SVM, DLDA are prose only with no 'not executed' label. |
| OC-010 | script (few lines) | T-3 of the tooling note: `rf_xgboost_classifier.py` XGBoost stops at round 0 of 2000 on 63 validation samples (AUC 0.597, spread [0.46, 0.49]); the printed note explains it but the row is a null model and cannot show XGBoost calibration direction. |
| OC-011 | text-only | usage-guide omits the 100-rarer-class condition; demo 2 'warnings raised: 0' unexplained; noise caution names 2-3 batches though SD is as large at 6; recalibration at n=20 can lose to raw probabilities (0.2089 / 0.2356 vs 0.1985); saga snippets set no `random_state`. |

## Inputs

### Input 1 (Canonical): Core Workflow fit and lasso + 1-SE snippet on real Golub ALL/AML (own splits 20-22, 2,000 high-variance probes), FutureWarning as error

Status COMPLETED. Dense elastic net (neg_log_loss) kept 1,004 / 1,199 / 2,000 of 2,000 coefficients, held-out AUC 1.00 on all three splits (prose: 1,059-2,000). Lasso + 1-SE kept 51 / 80 / 166, AUC 1.00 (prose: 45 / 142 / 60 on other splits). scores_ shape (5 folds, 1, 20 Cs), Cs_ ascending; a hand-recomputed fold score matches scores_ to 1e-3 and an independent 1-SE expression picks the identical C on all three splits. Golub is near-separable, so this shows sparsity and API behaviour, not discrimination.

Specialized dimensions: methodological_validity 17, code_executability 14, data_quality_control 8, reproducibility 8, security 5.

- PASS: Core Workflow and 1-SE snippets run under -W error::FutureWarning with no warning (ra_scoring.py seeds 20-22 and SKILL.md blocks 0-1 via run_snippets.py on Golub and synthetic: rc 0)
- PASS: The 'dense fit' statement matches behaviour under the pinned neg_log_loss scoring (1,004 / 1,199 / 2,000 non-zero of 2,000; prose range 1,059-2,000 on other splits; sparse-signature claim no longer made for the elastic net)
- PASS: The 1-SE rule is implemented correctly (smallest C whose CV mean is within one SE of the best mean) (independent expression gives the same C on 3/3 splits (1.6238, 1.6238, 4.2813); hand-fit fold score -0.4985 vs scores_ -0.4994)
- PASS: The 1-SE selection and the dense fit see training data only (CV inside X_train (50 rows); X_te (22 rows) first used for AUC; test-split perturbation leaves c_1se unchanged (input 5))
- PASS: The lasso + 1-SE snippet delivers a short list at unchanged discrimination (51 / 80 / 166 of 2,000 (2.6-8.3%), AUC 1.00 on all three; larger than the prose 45 / 142 / 60 on seed 22, same order)

### Input 2 (Variant A): OC-001 re-test: class_weight vs calibration on an independent generator (own coefficients, about 9% prevalence, 6 seeds, 30,000-sample test sets)

Status COMPLETED. Logistic mean predicted / observed prevalence: unweighted 0.99x, class_weight='balanced' 3.24x (Brier 0.143 vs 0.069), balanced then recalibrate() on 1,000 held-out samples (about 89 events) 0.98x (Brier 0.070). RF: 1.11x unweighted, 2.43x balanced. The Skill's 4.2x reproduces only in its own calibration_check.py setup (1,500 train, 50 features, 8%): 0.988 / 4.193 / 1.106, Brier 0.070 / 0.177 / 0.072, slopes 0.925 / 0.723 / 0.879. Prose attributes 4.2x to that setup and 2.6x/1.16x to the 300-feature, 500-train RF setup (staged rerun 2.58 / 1.16; the logistic arm of that setup gives 1.60x, not stated in the prose). New: RF AUC is higher with balanced weights in 6/6 seeds (0.812 vs 0.776), contradicting 'reweighting changes the probability scale, not the ranking' and 'no AUC gain' for the model the Skill recommends for nonlinear signal.

Specialized dimensions: methodological_validity 14, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Unweighted logistic stays calibrated at low prevalence (0.99x observed prevalence, 6 seeds)
- PASS: class_weight='balanced' inflates predicted risk as the Skill states (3.24x logistic and 2.43x RF on an independent generator; 4.19x in the Skill's own setup)
- PASS: Recalibration on held-out data restores the probability scale (0.98x (Brier 0.070) vs 3.24x (0.143); Skill's setup 1.106x)
- PASS: SKILL.md, usage-guide, failure-modes and decision tree agree on imbalance handling and attribute each number to its setup (grep: class_weight/scale_pos_weight only as hard-label-only or as prohibited; 4.2x tied to calibration_check.py, 2.6x/1.16x to the 300-feature RF run)
- FAIL: 'Reweighting changes the probability scale, not the ranking' (and 'for no AUC gain') holds for random forest (RF AUC balanced 0.812 vs plain 0.776 in 6/6 seeds here; the Skill's own staged RF run shows 0.720 vs 0.648; holds for logistic (0.820 vs 0.826))

### Input 3 (Variant B): SMOTE placement and effect (imblearn Pipeline vs resample-before-CV; own generator, noise labels and 8 held-out draws)

Status COMPLETED. Noise labels (12% positive): resample-before-CV AUC 0.780 vs 0.379 inside ImbPipeline (leak shown; the below-0.5 value is small-sample CV noise on 36 positives). Held-out, known logistic model at about 8%: mean AUC gain from SMOTE -0.007 (range -0.013..+0.006); mean predicted / observed prevalence 1.04x plain vs 4.75x SMOTE. The SKILL.md imblearn block runs in the 7-block harness.

Specialized dimensions: methodological_validity 17, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Resampling before the split leaks (inflated CV AUC on noise labels) (0.780 vs 0.379 in the Pipeline)
- PASS: The imblearn Pipeline placement removes the leak (AUC at or below chance inside the Pipeline)
- PASS: SMOTE gives no held-out AUC gain for the logistic baseline (mean -0.007 over 8 draws)
- PASS: SMOTE inflates predicted minority risk (4.75x vs 1.04x of observed prevalence)

### Input 4 (Edge): OC-004 re-test: recalibrate() branch boundaries, degenerate-calibrator warning through the shipped code, isotonic-vs-sigmoid rule on own RF and logistic bases

Status COMPLETED. Branches: n=999 sigmoid, n=1000 with 99 rarer-class events sigmoid, n=1000 with 100 isotonic. A separable base at n=1000 (isotonic) returns 2 distinct probabilities, test Brier 0.0001, and the shipped recalibrate() warns ('Calibrator is degenerate (2 distinct probabilities ...)'); the same data shape at n=20 takes sigmoid (6 distinct, no warning). Own generator, 25 repeats, isotonic beat sigmoid in at most 17% of repeats up to n=1,000 for RF and logistic bases at 10% and 30% prevalence (n=3,000: RF 4-24%, logistic 0%); mean gap at n=1,000 +0.0012..+0.0017 (isotonic worse), consistent with the Skill's 'within 0.002 for RF'. calibration_check.py demo 2 prints 'warnings raised: 0' for the sigmoid branch; the warning path is not exercised by any shipped demo, only by this run. At n=20, sigmoid Brier 0.2089 and isotonic 0.2356 are both worse than the raw RF 0.1985 in the shipped demo; the prose does not say recalibration at tens of samples can lose to raw probabilities.

Specialized dimensions: methodological_validity 16, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Isotonic is chosen only at >= 1,000 calibration samples and >= 100 rarer-class events (n=999 sigmoid; 1000/99 sigmoid; 1000/100 isotonic (ra_recal.py))
- PASS: A degenerate calibrator (<= 3 distinct probabilities) triggers the warning through the shipped code path (separable n=1000 isotonic: 2 distinct values, warning raised under default and 'always' filters (ra_recal.py case a))
- PASS: The Skill states the rule was derived on RF and XGBoost bases only ('Measured on RF and XGBoost bases (50 features, 10% and 50% prevalence, 40 repeats ...)')
- PASS: The sigmoid-default rule reproduces on an independent RF generator (isotonic wins 0.00-0.17 of repeats for n <= 1,000)
- PASS: The rule also holds for a base it was not derived on (logistic regression) (isotonic wins 0.00-0.17 up to n=1,000; mean gap +0.0013..+0.0017 at n=1,000)

### Input 5 (Scope Boundary): OC-005 re-test: three-way split, test-split perturbation, early-stopping numbers, and the bundled XGBoost demo

Status COMPLETED. Test split replaced by garbage X and flipped y after splitting: XGBoost best_iteration and predictions, lasso 1-SE C and calibrated outputs identical; negative controls (perturb validation: best_iteration 209 -> 4; perturb calibration set: outputs change) show the check can detect dependence. Rerun of the staged early-stopping experiment is identical to the fix run: 15 validation samples median best round 4.5, validation AUCPR 0.827, test AUC 0.607; 60 samples 0.717 / 0.649; Golub with 15: validation AUCPR 1.0, best round 4-18; CV-chosen rounds test AUC 0.691. The bundled demo's XGBoost stops at round 0 of 2000 on 63 validation samples (test AUC 0.597, Brier 0.248, probabilities in [0.46, 0.49]); a printed note explains this, but the row is a null model and cannot show the XGBoost calibration direction the script says it reveals.

Specialized dimensions: methodological_validity 15, code_executability 13, data_quality_control 7, reproducibility 9, security 5.

- PASS: Train, early-stopping validation and test are disjoint; the reported score is on the test split only (row-level disjointness check; snippet comments say report on (X_te, y_te))
- PASS: Selection, early stopping, 1-SE and calibration are unaffected by the held-out test split (perturbation test identical; negative controls change)
- PASS: The early-stopping and CV-rounds numbers quoted in SKILL.md reproduce (0.827/0.607, 0.717/0.649, Golub best round 4-18, CV rounds 0.691: identical to the fix run)
- FAIL: The bundled rf_xgboost_classifier.py XGBoost row is a meaningful model that shows its probability behaviour (best round 0 of 2000, AUC 0.597, spread [0.46, 0.49]; the SKILL.md small-n advice (CV-chosen rounds) is not what the script does)

### Input 6 (Adversarial): OC-002 re-test: planted batch effect with known answer (2, 3 and 6 batches, 20 replicates each) plus edge cases

Status COMPLETED. Batch-only signal (label tracks batch, features carry only a batch offset): random-split AUC 0.72 / 0.66 / 0.81, leave-one-batch-out mean per-batch AUC 0.48 / 0.48 / 0.52 (collapses to chance), pooled 0.22 / 0.52 / 0.73. Real signal only: per-batch 0.83 / 0.82 / 0.89 (survives). Both: 0.76 / 0.78 / 0.88. Across-replicate SD of the per-batch mean is 0.09-0.10 at 2, 3 and 6 batches in batch-only designs (range 0.28-0.75). leave_one_batch_out matches an independent loop to 0.0 on 6 batches. One-class held-out batch: NaN with 'AUC undefined: one class in this batch'; training batches all one class: 'skipped: training batches hold one class', pooled NaN; string/pandas inputs work; a single-sample batch makes batch_predictability raise a clear ValueError; a single batch raises from LeaveOneGroupOut.

Specialized dimensions: methodological_validity 18, code_executability 14, data_quality_control 9, reproducibility 9, security 5.

- PASS: Leave-one-batch-out per-batch AUCs equal an independent manual loop (max abs difference 0.0 over 6 batches)
- PASS: Signal that exists only through batch collapses under leave-one-batch-out (mean per-batch 0.48 / 0.48 / 0.52 vs random-split 0.72 / 0.66 / 0.81)
- PASS: Real within-batch signal survives leave-one-batch-out (0.83 / 0.82 / 0.89)
- PASS: One-class held-out batches and one-class training folds are reported, not silently averaged (NaN with note; 'skipped' row; pooled NaN when nothing predicted)
- PASS: The Skill is honest about estimate noise and about pooled AUC rewarding a batch-level shift (prose reads the per-batch mean and warns about pooling and 2-3-batch noise; pooled 0.73 vs per-batch 0.52 at 6 batches confirms; measured SD is as large at 6 batches (0.09), which the prose does not say)

### Input 7 (Stress): Every shipped script and every SKILL.md block as instructed under -W error::FutureWarning; run-location and prose-only-surface checks

Status PARTIAL. batch_checks.py 3 s, logistic_regression.py 3 s, rf_xgboost_classifier.py 22 s, calibration_check.py 53 s: rc 0, empty stderr; 7/7 SKILL.md blocks OK on Golub and synthetic. Printed values match the prose (0.82/0.88/0.86 random-split, 0.54/0.70/0.45 per-batch, 0.988/4.193/1.106, Brier 0.070/0.177/0.072). Scripts run from any cwd, but the SKILL.md batch and calibration blocks use sys.path.insert(0, 'scripts') and raise ModuleNotFoundError from any other cwd; the text does not say to run from the Skill directory. LightGBM, CatBoost, linear SVM and DLDA appear only in a table and prose with no code and no 'not executed' label.

Specialized dimensions: methodological_validity 15, code_executability 12, data_quality_control 7, reproducibility 9, security 5.

- PASS: All four scripts exit 0 with no warning under -W error::FutureWarning (script_rc.txt: rc 0 each; .err files empty)
- PASS: All seven SKILL.md python blocks run as written on real (Golub) and synthetic data (run_snippets.py golub / synthetic: 7/7 OK, no warnings)
- PASS: Numbers printed by the scripts match the numbers and captions in SKILL.md and docstrings (batch, calibration and logistic outputs match the cited values)
- FAIL: SKILL.md snippets run when the agent's working directory is not the Skill directory, or the text says where to run them (from /tmp: ModuleNotFoundError: No module named 'batch_checks'; text only says '# the Skill's scripts/ directory')
- FAIL: Algorithms with no code (LightGBM, CatBoost, SVM, DLDA) are labelled as not executed or untested (no such label in SKILL.md or usage-guide)

## Coverage and evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` (native Windows venv, Python 3.12.13, scikit-learn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 re-hashed unchanged; `pip freeze` identical to the staged freeze; TOOLS.md sha256 481d8543... unchanged. Inputs: Golub 1999 ALL/AML from staging `public-data` (OpenML 1104), synthetic generators with planted truth (own coefficients, not the Skill's `draw()`), and the staged claim generators for the early-stopping rerun and the 7-block snippet harness. No input was added and no environment changed.

Executed: all four scripts; all seven SKILL.md python blocks on Golub and synthetic data; independent calibration, batch, Golub scoring/1-SE, recalibration branch, isotonic-rule, SMOTE and perturbation scripts (published under `scripts/`). Staged generators were rerun only for early stopping (identical to the fix run); the 273 s, 421 s and 579 s generators were not rerun, replaced by own generators for the same claims. Static-only: LightGBM, CatBoost, linear SVM, DLDA (no code, no input; OC-009). Not covered: no public multi-batch expression cohort exists in staging, so batch checks use synthetic designs with planted truth; the sample-size rule and small-n early-stopping advice rest on synthetic generators; Golub is near-separable and only shows executability and sparsity.

Preflight warning accepted: no Skill-root LICENSE (frontmatter `license: MIT` plus repository licence evidence).

Raw run output is kept in the audit run directory (`evidence/`), not published; the commands and scripts are under `scripts/` (`ra_run_all.sh` runs the shipped surfaces).
