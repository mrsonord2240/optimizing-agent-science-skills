"""Builds report.json / viewer.md / source-identity.json / finding-ledger.md for the final re-audit. Run: python scripts/build_report.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lib import build
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = 'F:/OpenScience/wt/ml-lane3-normalize/skills/bio-machine-learning-biomarker-discovery'
ROOT = 'F:/optimizing-agent-science-skills'
D = lambda m, c, q, r, s: dict(methodological_validity=m, code_executability=c, data_quality_control=q, reproducibility=r, security=s)
spec = dict(
    skill_id='bio-machine-learning-biomarker-discovery',
    identity='27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134',
    origin_path='machine-learning/biomarker-discovery',
    tools_md='F:\\OpenScience\\audits\\bio-machine-learning-biomarker-discovery\\TOOLS.md',
    tools_sha='d6c742a3a070e4a0fd1541b5cda456bf7efe6ed0f7d99715476c474eb4537021',
    description=('Use when identifying candidate biomarkers from high-dimensional omics data, deciding between an all-relevant and a minimal-optimal selector, '
                 'or judging whether a selected gene set is reproducible.'),
    complexity='Moderate',
    veto=dict(
        skill_gate='PASS', research_gate='PASS',
        t1=('PASS', 'All six SKILL.md python blocks and all three scripts ran rc 0 under -W error::FutureWarning at 1,000 probes and (blocks 0-5, stability script) at the full 7,129 probes on sklearn 1.9.1 / numpy 2.5.3 / Boruta 0.4.3 / mrmr-selection 0.2.8; zero warnings or tracebacks.'),
        t2=('PASS', 'Documented outputs held: stability_selection returns (frequencies, Nogueira index) with a NaN index and the snippet message when nothing is selected; coef_ is (1, p); support_/support_weak_ masks; MRMRSelect.cols_.'),
        t3=('PASS', 'stability_selection is deterministic: identical seed gives bit-identical frequencies (raw and rescaled, 1,000 and 7,129 probes; my own synthetic data too), seed 1 or 7 differs (maxdiff 0.15-0.16). Both bundled scripts are seeded.'),
        t4=('PASS', 'No network, credentials, shell-out or destructive operation; scripts write nothing.'),
        m1=('PASS', 'Every number stated in SKILL.md for stability selection and scoring was re-measured and matches (see Lead verification); citations are named works; the Meinshausen-Buhlmann bound is quoted correctly as q^2/((2*pi_thr-1)*p) under exchangeability.'),
        m2=('PASS', 'Research-use selection guidance; routes unbiased performance to model-validation, refuses to read a minimal-optimal list as "the biomarkers", states that stability is not evidence of signal and that the Golub numbers are one dataset and partition.'),
        m3=('PASS', 'Selection, scaling and tuning verified to be fit on training rows only (held-out rows replaced by garbage with labels flipped leave scaler, selected columns, coefficients, best_params_ and inner CV scores bit-identical); the select-before-CV leak is real (positive control) and reproduced on permuted labels; the null control for stability selection holds on real and self-built data.'),
        m4=('PASS', 'All shipped runnable surfaces execute; one robustness gap (rare-class labels give a misleading ValueError, RA-001) fails loudly, never silently.'),
    ),
    static={
        'functional_suitability': (11, 'Method taxonomy, all-relevant vs minimal-optimal framing and the leakage-safe Pipeline, nested GridSearchCV, in-fold mRMR, Boruta, elastic-net and stability selection blocks are accurate and executable. Deduction: stability_selection assumes both classes survive every n/2 subsample (RA-001).'),
        'reliability': (10, 'Seeded, bit-reproducible, explicit empty-selection message instead of silent NaN, explicit scoring pin. Deduction: rare-class labels crash with a misleading liblinear "multiclass" ValueError and the limitation is undocumented (RA-001).'),
        'performance_context': (7, 'Progressive disclosure is correct (failure modes routed, scripts referenced); wall times are stated and match measured ones (elastic-net 34/263 s stated vs 39/278 s measured under load and 33/250 s in the tooling log; stability call 1-6 s / 15-24 s vs 1-3 s / 15-24 s). Boruta (about 60-100 s) has no stated time, only "Slow".'),
        'agent_usability': (15, 'Cold start is clear, the decision rule is explicit, the description is a pure trigger and separates the Skill from model-validation, prediction-explanation, omics-classifiers, survival-analysis and atlas-mapping. SKILL.md is long (21 KB) but the detail is routed.'),
        'human_usability': (7, 'Usage-guide prompts are natural; scientific strictness (loud failures) is appropriate.'),
        'security': (11, 'No credentials, network or destructive operation; array inputs only.'),
        'maintainability': (11, 'Clean split of SKILL.md, failure-modes, three scripts and a usage guide; script narrative strings now match what runs (lasso label reworded, Boruta/L1 counts computed). Snippets have no bundled tests.'),
        'agent_specific': (19, 'Honest scope and caveats (approximate unit invariance, non-zero null possible, one dataset and partition), explicit escape hatches, correct sklearn migration notes. Deduction: the R glmnet row has no explicit "not executed" marker (prose only, no claim of execution).'),
    },
    inputs=[
        dict(type='Canonical', label='Leakage-safe Pipeline, nested GridSearchCV and in-fold MRMRSelect (SKILL.md blocks 0-2) on Golub, with held-out perturbation and permuted-label null', status='COMPLETED', basic=36,
             note='Blocks 0-2 rc 0 under -W error::FutureWarning at 1,000 probes (2/14/20 s) and 7,129 probes (7/90/78 s): AUC 0.990 +/- 0.030, nested 0.99, mRMR 1.0. Perturbing held-out rows (values and labels) on folds 0 and 3 left scaler mean, selected columns, coefficients, best_params_, inner CV scores and mRMR cols_ bit-identical; the same perturbation changes a select-on-all-rows control (6 of 20 columns). Permuted labels, 5 draws, 1,000 probes: select-before-CV AUC 0.66 mean (0.55-0.78) vs in-pipeline 0.48 vs nested 0.47.',
             specialized=D(18, 14, 9, 9, 5),
             assertions=[
                 ('Scaler and SelectKBest inside the Pipeline are fit on training rows only', 'PASS', 'leakage_tests.py: scaler.mean_, get_support() and coef_ identical after held-out rows replaced by N(500,300) with labels flipped (folds 0, 3)'),
                 ('Nested GridSearchCV never lets tuning see the outer test fold', 'PASS', 'best_params_ and inner mean_test_score identical after the same perturbation; outer fold score changes (1.0 -> 0.4/0.8)'),
                 ('MRMRSelect runs and selects inside the fold', 'PASS', 'cols_ identical after perturbation; K=20; AUC 1.0'),
                 ('The leaky select-before-CV gap reproduces on permuted labels', 'PASS', '0.66 vs 0.48 (1,000 probes, k=20); script p=5000 shows 1.00 vs 0.56; positive control confirms test power'),
                 ('Every block runs warning-free under -W error::FutureWarning at both sizes', 'PASS', 'logs/snip012_1000.log, snip012_full.log'),
             ]),
        dict(type='Variant A', label='BorutaPy snippet and boruta_feature_selection.py', status='COMPLETED', basic=35,
             note='SKILL.md block 3: real labels 90 confirmed / 20 tentative at 1,000 probes (71 s; 96 s at 7,129); permuted labels (default_rng(1)) 8 confirmed. Script: 5/5 module members confirmed by Boruta, L1 4/5, both counts computed and printed.',
             specialized=D(17, 13, 8, 9, 5),
             assertions=[
                 ('Snippet returns confirmed/tentative masks on numpy input without warnings', 'PASS', 'logs/boruta_inspect.log, snip3_1000.log, snip3_full.log'),
                 ('Permuted labels confirm few features', 'PASS', '8 of 1,000 probes (0.8 percent) with perc=100'),
                 ('Script printed counts equal what runs (BD-005)', 'PASS', 'prints Boruta 5/5 and L1 4/5 from computed values; the old "~1" claim is gone'),
                 ('Script is seeded and warning-free', 'PASS', 'logs/boruta_1000.log rc 0'),
             ]),
        dict(type='Variant B', label='Elastic-net LogisticRegressionCV with scoring pinned to accuracy: stated size table and partition dependence', status='COMPLETED', basic=35,
             note='Stated table reproduced exactly on the stated partition (1,000 probes, cv=5): selected 601 / 203 / 148 for neg_log_loss / roc_auc / accuracy; permuted labels 16 / 0 / 0; outer AUC 0.991 / 0.983 / 0.991. Other inner partitions (shuffled seeds 1, 2): neg_log_loss 436 / 437, roc_auc 53 / 96, accuracy 150 / 150. sklearn 1.9.1 emits the FutureWarning naming the 1.11 default change to neg_log_loss. Block 4: 39 s at 1,000 and 278 s at 7,129 under load.',
             specialized=D(17, 13, 8, 8, 5),
             assertions=[
                 ('Stated 601/203/148 and permuted 16/0/0 reproduce', 'PASS', 'logs/bd002.log STATED PARTITION'),
                 ('Stated held-out AUC 0.991/0.983/0.991 reproduces and is within 0.01', 'PASS', 'same log'),
                 ('The sklearn 1.11 default-change statement is accurate and the pin is explicit', 'PASS', 'scoring_default_warn.py: FutureWarning text names accuracy -> neg_log_loss in 1.11'),
                 ('The Skill does not overgeneralize the size table from one partition', 'PASS', 'text says one dataset and partition and to re-check on your data; accuracy is the most partition-stable (148-150) so the pin is defensible for a compact signature, though roc_auc size swings 53-203 (RA-002)'),
                 ('Snippet runs warning-free at both sizes', 'PASS', 'logs/snip4_1000.log, snip4_full.log'),
             ]),
        dict(type='Edge', label='scripts/stability_selection.py on Golub: determinism, unit invariance, permuted-label null and every stated number at both sizes', status='COMPLETED', basic=36,
             note='1,000 probes (q=14): real labels 2 / 2 / 2 stable (raw / standardized / rescaled), Nogueira 0.25; 11 permutations: 0 stable in 10, one probe (454) at 0.81 in perm_109. 7,129 probes (q=37): 5 / 5 / 5 stable (probes 1778, 1833, 2287, 4846, 4950), Nogueira 0.228; 0 stable in all 11 permutations, highest frequency 0.57 (the snippet permutation; the 10 staged sets reach 0.52). Same seed bit-identical, seed 1 differs (maxdiff 0.16 / 0.15). One call 1-3 s and 15-24 s.',
             specialized=D(18, 14, 9, 10, 5),
             assertions=[
                 ('Identical seed gives identical frequencies; a different seed differs', 'PASS', 'determinism_1000.log, determinism_full.log: maxdiff 0.0 vs 0.16/0.15'),
                 ('Real-label counts 2/2/2 and 5/5/5 across raw, standardized and rescaled input match SKILL.md', 'PASS', 'stab_1000.log, stab_full.log; frequencies identical'),
                 ('Permuted null matches the stated 0-in-10-of-11 (1,000) and 0-in-all-11 with highest 0.57 (7,129)', 'PASS', 'NULL SUMMARY lines in both logs'),
                 ('Empty selection is reported rather than silent NaN', 'PASS', 'q=0 returns a NaN index; the snippet prints "no features selected"'),
                 ('Wording is honest: approximate invariance, non-zero null possible, count over runs', 'PASS', 'one probe at 0.81 in a 1,000-probe permutation is exactly the case the text warns about'),
             ]),
        dict(type='Stress', label='Independent self-built null: pure-noise features, planted true features, units, determinism (n=100-120, p=2000)', status='COMPLETED', basic=35,
             note='Pure-noise X and y, 8 draws, q=19: 0 stable in all (max frequency 0.22-0.57; EV bound is 1). Planted 5 of 2000 (moderate signal), 6 draws: 0-2 of 5 recovered, 0 false. Planted beta 2.5 (n=120), 6 draws: 1/4/0/4/1/4 of 5 recovered, 0 false stable; permuted-label nulls gave 0 stable in 5 draws and 1 (frequency 0.74) in one. Rescaled exp(N(0,2))*X+5, standardized and x1000 inputs give identical frequencies (maxdiff 0.00).',
             specialized=D(18, 13, 9, 9, 5),
             assertions=[
                 ('Near-zero stable features under pure noise', 'PASS', '0 stable in 8 independent draws; mean 0.0 vs bound EV=1'),
                 ('Planted features dominate the stable set and no false feature is called stable on real signal', 'PASS', 'strong planting: 14 true vs 0 false over 6 draws; moderate: 7 true vs 0 false'),
                 ('Unit invariance on raw, standardized, rescaled and x1000 input', 'PASS', 'maxdiff 0.00 in all comparisons'),
                 ('Recall is not oversold', 'PASS', 'recall is low to moderate (0-4 of 5): the Skill claims control of false selections and says a count not clearly above its null is not a signature; it makes no recall claim'),
             ]),
        dict(type='Adversarial', label='Rare-class labels in stability_selection (n=72, p=300, subsamples of 36 are not stratified)', status='PARTIAL', basic=28,
             note='With 20 positives of 72 the function runs and recovers the 3 planted features. With 8, 4 or 2 positives some n/2 subsample lacks a class and the call raises a ValueError whose text blames liblinear "multiclass classification (n_classes >= 3)", which misleads: the cause is a single-class subsample. The failure is loud, never silent.',
             specialized=D(13, 10, 6, 6, 5),
             assertions=[
                 ('Rare-class input fails loudly rather than returning wrong frequencies', 'PASS', 'ValueError raised (logs/imbalance.log)'),
                 ('The error message identifies the cause (single-class subsample)', 'FAIL', 'message cites multiclass/liblinear, not class absence'),
                 ('SKILL.md or the script docstring states the both-classes-per-subsample requirement', 'FAIL', 'not stated; subsampling is unstratified (RA-001)'),
             ]),
        dict(type='Scope Boundary', label='lasso_biomarker.py narrative, R glmnet prose row, constant-column and empty-selection guards', status='COMPLETED', basic=34,
             note='lasso_biomarker.py: noise AUC 1.00 select-before-CV vs 0.56 in-pipeline; stable [g0,g1,g2,g3] under the reworded label "[planted signal: g0..g4; a missing one was not recovered]" (4 of 5, now stated honestly); permuted 0; rescaled 4 (same set True); identical when run from the Skill directory. Constant column handled (frequency 0). glmnet is one troubleshooting row, no R code, nothing claimed executed.',
             specialized=D(16, 14, 8, 9, 5),
             assertions=[
                 ('Script print labels match what runs (BD-005 incl. the lasso reword)', 'PASS', 'output shows 4 stable and the label says a missing one was not recovered; Boruta script prints 5/5 and 4/5 from computed values'),
                 ('R glmnet is not presented as executed or bundled', 'PASS', 'single prose row in Common Errors, no code; static-only (no explicit "not executed" marker, noted as a deduction)'),
                 ('Degenerate inputs (constant column, q=0) do not crash or silently mislead', 'PASS', 'frequency 0.0 for the constant feature; q=0 gives a NaN index and the snippet prints "no features selected"'),
             ]),
    ],
    strengths=[
        'The stability-selection function controls false discoveries as claimed: 0 stable features in 8 self-built pure-noise datasets and in 11 of 11 (7,129 probes) permuted-label sets, bit-reproducible per seed and invariant to feature units.',
        'Selection, scaling and tuning provably stay in the training fold: perturbing held-out rows (values and labels) leaves scaler, selected columns, coefficients, best_params_ and inner CV scores bit-identical across Pipeline, nested GridSearchCV and in-fold mRMR, while a select-before-CV control changes.',
        'Every number the Skill states about size, stability and cost reproduces (601/203/148, 16/0/0, 2/2/2, 5/5/5, 0.57, wall times), with honest caveats about one dataset and partition and approximate invariance.',
        'The pure-trigger description parses and separates the Skill from the validation, explanation, classifier, survival and atlas siblings.',
    ],
    findings=[
        dict(id='RA-001', priority='P2', title='stability_selection fails obscurely on rare-class labels', observed_in=[6],
             problem='Subsamples of n/2 are not stratified; with 8 or fewer positives of 72 some subsample has one class and the call raises a ValueError citing liblinear multiclass (n_classes >= 3). The failure is loud but misleading, and neither SKILL.md nor the docstring states the both-classes requirement.',
             root_cause='Plain rng.choice subsampling and no pre-check of the class counts in each subsample.',
             fix='Text-only: state in SKILL.md that labels must be binary with enough minority samples that every n/2 subsample keeps both classes. Optional script change: stratified subsampling plus a clear error.',
             evidence='logs/imbalance.log; scripts/stab_imbalance.py', touches='SKILL.md prose (a docstring note would change script bytes)',
             summary='Rare-class labels raise a misleading ValueError; requirement undocumented.'),
        dict(id='RA-002', priority='P2', title='roc_auc signature size is partition-dependent, accuracy is not', observed_in=[3],
             problem='The stated table (601/203/148) is honestly labelled one dataset and partition, but on two other inner partitions roc_auc selected 53 and 96 probes (below accuracy 150) and neg_log_loss 436 and 437; a reader can take roc_auc as always larger than accuracy.',
             root_cause='Only one partition was measured and tabulated.',
             fix='Text-only: add one clause that over three partitions neg_log_loss gave 436-601, roc_auc 53-203 and accuracy 148-150 probes, which is also the reason accuracy is the stable pin.',
             evidence='logs/bd002.log OTHER PARTITION lines; scripts/scoring_bd002.py', touches='SKILL.md prose only',
             summary='roc_auc size swings 53-203 over partitions; accuracy 148-150.'),
    ],
    outcome=('Independent final re-audit of the exact candidate: score **88/100**, **Production Ready**, static 91, execution average 85.6, Layer 1 34.1, Layer 2 51.4, assertions 27 of 29 (93.1 percent), both vetoes PASS, no open P0 or P1. '
             'All six initial findings (BD-001 P1, BD-002 to BD-006 P2) are resolved on re-test: BD-001 stability selection is seeded, per-subsample standardized, budgeted by q, bit-reproducible, unit-invariant and null-calibrated; BD-002 the scoring pin and size table reproduce exactly; BD-003 to BD-006 verified. '
             'Two new P2 observations (RA-001 rare-class robustness, RA-002 partition caveat) do not block readiness and are both fixable with text only. The candidate bytes were not modified; identity re-verified after execution.'),
    leads=('## Lead verification\n\n'
           '- **BD-001 resolved.** Determinism: seed 0 twice bit-identical, seed 1 or 7 differs (1,000 and 7,129 probes; own data). Null: 0 stable in 8 own pure-noise draws; 0 stable in 10 of 11 (1,000) and 11 of 11 (7,129) permuted Golub sets. Planted: 0 false stable in 12 self-built draws on real signal; recall 0-4 of 5 (q caps recall, the Skill claims no recall). Units: raw, standardized, rescaled and x1000 give identical frequencies. All stated numbers match: 2/2/2, 5/5/5, one probe at 0.81 (1,000), highest frequency 0.57 (7,129; the staged ten reach 0.52, the snippet permutation 0.57).\n'
           '- **BD-002 resolved.** 601/203/148, permuted 16/0/0 and AUC 0.991/0.983/0.991 reproduce on the stated partition. Pinning accuracy is defensible for a compact signature: size is stable across partitions (148-150) while roc_auc varies 53-203 and neg_log_loss 436-601; the presentation says one dataset and partition and the 1.11 default change is real (FutureWarning in 1.9.1). neg_log_loss in omics-classifiers is a deliberate difference for calibrated probabilities. See RA-002.\n'
           '- **BD-003 resolved** (scaler inside the Pipeline, label reads "In-pipeline CV AUC (k fixed)", nested GridSearchCV verified to nest by perturbation). **BD-004 resolved** (seeded, "no features selected" guard). **BD-005 resolved** (lasso label reworded and matches the 4-of-5 output; Boruta script prints computed 5/5 and 4/5). **BD-006 resolved** (MRMRSelect fit inside the fold, cols_ unchanged by held-out perturbation).\n'
           '- **Description** parses as YAML, is a "Use when" trigger covering selector choice, candidate biomarkers and reproducibility; it separates the Skill from model-validation (performance estimation), prediction-explanation (SHAP), omics-classifiers (build a classifier), survival-analysis and atlas-mapping. No finding.\n'
           '- **Cost note** matches the tooling logs within load noise: elastic-net 39 s / 278 s here (33 / 250 s in the tooling log) vs "about 34 / 263 s"; stability call 1-3 s and 15-24 s vs 1-6 / 15-24 s.'),
    coverage=('Environment: `F:\\OpenScience\\audit-envs\\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, numpy 2.5.3, Boruta 0.4.3, mrmr-selection 0.2.8), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6, unchanged. '
              'Input: Golub ALL/AML (72 x 7,129) and the staged 1,000-probe subset from `derived\\biomarker-discovery`; synthetic data built by this audit, planted truth labelled. '
              'Executed: all six SKILL.md python blocks at 1,000 probes and at 7,129 probes (blocks 0-5), scripts/stability_selection.py via staged drivers at both sizes (every stated number), determinism at both sizes, lasso and Boruta scripts, own null/planted/invariance/imbalance/leakage/scoring-partition tests (scripts/). '
              'Static-only: R glmnet (prose row, nothing claimed executed). No blocked surface, no input missing, no tooling-delta needed. Run logs in `logs/`; runs executed concurrently on a shared machine, so times are upper-ish. '
              'The first leakage run (logs/leakage_run1_flawed_label_flip_changed_splits.log) was my own test bug (flipping held-out labels changed the stratified splits); it was fixed by passing fixed splits and rerun; only the corrected run is evidence.'),
)
build(spec, RUN, SKILL, ROOT)
