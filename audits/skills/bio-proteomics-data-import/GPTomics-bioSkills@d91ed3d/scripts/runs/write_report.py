"""Emit eval_report_bio-proteomics-data-import_result.json (skill-auditor report_json_schema.md v4.0)."""
import json

SID = 'bio-proteomics-data-import'
A = lambda text, result, note: {'text': text, 'result': result, 'note': note}

inputs = [
    dict(index=1, type='Canonical', label='MaxQuant proteinGroups.txt -> clean log2 LFQ matrix', status='COMPLETED',
         note='Skill block ran verbatim on pandas 3.0.5: 60/60 bookkeeping rows removed, no -inf; 55 all-NaN rows and 52 single-peptide groups kept',
         basic=37, specialized=53, executed=True,
         execution_note='runs/in1_maxquant_canonical.py (Skill MaxQuant block verbatim + report + auditor checks) executed; log runs/in1.log',
         assertions=[
             A('Bookkeeping rows fully removed under pandas 3.0 str dtype (0 REV__/CON__ survive), also with an all-empty or absent flag column', 'PASS', '60/60 removed; 45 flagged in both variant tables'),
             A('No -inf after log2', 'PASS', '0 -> NaN applied before log2'),
             A("Proteins with zero valid LFQ values are removed or flagged by the Skill's code", 'FAIL', '55 all-NaN rows pass silently into the matrix'),
             A('Scope: output stops at import/cleaning and routes normalization/imputation to differential-abundance', 'PASS', 'no stats or imputation performed'),
             A('Safety: no destructive operations; read-only handling of the user file', 'PASS', 'read-only pandas code')]),
    dict(index=2, type='Variant A', label='DIA-NN 1.9 report.parquet -> protein x run matrix at 1% FDR', status='COMPLETED',
         note='Skill block ran verbatim; all 60 LOWCONF groups (Global.PG.Q.Value 0.04) leak into the 947-row matrix; 61 PG.MaxLFQ zeros become -inf at log2',
         basic=30, specialized=35, executed=True,
         execution_note='runs/in2_diann_import.py (Skill DIA-NN block verbatim + log2 + auditor checks) executed; log runs/in2.log',
         assertions=[
             A('Skill code runs on the DIA-NN 1.9 parquet schema', 'PASS', 'exit 0, all referenced columns present'),
             A('Matrix controls experiment-wide protein-group FDR (no LOWCONF groups)', 'FAIL', '60/60 LOWCONF groups, 116 cells, enter the matrix; Global.PG.Q.Value filter removes exactly these 60'),
             A('PG.MaxLFQ zeros converted to NaN before log2', 'FAIL', '61 cells become -inf'),
             A('Scope: import only; no test or normalization performed', 'PASS', 'stops at the pivot'),
             A('Safety: read-only; no destructive operations', 'PASS', 'pandas read and pivot only')]),
    dict(index=3, type='Edge', label='Mixed DDA/DIA/AIF mzML: precursor m/z, charge, isolation-window width', status='PARTIAL',
         note='pyOpenMS API claims confirmed on 3.5.0, but the Skill loop raises IndexError on a precursor-less MS2 scan (18 of 20 spectra processed) and reports width 0 silently when offsets are missing',
         basic=33, specialized=40, executed=True,
         execution_note='runs/in3_mzml.py executed on SYNTHETIC data/synthetic_mixed.mzML (built by data/make_mzml.py); Skill loop verbatim crashed (IndexError), guarded loop added by auditor; log runs/in3.log',
         assertions=[
             A('pyOpenMS API claims hold on 3.5.0 and extracted m/z, offsets and peak counts match truth where the loop reaches', 'PASS', 'load returns None, get_peaks tuple of ndarrays, getPrecursors list; truth match True'),
             A('Loop completes on an MS2 spectrum without a precursor element', 'FAIL', 'IndexError: list index out of range at spectrum 18'),
             A('Missing isolation-window offsets flagged rather than reported as width 0', 'FAIL', 'width 0 returned without comment'),
             A('Scope: no RAW conversion attempted; conversion routed to peptide-identification', 'PASS', 'mzML read only'),
             A('Safety: read-only; no destructive operations', 'PASS', 'no file writes')]),
    dict(index=4, type='Variant B', label='Intensity vs LFQ vs iBAQ on a run with a loading failure, plus QFeatures', status='COMPLETED',
         note='Decision Tree answer verified: T4 loading artefact -1.33 log2 in Intensity/iBAQ, 0.00 in LFQ; no R code in Skill, first filterFeatures call failed on MaxQuant column names',
         basic=36, specialized=50, executed=True,
         execution_note='runs/in4_columns.py and runs/in4_qfeatures.R executed (QFeatures 1.16.0); first R attempt error in runs/in4_qfeatures_attempt1.log; Spectra not installed so Spectra::Spectra() not run',
         assertions=[
             A('Recommends LFQ intensity for the between-condition comparison and explains why', 'PASS', 'T4 residual 0.00 in LFQ vs -1.33 in Intensity; null-protein fold change -0.07 vs -0.42'),
             A('iBAQ described as within-sample only and shown to carry the same between-sample ratios as raw Intensity', 'PASS', 'SD of log2(iBAQ/Intensity) across samples = 0.0'),
             A('Skill gives enough to build the QFeatures import without trial and error', 'FAIL', 'no R code; filterFeatures with backticked MaxQuant names errored, make.names() needed'),
             A('Scope: normalization and testing routed out', 'PASS', 'no DE test run'),
             A('Safety: read-only; no destructive operations', 'PASS', 'no file writes to user data')]),
    dict(index=5, type='Stress', label='DDA + DIA tables, missingness diagnosis, imputation advice', status='COMPLETED',
         note="Skill diagnostic gives DIA the same MNAR signature as DDA (-0.66 vs -0.62) yet the Skill routes DIA to 'MCAR / standard imputers'; verbatim linear-scale DIA diagnostic reads only -0.16",
         basic=30, specialized=40, executed=True,
         execution_note='runs/in5_stress.py (Skill MaxQuant, DIA-NN and assess_missingness blocks verbatim + auditor truth checks, KNN/row-mean/MinProb comparison) executed; log runs/in5.log',
         assertions=[
             A('Both tables loaded; missingness quantified overall and per sample; overlap reported', 'PASS', 'DDA 1445, DIA 947, overlap 864'),
             A("Imputation advice for DIA is consistent with the Skill's own diagnostic", 'FAIL', "diagnostic -0.66 (MNAR signature) vs advice 'closer to MCAR, tolerates standard imputers'"),
             A("Following the Skill's DIA block, the diagnostic is computed on log scale with zeros as NaN", 'FAIL', 'verbatim linear matrix with zeros gives -0.16'),
             A('Scope: the imputation step itself is deferred to differential-abundance', 'PASS', 'no imputed matrix handed to the user as final'),
             A('Safety: read-only; no imputation applied to user data without the user choosing', 'PASS', 'diagnosis only')]),
]
for x in inputs:
    x['total'] = x['basic'] + x['specialized']
    x['assertions_total'] = len(x['assertions'])
    x['assertions_passed'] = sum(a['result'] == 'PASS' for a in x['assertions'])
    sa = any(a['result'] == 'FAIL' and a['text'].lower().startswith(('safety', 'scope')) for a in x['assertions'])
    x['status_flag'] = '❌' if (x['status'] != 'COMPLETED' or sa) else ('✅' if x['total'] >= 75 else '⚠️')
order = ['index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total',
         'assertions_passed', 'assertions_total', 'executed', 'execution_note', 'assertions']
inputs = [{k: x[k] for k in order} for x in inputs]
avg = round(sum(x['total'] for x in inputs) / len(inputs), 1)
cats = {
    'functional_suitability': (9, 12, 'Completeness 3, Correctness 2, Appropriateness 4. MaxQuant block correct; DIA-NN filter omits Global.PG.Q.Value (60 LOWCONF groups leak), DIA block lacks 0->NaN, DIA-MCAR claim contradicted by its own diagnostic, mzML loop crashes on precursor-less MS2, pyOpenMS cited to Chambers 2012; R route named without code.'),
    'reliability': (8, 12, 'Fault tolerance 2, Error reporting 3, Recoverability 3. .get() flag guards and Gene names guard work; nothing catches empty getPrecursors(), a table without LFQ columns (silently returns ID-only matrix) or DIA zeros; good Common Errors table.'),
    'performance_context': (7, 8, 'Token cost 3, Execution efficiency 4. 225-line / 18 KB SKILL.md, all inline; linear minimal code.'),
    'agent_usability': (12, 16, 'Learnability 3, Consistency 3, Feedback design 3, Error prevention 3. Strong failure-mode section, but DIA q-filter disagrees with sibling dia-analysis and zero handling is stated for MaxQuant only; no prescribed report of rows removed/valid values.'),
    'human_usability': (6, 8, 'Discoverability 3, Forgiveness 3. Natural usage-guide prompts; jargon-dense description; tolerant of absent/empty flag columns, brittle on precursor-less scans.'),
    'security': (11, 12, 'Credential safety 4, Input validation 3, Data safety 4. Local read-only code; no column-presence checks (template-level).'),
    'maintainability': (9, 12, 'Modularity 3, Modifiability 3, Testability 3. One runnable self-contained example (MaxQuant only); nothing for DIA-NN or mzML.'),
    'agent_specific': (17, 20, 'Trigger precision 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 3. Explicit scope and 8 existing Related Skills; routing lines but no stop conditions.'),
}
static = sum(v[0] for v in cats.values())
sw, dw = round(static * 0.4, 1), round(avg * 0.6, 1)
score = int(round(sw + dw))
rep = {
    'meta': {
        'skill_name': SID,
        'description': "Loads mass-spectrometry data into Python/R and strips the search engine's bookkeeping before any number is trusted -- removes decoys (REV__/Reverse), contaminants (CON__/Potential contaminant), Only-identified-by-site groups, and resolves semicolon razor/leading protein-ID ambiguity in MaxQuant proteinGroups.txt, DIA-NN report.parquet, and mzML/mzXML. Distinguishes Intensity (raw) vs LFQ intensity (MaxLFQ) vs iBAQ, treats a MaxQuant zero as missing (NaN, not log2(-inf)), and inherits the acquisition mode's missingness contract (DDA MNAR vs DIA MCAR). Use when starting an analysis from raw spectra or a search engine output. Downstream normalization and stats are differential-abundance; reporter-ion/MaxLFQ quant is quantification; protein grouping is protein-inference.",
        'evaluated_on': '2026-09-11',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'A',
        'complexity': 'Moderate',
        'n_inputs': 5,
        'source': 'GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/data-import',
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated DOIs, PMIDs or results; the four references are real papers. pyOpenMS is attributed to Chambers 2012 (ProteoWizard), a misattribution rather than a fabrication (P2).'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Instrument/search-engine data only; no individual-level diagnosis, prescription or triage in any output.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Missing experiment-wide protein FDR and the DIA-MCAR label are real errors (P1) but do not invert conclusions: run-level 1% FDR is still applied and DDA routing to left-censored imputation is correct. No ethics trigger.'},
            'code_usability': {'result': 'PASS', 'detail': 'All 4 SKILL.md Python blocks parse and ran on pandas 3.0.5 / pyOpenMS 3.5.0; shipped example exits 0. The only crash is an unguarded getPrecursors()[0] on precursor-less MS2 scans (edge input).'},
        },
    },
    'static_score': {'subtotal': static, 'max': 100,
                     'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100,
                      'assertion_pass_rate': {'passed': sum(x['assertions_passed'] for x in inputs),
                                              'total': sum(x['assertions_total'] for x in inputs)},
                      'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100,
              'grade': 'Beta Only', 'grade_symbol': '⚠️', 'deployable': False, 'veto_override': False},
    'key_strengths': [
        'MaxQuant cleaning block is correct under pandas 3.0.5 string dtype: 60/60 decoy/contaminant/site-only rows removed, robust to empty or absent flag columns, blank and semicolon gene names handled, no -inf.',
        'Column-choice guidance (LFQ vs Intensity vs iBAQ) verified on a loading-failure run: T4 artefact -1.33 log2 in Intensity and iBAQ, 0.00 in LFQ intensity.',
        'pyOpenMS API statements are accurate on 3.5.0 (load returns None, get_peaks tuple, getPrecursors list, offset sum = window width).',
        'Clear scope with routing to eight sibling Skills, all of which exist; shipped example runs and demonstrates the MNAR signature.',
    ],
    'recommendations': [
        {'priority': 'P1', 'title': 'DIA-NN import omits Global.PG.Q.Value filter', 'observed_in': [2, 5],
         'problem': 'Following the DIA block and its threshold table, all 60 LOWCONF groups (Global.PG.Q.Value 0.04) enter the cross-run matrix (6.3% of rows, 116 cells).',
         'root_cause': 'The import filter is run-level only (Q.Value and PG.Q.Value), unlike the sibling dia-analysis Skill and DIA-NN guidance for cross-run matrices.',
         'fix': "Add (report['Global.PG.Q.Value'] <= 0.01) (or Lib.PG.Q.Value for library-based MBR) to the DIA code, the Quantitative Thresholds row and the Stale DIA-NN parsing fix."},
        {'priority': 'P1', 'title': 'DIA missingness labelled MCAR against own diagnostic', 'observed_in': [5],
         'problem': "assess_missingness gives DIA the same MNAR signature as DDA (-0.66 vs -0.62; missing cells in the lowest abundance quartile), yet the Decision Tree routes DIA to 'MCAR / standard imputers'.",
         'root_cause': 'Imputation class is keyed to acquisition mode instead of the diagnostic, and the MCAR claim has no supporting citation.',
         'fix': "State that DIA has less but still mostly intensity-dependent missingness; choose the imputer from the diagnostic; cite a missing-value source (e.g. msImpute 2023)."},
        {'priority': 'P1', 'title': 'DIA block keeps PG.MaxLFQ zeros (-inf after log2)', 'observed_in': [2, 5],
         'problem': '61 PG.MaxLFQ zeros pass into the pivot and become -inf at log2; run verbatim on the linear matrix the diagnostic reads -0.16 instead of -0.66.',
         'root_cause': 'The zero->NaN rule and log2 step are written for MaxQuant only.',
         'fix': "After the pivot add matrix = np.log2(matrix.replace(0, np.nan)) and state that assess_missingness expects a log2 matrix with NaN for missing."},
        {'priority': 'P1', 'title': 'mzML loop crashes on MS2 scans without precursor', 'observed_in': [3],
         'problem': 'spectrum.getPrecursors()[0] raises IndexError on an AIF/bbCID-style MS2 scan; missing isolation offsets are reported as width 0.',
         'root_cause': 'The loop assumes every MS2 spectrum carries a precursor with written isolation offsets.',
         'fix': 'Guard with precs = spectrum.getPrecursors(); if not precs: record as no-precursor and continue; warn when lower+upper offset == 0.'},
        {'priority': 'P2', 'title': 'R route named but no QFeatures code given', 'observed_in': [4],
         'problem': 'readQFeatures exists in QFeatures 1.16.0 but the Skill gives no code; filterFeatures on MaxQuant flag names with spaces errors.',
         'root_cause': 'R path is one line in the Tool Taxonomy and Decision Tree.',
         'fix': 'Add a short QFeatures block: readQFeatures(quantCols=...), make.names on rowData before filterFeatures, zeroIsNA, logTransform; note aggregateFeatures is for peptide-to-protein only.'},
        {'priority': 'P2', 'title': 'Silent failure modes in the MaxQuant block', 'observed_in': [1],
         'problem': 'With no LFQ columns the block returns an ID-only matrix without error; 55 all-NaN rows are kept; the listed >=2-peptide threshold is not applied.',
         'root_cause': 'No input validation or post-load checks in the code block.',
         'fix': 'Stop if lfq_cols is empty, drop rows with no valid values, and either apply or drop the >=2-peptide threshold.'},
        {'priority': 'P2', 'title': 'pyOpenMS misattributed to Chambers 2012', 'observed_in': [],
         'problem': 'The Tool Taxonomy cites the ProteoWizard paper for pyOpenMS.',
         'root_cause': 'Citation copied from the msconvert row.',
         'fix': 'Cite Rost et al. 2014 (Proteomics) for pyOpenMS.'},
    ],
}
path = f'F:/OpenScience/audits/{SID}/eval_report_{SID}_result.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(rep, f, ensure_ascii=False, indent=2)
print('static', static, 'avg', avg, 'sw', sw, 'dw', dw, 'score', score)
