"""Builds report.json / viewer.md / source-identity.json / finding-ledger.md for the biomarker-discovery audit.
Run from the run directory:  python scripts/build_report.py
Evidence files referenced below are in evidence/ (outputs of scripts/run_cases.py c1..c7, warn_probe.py, and the two bundled scripts).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_lib import build

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = 'F:/OpenScience/wt/ml-lane3-normalize/skills/bio-machine-learning-biomarker-discovery'
ROOT = 'F:/optimizing-agent-science-skills'

D = lambda m, c, q, r, s: dict(methodological_validity=m, code_executability=c, data_quality_control=q, reproducibility=r, security=s)

spec = dict(
    skill_id='bio-machine-learning-biomarker-discovery',
    identity='e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71',
    origin_path='machine-learning/biomarker-discovery',
    tools_md='F:\\OpenScience\\audits\\bio-machine-learning-biomarker-discovery\\TOOLS.md',
    tools_sha='9af55f461bebaeda2ce6823e3a89eb7f3a04a6fb2f29deae77747548fb5c6e32',
    description=('Selects biomarker features from high-dimensional omics data using Boruta all-relevant selection, mRMR, LASSO/elastic-net, '
                 'and stability selection, while controlling the leakage, irreproducibility, and correlated-feature traps that make most '
                 'published signatures fail to replicate.'),
    complexity='Moderate',
    veto=dict(
        skill_gate='PASS', research_gate='PASS',
        t1=('PASS', 'Both bundled scripts and every SKILL.md snippet ran to completion on sklearn 1.9.1 / numpy 2.5.3 / Boruta 0.4.3; no crash or dependency conflict.'),
        t2=('PASS', 'No structured API contract; documented output shapes held (coef_ is (1, p) with use_legacy_attributes=False; support_/support_weak_ masks).'),
        t3=('PASS', 'Both scripts are seeded and byte-identical across two runs. Only the SKILL.md stability snippet is unseeded (61 vs 64 stable probes, Nogueira 0.519 vs 0.527): Monte-Carlo noise filed as BD-004, not a veto.'),
        t4=('PASS', 'No code execution of user strings, no network, no credentials, no destructive operations.'),
        m1=('PASS', 'Citations spot-checked (Ambroise 2002, Ein-Dor 2005/2006, Venet 2011, Nogueira 2018, Goring 2001, Squair 2021) match their titles and journals; no invented numbers. The Nogueira formula in the snippet matches the published estimator (unbiased variance, ddof=1).'),
        m2=('PASS', 'Research-use selection guidance; the Skill routes unbiased performance to model-validation and refuses to read selected genes as the biomarkers. No diagnostic or treatment claims.'),
        m3=('PASS', 'Core thesis verified on real data: selection-before-CV gives 0.85 mean AUC (min 0.79) on 10 label permutations of Golub versus 0.49 in-pipeline. The stability snippet is a scale/null-calibration weakness (BD-001), not a principled fallacy, because the Skill states stability is reported next to accuracy rather than as proof.'),
        m4=('PASS', 'All four snippets and both scripts executed; the one tooling-reported ConvergenceWarning lead did not reproduce on the real-label pipeline (it appears only under permuted labels).'),
    ),
    static={
        'functional_suitability': (10, 'Selection taxonomy, all-relevant vs minimal-optimal framing and leakage guidance are accurate and executable. mRMR is advertised in the description and taxonomy but has no snippet (BD-006); nested CV is named but the only code is a fixed-k single-level CV labelled "Nested-safe" (BD-003).'),
        'reliability': (9, 'Failure-modes reference is thorough. The stability snippet silently returns NaN when no feature is selected and gives scale-dependent answers (BD-001, BD-004); other snippets fail loudly or not at all.'),
        'performance_context': (7, 'Progressive disclosure is correct (failure-modes routed from one sentence, scripts referenced). Boruta takes 96 s on 1,000 probes; the Skill says "Slow" but gives no runtime guidance.'),
        'agent_usability': (12, 'Cold-start clarity is high and the decision rule is explicit. The elastic-net text says standardize because the penalty is scale-sensitive, but the stability and Pipeline snippets do not (BD-001, BD-003); the scoring choice is unexplained (BD-002).'),
        'human_usability': (7, 'Natural trigger phrasing in usage-guide prompts; strict-input behaviour is appropriate for a scientific skill.'),
        'security': (11, 'No credentials or network; no input sanitisation needed for array inputs.'),
        'maintainability': (10, 'Clean split of SKILL.md, failure-modes, scripts, usage-guide. Snippets have no tests; script narrative strings are not tied to measured output (BD-005).'),
        'agent_specific': (19, 'Description is a precise trigger with explicit routing to model-validation / prediction-explanation. Escape hatches are good. Deduction: one unseeded snippet.'),
    },
    inputs=[
        dict(type='Canonical', label='SKILL.md leakage-safe Pipeline on real Golub ALL/AML (72 x 7,129), with permutation nulls', status='COMPLETED', basic=34,
             note='Pipeline AUC 0.920 +/- 0.126 (raw) vs 0.990 +/- 0.030 with a scaler in the pipeline; 10 label permutations: selection-before-CV 0.846 mean (min 0.788), in-pipeline 0.492 (0.417-0.645).',
             specialized=D(17, 12, 7, 8, 5),
             assertions=[
                 ('CV AUC is computed on held-out folds with SelectKBest inside the Pipeline', 'PASS', 'evidence/c1.json verbatim_raw'),
                 ('In-pipeline AUC under permuted labels is chance', 'PASS', 'mean 0.492 over 10 permutations'),
                 ('Selection-before-CV reproduces the optimism the Skill warns about', 'PASS', 'mean 0.846, min 0.788 (tooling single draw: 0.79 vs 0.56)'),
                 ('Snippet runs without ConvergenceWarning on real labels (tooling lead)', 'PASS', 'not reproduced: 0 warnings on real labels, 3 only under permuted labels (evidence/warn_probe.json)'),
                 ('Snippet standardizes, as the Skill says the L1/elastic penalty requires, and labels its estimate accurately', 'FAIL', 'no scaler: AUC 0.92 vs 0.99; print label says "Nested-safe" for a single-level fixed-k CV'),
             ]),
        dict(type='Variant A', label='BorutaPy snippet on Golub (top-1,000 variance probes, label-free filter) with null and in-split held-out check', status='COMPLETED', basic=35,
             note='Real labels: 90 confirmed / 20 tentative in 96 s. Permuted labels: 2 confirmed. Boruta fit on a 60% training split only: 61-74 confirmed, held-out AUC 1.0 on three splits.',
             specialized=D(17, 13, 7, 8, 5),
             assertions=[
                 ('Snippet returns confirmed and tentative masks on numpy input', 'PASS', 'evidence/c2.json real_labels'),
                 ('Permuted labels confirm (almost) nothing', 'PASS', '2 of 1,000 probes'),
                 ('Boruta restricted to the training split still yields a held-out-valid signature', 'PASS', 'held-out AUC 1.0 x3 (Golub is near-separable; not evidence of calibration)'),
                 ('Skill keeps performance claims on the Pipeline pattern, not on the discovery fit', 'PASS', 'explicit sentence after the leakage-safe block'),
             ]),
        dict(type='Variant B', label='Elastic-net LogisticRegressionCV snippet (scoring=neg_log_loss, use_legacy_attributes=False) on Golub, scoring comparison', status='COMPLETED', basic=34,
             note='Runs with FutureWarning escalated: no warnings, coef_ shape (1, 1000), scalar l1_ratio_/C_. Signature size by scoring on 1,000 probes: neg_log_loss 329, accuracy (origin default) 152, roc_auc 96. Held-out pipeline AUC 1.0; permuted-label AUC 0.44.',
             specialized=D(16, 13, 7, 8, 5),
             assertions=[
                 ('Snippet runs on sklearn 1.9.1 with no FutureWarning/DeprecationWarning', 'PASS', 'evidence/c3.json scoring_variants'),
                 ('Scaler and C/l1_ratio tuning inside the pipeline give a held-out AUC with a chance-level null', 'PASS', 'AUC 1.0 real, 0.44 permuted'),
                 ('Repeated identical fits select the same set', 'PASS', '328 = 328, identical (saga, no random_state)'),
                 ('The Skill states why neg_log_loss was chosen and what it does to signature size', 'FAIL', 'sibling Skill explains the sklearn warning; this one is silent while size moves 96 -> 329'),
             ]),
        dict(type='Edge', label='Subsampling stability snippet with Nogueira index: determinism, scale, permuted-label null, empty selection', status='COMPLETED', basic=28,
             note='Raw Golub probes, C=0.1: 61 then 64 stable (Nogueira 0.519, 0.527). Same C on standardized probes: 0 stable, Nogueira 0.18. Permuted labels on raw probes: 35 stable, Nogueira 0.38. C=1e-7: NaN index.',
             specialized=D(11, 9, 5, 4, 5),
             assertions=[
                 ('Snippet runs and returns a stable set and a Nogueira index', 'PASS', 'evidence/c4.json verbatim_raw_run1'),
                 ('Identical re-run reproduces the result (seed management)', 'FAIL', 'np.random.choice is unseeded: 61 vs 64 stable features'),
                 ('Permuted labels produce no stable features', 'FAIL', '35 stable probes (pi>0.6) from noise labels on raw intensities'),
                 ('Result is invariant to the units of the input, consistent with the Skill standardize-first rule', 'FAIL', 'raw: 61 stable; standardized same C: 0 stable'),
                 ('Empty selection is reported, not silent NaN', 'FAIL', 'prints "Nogueira stability = nan"'),
             ]),
        dict(type='Stress', label='Both bundled scripts twice under -W default; correctness of their printed narrative', status='COMPLETED', basic=35,
             note='lasso_biomarker.py: noise AUC 1.00 selection-before-CV vs 0.57 in-pipeline, stable set g0-g4, Nogueira 0.22. boruta_feature_selection.py: 5/5 module members. Byte-identical across two runs, no warnings. Claim "a minimal-optimal selector would keep ~1" not reproduced: CV-chosen L1 logistic keeps 5/5 (4/5 at C=0.05).',
             specialized=D(15, 14, 8, 9, 5),
             assertions=[
                 ('Both scripts exit 0 with no warnings under -W default', 'PASS', 'evidence/*.run1.err empty'),
                 ('Outputs are byte-identical across two runs', 'PASS', 'cmp identical for both'),
                 ('Selection and scaling stay inside the fold; performance numbers come from held-out folds', 'PASS', 'honest estimate is a Pipeline in cross_val_score'),
                 ('Printed narrative matches measured behaviour', 'FAIL', 'module claim "~1" not reproduced (evidence/c6.json); comment "~0.7+" vs observed 1.00'),
             ]),
        dict(type='Scope Boundary', label='mRMR (advertised, table-only) and R glmnet (prose-only) surfaces', status='COMPLETED', basic=30,
             note='mrmr_classif(DataFrame, Series, K=5) returns 5 probes; numpy input raises AttributeError exactly as the Common Errors row says. mRMR top-20 chosen on permuted labels over the full matrix then CV: AUC 0.94 (the leakage the Skill describes), but the Skill gives no in-fold mRMR pattern.',
             specialized=D(14, 10, 7, 7, 5),
             assertions=[
                 ('mRMR Common Errors row (pandas backend) is accurate', 'PASS', 'numpy input -> AttributeError'),
                 ('Skill gives a runnable in-fold mRMR pattern for an advertised method', 'FAIL', 'no mRMR snippet; description and usage-guide advertise it'),
                 ('R glmnet is not presented as executed or bundled', 'PASS', 'one prose row; no R code claimed (static-only)'),
             ]),
    ],
    strengths=[
        'The central claim reproduced on real data: selecting before CV gives 0.85 mean AUC on label-permuted Golub against chance (0.49) inside a Pipeline.',
        'Both bundled scripts are seeded, warning-free and byte-identical across runs; the leakage and Boruta demonstrations are correct.',
        'Scientific framing (all-relevant vs minimal-optimal, random-signature null, donor-level pseudobulk) is accurate and well cited; the Nogueira estimator matches the paper.',
        'API drift (penalty= removal, boruta numpy aliases) is documented and the snippets run on current sklearn without warnings.',
    ],
    findings=[
        dict(id='BD-001', priority='P1', title='Stability snippet is scale-dependent and not null-calibrated', observed_in=[4],
             problem='On raw Golub intensities the snippet (C=0.1) reports 61-64 "stable" probes at pi>0.6 and, with labels permuted, still reports 35 stable probes (Nogueira 0.38); on standardized probes the same C gives 0 stable probes for real labels (Nogueira 0.18).',
             root_cause='A fixed C on unstandardized features sets the effective penalty by feature variance, and no permuted-label reference is given for the stability index.',
             fix='Standardize inside each subsample (as the elastic-net text already requires), choose C by CV or state its units, add a label-permutation null for the stable set and the Nogueira index, and say stability does not imply a real signal.',
             evidence='evidence/c4.json (run1, run2, scaled_C0.1, permuted_raw_C0.1)', touches='SKILL.md snippet + prose; scripts/ unchanged (lasso_biomarker.py uses N(0,1) data, C=1)',
             summary='Stable set and index depend on feature units; 35 "stable" probes from permuted labels.'),
        dict(id='BD-002', priority='P2', title='scoring/legacy-attribute choice unexplained; it sets signature size', observed_in=[3],
             problem='The normalizer replaced the default (accuracy) with scoring=neg_log_loss and use_legacy_attributes=False without a word in this Skill (the omics-classifiers sibling explains it); on Golub the selected signature is 329 probes (neg_log_loss), 152 (accuracy), 96 (roc_auc).',
             root_cause='The change tracks sklearn announced defaults (1.10 attributes, 1.11 scoring) and is defensible, but the Version Compatibility section and the "small signature" claim do not mention it.',
             fix='Add one sentence to Version Compatibility naming both parameters and the sklearn schedule, and state that the scoring metric controls signature size (neg_log_loss tolerates weaker penalty; use roc_auc or a 1-SE rule for a minimal panel).',
             evidence='evidence/c3.json scoring_variants; origin bytes F:\\OpenScience\\bioSkills-Improved\\machine-learning\\biomarker-discovery', touches='SKILL.md prose only',
             summary='Scoring change correct per sklearn but unstated; signature size varies 3x with it.'),
        dict(id='BD-003', priority='P2', title='Leakage-safe snippet: no scaler, "Nested-safe" label', observed_in=[1],
             problem='The Pipeline has no StandardScaler although the Skill says the penalty is scale-sensitive: AUC 0.920 +/- 0.126 raw vs 0.990 +/- 0.030 scaled on Golub (pessimistic, not optimistic). The print label calls a single-level fixed-k CV "Nested-safe", and no nested-CV code is given although the text says to estimate by nested CV when tuning.',
             root_cause='Snippet written for the leakage point only; tuning k or C would need an outer loop that is not shown (deferred to model-validation without a pointer in the snippet).',
             fix='Add StandardScaler as the first Pipeline step, rename the label (e.g. "In-pipeline CV AUC (k fixed)"), and add a one-line note or snippet showing GridSearchCV inside cross_val_score when k is tuned. The tooling ConvergenceWarning lead did not reproduce on real labels; do not add a convergence caveat for it.',
             evidence='evidence/c1.json, evidence/c7.json, evidence/warn_probe.json', touches='SKILL.md snippet (+ one line of prose); scripts/ unchanged',
             summary='Missing scaler costs 0.07 AUC; "Nested-safe" label overstates a non-nested estimate.'),
        dict(id='BD-004', priority='P2', title='Stability snippet unseeded; empty selection gives silent NaN', observed_in=[4],
             problem='np.random.choice is unseeded so two runs disagree (61/64 stable, 0.519/0.527) and the Nogueira expression divides by zero when no feature is ever selected (prints nan).',
             root_cause='Snippet omits a Generator seed and a guard on k.mean() in (0, p).',
             fix='Use rng = np.random.default_rng(0) for subsampling and guard the index: report "no features selected" when k.mean() == 0.',
             evidence='evidence/c4.json (verbatim_raw_run1/run2, tiny_C_raw_empty_selection)', touches='SKILL.md snippet only',
             summary='Run-to-run variation and silent NaN.'),
        dict(id='BD-005', priority='P2', title='Script narrative strings not tied to measured output', observed_in=[5],
             problem='boruta_feature_selection.py prints that a minimal-optimal selector "would keep ~1" module member without running one; CV-chosen L1 logistic on the same data keeps 5/5 (4/5 at C=0.05). lasso_biomarker.py comments the leaky AUC as "~0.7+" while it prints 1.00.',
             root_cause='Static comments/print strings assert results the scripts do not compute; the module members (r ~ 0.92) are not redundant enough for L1 to drop them.',
             fix='Either run an L1/elastic-net baseline in the Boruta script and print the count it actually keeps (tighten the module noise, e.g. scale 0.05, if the contrast is the point) or soften the sentence; update the "~0.7+" comment to the observed range.',
             evidence='evidence/c6.json; evidence/lasso_biomarker.run1.out; evidence/boruta_feature_selection.run1.out', touches='scripts/boruta_feature_selection.py and scripts/lasso_biomarker.py (print strings/comments; runnable bytes change)',
             summary='Unsupported "~1" and stale "~0.7+" narrative in the two scripts.'),
        dict(id='BD-006', priority='P2', title='mRMR advertised but no in-fold pattern; not labelled unexecuted', observed_in=[6],
             problem='mRMR appears in the description, taxonomy and usage-guide but no snippet shows it; mRMR selected on the full matrix with permuted labels gives CV AUC 0.94, the same leakage the Skill warns about, and nothing shows how to keep it inside the fold.',
             root_cause='Method listed from the origin Skill without a worked example; the normalizer believed the package was absent (it is installed and works).',
             fix='Add a short in-fold mRMR transformer (or GridSearch-compatible FunctionTransformer) snippet using mrmr_classif with a DataFrame/Series, or state in the Skill that mRMR is described but not exemplified.',
             evidence='evidence/c5.json', touches='SKILL.md snippet or sentence; scripts/ unchanged',
             summary='No runnable in-fold mRMR despite advertising it.'),
    ],
    outcome=('Diagnostic score is **81/100**; the numeric band is Limited Release but the assertion-pass-rate floor (68%) forces a one-tier downgrade to **Beta Only**. '
             'Both veto gates pass. The bundled scripts and the leakage-safe pattern are sound and reproduce the Skill\'s central claim on real Golub data. '
             'The open weaknesses are the stability snippet (scale-dependent, not null-calibrated), an unexplained normalizer scoring change that moves signature size three-fold, and small script/snippet inconsistencies. '
             'No safety assertion (fabrication, PHI, destructive action) failed. This is an initial diagnostic audit, not certification: route six open findings to `fix-scientific-skill`, then independently re-audit.'),
    leads=('## Lead verification\n\n'
           '- **neg_log_loss / use_legacy_attributes=False**: correct and consistent (SKILL.md is the only call site; the scripts do not use LogisticRegressionCV). sklearn 1.9.1 emits the FutureWarning for the old defaults and names neg_log_loss as the 1.11 default. Not stated in this Skill and it moves signature size (BD-002).\n'
           '- **No scaler in SelectKBest+LR**: confirmed as an omission (BD-003). The lbfgs ConvergenceWarning did **not** reproduce on real labels (7,129 and 3,564 probes, 0 warnings); it occurs only under permuted labels.\n'
           '- **Leakage inside vs outside the fold**: reproduced on 10 permutations (0.846 vs 0.492). Both bundled scripts and every snippet keep selection and scaling in a Pipeline or declare themselves discovery-only; no performance number comes from selection data.\n'
           '- **Tooling Golub AUC 1.000**: not used as evidence; all Golub numbers here come from this run with no supervised step before the split.\n'
           '- **mrmr-selection**: installed and working (evidence/c5.json).'),
    coverage=('Environment: `F:\\OpenScience\\audit-envs\\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, numpy 2.5.3, Boruta 0.4.3, mrmr-selection 0.2.8), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6. '
              'Input: Golub 1999 ALL/AML (OpenML 1104) from staging `public-data`; label-free variance filter only. '
              'Executed: SelectKBest pipeline, BorutaPy, elastic-net LogisticRegressionCV, stability/Nogueira, mrmr_classif, both bundled scripts. '
              'Static-only: R glmnet (prose, no code; light-optional). No blocked surface; no input missing. Scripts: `scripts/run_cases.py` (cases c1-c7), `scripts/warn_probe.py`, builders. '
              'No audit-local repair was made; the candidate bytes were not modified (identity re-verified after execution).'),
)

build(spec, RUN, SKILL, ROOT)
