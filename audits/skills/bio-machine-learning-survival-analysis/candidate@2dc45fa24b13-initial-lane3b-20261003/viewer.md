> **Audit record for `bio-machine-learning-survival-analysis`**
> - Audited working candidate `2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/survival-analysis), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-survival-analysis

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 32 | 44 | 76 | 4/5 | ✅ COMPLETED |
| 2 | Variant A | 28 | 40 | 68 | 4/5 | ⚠️ COMPLETED |
| 3 | Edge | 34 | 49 | 83 | 3/4 | ✅ COMPLETED |
| 4 | Variant B | 35 | 50 | 85 | 4/5 | ✅ COMPLETED |
| 5 | Stress | 26 | 39 | 65 | 2/4 | ⚠️ COMPLETED |

**Execution average:** 75.4 / 100  
**Assertion pass rate:** 17 / 23  
**Static score:** 80 / 100  
**Final score:** 77 / 100 — ✅ Limited Release  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

| Surface | Classification | Evidence |
|---|---|---|
| scripts/cox_regression.py | executed (twice incl. in km_baseline_check.py) | logs/cox_regression.log, logs/km_baseline_check.log |
| scripts/competing_risks_cif.py | executed | logs/competing_risks_cif.log; hand check scripts/competing_hand_check.py |
| SKILL.md fit and evaluation blocks (Surv, Coxnet, RSF, Uno C, AUC(t), IBS) | executed verbatim on GBSG2 | scripts/gbsg2_skill_snippets.py |
| lifelines/sksurv concordance direction, Harrell vs Uno | executed | scripts/metric_directions.py, scripts/pgtn_and_censoring_checks.py |
| pycox DeepSurv (compute_baseline_hazards) and DeepHit | executed on CPU (prose-only in the Skill) | scripts/pycox_smoke.py |
| Dependency statements | checked against installed metadata | scripts/dependency_metadata.py |
| Fine-Gray, landmarking, calibration curves/ICI, nested CV, survival SVM/boosting | static-only (prose only, no code shipped, not labelled not executed: SA-005) | n/a |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated values or citations; the documented traps (lifelines C as 1-C, 1-KM versus Aalen-Johansen, Harrell versus Uno under censoring) reproduce against hand-computed and simulated truth.
  - practice_boundaries: PASS — Prediction-modelling guidance with TRIPOD+AI and external-validation requirements; no diagnostic or prescriptive medical conclusions.
  - methodological_ground: PASS — The shipped Kaplan-Meier baseline IBS is miscomputed (SA-001) and the default Coxnet prediction uses the least-penalized alpha (SA-002); both are P1 defects that overstate benefit but do not invert a conclusion: the models still beat the true KM baseline on GBSG2 (IBS 0.161 vs 0.178) and on the synthetic data (0.159 vs 0.236).
  - code_usability: PASS — Both scripts ran warning-free on CPU in seconds; the evaluation snippet needs t_horizon and y_train/y_test supplied (SA-003), which is a documentation gap rather than unrunnable code.

## Static categories

- functional_suitability: 8/12 — Prediction-versus-inference scope is well drawn and the metrics are used with correct direction; the KM baseline in the shipped script is wrong, the Coxnet default silently under-penalizes, and the RSF competing-risks claim does not hold for scikit-survival.
- reliability: 7/12 — Scripts have no input or time-range guards (times must lie inside test follow-up) and the evaluation snippet fails with NameError as written; the Common Errors table covers the main sksurv traps.
- performance_context: 7/8 — SKILL.md is 185 lines with failure modes in a reference file; the model taxonomy table is dense; both scripts run in seconds.
- agent_usability: 13/16 — Strong error prevention (C-index-only warning, IPCW training-y order, bool event) with accurate sign-trap guidance; code blocks rely on undefined names and mix full-data and split targets.
- human_usability: 7/8 — Description and usage-guide prompts match how users phrase prognostic-model requests; the boundary with clinical-biostatistics/survival-analysis is explicit.
- security: 11/12 — No credentials, network access or shell execution; synthetic data only in scripts.
- maintainability: 9/12 — Clean split into SKILL.md, failure-modes reference and two small scripts; metric logic is duplicated between snippet and script, which is how the baseline bug diverged from sksurv's own KM.
- agent_specific: 18/20 — Precise description with sibling-Skill hand-offs, good progressive disclosure, seeded scripts; many recommended methods (Fine-Gray, landmarking, calibration curves, nested CV) are prose only and not labelled as not executed.

## Detailed outputs

### Input 1 — Canonical: SKILL.md fit and evaluation blocks run verbatim on GBSG2 (686 patients), stratified held-out split

**Status:** COMPLETED — Fitting block ran; evaluation block fails as written (t_horizon undefined) and, once supplied, gives held-out Uno C 0.668, mean AUC(t) 0.728, IBS 0.161 against proper KM-only IBS 0.178; RSF Uno C 0.688.  
**Scores:** Basic 32/40 | Specialized 44/60 | Total 76/100

**Assertions:**

- PASS — Fitting block (Surv.from_arrays, Coxnet with baseline, RSF) runs on real data (ran on 480 training patients)
- FAIL — Evaluation block copy-runs as written once the split exists (NameError: t_horizon is undefined; y_train/y_test are also not built by any block)
- PASS — Held-out Uno C is in a plausible range for GBSG2 (0.668 Coxnet, 0.688 RSF)
- PASS — Model IBS beats the proper Kaplan-Meier-only IBS on held-out data (0.161 vs 0.178 from kaplan_meier_estimator)
- PASS — IPCW metrics receive the training y first and are evaluated on the held-out set (concordance_index_ipcw(y_train, y_test, ...) on the 30% test split)

### Input 2 — Variant A: scripts/cox_regression.py (synthetic, Coxnet vs RSF, Uno C, AUC(t), IBS vs KM baseline)

**Status:** COMPLETED — Runs warning-free in seconds with held-out split: Coxnet Uno C 0.775 / IBS 0.159, RSF 0.756 / 0.193. The printed KM baseline IBS 0.290 is wrong: the script averages (time > t) over event-only subjects; hand-checked KM and sksurv KM give IBS 0.236 (GBSG2: 0.263 vs 0.178).  
**Scores:** Basic 28/40 | Specialized 40/60 | Total 68/100

**Assertions:**

- PASS — Script runs end to end without warnings and is seeded (rc 0 under -W default; rng seed 0 and random_state set)
- PASS — Metrics are computed on a held-out split with the training y first (train_test_split 40% test; IPCW calls take y_tr first)
- PASS — Models recover the planted signal (Uno C well above 0.5) (0.775 and 0.756 with 5 of 40 features prognostic)
- FAIL — Printed Kaplan-Meier baseline IBS equals the IBS of a true KM curve (0.290 printed vs 0.236 with kaplan_meier_estimator; tiny hand table: formula 0.50 vs hand KM 0.80 at t=1)
- PASS — Risk-score direction is correct (higher = higher risk) for every metric call (model.predict used as risk; survival matrix used for IBS)

### Input 3 — Edge: Competing risks: scripts/competing_risks_cif.py plus tiny hand-computed table, 1-KM vs Aalen-Johansen

**Status:** COMPLETED — Script: 1-KM 0.517 vs CIF 0.250 with 63% competing events. Six-subject table: hand CIF1 and hand 1-KM equal lifelines at every time (t=6: CIF 0.5833 vs 1-KM 1.0000); lifelines warns that tied event times cannot be handled and jitters them, which the Skill does not mention.  
**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Assertions:**

- PASS — Script runs and shows 1-KM above the Aalen-Johansen CIF (0.517 vs 0.250)
- PASS — lifelines AalenJohansenFitter equals hand-computed CIF at every time on the tiny table (6 of 6 times match to 1e-6)
- PASS — 1-KM >= CIF at every time (the Skill's stated inequality) (0.1667 to 1.0000 versus 0.1667 to 0.5833)
- FAIL — Skill names a runnable implementation for each competing-risks method it recommends (cause-specific Cox, Fine-Gray, CIF-based Brier, Wolbers concordance) (Only the Aalen-Johansen demo is runnable; scikit-survival has no CIF or competing-risks metric (sksurv_competing_check.py))

### Input 4 — Variant B: Metric-direction traps and deep models: lifelines/sksurv C signs, Harrell vs Uno under censoring, pycox DeepSurv/DeepHit on CPU, dependency metadata

**Status:** COMPLETED — lifelines held-out C 0.337 with +partial hazard vs 0.663 with the negation (sum 1.0), matching sksurv; Harrell 0.734 vs Uno 0.727 vs truth 0.723 at 74% censoring, so the upward-bias claim holds; pycox DeepSurv C-td 0.615 and DeepHit 0.620 on CPU (cuda False). sksurv 0.28 needs scikit-learn <1.10 and pandas >=2.2 (no cap); lifelines 0.30.3 alone needs pandas <3.  
**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100

**Assertions:**

- PASS — lifelines concordance sign trap reproduces on held-out data (+ph 0.337, -ph 0.663; sksurv Harrell gives the mirror image)
- PASS — Harrell C is biased upward under heavy censoring and Uno is closer to the uncensored truth (truth 0.723, Harrell 0.734, Uno 0.727 at 74% censoring)
- PASS — pycox DeepSurv (compute_baseline_hazards then predict_surv_df) and DeepHit run on CPU (C-td 0.615 and 0.620, 30 epochs, torch cuda unavailable)
- PASS — Skill's pandas/scikit-learn constraint statements match installed package metadata (sksurv scikit-learn <1.10 >=1.9; lifelines pandas <3.0; sksurv itself runs on pandas 3.0.6)
- FAIL — Version note attributes the pandas cap and the bundled-script test environment precisely (Says to install both packages apart from a pandas 3 stack though only lifelines caps pandas, and says scripts ran against pycox though neither script imports it)

### Input 5 — Stress: p>>n penalized Cox: default predict() of the Skill's Coxnet configuration vs CV-selected alpha (n=150 train, p=1000, 5 prognostic)

**Status:** COMPLETED — predict() defaults to the smallest alpha on the 100-alpha path: 161 nonzero coefficients and held-out Uno C 0.708, versus 6 nonzero and 0.790 with CV-selected alpha (oracle 0.802). On GBSG2 the two agree (0.668 vs 0.669), so the defect only bites in p>>n, the Skill's stated use case.  
**Scores:** Basic 26/40 | Specialized 39/60 | Total 65/100

**Assertions:**

- FAIL — The documented configuration, used as shown, yields a sparse penalized signature in p>>n (161 of 1000 coefficients nonzero at the default (smallest) alpha)
- FAIL — Held-out Uno C of the default prediction is within 0.02 of a CV-tuned alpha (0.708 vs 0.790)
- PASS — A CV-selected alpha recovers near-oracle held-out discrimination (0.790 vs oracle 0.802 with 6 nonzero coefficients)
- PASS — Evaluation uses held-out data with no selection leakage (alpha chosen by 5-fold CV inside the training set only)

## Key strengths

- Sharp prediction-versus-inference scope boundary and a decision-grade evaluation set (Uno C with tau, AUC(t), IBS vs KM, calibration) that matches current practice
- Direction and ordering traps are accurate and reproduce: lifelines C needs the negated partial hazard, IPCW metrics take the training y first, 1-KM overestimates versus the Aalen-Johansen CIF (hand-verified)
- Dependency statements for scikit-survival 0.28 (scikit-learn <1.10) and lifelines 0.30 (pandas <3) match installed metadata; pycox DeepSurv/DeepHit execute on CPU
- Scripts are seeded, warning-free, evaluate on held-out data, and run in seconds

## Recommendations

- **[P1] SA-001 KM baseline IBS in cox_regression.py is miscomputed** (inputs [2, 1]): km_surv = np.mean(ttr[etr] > t) averages over event-only training subjects, dropping censored patients. The printed baseline IBS is 0.290 versus 0.236 from a true KM on the script's data (GBSG2 with the same formula: 0.263 vs 0.178), overstating the margin by which a model beats 'no covariates'. On a tiny table the formula gives 0.50 at t=1 where the hand KM is 0.80. Fix: Replace with kaplan_meier_estimator(y_tr['event'], y_tr['time']) evaluated at times, and add the same line to the SKILL.md IBS example. Changes runnable bytes (script) plus text.
- **[P1] SA-002 Coxnet snippet predicts at the least-penalized alpha** (inputs [5, 2, 1]): CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, fit_baseline_model=True) fits a 100-alpha path and predict() uses the smallest alpha. With n=150, p=1000 that kept 161 nonzero coefficients and gave held-out Uno C 0.708, against 0.790 (6 nonzero) for a CV-selected alpha. Nothing in the snippet or script selects alpha although the Skill demands tuning inside nested CV. Fix: Select alpha by cross-validation (GridSearchCV over alphas or an explicit alpha argument) in the snippet and cox_regression.py, and state which alpha predict and predict_survival_function use. Changes runnable bytes (script) plus text.
- **[P2] SA-003 Evaluation snippet is not copy-runnable** (inputs [1]): The evaluation block raises NameError on t_horizon; y_train, y_test, X_train, X_test are never built, and the fitting block creates y from the full df, which an agent may then use for training and testing. Fix: Add a split step defining X_train/X_test/y_train/y_test and t_horizon (for example the 90th percentile of training event times) and drop the full-data y. Text only.
- **[P2] SA-004 Competing-risks claims lack an implementation** (inputs [3]): The taxonomy says RSF handles competing risks ('Yes (per-cause CIF)'), but scikit-survival 0.28 has no CIF or competing-risks metric. Fine-Gray, cause-specific CIF Brier and Wolbers concordance have no named package or code. lifelines Aalen-Johansen warns about tied event times (jittered), which the Skill does not mention. Fix: Qualify the RSF row as not available in scikit-survival, name the R or Python implementation for each recommended competing-risks step, and note tie handling. Text only.
- **[P2] SA-005 Prose-only methods unlabelled; dependency note imprecise** (inputs [4]): Fine-Gray, landmarking, calibration curves with ICI/E50/E90, nested-CV selection and the pycox DeepSurv/DeepHit models are described without code or a statement that they were not run. The version note says to isolate both scikit-survival and lifelines from a pandas 3 stack (only lifelines caps pandas; scikit-survival runs on pandas 3.0.6) and says the bundled scripts ran against pycox 0.3 (neither imports it). Fix: Mark these methods 'described, not executed or bundled', attribute the pandas <3 cap to lifelines alone (competing_risks_cif.py only), and drop pycox from the scripts-tested list. Text only.

## Ordered finding ledger

Audited identity: `2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | SA-001 | P1 | open | [2, 1] | KM baseline IBS in cox_regression.py is miscomputed. Replace with kaplan_meier_estimator(y_tr['event'], y_tr['time']) evaluated at times, and add the same line to the SKILL.md IBS example. Changes runnable bytes (script) plus text. |
| 2 | SA-002 | P1 | open | [5, 2, 1] | Coxnet snippet predicts at the least-penalized alpha. Select alpha by cross-validation (GridSearchCV over alphas or an explicit alpha argument) in the snippet and cox_regression.py, and state which alpha predict and predict_survival_function use. Changes runnable bytes (script) plus text. |
| 3 | SA-003 | P2 | open | [1] | Evaluation snippet is not copy-runnable. Add a split step defining X_train/X_test/y_train/y_test and t_horizon (for example the 90th percentile of training event times) and drop the full-data y. Text only. |
| 4 | SA-004 | P2 | open | [3] | Competing-risks claims lack an implementation. Qualify the RSF row as not available in scikit-survival, name the R or Python implementation for each recommended competing-risks step, and note tie handling. Text only. |
| 5 | SA-005 | P2 | open | [4] | Prose-only methods unlabelled; dependency note imprecise. Mark these methods 'described, not executed or bundled', attribute the pandas <3 cap to lifelines alone (competing_risks_cif.py only), and drop pycox from the scripts-tested list. Text only. |

No audit-local repair was made; no Skill bytes changed.

## Score-floor note

The Production Ready/Limited Release per-layer floors in `scoring_rubric.md` section 5 are not all met (assertion pass rate 17/23, below 80 percent); the grade shown follows the score table that `audits:check` enforces. This is a diagnostic initial audit; no readiness is claimed.
