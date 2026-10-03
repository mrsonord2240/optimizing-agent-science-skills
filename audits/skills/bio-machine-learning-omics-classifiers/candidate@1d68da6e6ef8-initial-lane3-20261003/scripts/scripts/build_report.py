"""Builds report.json / viewer.md / source-identity.json / finding-ledger.md for the omics-classifiers audit.
Run from the run directory:  python scripts/build_report.py
Evidence files referenced below are in evidence/ (outputs of scripts/run_cases.py o1..o8 and the two bundled scripts).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lib import build

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = 'F:/OpenScience/wt/ml-lane3-normalize/skills/bio-machine-learning-omics-classifiers'
ROOT = 'F:/optimizing-agent-science-skills'

D = lambda m, c, q, r, s: dict(methodological_validity=m, code_executability=c, data_quality_control=q, reproducibility=r, security=s)

spec = dict(
    skill_id='bio-machine-learning-omics-classifiers',
    identity='1d68da6e6ef86650cbb2f70c8fda804b7bbe5a9792b3c72bf0bf5d4c0173f047',
    origin_path='machine-learning/omics-classifiers',
    tools_md='F:\\OpenScience\\audits\\bio-machine-learning-omics-classifiers\\TOOLS.md',
    tools_sha='7f4a80ba28ac74641a3bf4ad8d7f5d8cfa2cb7664f7d8320debadc4daea1db73',
    description=('Builds diagnostic and prognostic classifiers on omics feature matrices with regularized logistic regression, random forest, '
                 'and gradient-boosted trees, handling the p>>n regime, batch shortcut learning, class imbalance, and probability calibration.'),
    complexity='Moderate',
    veto=dict(
        skill_gate='PASS', research_gate='PASS',
        t1=('PASS', 'Both bundled scripts and every SKILL.md snippet ran on sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2; no crash or dependency conflict.'),
        t2=('PASS', 'No structured API contract; documented shapes held (coef_ (1, p) with use_legacy_attributes=False; early_stopping_rounds accepted in the XGBClassifier constructor).'),
        t3=('PASS', 'Both scripts are seeded and byte-identical across two runs; snippet fits use random_state.'),
        t4=('PASS', 'No code execution of user strings, no network, no credentials, no destructive operations.'),
        m1=('PASS', 'Citations (Dudoit 2002, Statnikov 2008, Soneson 2014, Niculescu-Mizil 2005, van den Goorbergh 2022, Van Calster 2019, Chicco 2020) match their titles and venues; no invented numbers. The sklearn drift statements (cv=prefit removal, penalty= deprecation, scoring/use_legacy_attributes warnings) match installed 1.9.1 behaviour.'),
        m2=('PASS', 'Research-use modelling guidance; it defers unbiased evaluation to model-validation and states the probability is the product. No diagnostic or treatment claims.'),
        m3=('PASS', 'SMOTE-before-split leakage reproduced (noise-label CV AUC 0.994 vs 0.549 in an imblearn Pipeline) and the "SMOTE gives no AUC gain / inflates risk" claim reproduced (mean AUC gain -0.006, mean predicted risk roughly doubled). The class_weight contradiction (OC-001) is an internal inconsistency in a recommendation, not a principled inversion of a conclusion; it is filed P1.'),
        m4=('PASS', 'All snippets executed on Golub or synthetic data; the batch snippet fails by design limits (OC-002) rather than by syntax, so it is scored under reliability and the P1 ledger, not as non-runnable code.'),
    ),
    static={
        'functional_suitability': (8, 'Linear/RF/XGBoost, batch, imbalance and calibration are covered with accurate sklearn 1.9 / xgboost 3 API drift notes. Gaps: LightGBM, CatBoost, SVM, DLDA are table prose only; the headline claim "elastic net yields a sparse signature" fails under the shipped scoring on real data (OC-003); the batch snippet breaks for most real designs (OC-002).'),
        'reliability': (8, 'Failure-modes reference is good. Silent failures: batch-predictability returns NaN for >2 batches, group CV raises for <5 batches, isotonic collapses to 0/1 at tiny n (OC-002, OC-004).'),
        'performance_context': (7, 'Progressive disclosure is correct (failure-modes routed, scripts referenced); SKILL.md 222 lines.'),
        'agent_usability': (11, 'Clear cold start and strong decision tables. Inconsistent guidance: class_weight=balanced recommended while the XGBoost note says reweighting the prior distorts calibration; usage-guide states fixed RF/boosting probability directions that SKILL.md says are learner-dependent (OC-001, OC-006).'),
        'human_usability': (7, 'Prompts match how users ask (suspiciously perfect AUC, imbalance, calibration); strict inputs are appropriate.'),
        'security': (11, 'No credentials or network; array inputs only.'),
        'maintainability': (10, 'Clean separation of SKILL.md, failure-modes, scripts and usage-guide; the snippets have no tests and script captions are static (OC-006).'),
        'agent_specific': (19, 'Precise trigger and explicit routing to model-validation, biomarker-discovery and survival-analysis; good out-of-scope signals.'),
    },
    inputs=[
        dict(type='Canonical', label='Core Workflow snippet (StandardScaler + LogisticRegressionCV elastic net) on real Golub ALL/AML, 70/30 held-out split, 2,000 label-free high-variance probes', status='COMPLETED', basic=34,
             note='Runs clean (no FutureWarning/ConvergenceWarning). Held-out AUC 1.0, Brier 0.0004, mean predicted risk 0.369 vs test prevalence 0.364. Chosen C=545, l1_ratio 0.9, 1,998 of 2,000 coefficients non-zero. Golub is near-separable: the AUC is an executability check, not evidence of skill.',
             specialized=D(15, 13, 7, 8, 5),
             assertions=[
                 ('Snippet runs on sklearn 1.9.1 with no FutureWarning or ConvergenceWarning', 'PASS', 'evidence/o1.json warnings {}'),
                 ('Performance is measured on a split disjoint from tuning, scaler inside the Pipeline', 'PASS', 'train/test split; scaler fitted in pipe.fit'),
                 ('Quick-reference LogisticRegression(solver=saga, l1_ratio=0.5) runs unchanged', 'PASS', 'held-out AUC 1.0, no warnings'),
                 ('"The L1 component yields a sparse signature" holds under the shipped scoring', 'FAIL', '1,998/2,000 non-zero under neg_log_loss; 83-160 under accuracy, 160-508 under roc_auc (evidence/o8.json)'),
             ]),
        dict(type='Variant A', label='class_weight=balanced vs probability calibration on a risk model (known linear generative model, 8% prevalence, 20,000-sample test sets, 3 seeds)', status='COMPLETED', basic=28,
             note='Logistic: AUC identical with and without class_weight (0.70 vs 0.71) but mean predicted risk 0.119-0.133 vs prevalence 0.078-0.081, Brier 0.090-0.099 vs 0.073-0.077. RF balanced: mean risk 0.19-0.21, Brier 0.084-0.087 vs 0.071-0.074 unweighted.',
             specialized=D(8, 12, 7, 8, 5),
             assertions=[
                 ('class_weight=balanced preserves calibrated risk for a probability model', 'FAIL', 'predicted risk 1.5-2.6x the true prevalence (evidence/o2.json)'),
                 ('The imbalance advice is consistent with the XGBoost note that reweighting the prior distorts calibration', 'FAIL', 'core snippet and decision tree recommend class_weight=balanced; XGBoost snippet omits scale_pos_weight for that reason'),
                 ('AUC is unaffected by class weighting (the Skill premise that discrimination and calibration are separable)', 'PASS', 'logistic AUC 0.709 vs 0.708'),
                 ('Estimates come from a large held-out set drawn from the same generative model', 'PASS', '20,000 test samples per seed'),
             ]),
        dict(type='Variant B', label='SMOTE placement and "no AUC gain" claim (imblearn Pipeline vs resample-before-CV; known linear model, 8 draws)', status='COMPLETED', basic=36,
             note='Pure-noise labels: SMOTE-before-CV AUC 0.994 vs 0.549 inside ImbPipeline. Held-out: mean AUC gain from SMOTE -0.006 over 8 draws, mean predicted risk 0.063-0.116 -> 0.129-0.216 (about 2x).',
             specialized=D(17, 14, 8, 9, 5),
             assertions=[
                 ('Resampling before the split leaks (near-perfect CV AUC on noise)', 'PASS', '0.994'),
                 ('imblearn Pipeline placement removes the leak', 'PASS', '0.549, chance'),
                 ('SMOTE gives no AUC gain on held-out data in this regime', 'PASS', 'mean -0.006'),
                 ('SMOTE inflates predicted minority risk', 'PASS', 'mean predicted risk roughly doubled'),
             ]),
        dict(type='Variant B', label='Probability Calibration snippet (FrozenEstimator + isotonic) on Golub (tiny calibration fold) and on a 1,500-sample synthetic set', status='COMPLETED', basic=33,
             note='API runs clean. Golub, n_cal=20: isotonic outputs only two distinct probabilities (exactly 0 or 1), test Brier 0.000 (raw RF 0.073); sigmoid gives 22 distinct values, Brier 0.010. Synthetic n_cal=600: Brier raw 0.187, isotonic 0.168, sigmoid 0.166.',
             specialized=D(15, 13, 6, 8, 5),
             assertions=[
                 ('FrozenEstimator snippet runs with no warnings on sklearn 1.9.1', 'PASS', 'evidence/o4.json warnings {}'),
                 ('The calibration set is disjoint from the training and test sets', 'PASS', 'three-way split'),
                 ('Recalibrated probabilities are usable at the tens-of-samples scale the Skill targets', 'FAIL', 'isotonic at n_cal=20 returns exactly 0 or 1 for every test sample (silent Brier 0.000)'),
                 ('Calibration improves Brier when the calibration set is adequate', 'PASS', '0.187 -> 0.166-0.168'),
             ]),
        dict(type='Scope Boundary', label='XGBoost snippet (constructor early stopping, eval_set) on Golub, 5 splits', status='COMPLETED', basic=28,
             note='Accepted by xgboost 3.4.1 with no warnings. With a 15-sample validation set the metric saturates immediately: best_iteration 0-18 (seed 3: 0), validation aucpr 1.0 every split, test AUC 1.0, 0.969, 1.0, 0.830, 1.0.',
             specialized=D(12, 10, 6, 7, 5),
             assertions=[
                 ('early_stopping_rounds and eval_metric in the constructor run on xgboost 3.4.1', 'PASS', 'no TypeError or warning'),
                 ('The snippet or text separates the early-stopping validation set from the performance estimate', 'FAIL', 'only eval_set=[(X_val, y_val)] is shown; validation aucpr 1.0 vs test AUC as low as 0.83'),
                 ('Early stopping is meaningful at the tiny n the Skill cites as its reason', 'FAIL', 'metric saturates at iteration 0-18 on 15 validation samples'),
                 ('The bundled script exercises the early-stopping recommendation', 'FAIL', 'rf_xgboost_classifier.py uses fixed n_estimators=300, no early stopping'),
             ]),
        dict(type='Edge', label='Batch-shortcut snippet verbatim with 6, 3 and 2 synthetic batches, label confounded with batch (no public multi-batch set staged)', status='PARTIAL', basic=24,
             note='Batch-predictability step: NaN for 6 and 3 batches (roc_auc rejects multiclass, FitFailedWarning), 1.00 for 2 batches. StratifiedGroupKFold(n_splits=5) works for 6 batches (AUC 0.53) but raises ValueError for 3 and 2; it is not leave-one-batch-out. LeaveOneGroupOut AUC 0.47 / 0.34 / 0.52 vs random-split 0.82 / 0.76 / 0.79.',
             specialized=D(8, 5, 6, 6, 5),
             assertions=[
                 ('The batch-predictability step returns a number for more than two batches', 'FAIL', 'NaN for 6 and 3 batches'),
                 ('The batch-aware split runs with n_splits=5 for the batch counts typical of a study', 'FAIL', 'ValueError for 3 and 2 batches'),
                 ('The step described as leave-one-batch-out (SKILL.md comment, usage-guide, failure-modes) is leave-one-batch-out', 'FAIL', 'StratifiedGroupKFold(5) is group K-fold'),
                 ('The label-vs-batch association test flags the confounded design', 'PASS', 'chi-square p 3e-20, 3e-9, 2e-8'),
             ]),
        dict(type='Stress', label='Both bundled scripts twice under -W default; correctness of their narrative', status='COMPLETED', basic=31,
             note='logistic_regression.py: elastic net keeps 101/500; zero-signal batch data CV AUC 0.83, batch predictability 1.00; no batch-aware split is run although the docstring says one exposes it. rf_xgboost_classifier.py: EN AUC 0.749 / Brier 0.203, RF 0.545 / 0.249, XGB 0.625 / 0.247; captions "compressed toward 0.5" and "pushed toward extremes" are static strings. Both byte-identical across runs, no warnings.',
             specialized=D(13, 12, 6, 9, 5),
             assertions=[
                 ('Both scripts exit 0 with no warnings under -W default', 'PASS', 'evidence/*.err empty'),
                 ('Outputs are byte-identical across two runs', 'PASS', 'cmp identical'),
                 ('Performance numbers come from a held-out split', 'PASS', 'rf_xgboost_classifier.py scores X_te'),
                 ('Docstrings and captions match what the script computes, and agree with SKILL.md', 'FAIL', 'no batch-aware split despite docstring; fixed direction captions vs SKILL.md "direction depends on learner"; usage-guide tip repeats the fixed directions'),
                 ('The script shows the Skill headline finding (batch artifact) through its own metrics', 'PASS', 'CV AUC 0.83 on zero-signal data, batch predictability 1.00'),
             ]),
    ],
    strengths=[
        'SMOTE leakage and "no AUC gain, inflated risk" claims reproduce exactly; the imblearn Pipeline placement is correct.',
        'Both bundled scripts are seeded, warning-free and byte-identical; the batch-artifact demonstration reaches CV AUC 0.83 on zero-signal data with batch predictability 1.00.',
        'sklearn / xgboost drift notes (penalty=, cv=prefit, constructor early stopping, scoring/use_legacy_attributes warnings) match installed behaviour, and the normalizer scoring change is explained here, unlike in the sibling Skill.',
        'Routing to model-validation, biomarker-discovery and survival-analysis keeps scope tight; failure modes are specific and cited.',
    ],
    findings=[
        dict(id='OC-001', priority='P1', title='class_weight=balanced contradicts the Skill calibration stance', observed_in=[2],
             problem='The Core Workflow, decision tree and usage-guide recommend class_weight=balanced for imbalance and call the model well-calibrated, while the XGBoost note says reweighting the prior distorts calibration. At 8% prevalence balanced weighting leaves AUC unchanged but doubles mean predicted risk (logistic 0.12-0.13, RF 0.19-0.21 vs 0.08) and worsens Brier (0.090-0.099 vs 0.073-0.077).',
             root_cause='class_weight reweights the training prior exactly as resampling does, but the Skill treats it as safe and only resampling as harmful.',
             fix='Drop class_weight=balanced from the risk-model snippet and decision tree (keep it only for hard-label problems), state that class weights shift predicted risk like SMOTE, and point to threshold tuning or post-hoc recalibration; align the usage-guide and failure-modes text.',
             evidence='evidence/o2.json', touches='SKILL.md snippet + prose, usage-guide.md, references/failure-modes.md; scripts/ unchanged',
             summary='Balanced class weights inflate predicted risk 1.5-2.6x for the models the Skill calls calibrated.'),
        dict(id='OC-002', priority='P1', title='Batch-shortcut snippet fails for most real designs and is not LOBO', observed_in=[6],
             problem='roc_auc scoring on the batch label gives NaN for more than two batches; StratifiedGroupKFold(n_splits=5) raises for fewer than five batches and is group K-fold, not the leave-one-batch-out that the code comment, failure-modes and usage-guide name. On confounded synthetic data LeaveOneGroupOut gives 0.47/0.34/0.52 against random-split 0.82/0.76/0.79.',
             root_cause='Snippet was written for two balanced batches and a roc_auc metric and never exercised on multi-batch data.',
             fix='Use scoring="roc_auc_ovr" (or balanced accuracy) for the batch-prediction step and LeaveOneGroupOut (guarding groups with a single class) for the honest estimate; state the minimum number of batches and what to do with two.',
             evidence='evidence/o6.json', touches='SKILL.md snippet; text in failure-modes.md/usage-guide.md already says LOBO; scripts/ unchanged (script can optionally add the LOBO step, see OC-006)',
             summary='NaN / ValueError on 2-6 batch designs; step labelled LOBO is not.'),
        dict(id='OC-003', priority='P1', title='neg_log_loss scoring removes sparsity on near-separable omics data', observed_in=[1],
             problem='The Core Workflow claims the L1 component yields a sparse signature, but under the normalizer scoring=neg_log_loss CV selects C=545-10,000 on Golub and keeps 1,998/2,000 (seed 0), 2,000 (seed 1), 1,068 (seed 2) coefficients non-zero; accuracy gives 83-160 and roc_auc 160-508. Held-out AUC is the same. The change is defensible (proper score, sklearn 1.11 default) and consistent between SKILL.md and rf_xgboost_classifier.py, but the sparsity consequence is unstated.',
             root_cause='Log loss rewards near-unregularised fits when classes separate, so CV drifts to the top of the C grid; the Skill treats the normalizer choice as behaviour-neutral.',
             fix='State that the scoring metric governs sparsity, show the effect, and recommend roc_auc (or a one-standard-error rule / capped Cs) when a small signature is the goal; keep neg_log_loss when calibrated probabilities are the goal.',
             evidence='evidence/o1.json, evidence/o8.json; origin bytes F:\\OpenScience\\bioSkills-Improved\\machine-learning\\omics-classifiers', touches='SKILL.md snippet comment + prose; scripts/ unchanged',
             summary='"Sparse signature" claim fails on Golub: 99.9% of coefficients non-zero under the shipped scoring.'),
        dict(id='OC-004', priority='P1', title='Isotonic calibration hard-wired for tiny n collapses to 0/1', observed_in=[4],
             problem='The calibration snippet uses method="isotonic" in a Skill aimed at tens-to-hundreds of samples. With 20 calibration samples (Golub) isotonic returns exactly 0 or 1 for every test sample and a test Brier of 0.000, while sigmoid gives 22 distinct probabilities and Brier 0.010. At 600 calibration samples both help (0.187 -> 0.166-0.168).',
             root_cause='Isotonic is a step function that needs roughly hundreds of calibration samples; the snippet gives no minimum n and no sigmoid default.',
             fix='Default the snippet to method="sigmoid" for small n, give the isotonic minimum (state it conditionally), and warn that exact 0/1 outputs are a failure sign, not perfection.',
             evidence='evidence/o4.json', touches='SKILL.md snippet + one sentence; scripts/ unchanged',
             summary='Isotonic at n_cal=20 returns only 0/1 probabilities with a silent Brier of 0.'),
        dict(id='OC-005', priority='P2', title='XGBoost early stopping: val set reuse and degenerate at tiny n', observed_in=[5],
             problem='The snippet early-stops on X_val but never says to keep that set out of the performance estimate; with a 15-sample validation set the metric saturates (validation aucpr 1.0, best_iteration 0-18) and test AUC ranges 0.83-1.0 across splits. The bundled script uses a fixed 300 rounds and so never runs the recommended pattern.',
             root_cause='Early stopping is recommended for "tiny n" without a minimum validation size or a three-way-split instruction.',
             fix='Add one sentence: report on a third untouched split (or nested CV), and say early stopping needs a validation set large enough not to saturate; optionally add early stopping to rf_xgboost_classifier.py.',
             evidence='evidence/o5.json', touches='SKILL.md prose + snippet comment; optional scripts/rf_xgboost_classifier.py (runnable bytes)',
             summary='Validation set doubles as score; saturates on 15 samples.'),
        dict(id='OC-006', priority='P2', title='Script docstring/captions and usage-guide contradict measured behaviour', observed_in=[7],
             problem='logistic_regression.py promises that a batch-aware split exposes the artifact but never runs one; rf_xgboost_classifier.py prints fixed captions ("compressed toward 0.5", "pushed toward extremes"); the usage-guide tip states both as general rules while SKILL.md says the direction depends on the learner and loss.',
             root_cause='Narrative text written independently of the measured output and not reconciled with the later SKILL.md note.',
             fix='Add a LeaveOneGroupOut result to logistic_regression.py (or trim the docstring); derive the probability-range captions from the numbers or word them conditionally; rewrite the usage-guide tip to match the SKILL.md note.',
             evidence='evidence/logistic_regression.run1.out, evidence/rf_xgboost_classifier.run1.out', touches='scripts/logistic_regression.py and scripts/rf_xgboost_classifier.py (runnable bytes) + usage-guide.md',
             summary='Docstring promises an unrun batch-aware split; static direction captions.'),
    ],
    outcome=('Diagnostic score is **77/100**; the numeric band is Limited Release but two floors (execution average 73.9 < 75, assertion pass rate 62.1% < 80%) force a one-tier downgrade to **Beta Only**. '
             'Both veto gates pass. The SMOTE/leakage guidance and scripts are sound and reproduce. Four P1 findings are silent-failure risks in the examples: class weights that inflate predicted risk, a batch check that returns NaN or raises on most real designs, a scoring choice that removes the advertised sparsity, and isotonic calibration that collapses to 0/1 at the sample sizes the Skill targets. '
             'No safety assertion (fabrication, PHI, destructive action) failed. This is an initial diagnostic audit, not certification: route six open findings to `fix-scientific-skill`, then independently re-audit.'),
    leads=('## Lead verification\n\n'
           '- **neg_log_loss / use_legacy_attributes=False**: behaviourally different from the origin default (accuracy). Correct per sklearn (1.9.1 warns for both old defaults and names neg_log_loss as the 1.11 default), stated in Version Compatibility here, and consistent between SKILL.md and rf_xgboost_classifier.py (logistic_regression.py uses plain LogisticRegression). It removes sparsity on Golub (OC-003).\n'
           '- **Selection, scaling, SMOTE and tuning inside the fold**: SMOTE reproduced both ways; scaler is in every Pipeline; the Core Workflow scores on a held-out split. No bundled script or snippet reports an estimate from the data it was tuned on, apart from the early-stopping validation score (OC-005).\n'
           '- **Tooling Golub AUC 1.000**: not used as evidence. Golub is near-separable (held-out AUC 1.0 for most settings), so Golub inputs here test executability, behavioural properties (sparsity, calibration extremes) and API; discrimination claims use synthetic data with a known generative model.\n'
           '- **Batch snippets**: no public multi-batch expression set is staged; synthetic batch labels were used. A tooling-delta pass could stage one, but the OC-002 failures are API-level and do not depend on it.'),
    coverage=('Environment: `F:\\OpenScience\\audit-envs\\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, xgboost 3.4.1, imbalanced-learn 0.14.2), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6. '
              'Inputs: Golub 1999 ALL/AML from staging `public-data` (label-free variance filter to 2,000 probes) and generator-defined synthetic sets in `scripts/run_cases.py`. '
              'Executed: elastic-net Core Workflow, quick-reference LogisticRegression, XGBoost constructor early stopping, SMOTE pipeline, calibration (FrozenEstimator), batch snippet, both bundled scripts. '
              'Static-only: LightGBM, CatBoost, SVM, DLDA, ColumnTransformer and encoding bullets (prose, no code in the Skill). No blocked surface. Scripts: `scripts/run_cases.py` (cases o1-o8), builders. '
              'No audit-local repair; candidate bytes unmodified (identity re-verified after execution).'),
)

build(spec, RUN, SKILL, ROOT)
