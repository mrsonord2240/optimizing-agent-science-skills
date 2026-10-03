"""Builds report.json for the final re-audit 2 from the measured evidence (evidence/*.log)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda t, ok, n: {'text': t, 'result': 'PASS' if ok else 'FAIL', 'note': n}
inputs = [
 dict(index=1, type='Canonical', label='Core Workflow and lasso + 1-SE snippets on real Golub ALL/AML (own splits 31 and 32, 2,000 high-variance probes), FutureWarning as error',
  note='Dense neg_log_loss fit kept 2000/2000 coefficients on both splits (prose 1,059-2,000). Lasso + 1-SE kept 369 and 273 of 2,000 (held-out AUC 0.97 and 1.00); SKILL.md quotes 45 / 142 / 60 from three other splits. c_1se, signature and XGB best round (3, validation AUCPR 1.0) are bit-identical when the held-out split is replaced by noise.',
  basic=35, specialized=51, assertions=[
   A('Core Workflow and 1-SE snippets run under -W error::FutureWarning with no warning', True, 'r2_golub_oc3_oc6.py (seeds 31, 32) and SKILL.md blocks 0-1 via run_snippets.py on Golub and synthetic: rc 0, warnings []'),
   A("The 'dense fit' statement matches behaviour under the pinned neg_log_loss scoring", True, '2000/2000 non-zero on both own splits; no sparse-signature claim is made for the elastic net'),
   A('The 1-SE selection and both fits see training data only', True, 'Replacing X_te/y_te by noise leaves c_1se (11.2884 on both seeds), the lasso support (369, 273) and the block-2 XGB best round unchanged'),
   A('The lasso + 1-SE snippet delivers a list that is smaller than the dense fit at unchanged discrimination', True, '369 and 273 of 2,000 (13.7-18.5%) against 2,000; held-out AUC 0.973 and 1.000'),
   A('The quoted Golub 1-SE counts (45 / 142 / 60) convey the range a user will see on a new split', False, 'Two further splits gave 369 and 273, 2-8x the quoted values and above the 50 training samples; the prose presents three splits as the measurement and does not say the count varies by this much'),
  ]),
 dict(index=2, type='Variant A', label='OC-007 re-test: balanced weights per model family on two own generators (p=60 k=10 n=1500 ~16% prevalence; p=200 k=15 n=800 ~24%), 6 seeds each, 15,000-sample test sets; plus a text sweep of every place the claim appears',
  note='Setup A: logistic AUC 0.910 plain vs 0.907 balanced, risk ratio 1.01x vs 1.89x; RF 0.876 vs 0.891 (higher in 6 of 6), 1.06x vs 1.80x. Setup B: logistic 0.824 vs 0.823, 1.00x vs 1.36x; RF 0.821 vs 0.836 (6 of 6), 1.06x vs 1.54x. The staged generator gives 0.826/0.820 and 0.776/0.812 (6/6), 1.11x/2.43x as stated.',
  basic=36, specialized=54, assertions=[
   A('For logistic regression reweighting moves the probability scale and leaves the ranking essentially unchanged', True, 'AUC differences -0.003 and -0.001; risk ratio 1.89x and 1.36x; prose 0.826 vs 0.820'),
   A('For random forest balanced weights change the ranking, as SKILL.md now states (better in this setup, not generally)', True, 'RF AUC higher with balanced weights in 6/6 seeds in both setups (+0.015 each); prose says "in this setup for the better" and "test it"'),
   A('RF risks stay inflated under balanced weights', True, '1.80x and 1.54x in my setups; prose 2.4x in its setup; direction agrees'),
   A('No blanket "no AUC gain" or "not the ranking" claim survives in SKILL.md (decision tree, imbalance paragraph, thresholds), usage-guide or failure-modes', True, 'Searched all three: SKILL.md lines 56, 179, 181, 239; usage-guide line 59; failure-modes line 22 all scope the statement to logistic and say RF can change'),
   A('Imbalance guidance (no class_weight/scale_pos_weight/SMOTE for risk models; tune the threshold; recalibrate if reweighted) is consistent across documents and scripts', True, 'Same advice in decision tree, approach paragraph, XGBoost comment, usage-guide steps 4-5 and failure modes'),
  ]),
 dict(index=3, type='Variant B', label='SMOTE placement and effect (imblearn Pipeline vs resample-before-CV; own generator, noise labels, 8 draws; held-out AUC and risk ratio on 8%-prevalence real-signal data)',
  note='Noise labels: AUC 0.898 when SMOTE precedes CV vs 0.472 inside the imblearn Pipeline. Real signal: SMOTE minus plain logistic test AUC -0.0076 (range -0.019..+0.004); predicted risk 3.56x the prevalence vs 0.99x. SKILL.md block 4 (ImbPipeline) runs clean.',
  basic=35, specialized=53, assertions=[
   A('Resampling before the split leaks (inflated CV AUC on noise labels)', True, '0.898 vs chance-level 0.472 in the Pipeline'),
   A('The imblearn Pipeline placement removes the leak', True, 'AUC 0.472 on noise labels'),
   A('SMOTE gives no held-out AUC gain for logistic and inflates predicted minority risk', True, '-0.0076 mean AUC change; 3.56x vs 0.99x'),
   A('The SMOTE snippet as written in SKILL.md executes', True, 'run_snippets.py block 4: OK on Golub and synthetic'),
  ]),
 dict(index=4, type='Edge', label='OC-004/OC-011 re-test: recalibrate() branch boundaries and degenerate-calibrator warning through the shipped code; n=20 calibration vs raw probabilities (shipped calibration_check.py demo 2)',
  note='n=999 sigmoid; 1000 with 498 and 103 rarer-class events isotonic; 1000 with 52 events sigmoid; n=200 and 1200 as expected; the degenerate stump calibrator warns ("2 distinct probabilities") on every branch; healthy RF at n=300 raises no warning (85 distinct values). RF Brier raw 0.1985 / sigmoid 0.2089 / isotonic 0.2356 at n=20; 0.1985 / 0.1980 / 0.2039 at 100; 0.1985 / 0.1944 / 0.1962 at 1000.',
  basic=35, specialized=53, assertions=[
   A('Isotonic is chosen only at >= 1,000 calibration samples and >= 100 rarer-class events', True, 'r2_recal_paths.py: n=999 and 1000 with 52 events -> sigmoid; 1000 with 103 and 1200 with 597 -> isotonic'),
   A('usage-guide states the same isotonic condition (1,000 samples and 100 in the rarer class) as SKILL.md and the code constants', True, 'usage-guide line 58; ISOTONIC_MIN_N 1000, ISOTONIC_MIN_EVENTS 100'),
   A('A degenerate calibrator warns through the shipped code path and the text tells the reader not to report its Brier', True, 'warning raised under the always filter; SKILL.md: treat three or fewer distinct output values as a failed calibration'),
   A('Recalibration at n=20 can lose to raw probabilities, with numbers that reproduce', True, 'calibration_check.py demo 2 run here: 0.1985 / 0.2089 / 0.2356'),
   A('Every saga snippet in SKILL.md sets random_state', True, 'Both LogisticRegressionCV snippets and the LogisticRegression saga snippet carry random_state=0; the unseeded script fit gave 101 non-zero in 8 of 8 repeats'),
  ]),
 dict(index=5, type='Scope Boundary', label='OC-005/OC-010 re-test: three-way split, test-split independence, learning-rate choice, round-0 warning, determinism and thread count for the bundled XGBoost demo',
  note='Perturbing the test split (random features, shuffled labels) leaves best round 223, validation logloss 0.588094 and the train and validation predictions bit-identical, while the test scores change. Validation logloss by learning rate 0.03 / 0.1 / 0.3: 0.588 / 0.597 / 0.610. At n=300 the script prints the loud warning (best round 0, validation 0.692). Two runs are identical. With n_jobs 1 / 2 / 4 / default the best round is 160 / 133 / 397 / 223 and test AUC 0.828 / 0.840 / 0.833 / 0.834.',
  basic=33, specialized=50, assertions=[
   A('The test split plays no part in choosing rounds or learning rate', True, 'by construction (X_te appears only in scoring) and by perturbation: best round, score and train/validation predictions identical'),
   A('The loud warning fires when the best round is 0', True, 'n=300 case: "!!! WARNING: best round is 0 ..." printed, best_iteration 0'),
   A('Two runs of the demo are identical', True, 'script_rf_xgboost_classifier.log and ..._run2.log: 0.944 / 0.729 / 0.834, round 223 in both'),
   A('The headline "stops at round 223" and the comment figures (0.577 / 0.601 / 0.632) are properties of the setup, not of the machine', False, 'Round and validation logloss depend on XGBoost thread count: 160 / 133 / 397 / 223 for n_jobs 1 / 2 / 4 / default; the comment figures come from n_jobs=4 while the default-thread run prints 0.588. Test AUC stays 0.83-0.84, so the conclusion holds and only the quoted round does not transfer'),
  ]),
 dict(index=6, type='Adversarial', label='OC-002 re-test and noise caution: planted batch effect with known answer (2, 3 and 6 batches, 30 reps each, own generator) plus one-class edge cases',
  note='Zero-signal, label confounded with batch: random-split AUC 0.66 / 0.60 / 0.67, leave-one-batch-out per-batch mean 0.51 / 0.48 / 0.51 (sd across reps 0.112 / 0.071 / 0.072). Real signal plus confounded batch: per-batch mean 0.77 / 0.81 / 0.85 vs pooled 0.68 / 0.73 / 0.87. Batch predictability 1.00 throughout. Shipped self-test: NaN with note for one-class held-out batches.',
  basic=36, specialized=54, assertions=[
   A('Signal that exists only through batch collapses under leave-one-batch-out', True, 'per-batch mean 0.48-0.51 vs random-split 0.60-0.67'),
   A('Real within-batch signal survives leave-one-batch-out', True, '0.77 / 0.81 / 0.85'),
   A('One-class held-out batches are reported, not silently averaged', True, 'batch_checks.py self-test rerun here: NaN with an "AUC undefined" note, pooled number still computed'),
   A('The noise caution (a single leave-one-batch-out mean is noisy at every batch count) holds', True, 'sd across reps 0.07-0.11 at 2, 3 and 6 batches in my generator; the stated 0.09-0.10 reproduces only in the staged generator (40 per batch)'),
   A('The Skill reads the per-batch mean and warns that pooled AUC can still reward a batch-level shift', True, 'zero-signal pooled AUC 0.32 / 0.51 / 0.64 swings around chance while the per-batch mean stays near 0.5'),
  ]),
 dict(index=7, type='Stress', label='Every shipped script and every SKILL.md block as instructed under -W error::FutureWarning; run location; prose-only surfaces',
  note='Four scripts rc 0, no warnings (4 s, 62 s, 4 s, 46 s). Seven of seven SKILL.md blocks OK on Golub and on synthetic data, warnings []. Batch snippet: relative path from the Skill directory rc 0; foreign cwd relative ModuleNotFoundError, as the shipped comment says; foreign cwd with the absolute scripts path rc 0.',
  basic=36, specialized=54, assertions=[
   A('All four scripts exit 0 with no warning under -W error::FutureWarning', True, 'script_*.log: rc=0 each'),
   A('All seven SKILL.md python blocks run as written on real (Golub) and synthetic data', True, 'snippets_golub.log, snippets_synthetic.log: 7/7 OK'),
   A("SKILL.md snippets run when the agent's working directory is the Skill directory or the absolute scripts path is used, and the text says so", True, 'cwd.log; comment: "relative to the cwd: run from the Skill directory, or use the absolute path of its scripts/"'),
   A('LightGBM, CatBoost, linear SVM and DLDA guidance is labelled as not executed in SKILL.md and usage-guide', True, 'SKILL.md line 35 and usage-guide line 63'),
   A('Numbers printed by the scripts match the numbers and captions in SKILL.md', True, 'batch 0.54 / 0.70 / 0.45; 0.988 / 4.193 / 1.106 and 0.1985 / 0.2089 / 0.2356; 101 non-zero; AUC 0.944 / 0.729 / 0.834, round 223'),
  ]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions']); i['assertions_total'] = len(i['assertions'])
    i['status'] = 'COMPLETED'; i['status_flag'] = '✅' if i['total'] >= 75 else '⚠️'
avg = round(sum(i['total'] for i in inputs) / 7, 1)
cats = {
 'functional_suitability': (11, 12, 'Linear, tree, batch, imbalance and calibration workflows are covered with verified API notes and measured claims; the RF ranking overclaim is gone and prose-only algorithms are labelled; residual: 1-SE counts quoted from three splits only.'),
 'reliability': (11, 12, 'Guards are loud and correct: one-class batches reported, degenerate calibrator warns, scoring pinned, round-0 warning fires (checked at n=300), the cwd rule is stated. Residual: the demo round and validation loss depend on XGBoost thread count.'),
 'performance_context': (6, 8, 'SKILL.md is 277 lines and about 26 KB with a long inline measurement narrative; failure modes are routed out and scripts are referenced.'),
 'agent_usability': (14, 16, 'Decision table, explicit routing, consistent imbalance and isotonic guidance across four documents, run location stated; a few quoted figures lack setup or variability notes.'),
 'human_usability': (7, 8, 'Prompts match how users ask; per-batch mean is distinguished from pooled AUC; numbers are tied to named setups.'),
 'security': (11, 12, 'No credentials, network or execution of user strings; array inputs only.'),
 'maintainability': (10, 12, 'Four small scripts that self-test their own claims; the generators behind the 40-repeat isotonic, elastic-net sparsity and early-stopping figures are not shipped.'),
 'agent_specific': (18, 20, 'Precise trigger with explicit hand-offs to model-validation, biomarker-discovery and survival-analysis; scope of each rule is stated.'),
}
sub = sum(v[0] for v in cats.values())
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1); score = round(sw + dw)
rec = [dict(priority='P2', title='OC-012 Quoted demo and 1-SE figures are setup-specific', observed_in=[1, 5, 6],
  problem='XGBoost best round in rf_xgboost_classifier.py is 160 / 133 / 397 / 223 for n_jobs 1 / 2 / 4 / default (test AUC 0.83-0.84), but SKILL.md and the script comment quote round 223 and validation logloss 0.577 / 0.601 / 0.632 (n_jobs=4) as the result; Golub lasso + 1-SE counts quoted as 45 / 142 / 60 were 369 and 273 on two further splits; the 0.09-0.10 leave-one-batch-out spread names no setup (0.07-0.11 on mine).',
  root_cause='Single-configuration measurements were written as if they were stable properties.',
  fix='Text-only: say the stopping round varies with thread count (about 130-400) while test AUC stays near 0.83, correct or drop the comment figures, give the Golub 1-SE range over five splits (45-369), and name the setup (40 per batch, 60 features) behind the 0.09-0.10 spread. Optionally pin n_jobs=1 in the demo.')]
rep = {
 'meta': dict(skill_name='bio-machine-learning-omics-classifiers',
  description='Builds diagnostic and prognostic classifiers on omics feature matrices with regularized logistic regression, random forest, and gradient-boosted trees, handling the p>>n regime, batch shortcut learning, class imbalance, and probability calibration. Use when building a classifier from expression, methylation, or variant data, choosing an algorithm for high-dimensional small-n data, or diagnosing a suspiciously perfect AUC.',
  evaluated_on='2026-10-03', evaluator_version='skill-auditor@1.0', category='Data Analysis', execution_mode='D', complexity='Moderate', n_inputs=7, auditor_independent=True, audit_kind='final re-audit 2 (full mode)'),
 'veto_gates': {
  'skill_veto': dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
  'research_veto': dict(applicable=True, gate='PASS',
   scientific_integrity=dict(result='PASS', detail='Citations match titles and venues; the quoted measurements reproduce on the staged generators or on my own (calibration 0.1985 / 0.2089 / 0.2356, RF 0.776 / 0.812, XGBoost 0.834, 45 non-zero lasso on its split); three figures are single-setup values (P2 OC-012) but none is contradicted.'),
   practice_boundaries=dict(result='PASS', detail='Research-use modelling guidance; defers unbiased evaluation to model-validation; no diagnostic or treatment claims.'),
   methodological_ground=dict(result='PASS', detail='No selection, scaling, SMOTE, calibration or tuning sees held-out data (held-out perturbation leaves c_1se, lasso support, XGBoost best round and predictions bit-identical; negative controls change); imbalance and RF-ranking guidance is scoped correctly.'),
   code_usability=dict(result='PASS', detail='All four scripts and seven SKILL.md blocks run under -W error::FutureWarning on Golub and synthetic data; the cwd rule is stated and the failure off-directory is loud.'))},
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: dict(score=v[0], max=v[1], note=v[2]) for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': sum(i['assertions_passed'] for i in inputs), 'total': sum(i['assertions_total'] for i in inputs)}, 'inputs': inputs},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Production Ready', 'grade_symbol': '⭐', 'deployable': True, 'veto_override': False},
 'key_strengths': [
  'All eleven earlier findings (OC-001 to OC-011) hold under independent retest on the exact bytes; no regression found.',
  'Claims are tied to named setups and mostly reproduce on independent generators: RF ranking by family, isotonic rule, n=20 recalibration, SMOTE and leave-one-batch-out behaviour.',
  'Failure guards are loud and tested: the round-0 warning fires at n=300, a degenerate calibrator warns, one-class batches are listed, scoring is pinned, and held-out data never touches selection.',
  'Imbalance, calibration and not-executed guidance is consistent across SKILL.md, usage-guide, failure-modes and the scripts.'],
 'recommendations': rec}
json.dump(rep, open(os.path.join(R, 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
l1 = sum(i['basic'] for i in inputs) / 7; l2 = sum(i['specialized'] for i in inputs) / 7
print(sub, avg, sw, dw, score, 'L1 %.1f L2 %.1f' % (l1, l2), rep['dynamic_score']['assertion_pass_rate'])
