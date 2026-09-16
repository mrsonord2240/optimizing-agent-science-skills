import json, os

OUT = 'F:/OpenScience/audits/bio-proteomics-ptm-analysis'
SRC = 'mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:proteomics/ptm-analysis'

inputs = [
 dict(index=1, type='Canonical', label='Regression: Fe-IMAC phosphoproteomics, 4 vs 4, with a paired global proteome -- which sites are really regulated once protein abundance is accounted for',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in1.R -- the label-free MSstatsPTM block extracted programmatically from the FIXED SKILL.md and eval\'d verbatim (one substitution: the synthetic FASTA name). MSstatsPTM 2.8.1, R 4.4.3.',
   note='Byte-identical regression against the pass-3 run: names(input) = PTM PROTEIN, all four models, Label "Treatment vs Control", 36 ADJUSTED site rows, 10 regulated by the TREAT threshold, 1 non-finite log2FC row. Against planted truth the adjustment does its job: protein_driven called 7/8 unadjusted -> 1/8 adjusted, site_regulated 8/8 -> 8/8, masked 1/4 -> 3/4, null 4/20 in both, sign agreement 5/5 on the regulated set. Adding the TMT section changed nothing here, which is the point of the regression.',
   basic=36, specialized=54, total=90,
   assertions=[
     dict(text='The label-free block still runs verbatim after the TMT section was inserted', result='PASS', note='Extracted programmatically; the label-free block is still the first groupComparisonPTM fence and eval\'d without edit.'),
     dict(text='Protein adjustment removes protein-driven calls and recovers masked ones', result='PASS', note='7/8 -> 1/8 and 1/4 -> 3/4 against labelled truth.'),
     dict(text='Only ADJUSTED.Model hits are called regulated', result='PASS', note='The block filters ADJUSTED.Model and applies a TREAT-style threshold.'),
     dict(text='Every number matches the pass-3 audit', result='PASS', note='36 / 10 / masked 2, null 3, site_regulated 5 / 1 non-finite -- cell for cell.'),
   ]),
 dict(index=2, type='Variant A', label='Regression: phospho-enriched runs only, no global proteome -- the use_unmod proxy-adjustment route',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in3.R, the same block with use_unmod <- TRUE as the Skill\'s decision-tree row directs.',
   note='Unchanged from pass-3: 507 evidence rows kept by the filter, 288 PTM rows, ADJUSTED.Model present. Proxy-adjusted results behave like the real thing but slightly weaker, exactly as the Skill warns -- protein_driven 1/8 called, site_regulated 8/8, masked 2/4 (against 3/4 with a real global proteome). The Skill\'s instruction to label these "proxy-adjusted" rather than "adjusted" is borne out by the masked-recovery gap.',
   basic=34, specialized=52, total=86,
   assertions=[
     dict(text='use_unmod keeps unmodified rows and still produces ADJUSTED.Model', result='PASS', note='507 rows kept, ADJUSTED.Model NULL = FALSE.'),
     dict(text='The Skill flags the proxy route as weaker than a paired global proteome', result='PASS', note='Decision-tree row says "label those results proxy-adjusted"; masked recovery drops 3/4 -> 2/4, confirming the caveat.'),
     dict(text='The route is not presented as equivalent to a paired global run', result='PASS', note='"Cannot separate occupancy from abundance; do not claim regulation" is stated in the same row.'),
     dict(text='Output is deterministic', result='PASS', note='Identical to pass-3.'),
   ]),
 dict(index=3, type='Adversarial', label='Regression: "Skip the global proteome, just give me adj.p < 0.05 and |log2FC| > 1, call it regulated phosphorylation, and write the FLR as the localization probability"',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/p5_in7.R.',
   note='Unchanged from pass-3 and still the right refusal. The requested unadjusted double filter returns 18 sites of which 6 are protein_driven and 3 are null -- i.e. a third of the list is protein abundance or noise. The Skill\'s route (ADJUSTED + TREAT) returns 10, of which 5 site_regulated and 2 masked. The FLR request is refused with the correct distinction: mean(1 - Localization prob) over class I is 0.0382 and is a MODEL-BASED expected FLR, not the empirical global FLR the Skill requires reporting.',
   basic=36, specialized=52, total=88,
   assertions=[
     dict(text='The unadjusted double filter is refused with a quantified cost', result='PASS', note='18 sites requested vs 10 by the Skill route; 6 protein_driven and 3 null in the requested list.'),
     dict(text='Model-based and empirical FLR are not conflated', result='PASS', note='0.0382 is reported as expected-FLR, explicitly not the empirical global FLR.'),
     dict(text='The Skill still requires three numbers (peptide FDR, localization probability, global FLR)', result='PASS', note='Stated in the Skill and in the usage-guide workflow step 6.'),
     dict(text='No claim of "regulated phosphorylation" is made without protein adjustment', result='PASS', note='The output labels the unadjusted list as confounded.'),
   ]),
 dict(index=4, type='Edge / boundary', label='Regression + new probe: KSEA over seven degenerate PX shapes -- are the two new guards right, and is the pass-2 correctness fix untouched?',
   status='COMPLETED', status_flag='PASS', executed=True,
   execution_note='pass5/in7_ksea_guards.R -- the KSEA block extracted programmatically from the FIXED SKILL.md and eval\'d verbatim against seven PX shapes (D1-D6 from the pass-3 probe, plus a new D7 I added). KSEAapp 2.0.',
   note='BOTH FIXER CLAIMS REPRODUCED. Structurally, the pass-2 correctness line `ks <- adjusted[is.finite(adjusted$log2FC), ]` is present verbatim and all four guards sit around it, none inside. Numerically, D1 gives SYN_BASO_KINASE z = -2.5514840725 FDR 0.008044892010, SYN_PRO_KINASE z = 3.3688957209 FDR 0.001132049635, SYN_RANDOM_KINASE z = -0.6524594878 FDR 0.257052399630 -- the fix log claims "-2.5514841 / 0.008044892, 3.3688957 / 0.001132050, -0.6524595 / 0.257052400", i.e. UNCHANGED TO THE LAST DIGIT. D2, D3 and D5 also compute normally with no NaN. D4 (prior matching one site) now stops with "The kinase-substrate prior covers 0 of 31 sites ..." instead of the package\'s `no rows to aggregate`; D6 (all sites non-finite) stops with the one-condition message instead of `differing number of rows: 0, 1`. My new D7 (proteinGroups with no gene symbols) is caught by the third guard with its own message.',
   basic=37, specialized=53, total=90,
   assertions=[
     dict(text='The guards were added around the pass-2 correctness fix, not inside it', result='PASS', note='The filter line is present verbatim and D1/D2/D3/D5 are numerically identical to pass 2 at 10 significant figures.'),
     dict(text='A prior with no usable overlap stops with a coverage message', result='PASS', note='D4: "covers 0 of 31 sites", naming the three real causes.'),
     dict(text='An empty filtered table stops before the PX construction', result='PASS', note='D6: the nrow(ks) == 0 guard fires with the detected-in-one-condition explanation.'),
     dict(text='A third degenerate shape the fixer did not test is also caught', result='PASS', note='D7 (no gene symbols anywhere) hits the nrow(PX) == 0 guard with an actionable message.'),
     dict(text='No shape produces a silent NaN z-score', result='PASS', note='0 NaN z across all four shapes that reach KSEA.Scores.'),
   ]),
 dict(index=5, type='Variant B (NEW route, the P1 fix)', label='"Protein-adjust my TMT phosphoproteomics -- enriched and global runs are labelled plexes with a pooled reference channel."',
   status='COMPLETED', status_flag='WARN', executed=True,
   execution_note='pass5/in8_tmt.R on a SYNTHETIC TMT10 evidence pair built by pass5/make_tmt.py from this audit\'s own labelled label-free set (8 biological channels + 2 pooled Norm), so data/phospho/truth_sites.csv still applies. The new SKILL.md TMT block is extracted programmatically and eval\'d verbatim (FASTA name substituted). MSstatsPTM 2.8.1 + MSstatsTMT 2.14.2.',
   note='FIXER CLAIM REPRODUCED IN SUBSTANCE on an independently built TMT set. The block completes: names(input) = PTM PROTEIN, all four models, 35 ADJUSTED site rows (fixer: 39 on their reshape), Label "Treatment vs Control". Against planted truth: protein_driven 5/8 -> 1/8 after adjustment (fixer: 6/8 -> 1/8), site_regulated 8/8 -> 8/8 (exact match), masked 0/4 -> 3/4 (fixer: 1/4 -> 3/4), null 4/20 unchanged, sign agreement 11/11 on regulated+masked, Spearman rho 0.766 vs true occupancy log2FC (fixer: 0.691). Same direction, same endpoints; the small count differences come from my reshape not being byte-identical to theirs. NEW FINDING (a defect in the newly added text): SKILL.md states "Channel is \'channel.1\' ... \'channel.N\' and maps to the evidence\'s \'Reporter intensity corrected <n>\' columns". MaxQuant writes those columns 0-INDEXED for a 10-plex ("Reporter intensity corrected 0" .. "9"), and an annotation using channel.1 .. channel.10 is REJECTED with "** Please check the annotation file. The channel name must be matched with that in input data."; channel.0 .. channel.9 is what completes. A real MaxQuant TMT user following the Skill fails at the first call, on an error that never mentions the off-by-one.',
   basic=35, specialized=52, total=87,
   assertions=[
     dict(text='The three documented switches are the right three and the route reaches ADJUSTED.Model', result='PASS', note='labeling_type = TMT, dataSummarizationPTM_TMT, data.type = TMT -> PTM + PROTEIN, four models, 35 adjusted site rows.'),
     dict(text='The TMT adjustment behaves like the label-free one against planted truth', result='PASS', note='protein_driven 5/8 -> 1/8, site_regulated 8/8, masked 0/4 -> 3/4, sign agreement 11/11.'),
     dict(text='The documented Channel naming matches real MaxQuant reporter columns', result='FAIL', note='SKILL.md says channel.1..channel.N; MaxQuant is 0-indexed and only channel.0..channel.(N-1) is accepted. Reproduced by running both.'),
     dict(text='The Norm reference-channel requirement is stated and enforced in the example', result='PASS', note='Condition = Norm in every plex, reference_norm/remove_norm_channel defaults explained; the contrast names only the biological conditions and it worked.'),
     dict(text='The TMT-specific adjustment traps are correct and non-obvious', result='PASS', note='Ratio compression biasing dFC_PTM - dFC_protein (not merely attenuating it) and same-plex labelling of enriched + global are both sound and are the two that matter for the SUBTRACTION, not just the quant.'),
   ]),
 dict(index=6, type='Stress / misconfiguration (NEW this pass)', label='"I think I set the TMT options wrong somewhere -- what does MSstatsPTM actually say when the labeling type and the annotation disagree?"',
   status='COMPLETED', status_flag='WARN', executed=True,
   execution_note='pass5/p5_tmt_errors.R and pass5/p5_tmt_err2.R -- three mismatched configurations of the new TMT block, run verbatim.',
   note='The doctrine is confirmed, one quoted message is not. Confirmed: mismatching the two halves fails LOUDLY in every direction and NO message mentions labeling type -- exactly the Skill\'s point. The forward direction reproduces verbatim: a label-free annotation with labeling_type = TMT gives "Extra columns included in the annotation file that are not required ... Run, Raw.file, Fraction, TechRepMixture, Channel, Condition, Mixture, BioReplicate", which is also the TMT annotation spec as the Skill says. NOT reproduced: the Skill quotes "A non-empty vector of column names for \'by\' is required" for TMT evidence left on the default LF. Two attempts at that configuration gave different loud errors instead -- "Extra columns ... Run, Raw.file, Condition, BioReplicate, IsotopeLabelType" (TMT annotation on LF) and "** Please check annotation. Each MS run (Raw.file) can\'t have multiple conditions or BioReplicates." (LF annotation on LF with TMT evidence). The quoted text is presumably reachable on some input shape, but it is not the message a user of this data will see.',
   basic=33, specialized=50, total=83,
   assertions=[
     dict(text='A mismatched labeling_type fails loudly rather than silently collapsing channels', result='PASS', note='Three distinct hard errors across three configurations; none produced a wrong-but-plausible result.'),
     dict(text='No error message names the labeling type, as the Skill warns', result='PASS', note='Confirmed for all three.'),
     dict(text='The forward-direction error text in Common Errors reproduces verbatim', result='PASS', note='Annotation-column list matched character for character.'),
     dict(text='The reverse-direction error text in Common Errors reproduces', result='FAIL', note='Could not reproduce "A non-empty vector of column names for \'by\' is required" in three configurations of the same data.'),
     dict(text='The Common Errors fixes are actionable regardless', result='PASS', note='Both rows point at labeling_type/dataSummarizationPTM_TMT/data.type, which is the correct remedy in every case observed.'),
   ]),
]

for i in inputs:
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['assertions_total'] = len(i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'], i['index']

exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (11, 12, 'Completeness 4 (up from 3): the pass-3 P1 is closed -- TMT/isobaric phosphoproteomics now has a runnable route that reaches a protein-adjusted result, and the scope sentence admits it ("label-free AND TMT"). PTM-SEA and empirical FLR remain prescribed-but-unimplemented. Correctness 3 (down from 4): the new TMT section states Channel names as "channel.1 ... channel.N" against MaxQuant reporter columns that are 0-indexed, and the annotation that follows the Skill is rejected outright. Appropriateness 4.'),
 'reliability': (11, 12, 'Fault tolerance 4 (up from 3): four guards now sit around the KSEA path and all four fire on the shapes that previously died inside KSEAapp -- verified on seven PX shapes including one the fixer did not test. Error reporting 3: two of the four new Common Errors rows reproduced verbatim (both KSEA ones) and one of the two TMT ones did; the reverse-direction TMT message could not be reproduced in three configurations, and the channel-naming statement is wrong. Recoverability 4: stateless, idempotent, results identical across sessions to ten significant figures.'),
 'performance_context': (5, 8, 'Token cost 2: 391 -> 478 lines with three large taxonomy tables and a 23-entry reference list, all loaded, still no references/ split. The growth bought a real route, but this is an always-loaded Skill and the cost is real. Execution efficiency 3: MSstatsPTM summarization and modelling dominate; the TMT route is the same cost as the label-free one.'),
 'agent_usability': (14, 16, 'Learnability 3: the new TMT block is self-contained, but the KSEA and motif blocks still depend on session variables (adjusted, rd, pg, gene_symbol). Consistency 4: the TMT route is written as a delta against the label-free one ("only three things change") and that framing held exactly when executed. Feedback design 3: no output/reporting template. Error prevention 4: the guards, the Norm-channel requirement, and the refusal to compare plexes without a bridge are all preventive rather than diagnostic.'),
 'human_usability': (6, 8, 'Discoverability 3: the description is dense but precise about what the Skill owns; the usage-guide gained a TMT prompt that matches how a researcher would phrase it. Forgiveness 3: one substitution needed for a non-default FASTA name, six for a non-phospho modification, and now a seventh place where phospho is hard-coded (the TMT block).'),
 'security': (11, 12, 'Credential safety 4, input validation 3, data safety 4. No eval/exec of user strings, no network calls, no credentials. The kinase prior remains a user-supplied download, correctly not shipped.'),
 'maintainability': (9, 12, 'Modularity 3, modifiability 3, testability 3. Modification names are still hard-coded to phospho, and the TMT block adds a third code path that would need the same substitutions. All three R fences parse, all three Python fences and examples/phospho_analysis.py compile.'),
 'agent_specific': (18, 20, 'Trigger precision 4, progressive disclosure 3 (one long file, now longer), composability 4 (clean hand-offs to peptide-identification, quantification, differential-abundance, dia-analysis), idempotency 4 (KSEA D1 reproduced to ten significant figures across sessions), escape hatches 3 (the TMT route adds a good one -- refuse to compare plexes without a pooled reference channel).'),
}
static = sum(v[0] for v in cats.values())

report = {
 'meta': {
   'skill_name': 'bio-proteomics-ptm-analysis',
   'description': 'PTM-centric proteomics: enrichment-chemistry framing, site localization and FLR, multiplicity-resolved site quantification, protein-level adjustment with MSstatsPTM (label-free and TMT/isobaric), motif analysis against an experiment-matched background, and kinase-activity inference.',
   'source': SRC,
   'evaluated_on': '2026-09-15',
   'evaluator_version': 'skill-auditor@1.0',
   'category': 'Data Analysis',
   'execution_mode': 'A',
   'complexity': 'Moderate',
   'n_inputs': 6,
   'execution_note': 'Pass-5 confirmation audit of the FIXED Skill at fork commit 45a0c5a (fix commit b5355db), superseding the pass-3 report that scored 85. All 6 inputs executed. Inputs 1-4 re-run the pass-3 scripts as regression tests (Input 4 with a seventh PX shape I added); Inputs 5 and 6 are new and exercise the TMT route the fix added. Complexity Moderate (5 required); 6 run so both new routes get their own input. Every R and Python fence is pulled programmatically from the fork\'s SKILL.md and eval\'d verbatim -- nothing is retyped. A SYNTHETIC TMT10 evidence pair was built for Input 5 by pass5/make_tmt.py, reshaping this audit\'s own labelled label-free set so data/phospho/truth_sites.csv still applies. All data synthetic with ground truth. R 4.4.3 via the candidate r.sh: MSstatsPTM 2.8.1, MSstatsTMT 2.14.2, KSEAapp 2.0.'
 },
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS',
     'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {
     'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or results. The fix log\'s central numerical claim -- that the pass-2 KSEA correctness fix is untouched -- reproduced to ten significant figures (BASO -2.5514840725 / 0.008044892010, PRO 3.3688957209 / 0.001132049635, RANDOM -0.6524594878 / 0.257052399630). The TMT truth-table claim reproduced in direction and endpoint on an independently constructed TMT set. One documented error string could not be reproduced and one documented Channel naming is wrong; both are recorded as findings, not as fabrication -- they are tool-behaviour statements, not results.'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'No output diagnoses, prescribes or triages an individual. Input 3 pushed for an unadjusted "regulated phosphorylation" call and a mislabelled FLR, and both were refused with numbers.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'The three-inference framing holds; protein adjustment demonstrably removes protein-driven calls and recovers masked ones in BOTH the label-free and the new TMT route against planted truth. The two TMT-specific traps the fix added -- ratio compression biasing rather than merely attenuating the site-minus-protein subtraction, and labelling enriched and global aliquots in the same plex -- are correct and are the ones that matter for the adjustment rather than the quant.'},
     'code_usability': {'result': 'PASS', 'detail': 'All three R fences parse and all three were executed; all three Python fences and examples/phospho_analysis.py compile. The new TMT block runs end to end on real TMT-shaped MaxQuant evidence once the annotation Channel index is corrected from the Skill\'s stated channel.1..N to MaxQuant\'s 0-indexed channel.0..N-1.'}
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
   'The pass-3 P1 is genuinely closed: the new TMT/isobaric route runs end to end on TMT-shaped MaxQuant evidence and its protein adjustment behaves against planted truth exactly as the label-free one does -- protein-driven calls 5/8 -> 1/8, site_regulated 8/8 held, masked 0/4 -> 3/4, sign agreement 11/11.',
   'The KSEA guards were added AROUND the pass-2 correctness fix, not inside it, and this is verifiable rather than asserted: four PX shapes that already worked reproduce to ten significant figures while the two that used to die inside KSEAapp now stop with messages naming the real cause.',
   'The TMT section is written as a delta ("only three things change") and that framing survived execution exactly -- the converter switch, the separate summarization FUNCTION, and the test branch were the only differences that mattered.',
   'The two TMT traps the fix chose are the right ones: ratio compression biases the site-minus-protein subtraction rather than merely attenuating it, and enriched plus global aliquots should share a plex. Both concern the ADJUSTMENT, which is what this Skill owns.',
   'Mismatched TMT configuration fails loudly in every direction tested, so a wrong-but-plausible result is not reachable by the misconfiguration the Skill warns about.'
 ],
 'recommendations': [
   {'priority': 'P1',
    'title': 'The new TMT section states the wrong Channel index, and the Skill\'s own annotation is rejected',
    'observed_in': 'Input 5',
    'problem': 'SKILL.md says "Channel is \'channel.1\' ... \'channel.N\' and maps to the evidence\'s \'Reporter intensity corrected <n>\' columns". MaxQuant writes those columns 0-indexed for a 10-plex ("Reporter intensity corrected 0" through "9"), so the channel names MSstatsTMT derives are channel.0 .. channel.9. An annotation built to the Skill\'s spec is rejected with "** Please check the annotation file. The channel name must be matched with that in input data." -- a message that says nothing about an off-by-one. Reproduced by running both indexings on the same evidence: channel.1..10 fails, channel.0..9 completes.',
    'root_cause': 'The channel naming was written from the MSstatsTMT convention rather than from a MaxQuant evidence file\'s actual column suffixes.',
    'fix': 'Change the comment to: "Channel names follow the reporter-column suffixes MaxQuant wrote -- for a 10-plex those are `Reporter intensity corrected 0` .. `9`, so the annotation needs `channel.0` .. `channel.9`. Read the suffixes off your own evidence header before writing the annotation; a mismatch gives `the channel name must be matched with that in input data`, which does not mention the index."'},
   {'priority': 'P2',
    'title': 'One of the two new TMT Common Errors messages could not be reproduced',
    'observed_in': 'Input 6',
    'problem': 'The row for "TMT evidence left on the default labeling_type = LF" quotes "A non-empty vector of column names for \'by\' is required". Three mismatched configurations on this data produced three other loud errors instead ("Extra columns ... Run, Raw.file, Condition, BioReplicate, IsotopeLabelType" and "** Please check annotation. Each MS run (Raw.file) can\'t have multiple conditions or BioReplicates."). The doctrine around it -- fails loudly in both directions, no message mentions labeling -- is confirmed.',
    'root_cause': 'The quoted text was captured from one particular evidence/annotation shape and written up as the message for that direction generally.',
    'fix': 'Generalise the row: "several different loud errors are possible depending on which half is mismatched (observed: `A non-empty vector of column names for \'by\' is required`, `Extra columns included in the annotation file ...`, `Each MS run (Raw.file) can\'t have multiple conditions or BioReplicates`); none of them names the labeling type, so check labeling_type first whenever the converter rejects a TMT input."'},
   {'priority': 'P2',
    'title': 'Modification names are hard-coded to phospho, now in three code paths',
    'observed_in': 'Inputs 1, 2, 5',
    'problem': 'The label-free block, the Python Sites-table path and now the TMT block each hard-code `Phospho (STY)` in the regex, the mod_id and the probability column. Any other PTM needs the same substitutions in one more place than before.',
    'root_cause': 'Copy-ready snippets favour the dominant PTM over a parameterised constant.',
    'fix': 'Lift MOD_NAME / MOD_ID / PROB_COL to three constants at the top of the MSstatsPTM section and reference them from all three blocks; the diGly example in the failure-modes table then becomes a three-line change rather than a six-substitution rewrite.'},
   {'priority': 'P2',
    'title': 'PTM-SEA and empirical FLR are prescribed but still have no runnable route',
    'observed_in': 'Inputs 1, 3',
    'problem': 'The Skill requires reporting an empirical global FLR and names PTM-SEA as the site-level enrichment method, but ships neither. Input 3 could only produce a model-based expected FLR (0.0382), which the Skill itself says is not the number to report.',
    'root_cause': 'Both were left for a later pass while the TMT route was added.',
    'fix': 'Add a short ssGSEA2.0/PTM-SEA invocation and a LuciPHOr2 (or decoy-site) empirical-FLR recipe; both tools are installed in this environment, so this is now writable rather than blocked.'},
   {'priority': 'P2',
    'title': 'The file is heavy for an always-loaded Skill and got heavier',
    'observed_in': 'Static evaluation',
    'problem': '391 -> 478 lines, three large taxonomy tables and a 23-entry reference list, all loaded on every invocation, with no references/ split.',
    'root_cause': 'The TMT route necessarily grew the file and splitting is a restructure.',
    'fix': 'Move the Tool Taxonomy, the Per-Method Failure Modes and the reference list into references/ and leave the decision tree, the input contract and the code blocks in SKILL.md.'}
 ]
}

with open(os.path.join(OUT, 'eval_report_bio-proteomics-ptm-analysis_result.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print('static', static, 'exec_avg', exec_avg, 'final', report['final']['score'], 'assertions', ap, '/', at)
