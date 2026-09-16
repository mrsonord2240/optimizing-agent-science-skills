import json, os

OUT = 'F:/OpenScience/audits/bio-proteomics-proteomics-qc'
SRC = 'mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:proteomics/proteomics-qc'

inputs = [
 dict(index=1, type='Canonical', label='Regression: MaxQuant LFQ QC before limma, plus the PTXQC createReport(txt_folder=...) decision-tree row run with and without Pandoc',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in1_canonical.py (all six SKILL.md python blocks exec\'d verbatim via pass5/skill.py) + pass5/p5_ptxqcA.R (clean session) and p5_ptxqcB.R (RSTUDIO_PANDOC set), PTXQC 1.1.5 / rmarkdown 2.31 / Pandoc 3.11, fresh qcA/ and qcB/ txt folders.',
   note='FIXER CLAIM REPRODUCED. All 6 python blocks of the FIXED SKILL.md exec cleanly and define all 10 named functions. Leg A (no Pandoc): pandoc_available() FALSE, createReport completes in 0.23 min, prints "The \'Pandoc\' converter is not installed ... Pandoc is required for HTML reports", and writes report.pdf + .mzQC + .yaml + _heatmap.txt with NO html -- exactly the "NOT fatal" behaviour the fix wrote into the Common Errors table and the PTXQC decision-tree row. Leg B (RSTUDIO_PANDOC=pandoc-3.11): pandoc_available() TRUE, same call adds a 1,367 kB HTML alongside the 59 kB PDF, 8 x 13 heatmap. Canonical QC numbers unchanged from pass-3 (contaminants 4.2-6.5%, 1560 -> 1500 rows, r 0.956-0.966, CV 24.3/23.6%, PCA PC1 ~ batch p=0.0000).',
   basic=37, specialized=55, total=92,
   assertions=[
     dict(text='Every python block in the fixed SKILL.md executes unchanged', result='PASS', note='6/6 blocks, 10/10 functions, no syntax or import failure on pandas 3.0.5 / numpy 2.5.3 / scikit-learn 1.9.1.'),
     dict(text='The Pandoc claim is correct: the PDF leg never depended on Pandoc', result='PASS', note='Leg A completed and wrote PDF, mzQC, YAML and heatmap with pandoc_available() FALSE.'),
     dict(text='Pandoc adds only the HTML report, and only when RSTUDIO_PANDOC (or PATH) points at it', result='PASS', note='Leg B is the only leg that produced report_*.html.'),
     dict(text='The corrected PTXQC table row matches the files the tool writes', result='PASS', note='"PDF (+ mzQC + YAML; HTML only when Pandoc is reachable)" is exactly the observed file set.'),
     dict(text='Canonical QC output is unchanged by the fix', result='PASS', note='Every metric identical to the pass-3 run.'),
   ]),
 dict(index=2, type='Variant A (the P1 driver)', label='Regression on real data: "Three DIA runs, one per condition, no replicates. QC them before I look at fold changes."',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in3_diann_real.py on the real PXD070049 DIA-NN 2.6.1 report (4,851 precursor rows, runs A/B/C), functions taken live from the fixed SKILL.md.',
   note='FIXER CLAIM REPRODUCED -- this is the input that produced the pass-3 P1 and all four degenerate-design guards now fire. raw_sample_qc prints "WARNING: single-sample group(s) [A, B, C]: the within-group loading rule cannot fire there ... A loading difference that tracks condition is NOT detectable in a design with no replicates" and falls back to an ALL-sample baseline. replicate_correlation raises "needs >=2 samples in a group; sizes are {A:1, B:1, C:1} ... do not report \'no outliers found\'". median_cv_linear raises "CV is undefined with no replicates -- report \'not measurable\', not NaN". pca_batch_check prints "PC1 ~ batch: NOT TESTABLE, level sizes [3] ... this is not evidence of no batch effect" instead of raising. Nothing silently returns an empty table any more. Residual: the Level-1 metrics the description advertises (RT/iRT fit, FWHM) are still prose -- the r=0.9996-0.9999 and 0.047-0.050 min FWHM in this output were computed by the auditor, not by anything the Skill ships.',
   basic=36, specialized=53, total=89,
   assertions=[
     dict(text='replicate_correlation and median_cv_linear fail loudly at n=1 instead of returning empty/NaN', result='PASS', note='Both raise ValueError naming the group sizes and the correct interpretation.'),
     dict(text='raw_sample_qc warns and falls back rather than silently reporting fold = 1.000', result='PASS', note='Warning printed, baseline column set to ALL, and the design limitation stated.'),
     dict(text='pca_batch_check reports NOT TESTABLE rather than raising or implying no batch effect', result='PASS', note='Level sizes printed with an explicit "this is not evidence of no batch effect".'),
     dict(text='The decision tree tells a no-replicate user what to report', result='PASS', note='New row: "One run per condition -> Report which checks could NOT run ... An empty correlation table and a NaN CV mean not measured, never clean."'),
     dict(text='Level-1 metrics the description advertises are backed by code or a threshold', result='FAIL', note='RT/iRT fit and FWHM remain prose in the Levels table; no function, no cutoff.'),
   ]),
 dict(index=3, type='Variant B', label='Regression: a failed-loading run hidden by MaxLFQ-normalised LFQ columns',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in3_failed.py on the synthetic data/proteinGroups_failed.txt.',
   note='Identical to pass-3. The loading rule applied to raw Intensity flags T4 (fold 0.409, ids 0.814); applied to LFQ intensity it flags nothing; T4\'s raw log2 MEDIAN fold is only 0.623 because left-censoring hides the loss, and after median normalisation every median is 0.0. The Skill\'s "apply the rule to TOTAL raw signal and ID count, not the boxplot median" is demonstrably the load-bearing instruction.',
   basic=37, specialized=55, total=92,
   assertions=[
     dict(text='The Skill\'s raw-total rule catches a failure that the normalised columns hide', result='PASS', note='T4 flagged on Intensity, not flagged on LFQ intensity.'),
     dict(text='The documented median-vs-total discrepancy reproduces', result='PASS', note='0.409 total vs 0.623 median, matching the Skill\'s stated 0.41x/0.62x example.'),
     dict(text='No sample is excluded without the rule being stated', result='PASS', note='Thresholds (>=2x low total, >15-20% fewer IDs) are printed with the decision.'),
     dict(text='Output is deterministic', result='PASS', note='Byte-identical to pass-3.'),
   ]),
 dict(index=4, type='Variant C', label='Regression: TMT channel balance across two 10-plexes plus MSstatsTMT normalisation arguments',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in4_tmt.py on synthetic data/tmt_plexA.csv + tmt_plexB.csv.',
   note='Identical to pass-3: no channel flagged within either plex, plex B/A median channel total 2.08 (a between-plex offset the within-plex rule correctly does not chase), positive control A/128C at x0.3 flagged at fold 0.403, and PCA on raw log2 reporters gives PC1 ~ plex p=0.0000. The Skill\'s warning that MSstatsTMT proteinSummarization global_norm=TRUE erases the balance view is still the right gotcha.',
   basic=34, specialized=51, total=85,
   assertions=[
     dict(text='tmt_channel_balance operates within plex, not across plexes', result='PASS', note='The 2.08x between-plex offset is left alone, as designed.'),
     dict(text='A planted channel failure is detected', result='PASS', note='A/128C at 0.3x flagged at fold 0.403.'),
     dict(text='The MSstatsTMT global_norm gotcha is stated with the fix', result='PASS', note='Common Errors row gives global_norm=FALSE, reference_norm=FALSE.'),
     dict(text='The reporter-ion matrix path has an output/threshold spec', result='FAIL', note='The 1.5x/0.67x investigate band is inside the code only; no stated reporting template for the QC decision.'),
   ]),
 dict(index=5, type='Stress / multi-part', label='Regression: batch fully confounded with condition, user demands batch correction before testing',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in7_confounded.py on the synthetic 8-sample set with 104 labelled true-DA proteins.',
   note='FIXER CLAIM REPRODUCED. crosstab shows day1 = 4 Control / 0 Treatment and day2 = 0 / 4, i.e. total confounding. Mean |log2FC| over the 104 truly changed proteins is 1.546 before batch removal and 0.000 after -- the fix wrote "went from 1.55 to 0.00" into SKILL.md and that is exactly the measurement. The pass-3 P2 is closed: the Skill now says "Report the design as non-identifiable and stop; do not correct, and do not test."',
   basic=36, specialized=53, total=89,
   assertions=[
     dict(text='The Skill refuses batch correction on a fully confounded design', result='PASS', note='Explicit stop instruction added, with the mechanism (batch and condition are the same variable).'),
     dict(text='The quantitative claim in the new text reproduces', result='PASS', note='1.546 -> 0.000 mean |log2FC| on 104 labelled true positives.'),
     dict(text='The Skill still distinguishes correctable from non-correctable batch structure', result='PASS', note='Balanced case: batch in the design matrix; plots-only removeBatchEffect; confounded case: stop.'),
     dict(text='No corrected matrix is handed onward for testing', result='PASS', note='The instruction is "do not correct, and do not test".'),
   ]),
 dict(index=6, type='Edge / boundary', label='Regression: suspected sample swap -- C2 and T3 columns exchanged',
   status='COMPLETED', status_flag='WARN', executed=True,
   execution_note='pass5/in6_swap.py on the synthetic 8-sample set with two columns deliberately exchanged.',
   note='Unchanged from pass-3, and the gap is unchanged too. raw_sample_qc flags nothing (correct -- a swap is not a loading failure) and the within-group r table alone does not isolate it (all pairs 0.93-0.96). The swap only becomes visible under a mean-centred own-group vs other-group correlation, which the auditor had to write: C2 own -0.510 / other +0.141 and T3 own -0.508 / other +0.132. The Skill\'s decision-tree row "Check if it correlates better with a DIFFERENT group" states the idea but ships no code for it.',
   basic=33, specialized=50, total=83,
   assertions=[
     dict(text='The Skill names the correct diagnostic for a suspected swap', result='PASS', note='"Check if it correlates better with a DIFFERENT group" is precisely what identified C2/T3.'),
     dict(text='The Skill ships code for that diagnostic', result='FAIL', note='No cross-group correlation function; replicate_correlation computes within-group pairs only.'),
     dict(text='The Skill does not misattribute the swap to a loading failure', result='PASS', note='raw_sample_qc flags nothing and the Skill separates the two causes.'),
     dict(text='Output is deterministic', result='PASS', note='Byte-identical to pass-3, PCA included, now that the PCA is seeded.'),
   ]),
 dict(index=7, type='Adversarial / reproducibility (NEW this pass)', label='"Our QC PCA printed one batch p-value yesterday and a different one today on the same file. Is our data unstable, or is your code?"',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in7_determinism.py -- the fixed SKILL.md pca_batch_check called 6x, against a reconstruction of the pre-fix `PCA(n_components=n_pc)` line called 6x, on both the 738x8 QC matrix and a wide 20x600 matrix.',
   note='FIXER CLAIM REPRODUCED EXACTLY, with a nuance the fix log does not state. On the wide 20x600 matrix the pre-fix construction gives SIX different PC3 p-values (0.56520, 0.69045, 0.69205, 0.69796, 0.72069, 0.89537 -- a 0.33 spread), while the fixed seeded function gives one identical stdout across 6 calls. On the 738x8 QC matrix the unseeded path is ALREADY deterministic (sklearn\'s auto solver picks exact full SVD at that shape), so the defect only bites on wide matrices -- which is exactly what the new SKILL.md note says ("randomized on wide matrices") and it means the fix changes no existing small-n result. svd_solver=\'full\' plus random_state=0 is the right call at QC sizes.',
   basic=38, specialized=55, total=93,
   assertions=[
     dict(text='The fixed pca_batch_check is byte-identical across repeated identical calls', result='PASS', note='1 distinct stdout across 6 runs on both matrices.'),
     dict(text='The defect the fix claims to remove was real', result='PASS', note='6 distinct PC3 p-values from 6 unseeded fits on 20x600.'),
     dict(text='The new Version Compatibility note correctly scopes the problem to wide matrices', result='PASS', note='Confirmed: 738x8 unseeded is already stable; 20x600 is not.'),
     dict(text='The fix does not silently change previously reported small-n results', result='PASS', note='Seeded and unseeded agree to 6 dp on the 8-sample matrix.'),
     dict(text='The shipped example is seeded too', result='PASS', note='examples/qc_analysis.py now constructs PCA(n_components=3, svd_solver=\'full\', random_state=0).'),
   ]),
 dict(index=8, type='Scope boundary (NEW this pass)', label='"We have four runs: two controls, one treated, one treated+drug. Run your full QC and tell me what you can and cannot conclude."',
   status='COMPLETED', status_flag='WARN', executed=True,
   execution_note='pass5/in8_mixed_design.py -- a PARTIALLY degenerate design (group sizes 2/1/1) on synthetic data. The fixer verified only the all-singleton case; this is the untested middle.',
   note='The guards behave correctly in the case the fix log never tested. raw_sample_qc warns about the two singleton groups only and keeps the real within-group baseline for Control. replicate_correlation does NOT raise (one group has 2 samples), returns the single real Control pair r=0.962, and prints "no within-group pairs for [Treated, Treated_drug]; those samples are UNCHECKED here". median_cv_linear returns Control 16.2% with the singletons NaN and warns "its CV is NaN (undefined), not low". pca_batch_check prints NOT TESTABLE with level sizes [2,1,1]. NEW FINDING: every one of those caveats is a print() to stdout -- the RETURNED objects still carry a bare NaN for Treated/Treated_drug in median_cv_linear and simply omit them from replicate_correlation. An agent consuming the return value, which is how this Skill is meant to be used, sees NaN and absence with no machine-readable signal that the groups were unmeasurable.',
   basic=34, specialized=53, total=87,
   assertions=[
     dict(text='Partially degenerate designs compute what is computable instead of raising', result='PASS', note='Control r and CV both returned; only the singletons are marked.'),
     dict(text='Unmeasurable groups are called out rather than passed off as clean', result='PASS', note='Explicit WARNING lines for both singleton groups from all three functions.'),
     dict(text='The caveat reaches the caller, not just the terminal', result='FAIL', note='Warnings are print() only; the returned frames carry NaN / silent omission with no flag column or status field.'),
     dict(text='pca_batch_check refuses a meaningless 2-vs-1 ANOVA', result='PASS', note='NOT TESTABLE with level sizes [2,1,1], which is stricter than f_oneway\'s own requirement and correct here.'),
     dict(text='No QC conclusion is drawn for the groups with no replicate evidence', result='PASS', note='Output ends by stating Treated and Treated_drug have no within-group evidence at all.'),
   ]),
]

for i in inputs:
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['assertions_total'] = len(i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'], i['index']

exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (11, 12, 'Completeness 3 (unchanged): Levels 1-2 and DIA matrix construction are still prose, and the real DIA-NN run shows the Level-1 metrics the description advertises (RT/iRT fit, FWHM) still have no code and no threshold -- the auditor had to compute them. Correctness 4: the PTXQC decision-tree row and Tool table are now accurate about what createReport writes with and without Pandoc, verified both ways; the new "one run per condition" row is correct. Appropriateness 4.'),
 'reliability': (11, 12, 'Fault tolerance 4 (up from 3): the pass-3 silent-degradation defect is gone -- replicate_correlation and median_cv_linear raise with the group sizes, raw_sample_qc warns and falls back, pca_batch_check prints NOT TESTABLE, all four confirmed on real 3-run DIA-NN data and again on an untested 2/1/1 design. Error reporting 4 (up from 3): four Common Errors rows rewritten or added with texts reproduced verbatim from the tools (Pandoc message, PCA p-value drift, empty replicate/CV tables, the dual cause of "At least two samples are required; got 1"). Recoverability 3: idempotent and stateless, but the degenerate-design caveats are print() rather than parseable status.'),
 'performance_context': (6, 8, 'Token cost 3: SKILL.md grew 321 -> 369 lines (+15%) and still carries 13 references with no references/ split; the additions are guards and error rows, not padding. Execution efficiency 3: the python functions are vectorised and fast; createReport takes 0.23 min without Pandoc and 0.34 min with it on an 8-run synthetic txt/ folder.'),
 'agent_usability': (14, 16, 'Learnability 4: the raw-column-per-tool table and the loading rule were followed verbatim on real DIA-NN output again. Consistency 3: raw_sample_qc warns and continues where the other two raise when nothing is computable -- defensible but not uniform. Feedback design 3: the new WARNING / NOT TESTABLE lines are good terminal feedback, but there is still no QC report or exclusion-decision template, and the caveats never reach the returned objects. Error prevention 4: names the un-normalised column per tool, forbids CV on logs, and now forbids testing a confounded design.'),
 'human_usability': (7, 8, 'Discoverability 4: the description names the symptoms a researcher actually types. Forgiveness 3 (Category 3 override applied): input requirements and error messages are explicit and now name the design that caused them; no deduction for strict rejection.'),
 'security': (11, 12, 'Credential safety 4: no credentials or tokens; the only network access observed was PTXQC fetching the public HUPO-PSI psi-ms.obo controlled vocabulary. Input validation 3: pca_batch_check and now the two replicate functions validate; the rest assume well-formed frames. Data safety 4: read-only analysis; the only writes are PTXQC\'s own report files into the folder the user names.'),
 'maintainability': (9, 12, 'Modularity 3, modifiability 3, testability 3: examples/qc_analysis.py is now seeded and reproducible, but it still states no expected output, so a regression cannot be checked against the file itself.'),
 'agent_specific': (18, 20, 'Trigger precision 4, progressive disclosure 3, composability 3. Idempotency 4 (up from 3): PCA is seeded with svd_solver="full", random_state=0 in both SKILL.md and the example, and six identical calls now produce one identical stdout where six unseeded fits on a wide matrix produced six different p-values. Escape hatches 4 (up from 3): the pass-3 gap is closed -- a batch fully confounded with condition is now an explicit, quantified stop ("report the design as non-identifiable and stop; do not correct, and do not test").'),
}
static = sum(v[0] for v in cats.values())

report = {
 'meta': {
   'skill_name': 'bio-proteomics-proteomics-qc',
   'description': 'Quality control for bottom-up proteomics: three-level QC (instrument, identification, quantification), the raw-total loading rule, replicate correlation and CV on the right scale, missingness diagnosis, PCA/batch inspection, TMT channel balance, and PTXQC reporting.',
   'source': SRC,
   'evaluated_on': '2026-09-15',
   'evaluator_version': 'skill-auditor@1.0',
   'category': 'Data Analysis',
   'execution_mode': 'A',
   'complexity': 'Complex',
   'n_inputs': 8,
   'execution_note': 'Pass-5 confirmation audit of the FIXED Skill at fork commit 45a0c5a (fix commit 95a8460), superseding the pass-3 report that scored 85. All 8 inputs executed. All six SKILL.md python blocks are extracted programmatically from the fork path and exec\'d unchanged (pass5/skill.py). Inputs 1-6 re-run the pass-3 scripts unchanged as regression tests; Inputs 7 and 8 are new, written for this pass. Complexity is Complex (7 required); 8 were run so the whole previous set survives as regression alongside the two new ones. Real data: PXD070049 DIA-NN 2.6.1 report, 3 runs, one per condition. Synthetic data in data/ and pass5/qcA, qcB. R legs via the candidate r.sh with PTXQC 1.1.5, rmarkdown 2.31, Pandoc 3.11.'
 },
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS',
     'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {
     'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or results. Both quantitative claims the fix wrote into SKILL.md were independently reproduced: six unseeded PCA fits on a 20x600 matrix gave six different PC3 p-values while the seeded function gives one, and mean |log2FC| over 104 labelled true-DA proteins went from 1.546 to 0.000 after batch removal on a fully confounded design (SKILL.md says "1.55 to 0.00").'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'No output diagnoses, prescribes or triages an individual. The Skill operates on run- and sample-level QC metrics only and stops at "report the design as non-identifiable" rather than producing a result.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'The pass-3 defect that most threatened this gate -- QC functions returning an empty table or a table of NaNs at n=1, which reads as "clean" -- is fixed and verified on the real 3-run DIA-NN data and on an untested partially degenerate 2/1/1 design. CV is still required on linear scale, Pearson still required after log2, batch correction on a confounded design is now explicitly refused.'},
     'code_usability': {'result': 'PASS', 'detail': 'All six SKILL.md python blocks exec unchanged and define all ten named functions on pandas 3.0.5 / numpy 2.5.3 / scikit-learn 1.9.1; every function was called on real or synthetic data. The R leg (PTXQC createReport) completed in both the with-Pandoc and without-Pandoc configuration. examples/qc_analysis.py runs and is now seeded.'}
   }
 },
 'static_score': {'subtotal': static, 'max': 100,
   'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': exec_avg, 'max': 100,
   'assertion_pass_rate': {'passed': ap, 'total': at}, 'inputs': inputs},
 'final': {
   'static_weighted': round(static * 0.4, 1),
   'dynamic_weighted': round(exec_avg * 0.6, 1),
   'score': round(static * 0.4 + exec_avg * 0.6, 1),
   'max': 100, 'grade': 'Production Ready', 'grade_symbol': '\u2b50',
   'deployable': True, 'veto_override': False
 },
 'key_strengths': [
   'The silent-degradation class of defect is gone and stays gone in a case the fixer never tested: on real 3-run DIA-NN data and on a 2/1/1 design, every QC function either raises with the group sizes, warns and falls back to a stated baseline, or prints NOT TESTABLE -- none of them returns an empty table or a NaN that could be read as "clean".',
   'PCA is now reproducible and the fix is correctly scoped: six unseeded fits on a wide 20x600 matrix give six different PC3 p-values, the seeded function gives one, and at QC sample sizes the seeded and unseeded results agree to six decimal places, so no previously reported small-n result silently changes.',
   'The PTXQC/Pandoc story is now accurate in both directions, verified by running createReport twice: without Pandoc it completes and writes PDF + mzQC + YAML + heatmap; with RSTUDIO_PANDOC set it additionally writes a 1.37 MB HTML.',
   'A batch fully confounded with condition is an explicit, quantified stop rather than a correction -- and the quantity (mean |log2FC| 1.55 -> 0.00 on 104 labelled true positives) reproduces exactly.',
   'The raw-total loading rule remains the load-bearing insight and still catches a failure that every normalised column hides (0.41x total flagged, 0.62x median not, all medians identical after normalisation).'
 ],
 'recommendations': [
   {'priority': 'P1',
    'title': 'The new degenerate-design caveats are print() only and never reach the returned objects',
    'observed_in': 'Inputs 2, 8',
    'problem': 'When some but not all groups are singletons, median_cv_linear returns a frame with a bare NaN in median_cv_pct for those groups and replicate_correlation simply omits them, while the explanation goes to stdout. An agent (the intended caller of this Skill) that consumes the return value sees NaN and absence with no machine-readable signal that the group was unmeasurable -- which is the exact misreading the fix set out to prevent, moved one layer down.',
    'root_cause': 'The all-singleton case was fixed with a raise (which the caller cannot miss) and the partial case with a print (which it can).',
    'fix': 'Return the status in the data: add a `status` column to median_cv_linear (\'measured\' / \'not_measurable_n1\') and an `unchecked_groups` entry (or a second returned frame) to replicate_correlation, and have pca_batch_check return the per-PC test status alongside coords rather than only printing it.'},
   {'priority': 'P2',
    'title': 'Levels 1-2 and DIA matrix construction are still prose only',
    'observed_in': 'Input 2',
    'problem': 'The description advertises instrument-level QC, and the Levels table names RT/iRT fit and FWHM, but no function and no threshold is offered for either. On the real DIA-NN report those metrics were sitting in columns the Skill already tells the reader to load (RT, Predicted.RT, FWHM, Quantity.Quality) and the auditor had to compute r = 0.9996 and median FWHM 0.050 min by hand.',
    'root_cause': 'The python blocks cover Levels 2-3 only; Level 1 was left as taxonomy.',
    'fix': 'Add one short block: correlate RT against Predicted.RT per run, report median FWHM and median Quantity.Quality per run, and give the thresholds you would act on (e.g. RT/iRT r < 0.99, FWHM drift > 1.5x across runs).'},
   {'priority': 'P2',
    'title': 'Sample-swap detection is named in the decision tree but has no code',
    'observed_in': 'Input 6',
    'problem': 'The row "Replicate correlation low for one sample -> Check if it correlates better with a DIFFERENT group" is the correct diagnostic and it is what identified the planted C2/T3 swap, but replicate_correlation computes within-group pairs only. The auditor had to write the mean-centred own-vs-other comparison; the within-group table alone shows nothing (all pairs 0.93-0.96).',
    'root_cause': 'The insight was captured in the decision tree and never turned into a function.',
    'fix': 'Extend replicate_correlation (or add cross_group_correlation) to report, per sample, mean centred r against its own group and against every other group, and flag any sample whose best match is not its own label.'},
   {'priority': 'P2',
    'title': 'No QC report or exclusion-decision template',
    'observed_in': 'Inputs 1, 4, 6',
    'problem': 'The Skill instructs the reader to document and justify every exclusion and to run a sensitivity check, but ships no structure for either, so each run produces a different ad-hoc write-up and the TMT investigate band exists only inside the code.',
    'root_cause': 'Reporting was left to the caller.',
    'fix': 'Add a short template: per sample, the metric that failed, its value and threshold, the decision, and the with/without sensitivity result -- then point the TMT and loading rules at it.'},
   {'priority': 'P2',
    'title': 'examples/qc_analysis.py still states no expected output',
    'observed_in': 'Input 1',
    'problem': 'The example is now seeded and therefore reproducible, but nothing in the file says what it should print, so it cannot serve as its own regression test the way protein-inference\'s example does.',
    'root_cause': 'The fix seeded the PCA without adding the expected-output docstring.',
    'fix': 'Add the "Expected output:" block at the top of the file, now that the seeding makes the numbers stable.'}
 ]
}

with open(os.path.join(OUT, 'eval_report_bio-proteomics-proteomics-qc_result.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print('static', static, 'exec_avg', exec_avg, 'final', report['final']['score'], 'assertions', ap, '/', at)
