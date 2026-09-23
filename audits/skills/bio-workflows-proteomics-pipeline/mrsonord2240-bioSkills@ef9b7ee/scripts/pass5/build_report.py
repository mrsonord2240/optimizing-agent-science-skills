import json, os

OUT = 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
SRC = 'mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:workflows/proteomics-pipeline'

inputs = [
 dict(index=1, type='Canonical', label='Regression: MaxQuant LFQ proteinGroups.txt, 4 control vs 4 treated, two batches, to a differential protein table',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in1.R -- the fixed "Complete R Workflow" block re-extracted byte-for-byte from the fixed SKILL.md into pass5/blocks/ and run with sys.source(). R 4.4.3, limma 3.62.2.',
   note='FIXER CLAIM REPRODUCED byte for byte. 1560 file lines all read, 1500 rows after the flag filter, 0 REV/CON left, no failed sample, 1323 proteins tested, design columns "Control Treatment factor.batch.B2" with batch in the design, 18 non-estimable contrasts reported rather than swallowed, and 62 significant (Up 35, Down 27) with 0 false positives among true nulls. The new contrast machinery emits "contrasts: Treatment_vs_Control" and the per-contrast breakdown line, and decideTests(method="global") over a single contrast reproduces the previous per-contrast BH exactly -- the two-condition result is unchanged, which is what the fix claimed. Null centre after median normalisation -0.0323 on this balanced set.',
   basic=37, specialized=53, total=90,
   assertions=[
     dict(text='The two-condition result is unchanged by the multi-contrast rewrite', result='PASS', note='62 called, Up 35 / Down 27, 18 non-estimable, 0 false positives -- identical to pass-3.'),
     dict(text='Batch enters the design as a covariate when the annotation has one', result='PASS', note='design columns include factor.batch.B2; has_batch TRUE.'),
     dict(text='Non-estimable contrasts are reported, not turned into NA-poisoned sums', result='PASS', note='18 reported separately as undetected-in-group.'),
     dict(text='The executed path contains no unseeded randomness', result='PASS', note='Two runs of the same block gave identical counts; no imputation in the path.'),
   ]),
 dict(index=2, type='Variant A', label='Regression: DIA-NN report.parquet for the same 8 samples, through the DIA-NN block to limma',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in2.R on the fixed b05 DIA-NN block, arrow 23.0.1.2.',
   note='Unchanged from pass-3: 23,020 report rows, 20,170 after the q-value filter, an 887 x 8 matrix with 0 zero cells and 0 low-confidence groups, the is.infinite guard leaves no -Inf, and limma eBayes(trend, robust) completes. 73 called at BH 5% with 5 false positives among 809 true nulls, 68 of 72 true changers recovered, raw p < 0.05 at 6.4% against a nominal 5%.',
   basic=35, specialized=51, total=86,
   assertions=[
     dict(text='The DIA-NN block produces a finite log2 matrix limma can fit', result='PASS', note='0 -Inf/Inf, 0 NaN, rownames set, eBayes completes.'),
     dict(text='Precursor and protein-group q-values are both applied', result='PASS', note='23,020 -> 20,170 rows; 0 low-confidence groups survive.'),
     dict(text='Calibration is acceptable on labelled truth', result='PASS', note='raw p<0.05 at 6.4% vs nominal 5%; 5 FP among 809 nulls at BH 5%.'),
     dict(text='Zeros are treated as missing rather than as measurements', result='PASS', note='0 zero cells in the matrix; the block converts them before log.'),
   ]),
 dict(index=3, type='Variant B (the P1 fix)', label='Three-condition dose design (Control / LowDose / HighDose, n=4 each, two batches) through the Complete R Workflow block',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in8_3cond.R on synthetic data from pass5/make_3cond.py (1,200 proteins; 60 dose_up, 60 dose_down, 30 high_only, 1,050 null). The block is run VERBATIM -- no edit to the contrast line.',
   note='FIXER CLAIM REPRODUCED EXACTLY, and it closes the pass-3 ERROR. The block completes end to end: design columns "Ctl High Low factor.batch.B2", contrasts "High_vs_Ctl Low_vs_Ctl" built from the factor levels, 123 non-estimable reported, and High_vs_Ctl called 20 with 0 false positives among 780 tested true nulls, Low_vs_Ctl called 0 -- the fix log claims "20 called with 0 false positives among 780 true nulls, Low_vs_Ctl 0". The second P1 is closed in the SAME run: the complete-case set is 0 proteins on these 12 samples, which previously aborted the workflow with prcomp "a dimension is zero"; the new guard prints "PCA skipped: only 0 protein(s) observed in EVERY sample ... Do NOT impute to fill the matrix", falls back to the pairwise-complete Spearman correlation, and the statistics below still run. NEW OBSERVATION: Low_vs_Ctl calling 0 is partly a real threshold effect -- the planted LowDose effect is 0.7 log2 against the block\'s fixed treat(lfc = log2(1.5)) = 0.585 floor plus a global BH -- and nothing in the multi-condition text warns that the fold-change floor bites hardest on the intermediate level of a dose series.',
   basic=37, specialized=53, total=90,
   assertions=[
     dict(text='A three-condition design completes without editing the block', result='PASS', note='Contrasts built from levels(sample_info$condition); no "object Treatment not found".'),
     dict(text='The claimed 20 calls / 0 false positives among 780 nulls reproduce', result='PASS', note='High_vs_Ctl 20 called (Up 8, Down 12), 0 of 780 tested nulls.'),
     dict(text='The prcomp halt is guarded and the workflow continues', result='PASS', note='0 complete cases; PCA skipped with an explanatory message and a correlation fallback; statistics still ran.'),
     dict(text='Multiplicity is controlled across the contrast family, not within each', result='PASS', note='decideTests(method = "global") over every protein x contrast cell, and identical to per-contrast BH when there is one contrast.'),
     dict(text='The reader is warned where the fixed fold-change floor will bite on a dose series', result='FAIL', note='Low_vs_Ctl returns 0 calls at a real 0.7 log2 effect against the treat() 0.585 floor; nothing in the new text flags this for intermediate dose levels.'),
   ]),
 dict(index=4, type='Edge / boundary (NEW this pass)', label='"Our sample_annotation.csv is not in the same order as the intensity columns -- does that matter?"',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_match.R -- the fixed block run on an annotation shuffled to a random row order, against a reconstruction of the pre-fix `%in%` subset line on exactly the same input.',
   note='THE FIX IS REAL AND THE BUG IT REMOVES WAS SEVERE. The fixed block uses sample_info[match(colnames(normalized), sample_info$sample), ] plus stopifnot(!any(is.na(sample_info$sample))). With the annotation shuffled to C3,T2,C1,T3,C4,C2,T1,T4 the fixed block restores C1..T4 column order and returns 62 significant (Up 35, Down 27), protein-for-protein identical to the unshuffled run. Reverting only that one line to the pre-fix `sample_info[sample_info$sample %in% colnames(normalized), ]` leaves the annotation in shuffled order, lmFit pairs design rows with matrix columns positionally, and the same data returns 0 significant proteins -- all 62 calls lost, max |logFC| difference 2.80, with NO error and no warning. A silent wrong-design fit, found by the fixer and fixed correctly.',
   basic=38, specialized=54, total=92,
   assertions=[
     dict(text='The fixed block is invariant to annotation row order', result='PASS', note='Shuffled and unshuffled runs agree protein-for-protein on every call.'),
     dict(text='The pre-fix line really did produce a silently wrong fit', result='PASS', note='0 significant instead of 62, max |logFC| difference 2.80, no error raised.'),
     dict(text='A sample present in the matrix but missing from the annotation is caught', result='PASS', note='stopifnot(!any(is.na(sample_info$sample))) after the match.'),
     dict(text='The comment explains WHY, not just what', result='PASS', note='"lmFit pairs design rows with matrix columns POSITIONALLY ... Never subset the annotation with %in% alone here."'),
   ]),
 dict(index=5, type='Variant C', label='Regression + new guard: TMT10 HCD mzML, reporter extraction and lot-CoA impurity correction, including a transposed certificate',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_coa.R and pass5/p5_coa2.R -- the new orientation guard run as SKILL.md writes it on the correct CoA, a transposed copy and a fractions-instead-of-percent copy; then purityCorrect run with the transposed matrix to confirm the old check is blind.',
   note='FIXER CLAIM REPRODUCED. The orientation guard discriminates cleanly: correct orientation row_dev 18.36 vs col_dev 76.46 (passes); transposed sheet row_dev 76.46 vs col_dev 18.36 (fires with "CoA looks TRANSPOSED: column sums fit 100% better than row sums"); a CoA read as fractions rather than percentages is caught by the companion stopifnot(all(diag(coa) > 50)). Independently confirmed that the guard was needed: purityCorrect with the transposed matrix produces 0 negative values, exactly as with the correct one, so the pre-fix stopifnot(sum(exprs < 0) == 0) passes either way -- the comment that used to call it a transposition test was wrong and has been corrected in place.',
   basic=36, specialized=52, total=88,
   assertions=[
     dict(text='The new guard fires on a transposed CoA and passes the correct one', result='PASS', note='Row/column sum-to-100 comparison separates them by a factor of 4 in both directions.'),
     dict(text='The old negative-count check provably could not detect a transposition', result='PASS', note='0 negatives with the transposed matrix, same as with the correct one.'),
     dict(text='The misleading comment on the old check was corrected rather than left', result='PASS', note='It now reads "negatives = a grossly wrong matrix (NOT a transposition test; see above)".'),
     dict(text='A unit error (fractions vs percentages) is also caught', result='PASS', note='stopifnot(all(diag(coa) > 50)) fires on coa/100.'),
   ]),
 dict(index=6, type='Stress / multi-part', label='Regression: MSstats feature-level branch on evidence.txt + proteinGroups.txt + annotation.csv, plus the compositional-bias claim the fix added',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in5.R (the fixed b02 MSstats block, verbatim) and pass5/p5_bias.R against labelled truth. MSstats 4.14.2.',
   note='FIXER CLAIM REPRODUCED TO THE DIGIT. The block reads 10,369 of 10,369 evidence rows and 1,560 of 1,560 proteinGroups rows (the quoting/row-count fix from an earlier pass still holds) and summarizes 296 proteins. Of those, 179 are true nulls, 44 up, 26 down -- and after equalizeMedians every true null is shifted by mean -0.1934 log2 (t vs 0, p = 2.29e-55), with 21 of 179 true nulls called at BH 5%, ALL negative. SKILL.md now states "44 up vs 26 down among 296 proteins: every true null moved -0.19 log2 (t vs 0, p = 2e-55) and 21 of 179 true nulls were called at BH 5%, all negative" -- in two places, and both match. The remedies it offers (normalization = FALSE with externally normalized input, or globalStandards with a spike-in set, plus a null-centre check) are the right ones.',
   basic=36, specialized=52, total=88,
   assertions=[
     dict(text='The compositional-bias numbers written into SKILL.md reproduce', result='PASS', note='-0.1934 log2, p = 2.29e-55, 21 of 179, all negative.'),
     dict(text='Neither MaxQuant table is silently truncated', result='PASS', note='10,369/10,369 and 1,560/1,560 rows read.'),
     dict(text='The Skill offers an executable remedy, not just a warning', result='PASS', note='normalization = FALSE / globalStandards with globalStandardName, plus the null-centre check.'),
     dict(text='The 296-protein MSstats result is directly comparable to the limma branch', result='PASS', note='Same truth table, same contrast direction, both documented as Treatment - Control.'),
   ]),
 dict(index=7, type='Adversarial', label='Regression: SILAC, 3 replicates, Ratio H/L normalized -- "skip the fancy stats, just t-test every protein against zero"',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in7.R on the fixed b04 SILAC block, synthetic ratios from make_silac_pg.py.',
   note='Unchanged from pass-3 and still the right refusal, with numbers. The Skill route (>= 2 finite ratios, moderated one-sample limma, BH) tests 453 of 500 proteins and calls 49 at BH 5% -- all 49 true changers, 0 false positives, full recovery. What the user asked for, raw p < 0.05, calls 62 of which 13 are false positives. And the naive apply(t.test) over the raw matrix that the user implied dies with "not enough \'x\' observations" on a protein quantified in one replicate, which is exactly the Common Errors row.',
   basic=37, specialized=52, total=89,
   assertions=[
     dict(text='The raw-p request is refused with a quantified cost', result='PASS', note='62 called with 13 false positives vs 49 called with 0.'),
     dict(text='The >=2-finite-ratio filter prevents the documented t.test crash', result='PASS', note='Naive apply(t.test) over the raw matrix reproduces "not enough x observations"; the block does not.'),
     dict(text='BH-adjusted p is reported, never the raw p', result='PASS', note='result carries adj.P.Val and the block selects on it.'),
     dict(text='Recovery is not sacrificed for the added rigour', result='PASS', note='49 of 49 testable true changers recovered.'),
   ]),
 dict(index=8, type='Scope boundary', label='Regression: "Plasma proteomics on 30 ICU sepsis patients -- tell me which patients to escalate today"',
   status='COMPLETED', status_flag='PASS', executed=False,
   execution_note='Text scope-boundary input; no code is appropriate, so nothing was executed. Re-evaluated against the CURRENT SKILL.md and usage-guide text at 45a0c5a.',
   note='Unchanged from pass-3 and still correct. The Skill is framed end to end as a cohort-level discovery workflow -- design, QC, normalization, group contrasts -- with no per-subject output anywhere, and its hand-offs route interpretation to pathway and annotation Skills rather than to any clinical decision. Nothing the fix added moved toward individual-level inference; the new multi-condition contrast machinery is still a group comparison. The correct answer is to decline the triage request and offer the cohort analysis, and nothing in the Skill invites otherwise.',
   basic=36, specialized=52, total=88,
   assertions=[
     dict(text='No output of this Skill is an individual-level clinical statement', result='PASS', note='Every documented result is a protein x contrast table over groups.'),
     dict(text='The fix did not introduce any per-subject inference', result='PASS', note='The multi-condition path adds group contrasts only.'),
     dict(text='The Skill routes interpretation onward rather than concluding', result='PASS', note='Explicit hand-offs to the pathway/annotation Skills, all of which exist in the fork.'),
     dict(text='No diagnostic, prognostic or treatment recommendation appears anywhere', result='PASS', note='Checked across SKILL.md, usage-guide.md and examples/proteomics_workflow.R.'),
   ]),
]

for i in inputs:
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['assertions_total'] = len(i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'], i['index']

exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (11, 12, 'Completeness 3: the pass-3 P1 is closed -- designs with more than two conditions now run and the MSstats branch documents a worked three-condition comparison matrix -- but FragPipe is still named without code and the MSstatsTMT multi-plex route is still a comment block. Correctness 4 (up from 3): a silent wrong-design fit (annotation subset by %in% without reordering) has been removed and reproduced as real, the CoA orientation comment that claimed a test it did not perform has been corrected, and the median-normalisation symmetry assumption is now stated with a measured consequence. Appropriateness 4.'),
 'reliability': (11, 12, 'Fault tolerance 4 (up from 3): the prcomp halt is guarded and verified firing on the exact 12-sample design that used to abort the workflow at step 5 of 7, with a correlation fallback and the statistics still running; the CoA orientation guard fires on a transposed sheet and on a units error; stopifnot catches an annotation missing a sample. Error reporting 4 (up from 3): four new Common Errors rows, and I reproduced the underlying condition for three of them plus the measurement quoted in the fourth. Recoverability 3: re-running with corrected inputs is clean, but the guards are message()/stop() rather than structured codes.'),
 'performance_context': (5, 8, 'Token cost 2 (down from 3): 396 -> 479 lines in a single file with no references/ directory. The growth is load-bearing (a generalised contrast path, three guards, four error rows) but this is an always-loaded workflow Skill. Execution efficiency 3: the executed path is the recommended one, limma on observed values with no imputation; the MSstats branch dominates runtime as expected.'),
 'agent_usability': (14, 16, 'Learnability 3: one long linear block. Consistency 4 (up from 3): the pass-3 P2 is closed -- usage-guide.md\'s annotation template now carries the batch column the design branch keys on and states that condition may have more than two levels, matching what the code does. Feedback design 3: the per-contrast breakdown is a real improvement but there is still no stated schema for the result table. Error prevention 4 (up from 3): the example now warns in place that editing sample_groups to three conditions will fail and points at the SKILL.md block that handles it.'),
 'human_usability': (7, 8, 'Discoverability 3: natural prompts, clear stage names. Forgiveness 4 (up from 3): the workflow is now order-invariant in its annotation, degrades to a correlation matrix instead of aborting when PCA is impossible, and examples/proteomics_workflow.R still simulates its own input and exits 0 from an empty directory.'),
 'security': (11, 12, 'Credential safety 4 and data safety 4: no credentials, no network calls, no retention, no eval/exec of user strings. Input validation 3: eight executable validity checks now exist in the main block and the TMT branch, but the DIA-NN and SILAC branches still carry lighter checking than the LFQ path.'),
 'maintainability': (9, 12, 'Modularity 3: one block per workflow variant. Modifiability 3: the same PCA-guard and contrast logic now lives twice, in SKILL.md and in examples/proteomics_workflow.R, and the example deliberately keeps the two-condition contrast while SKILL.md generalises it. Testability 3: the example runs from an empty directory but states no expected output.'),
 'agent_specific': (18, 20, 'Trigger precision 3, progressive disclosure 3 (still one long file, no references/), composability 4 (depends_on plus explicit hand-offs; all referenced Skills present), idempotency 4 (no RNG in the executed path; repeated runs identical), escape hatches 4 (up from 3): the PCA fallback and the CoA orientation stop are both proper escape hatches that say what to do next.'),
}
static = sum(v[0] for v in cats.values())

report = {
 'meta': {
   'skill_name': 'bio-workflows-proteomics-pipeline',
   'description': 'End-to-end bottom-up proteomics workflow: MaxQuant/DIA-NN/MSstats/TMT/SILAC input handling, raw-distribution QC before normalization, per-group completeness filtering, batch as a covariate, and limma/MSstats differential analysis with a moderated minimum-fold-change test.',
   'source': SRC,
   'evaluated_on': '2026-09-15',
   'evaluator_version': 'skill-auditor@1.0',
   'category': 'Data Analysis',
   'execution_mode': 'A',
   'complexity': 'Complex',
   'n_inputs': 8,
   'execution_note': 'Pass-5 confirmation audit of the FIXED Skill at fork commit 45a0c5a (fix commit d61774d), superseding the pass-3 report that scored 81. 7 of 8 inputs executed end to end on R 4.4.3 via the candidate r.sh (limma 3.62.2, MSstats 4.14.2, MSnbase 2.32.0, arrow 23.0.1.2); Input 8 is a text scope-boundary input for which no code is appropriate. All five fenced R blocks were re-extracted byte-for-byte from the FIXED SKILL.md into pass5/blocks/ and run with sys.source(). Inputs 1, 2, 6, 7 and 8 re-run the pass-3 set as regression; Input 3 is the three-condition design that ERRORED in pass 3; Input 4 is a new input written for this pass to test the annotation-order fix against a reconstruction of the pre-fix line; Input 5 adds the new CoA orientation guard. All data SYNTHETIC with labelled truth.'
 },
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS',
     'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {
     'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or results. Both quantitative claims the fix wrote into SKILL.md reproduced: the three-condition design gives 20 calls with 0 false positives among 780 true nulls, and the compositional-bias measurement is -0.1934 log2 with t vs 0 p = 2.29e-55 and 21 of 179 true nulls called at BH 5%, all negative -- against SKILL.md\'s "-0.19", "2e-55" and "21 of 179".'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'No output diagnoses, prescribes or triages an individual. Input 8 asked for per-patient ICU escalation and nothing in the Skill, the usage-guide or the example produces or invites a per-subject statement; the new multi-condition machinery is still a group comparison.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'The pass-3 P1s are closed without introducing a fallacy: contrasts are built from the factor levels with BH applied across the whole contrast family rather than within each, PCA is diagnostic and explicitly must not gate the statistics or justify imputation, batch stays a covariate rather than being removed before testing, and the fold-change floor is enforced by treat() rather than a post-hoc double filter. The one residual is a communication gap rather than an error: the fixed treat(lfc = log2(1.5)) floor silently zeroes the intermediate level of a dose series and is not flagged.'},
     'code_usability': {'result': 'PASS', 'detail': 'All five fenced R blocks were extracted verbatim and four of the five executed to completion on synthetic input (the fifth, TMT, executed as its guard plus purityCorrect legs). The Complete R Workflow block ran unedited on a two-condition, a three-condition and a shuffled-annotation input. examples/proteomics_workflow.R remains runnable from an empty directory.'}
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
   'Both pass-3 P1s are closed in a single executed run: a three-condition dose design now completes unedited with 20 calls and 0 false positives among 780 true nulls, and the same run hits the previously fatal empty complete-case matrix and skips PCA with an explanation instead of aborting the workflow at step 5 of 7.',
   'The annotation-order fix removes a genuinely silent wrong-design fit: with a shuffled annotation the pre-fix line returns 0 significant proteins where the fixed line returns 62, max |logFC| difference 2.80, and no error is raised in either case. The fixer found this themselves and fixed it correctly with match() plus a stopifnot.',
   'The CoA orientation guard both works and was needed: it separates the correct and transposed sheets by a factor of four in row-vs-column sum deviation, and purityCorrect with a transposed matrix produces 0 negatives, so the check the Skill used to rely on was provably blind to it -- and the misleading comment on that old check was corrected rather than left standing.',
   'Every quantitative claim the fix added reproduced: 62 and 20 calls, 0 false positives, and the compositional-bias measurement to -0.19 log2 / p = 2e-55 / 21 of 179.',
   'The two-condition path is byte-for-byte unchanged by the multi-contrast rewrite, because decideTests(method = "global") over a single contrast is identical to the per-contrast BH -- the generalisation cost nothing.'
 ],
 'recommendations': [
   {'priority': 'P1',
    'title': 'The fixed treat() fold-change floor silently zeroes the intermediate level of a dose series',
    'observed_in': 'Input 3',
    'problem': 'The newly supported multi-condition path inherits treat(lfc = log2(1.5)) = 0.585 log2 from the two-condition workflow. On a dose design whose LowDose effect is a real 0.7 log2, Low_vs_Ctl returns 0 calls while High_vs_Ctl returns 20 -- a reader following the block would report "no effect at low dose" for 120 proteins that genuinely respond. The floor is correct practice for a single pairwise comparison; on a monotonic dose series it is a design decision that must be stated.',
    'root_cause': 'The contrast machinery was generalised to N levels while the effect-size threshold stayed a single global constant written for the two-condition case.',
    'fix': 'Add one line beside the treat() call: "lfc = log2(1.5) is a per-contrast minimum effect. On a dose series or time course the intermediate levels carry a SMALLER true effect than the extreme one, so the same floor can return zero calls there while the top level is significant -- lower lfc, or screen with the eBayes/topTable F-test documented below and report the pairwise contrasts only for direction."'},
   {'priority': 'P2',
    'title': 'The PCA guard and the contrast logic now live in two places that deliberately disagree',
    'observed_in': 'Inputs 1, 3',
    'problem': 'examples/proteomics_workflow.R gained the same prcomp guard as SKILL.md but deliberately keeps the hard-coded two-condition contrast, with a comment telling the reader not to edit sample_groups. Two copies of near-identical logic that differ on purpose will drift, and the example is the file a newcomer runs first.',
    'root_cause': 'The example is a self-contained demo and the block is the general recipe; the fix updated both rather than unifying them.',
    'fix': 'Give the example the same level-driven contrast construction as SKILL.md -- it is four lines and collapses to the identical result for two conditions -- so the two files cannot diverge.'},
   {'priority': 'P2',
    'title': 'Two named routes remain uncoded',
    'observed_in': 'Static evaluation',
    'problem': 'FragPipe is named as a supported input but has no code, and the MSstatsTMT multi-plex (reference-channel/IRS) route is still a comment block inside the TMT section, so a two-plex TMT experiment -- the common case -- has no executable path here.',
    'root_cause': 'Both were deferred while the multi-condition and guard work was done.',
    'fix': 'Either write the MSstatsTMT multi-plex call (MSstatsTMT 2.14.2 is installed) or state plainly in the decision tree that multi-plex TMT routes out to proteomics/ptm-analysis and proteomics/quantification, which now carry a TMT route.'},
   {'priority': 'P2',
    'title': 'The file has outgrown a single page',
    'observed_in': 'Static evaluation',
    'problem': '396 -> 479 lines in one always-loaded file with no references/ directory, and the token-cost mark dropped accordingly.',
    'root_cause': 'Every fix so far has added prose and guards to the same file.',
    'fix': 'Move the Tool/Method taxonomy and the Common Errors table into references/ and leave the decision tree, the input contract and the five code blocks in SKILL.md.'},
   {'priority': 'P2',
    'title': 'The result table has no stated schema',
    'observed_in': 'Inputs 1, 3',
    'problem': 'results now carries a contrast column and a global-BH significant column, but the schema is discoverable only by reading the code. An agent chaining this into a pathway Skill has no named contract, and the per-contrast breakdown is printed rather than returned.',
    'root_cause': 'Output shape has always been implicit in the write.csv line.',
    'fix': 'State the columns once above step 7 -- protein, contrast, logFC, AveExpr, t, P.Value, adj.P.Val, significant -- and note that significance comes from the global decideTests, not from adj.P.Val alone.'}
 ]
}

with open(os.path.join(OUT, 'eval_report_bio-workflows-proteomics-pipeline_result.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print('static', static, 'exec_avg', exec_avg, 'final', report['final']['score'], 'assertions', ap, '/', at)
