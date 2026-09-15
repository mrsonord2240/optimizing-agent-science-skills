# Builds eval_report_bio-proteomics-peptide-identification_result.json (arithmetic done here, not by hand).
import json

SID = 'bio-proteomics-peptide-identification'
OUT = f'F:/OpenScience/audits/{SID}/eval_report_{SID}_result.json'

static = {
    'functional_suitability': (7, 12, "Completeness 2: TDC, PEP vs q, FDR cascade, open search and rescoring are covered as guidance, but the usage-guide's promised tasks 'configure trypsin/2 missed cleavages/10 ppm/0.02 Da', 'set up an MSFragger open search' and 'rescore with mokapot/Percolator' get no code or commands, and SimpleSearchEngineAlgorithm parameters are never shown. Correctness 2: the Elias-Gygi 2*decoy/(target+decoy) estimator is attributed to SEPARATE searches in four places (it is Elias & Gygi 2007's formula for a concatenated composite search; Kall et al. 2008 give pi0*decoy/target for separate searches), the pyOpenMS blocks fail on pyopenms 3.5.0 (TypeError, PeptideIdentificationList) despite 'tested with 3.1+', and the Common Errors claim that MSnbase::readMzIdData does not exist is false (it exists and ran). Appropriateness 3: right default (Comet/Sage + Percolator/mokapot, q<=0.01), pyOpenMS SSE is a teaching-scale engine."),
    'reliability': (8, 12, "Fault tolerance 3: explicit 'introspect and adapt on TypeError' rule, small-PSM warning, open-search warning. Error reporting 2: Common Errors table has cause/solution rows, but two are wrong on current tools (readMzIdData exists; an unannotated idXML makes FalseDiscoveryRate raise 'Meta value target_decoy does not exist', not 'all q-values 0'), and the table snippet silently writes inf when rank 1 is a decoy. Recoverability 3: stateless code, re-runs overwrite outputs."),
    'performance_context': (6, 8, "Token cost 3: 231-line, 21.6 kB SKILL.md all loaded at once (long reference list), no conditional loading. Execution efficiency 3: PeptideIndexing after SimpleSearchEngineAlgorithm is redundant (the search already annotates target/decoy) and removeDecoyHits after FalseDiscoveryRate is redundant (decoy hits already dropped); harmless."),
    'agent_usability': (13, 16, "Learnability 3: clear goal/approach blocks. Consistency 3: insight 2 says a q-value is valid only if targets and decoys competed in ONE concatenated search, then offers separate-search estimators; usage-guide says 'separate searches use the mix-max / 2x form'. Feedback design 3: each block states its product (idXML, kept list) but no reporting template (ID counts, decoy counts, threshold score). Error prevention 4: raw-score thresholding, cross-engine scores, PEP vs q, PSM vs protein FDR, few PSMs, open search, rescoring overfitting, DIA entrapment all called out."),
    'human_usability': (6, 8, "Discoverability 3: 'identifying peptides from tandem mass spectra and deciding what FDR threshold to act on' is natural, but the description is long and jargon-dense. Forgiveness 3: snippet accepts three decoy prefixes; assumes 'protein'/'score' columns and one row per spectrum without saying so."),
    'security': (11, 12, "Credential safety 4: none needed. Input validation 3: no column/rank/decoy-count checks in the snippet (template-wide). Data safety 4: local files only."),
    'maintainability': (9, 12, "Modularity 3: search, annotation/FDR and table FDR are separate blocks. Modifiability 3: version header is stale (3.1+ vs a 3.5 API change). Testability 3: examples/fdr_filtering.py is self-contained, seeded and runs, but ships no expected output and its demo is not a per-spectrum competition; the pyOpenMS blocks have no test data."),
    'agent_specific': (18, 20, "Trigger precision 4: explicit routing to protein-inference, ptm-analysis, dia-analysis, quantification, data-import; all seven related Skills exist. Progressive disclosure 3: under 500 lines but no references/ split. Composability 4: idXML/q-value outputs hand off cleanly. Idempotency 4: deterministic code, seeded example. Escape hatches 3: 'few PSMs -> inspect spectra manually' and scope routing, no explicit stop conditions."),
}

inputs = [
    dict(type='Canonical', label='pyOpenMS search of a synthetic mzML + DECOY_ FASTA, 1% FDR idXML',
         status='COMPLETED', basic=32, specialized=45,
         note="Skill code as written: TypeError at search() (pep_ids must be PeptideIdentificationList in pyopenms 3.5.0). After that one-line fix: 381 PSMs (348 target, 33 decoy) -> 311 at q<=0.01, 298 correct, 13 false (FDP 4.2% this seed; pooled over 8 more seeds 22/2326 = 0.95%). Search settings had to be set by introspection.",
         executed=True,
         execution_note="runs/in1_skill_verbatim.py (Skill blocks verbatim) exit 1: TypeError: Argument 'pep_ids' has incorrect type (expected PeptideIdentificationList, got list). runs/in1_adapted.py (peptide_ids = PeptideIdentificationList(); user settings via getParameters/setValue) exit 0; runs/in1_replicates.py reran on 8 seeds; runs/null_check.log showed a symmetric target/decoy null on 2000 noise spectra.",
         assertions=[
             ("The Skill's pyOpenMS code runs as written on pyopenms 3.5.0", 'FAIL', "TypeError at SimpleSearchEngineAlgorithm.search; IdXMLFile().load with a list also fails ('can not handle type')"),
             ('Output filters on the q-value (not ln(hyperscore)) at 0.01 and removes decoys', 'PASS', 'score_type becomes q-value, higher_better False; 311 target PSMs kept, max q 0.0096'),
             ('The delivered 1%-FDR list is calibrated against ground truth', 'PASS', 'pooled realised FDP 0.95% over 8 seeds (per-run 0-3.9%, the variance the Skill warns about below hundreds of PSMs)'),
             ('Scope: protein-level FDR and grouping are handed to protein-inference, not claimed from PSM FDR', 'PASS', 'stated in the output, per the Skill routing'),
             ("The Skill supplies code to apply the user's search settings (0.02 Da fragment, 2 missed cleavages)", 'FAIL', 'no SimpleSearchEngineAlgorithm parameter code; defaults are 10 ppm fragment and 1 missed cleavage'),
         ]),
    dict(type='Variant A', label='q-values from a Comet .txt (concatenated, 5 rows per scan)',
         status='COMPLETED', basic=34, specialized=47,
         note="Snippet needs 'xcorr'->'score' (KeyError as written, expected for a generic column). Rank-1 only: 2659 PSMs at q<=0.01, realised FDP 0.83%, XCorr cut 3.484. Run on all Comet rows as the snippet reads: 2602 rows, 4 scans counted twice. E-value ranking: 2706 (0.85%).",
         executed=True,
         execution_note="runs/in2_comet_table.py on SYNTHETIC data/comet_concat.txt (12,000 scans, Comet default num_output_lines=5); exit 0.",
         assertions=[
             ('Snippet yields monotone q-values and a 1% list with realised FDP <= 1%', 'PASS', 'rank-1 list: 2659 PSMs, FDP 0.83%'),
             ('The Skill says to keep only the rank-1 hit per spectrum before counting', 'FAIL', 'not in the snippet or text; on all rows the list lost 57 PSMs and contained 4 duplicate scans'),
             ('Output does not threshold on raw XCorr or compare scores across engines', 'PASS', 'XCorr 3.484 reported only as the score that the q-value cut maps to'),
             ('Scope: stays at PSM level and routes protein FDR to protein-inference', 'PASS', 'routing stated'),
         ]),
    dict(type='Edge', label='33-PSM single-bait pulldown, all q = 0; rank-1 decoy variant',
         status='COMPLETED', basic=34, specialized=48,
         note="No-decoy list: snippet gives q = 0 for all 33 PSMs while 11 are false (FDP 33%). Top-decoy list: fdr = inf at row 1, no exception or warning, q = 0.031 for all, 0 kept. The Skill's 'Decoy FDR on too few PSMs' failure mode gives the right verdict; the snippet itself does not.",
         executed=True,
         execution_note='runs/in3_pulldown.py on SYNTHETIC data/pulldown_nodecoy.tsv and pulldown_topdecoy.tsv; exit 0, no warnings captured.',
         assertions=[
             ("Safety: output refuses to report the 33-PSM list as '0% FDR' or as 1%-FDR controlled", 'PASS', "Skill's failure mode 'zero observed decoys does not mean zero false targets' applied"),
             ('Snippet survives a decoy at rank 1 without crashing', 'PASS', '1/0 gives inf in the fdr column; the running minimum masks it; no exception'),
             ('Snippet q-values reveal that the list is too small to control FDR (e.g. +1 correction)', 'FAIL', 'q = 0 for all 33 rows; (D+1)/T would give a floor of 1/33 = 0.030'),
             ('Output recommends manual spectrum inspection or orthogonal validation', 'PASS', 'manual inspection per the Skill, plus synthetic-peptide or PRM confirmation'),
         ]),
    dict(type='Variant B', label="PEP vs q-value: PI wants the 'safer' PEP <= 0.01 list",
         status='COMPLETED', basic=35, specialized=52,
         note="On the synthetic rank-1 table: 2659 PSMs at q<=0.01 (FDP 0.83%) vs 1406 at PEP<=0.01 (FDP 0.07%); worst PEP in the 1% list 0.077; last 100 accepted PSMs mean PEP 0.070 vs observed error 0.070. Example smoke test ran (666 vs 371, worst PEP 0.102). The example's demo is not a per-spectrum competition: realised FDP 0.60% at nominal 1%.",
         executed=True,
         execution_note='examples/fdr_filtering.py run as-is (exit 0, runs/smoke_fdr_filtering.log); runs/in4_pep_vs_q.py imports its add_qvalues/add_pep (bytecode writing disabled) on data/comet_concat.txt; exit 0.',
         assertions=[
             ('Output recommends the q-value for the reported list and PEP for the single-peptide decision', 'PASS', "matches the Skill's insight 3"),
             ('Every number in the output comes from executed code', 'PASS', 'runs/in4_pep_vs_q.log'),
             ('The shipped example runs as a smoke test', 'PASS', 'exit 0'),
             ('The example demo is a faithful concatenated-competition simulation', 'FAIL', '1000 null targets vs 2000 independent decoys; decoys/targets over-estimates FDR (realised 0.60% at q 1%)'),
         ]),
    dict(type='Stress', label='Separate target/decoy searches merged + Percolator rescoring',
         status='COMPLETED', basic=30, specialized=42,
         note="Skill-prescribed 2d/(t+d) on separate searches: 2138 PSMs, realised FDP 0.33% (estimate 2.06% where truth is 0.62%). Kall 2008 pi0*d/t (pi0-hat 0.611): 2888 PSMs, FDP 1.04%; oracle 2853. TDC: 2659 (0.83%). Percolator flags match docs; Percolator not executed.",
         executed=True,
         execution_note='runs/in5_separate_search.py on SYNTHETIC data/separate_target.tsv + separate_decoy.tsv; exit 0. Percolator has no build here: -Y/--post-processing-tdc, mix-max default and --picked-protein <fasta> checked against the Percolator wiki (Command-line options), not executed.',
         assertions=[
             ('Output identifies the search mode as separate and does not apply the concatenated snippet blindly', 'PASS', "follows the Skill's 'confirm the search mode' step"),
             ('The separate-search estimator the Skill prescribes is correctly attributed and calibrated', 'FAIL', "2d/(t+d) is Elias & Gygi's concatenated composite-DB formula; on separate searches FDP 0.33% at nominal 1%, 26% fewer PSMs than pi0*d/t"),
             ('Percolator guidance matches documentation (mix-max default for separate input, -Y/--post-processing-tdc, --picked-protein <fasta>)', 'PASS', 'Percolator wiki help text'),
             ('Output warns about rescoring overfitting and cross-validation', 'PASS', "Skill's 'Rescoring overfitting' failure mode"),
             ('Scope: protein-level (picked) FDR is routed to protein-inference', 'PASS', 'stated'),
         ]),
]

rep = {
    'meta': {
        'skill_name': SID,
        'description': "Peptide-spectrum matching from MS/MS with target-decoy FDR control, framing identification confidence as a property of a ranked list (q-value/PEP) rather than a raw engine score (XCorr, hyperscore, Andromeda, SpecEValue). Covers Comet, MS-GF+, MSFragger, Sage, MaxQuant, MetaMorpheus, concatenated vs separate target-decoy competition, PEP vs q-value, rescoring and pyOpenMS SimpleSearchEngineAlgorithm + FalseDiscoveryRate.",
        'evaluated_on': '2026-09-11',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'A',
        'complexity': 'Moderate',
        'n_inputs': 5,
        'source': 'GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/peptide-identification',
        'executed': '5/5 inputs executed (pyopenms 3.5.0, pandas 3.0.5, numpy 2.5, R 4.4.3 with mzID 1.44.0 / mzR 2.40.0 / MSnbase 2.32.0); Percolator not available (checked against documentation)',
        'execution_note': "All data SYNTHETIC with ground truth (data/make_synthetic_ms2.py, data/make_psm_tables.py). The Skill's pyOpenMS blocks fail as written on pyopenms 3.5.0 (TypeError: PeptideIdentificationList) and run after a one-line change.",
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': "No fabricated citations or numbers; every reported count came from runs on synthetic data. The Skill mis-attributes the Elias-Gygi 2x formula to separate searches (a real paper, wrong setting); recorded as a correctness defect (P1), not fabrication."},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Research proteomics only; nothing diagnoses, prescribes or triages an individual.'},
            'methodological_ground': {'result': 'PASS', 'detail': "Core method (per-spectrum TDC, q-value cut at 0.01, PEP for per-ID decisions, PSM vs protein FDR, few-PSM warning) is sound. The separate-search prescription over-estimates FDR (conservative, 2138 vs 2888 PSMs) rather than inverting conclusions."},
            'code_usability': {'result': 'PASS', 'detail': "pyOpenMS blocks fail on pyopenms 3.5.0 with a self-explanatory TypeError; the Skill's own version rule directs the one-line adaptation and the pipeline then runs end to end. Table snippet, example script and the R readers (mzID::mzID+flatten, mzR::openIDfile+psms) all ran. Percolator flags exist in its documentation."},
        },
    },
}

cats = {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}
subtotal = sum(v[0] for v in static.values())
rep['static_score'] = {'subtotal': subtotal, 'max': 100, 'categories': cats}

dyn_inputs = []
for i, x in enumerate(inputs, 1):
    total = x['basic'] + x['specialized']
    a = [{'text': t, 'result': r, 'note': n} for t, r, n in x['assertions']]
    p = sum(1 for q in a if q['result'] == 'PASS')
    sa_fail = any(q['result'] == 'FAIL' and q['text'].lower().startswith(('safety', 'scope')) for q in a)
    flag = '❌' if sa_fail or x['status'] != 'COMPLETED' else ('✅' if total >= 75 else '⚠️')
    dyn_inputs.append({'index': i, 'type': x['type'], 'label': x['label'], 'status': x['status'], 'status_flag': flag,
                       'note': x['note'], 'basic': x['basic'], 'specialized': x['specialized'], 'total': total,
                       'assertions_passed': p, 'assertions_total': len(a), 'assertions': a,
                       'executed': x['executed'], 'execution_note': x['execution_note']})
avg = round(sum(d['total'] for d in dyn_inputs) / len(dyn_inputs), 1)
passed = sum(d['assertions_passed'] for d in dyn_inputs)
tot_a = sum(d['assertions_total'] for d in dyn_inputs)
rep['dynamic_score'] = {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': tot_a},
                        'inputs': dyn_inputs}
sw = round(subtotal * 0.4, 1)
dw = round(avg * 0.6, 1)
score = int(round(sw + dw))
band = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
l1 = sum(d['basic'] for d in dyn_inputs) / 5
l2 = sum(d['specialized'] for d in dyn_inputs) / 5
lr_ok = subtotal >= 70 and avg >= 75 and l1 >= 28 and l2 >= 42 and passed / tot_a >= 0.8
grade = band
if band == 'Limited Release' and not lr_ok:
    grade = 'Beta Only'
sym = {'Production Ready': '⭐', 'Limited Release': '✅', 'Beta Only': '⚠️', 'Reject': '❌'}[grade]
rep['final'] = {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade,
                'grade_symbol': sym, 'deployable': grade in ('Production Ready', 'Limited Release'),
                'veto_override': False}
rep['key_strengths'] = [
    "Correct core doctrine: act on a list-level q-value, never a raw engine score; PEP for per-ID decisions; PSM FDR is not protein FDR",
    "The pyOpenMS SimpleSearchEngineAlgorithm -> PeptideIndexing -> FalseDiscoveryRate -> IDFilter path, once adapted to PeptideIdentificationList, gave a calibrated 1% list on synthetic data (pooled FDP 0.95% over 8 seeds)",
    "The 'Decoy FDR on too few PSMs' failure mode catches the q = 0 trap on a 33-PSM pulldown (11 false PSMs)",
    "Percolator guidance (mix-max default for separate input, -Y/--post-processing-tdc, --picked-protein) matches the tool's documentation",
    "Tight scope with explicit routing to protein-inference, ptm-analysis, dia-analysis and quantification; all related Skills exist",
]
rep['recommendations'] = [
    {'priority': 'P1', 'title': 'Correct the separate-search FDR estimator and citation', 'observed_in': [5],
     'problem': "SKILL.md insight 2, the FDR vocabulary, the 'Concatenated vs separate' failure mode and the usage-guide tip give Elias-Gygi 2*decoy/(target+decoy) as the separate-search estimator. On synthetic separate searches it reported 2.06% where the truth was 0.62% and kept 2138 PSMs vs 2888 for pi0*decoy/target.",
     'root_cause': "Elias & Gygi 2007 proposed 2*decoy/(target+decoy) for a concatenated composite search; Kall et al. 2008 (J Proteome Res 7:29) give pi0*decoy/target for separate searches, refined by mix-max (Keich 2015).",
     'fix': "State: concatenated TDC -> (decoy+1)/target (Elias-Gygi's 2d/(t+d) is the older, conservative whole-list form); separate searches -> pi0*decoy/target (Kall 2008) or mix-max (Keich 2015). Replace the failure-mode 'Mechanism' line, which describes the factor 2 wrongly."},
    {'priority': 'P1', 'title': 'Update pyOpenMS code to PeptideIdentificationList', 'observed_in': [1],
     'problem': "peptide_ids = [] makes SimpleSearchEngineAlgorithm.search raise TypeError on pyopenms 3.5.0; IdXMLFile().load with a list fails too, although the header says 'tested with pyOpenMS 3.1+'.",
     'root_cause': 'OpenMS 3.5 replaced vector<PeptideIdentification> with PeptideIdentificationList in the Python bindings.',
     'fix': "Use 'from pyopenms import PeptideIdentificationList; peptide_ids = PeptideIdentificationList()' in both blocks and the Common Errors row; change the version header to the tested version."},
    {'priority': 'P2', 'title': 'Make the table snippet rank-1 and +1 corrected', 'observed_in': [2, 3],
     'problem': "The snippet never keeps one hit per spectrum (Comet .txt has 5 rows per scan by default; 4 scans entered the list twice) and uses decoys/targets, so a 33-PSM list with no decoys gets q = 0 for every row while 11 are false.",
     'root_cause': "'One best hit per spectrum' is stated in prose but not enforced in code; no (D+1) correction.",
     'fix': "Add psms = psms.sort_values('score', ascending=False).drop_duplicates('scan') and fdr = (decoys + 1) / targets.clip(lower=1), matching OpenMS FalseDiscoveryRate's conservative default."},
    {'priority': 'P2', 'title': 'Show SimpleSearchEngineAlgorithm parameter setting', 'observed_in': [1],
     'problem': "The thresholds table recommends 0.02 Da fragment tolerance and 2 missed cleavages, but the search block runs defaults (10 ppm fragment, 1 missed cleavage) with no parameter code.",
     'root_cause': 'Parameter handling is shown only for PeptideIndexing.',
     'fix': "Add getParameters()/setValue for 'precursor:mass_tolerance', 'fragment:mass_tolerance(_unit)', 'peptide:missed_cleavages', 'modifications:fixed/variable', and note that 'decoys' can generate decoys and that the search already annotates target/decoy."},
    {'priority': 'P2', 'title': 'Fix two Common Errors rows and the example demo', 'observed_in': [4],
     'problem': "MSnbase::readMzIdData exists (it read 387 rows here); an unannotated idXML makes FalseDiscoveryRate raise RuntimeError, not return all-zero q-values; examples/fdr_filtering.py simulates independent rows (1000 null targets vs 2000 decoys) and labels it a concatenated search.",
     'root_cause': 'Rows written from memory rather than checked against installed packages; demo lacks per-spectrum competition.',
     'fix': "Drop or correct the readMzIdData row, give the real FalseDiscoveryRate error text, and have build_demo_table draw one target and one decoy score per null spectrum and keep the higher."},
]
json.dump(rep, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('static', subtotal, 'avg', avg, 'L1', l1, 'L2', l2, 'assert', passed, tot_a, 'sw', sw, 'dw', dw, 'score', score, band, '->', grade)
