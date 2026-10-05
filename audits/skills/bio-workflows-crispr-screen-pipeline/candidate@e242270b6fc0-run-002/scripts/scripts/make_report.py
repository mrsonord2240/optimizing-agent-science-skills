"""Assemble report.json and viewer.md for run-002 from the recorded observations; checks the schema arithmetic."""
import json
import os

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def A(text, ok, note):
    return {'text': text, 'result': 'PASS' if ok else 'FAIL', 'note': note}


def inp(i, typ, label, status, note, basic, spec, asserts):
    total = basic + spec
    flag = '❌' if status != 'COMPLETED' else ('✅' if total >= 75 else '⚠️')
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': flag, 'note': note,
            'basic': basic, 'specialized': spec, 'total': total,
            'assertions_passed': sum(a['result'] == 'PASS' for a in asserts), 'assertions_total': len(asserts),
            'assertions': asserts}


inputs = [
    inp(1, 'Canonical', 'HAP1 TKOv3 table: qc.py then rra.py (route commands)', 'COMPLETED',
        'QC FAIL reported as expected (plasmid Gini 0.288, replicate r 0.789); RRA 18,056 genes, 848 negative and 3 positive hits; volcano legible', 34, 54, [
            A('qc.py prints per-sample Gini and replicate Pearson and exits 1 on a failed gate', True, 'T0 Gini 0.288 > 0.1, T18 Gini 0.34-0.375 > 0.3, Pearson 0.789 < 0.8, exit 1'),
            A('rra.py writes gene_summary, both hit tables and a volcano', True, 'all four files present'),
            A('Hit table is internally consistent with gene_summary', True, '848 neg hits all have neg|fdr<0.05 and |lfc|>=0.5'),
            A('Known essentials deplete', True, 'POLR2L lfc -7.0 fdr 0.001, RPL11 -5.7; RPS6 has one guide in this table (num=1) so is not called'),
            A('Volcano is readable', True, 'axes labelled, FDR line drawn, red negative/blue positive; y saturates at 3 because MAGeCK permutation FDR floors at 0.001')]),
    inp(2, 'Variant A', 'HAP1: BAGEL2 fc/bf/pr with --seed 42, then consensus.py', 'COMPLETED',
        'BF>6 for 1,746 of 18,053 genes; 93.7% of CEGv2 above BF 6; consensus on shipped HAP1 outputs Tier-1 481, Tier-2 399, Tier-3 874; two-method rerun on this run own outputs Tier-2 840, Tier-3 914', 33, 53, [
            A('fc, bf, pr run as written and write the documented files', True, 'foldchange, bayes_factor.txt (GENE, BF), pr_curve.txt (Recall, Precision, FDR)'),
            A('Core essentials score high BF', True, 'CEGv2 mean BF 42.9; fraction BF>6 0.937'),
            A('consensus.py tiers agree with the per-method hit rules', True, 'n_hits column equals sum of method flags; two methods never give Tier-1'),
            A('Seeded run is reproducible', True, 'route-mandated --seed 42; background.md reports max BF difference 0.0 on rerun; not re-diffed here'),
            A('consensus.py rejects a single method', True, 'stops with "a consensus of one method is not a consensus"')]),
    inp(3, 'Edge', 'count route: FASTQ to guide counts, library.csv columns as route text states', 'PARTIAL',
        'Literal sgRNA,Gene,Sequence library: 0% of reads mapped, all 60 guides zero, Gini -1.03, exit 0 (silent). With id,sequence,gene order: 100% mapped, Gini 0.074 plasmid / 0.106 endpoint', 24, 32, [
            A('mageck count runs with the route command', True, 'exit 0, count.txt and countsummary.txt written'),
            A('Library format stated by the route produces a usable table', False, '0 mapped reads, 60/60 zero-count guides'),
            A('Failure is surfaced rather than silent', False, 'mageck exits 0 and writes an all-zero table; only the route bullet on mapping rate would catch it'),
            A('Corrected library order maps reads', True, '100% mapped, 25,000 reads per sample, counts parse back')]),
    inp(4, 'Variant B', 'A375 cancer line: cn_correction.R (WSL crispr-ccr) then rra.py on the corrected table', 'COMPLETED',
        'CRISPRcleanR 3.0.1 ran the shipped script unchanged: 86,881 of 90,709 guides corrected; BRAF -3.5 to -2.7, MYC -2.4 to -3.1 (guide-level LFC); rra.py accepts the corrected table (952 negative hits); qc.py refuses it', 33, 52, [
            A('Script runs as the route shows and writes the corrected table', True, 'screen_cleanr_corrected_counts.txt, same columns as input, 0 NA'),
            A('Correction changes amplified-locus genes in the expected direction', True, 'guide-level correlation raw vs corrected 0.917; BRAF and MYC shift; 3,828 low-count guides dropped'),
            A('Downstream caller reads the corrected table', True, 'rra.py exit 0, 17,995 genes'),
            A('Route states the corrected table is non-integer and shorter than the input', False, 'only 0.8% of values are integers; 3,828 guides dropped; neither stated; qc.py refusal is not mentioned'),
            A('Non-integer input to the script stops with the fix named', True, 'T6: "counts are not integers: give the raw .count.txt"')]),
    inp(5, 'Variant B', 'mle on MAGeCK demo leukemia table; drugz on HAP1 relabelled as a drug screen', 'COMPLETED',
        'mle: 1,000 genes, per-line beta/z/p/fdr columns, KBM7 52 genes fdr<0.05; drugz: 18,054 genes, 0 NaN, 0 hits at 0.05 (no drug signal expected: labels only)', 31, 48, [
            A('mageck mle runs with the route command and design matrix', True, '2m23s class run, 14 output columns'),
            A('mle output has per-condition beta scores and wald-fdr', True, 'KBM7 and HL60 beta/z/p/fdr/wald columns'),
            A('drugz runs with the route flags (-unpaired variant)', True, 'documented columns GENE..fdr_supp present, 0 NaN'),
            A('Both drugz modes exercised', False, 'paired -c/-x with two drug replicates not run: no staged data has two drug replicates')]),
    inp(6, 'Stress', 'Five-line panel: jacks and chronos, route text as written then tooled variants', 'PARTIAL',
        'jacks literal command: exit 2 (run_JACKS.py is in JACKS/jacks/); chronos literal snippet: AssertionError (cell_line_name), then pDNA row, then negative controls required. Tooled variants: jacks 4,502 genes x 5 lines, ribosomal mean -1.04 to -1.83; chronos ribosomal mean -2.7 to -2.9, all-gene mean 0', 22, 30, [
            A('jacks route command runs as written', False, 'python run_JACKS.py ... exit 2, file not found at the clone root'),
            A('chronos route snippet runs as written', False, 'AssertionError on sequence_map columns; after fixing, needs a cell_line_name==pDNA row and negative_control_sgrnas'),
            A('Tooled jacks output shows ribosomal depletion and null mean near zero', True, 'ribosomal -1.04 to -1.83, all-gene mean about 0'),
            A('Tooled chronos output shows ribosomal depletion and null mean near zero', True, 'ribosomal -2.68 to -2.94, all-gene mean 0.00')]),
    inp(7, 'Adversarial', 'Trap trips: normalized table, missing baseline, one method, no plasmid label', 'COMPLETED',
        'qc.py and cn_correction.R refuse non-integer counts and name the fix; rra.py refuses missing control=; consensus.py refuses one method; qc.py without plasmid= silently applies the endpoint Gini gate to the plasmid (T0 Gini 0.288 passes)', 33, 50, [
            A('Non-integer table refused by qc.py with the fix named', True, 'T1, exit 1'),
            A('Non-integer table refused by cn_correction.R with the fix named', True, 'T6, exit 1'),
            A('Missing control= refused with the reason', True, 'T3 message names the baseline commitment'),
            A('Single-method consensus refused', True, 'T5'),
            A('Omitted plasmid= is flagged', False, 'T2 prints no warning; plasmid sample passes the 0.3 endpoint gate instead of failing 0.1')]),
]

n = len(inputs)
avg = round(sum(i['total'] for i in inputs) / n, 1)
passed = sum(i['assertions_passed'] for i in inputs)
total = sum(i['assertions_total'] for i in inputs)
cats = {
    'functional_suitability': (9, 'Eleven routes cover count to consensus; count, jacks and chronos route text does not run as written'),
    'reliability': (9, 'Scripts stop with the fix named on tripped traps; omitted plasmid= and all-zero mageck count are silent'),
    'performance_context': (7, 'SKILL.md is a short router; routes and references are loaded on demand'),
    'agent_usability': (12, 'Routing check fails 4 of 11 routes; the Order-on-every-screen line pulls agents to qc.md first'),
    'human_usability': (6, 'Terse routes with clear Done-when lines; several omit prerequisites the tool needs'),
    'security': (11, 'No credentials or destructive operations; scripts take file paths and fixed option names only'),
    'maintainability': (9, 'Tested-with line and cn_correction.R header still say CRISPRcleanR was not run; no Skill-root LICENSE'),
    'agent_specific': (15, 'Trigger description is a clean Use-when; four commitments gate and no-hits-first order are strong; route table rows for mle and jacks miss real requests'),
}
sub = sum(v[0] for v in cats.values())
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = int(round(sw + dw))

recs = [
    ('P0', 'chronos.md snippet cannot run (research-veto M4)', [6],
     'The Chronos snippet fails on the first sequence_map assertion; fixing the column name then fails on a missing pDNA row and missing negative_control_sgrnas.',
     'Route shows a constructor call written from the docstring, not a tested one.',
     'Replace the snippet with the tested construction: sequence_map columns sequence_ID, cell_line_name, days, pDNA_batch with a cell_line_name==pDNA row; negative_control_sgrnas per library; counts with sequence_ID rows. Execute it on the staged panel.'),
    ('P1', 'jacks.md command fails: wrong script path and map columns', [6],
     'python run_JACKS.py at the clone root exits 2; the script lives in JACKS/jacks/. replicatemap needs a Control column and guidemap the same sgRNA/Gene headers.',
     'Command was never run from a clone.',
     'Give the real path (JACKS/jacks/run_JACKS.py) and the required map columns; run the command as written.'),
    ('P1', 'count.md library column order gives 0% mapped, exit 0', [3],
     'Route says library.csv columns are sgRNA, Gene, Sequence; mageck count reads id, sequence, gene by position. Following the text gives an all-zero table with exit 0.',
     'Column list written by name, tool reads by position.',
     'State the order id, sequence, gene and make the 65-70% mapping check a stop, not a hint.'),
    ('P1', 'rra route fails routing 0/3: agent opens qc.md first', [1],
     'For a two-condition dropout request the agent opens qc.md (and often cn-correction and bagel2) before rra.md and never runs rra.py within the step budget.',
     'SKILL.md line "Order on every screen: count, QC, copy-number correct..." reads as a reading order; the table row says nothing about the user already having counts.',
     'Reword the order line as the analysis order the answer must respect (QC reported, not read first), and have the rra row name the case: counts in hand, baseline and endpoint known.'),
    ('P1', 'cn-correction route fails routing 1/3', [4],
     'Agent opens qc.md first and in two of three runs never issues the Rscript command.',
     'Same ordering line pulls qc.md first; the row "A cancer cell line screen" is a property of the sample, not an action.',
     'Phrase the row as the action (cancer line, count table in hand, remove amplicon bias) and fix the ordering line.'),
    ('P1', 'mle route fails routing 0/3: row does not describe the request', [5],
     'A two-cell-line initial/final design with a design matrix leads the agent to read every route file; none of three runs reaches mle.md first.',
     'Row text "Time course, several conditions, or several batches" does not match "per-cell-line selection score with a design matrix".',
     'Name the design-matrix case in the row (design matrix, several cell lines or time points, beta scores).'),
    ('P1', 'jacks route fails routing 0/3: panel request goes to chronos', [6],
     'Five cell lines with one library, a replicate map and a guide map: the agent opens chronos.md first, then reads most routes.',
     'jacks row "Several screens in one library" is beaten by chronos row "A DepMap-style panel of cell lines".',
     'Differentiate the two rows (JACKS: replicate map and guide map, no copy-number input; Chronos: needs plasmid, days, negative controls).'),
    ('P2', 'cn-correction.md omits non-integer output and dropped guides', [4],
     'Corrected table has 86,881 of 90,709 guides and non-integer counts; qc.py refuses it. Tested-with line and cn_correction.R header still say CRISPRcleanR was not run, but it ran unchanged.',
     'Route and script header predate execution.',
     'State both properties and the qc-before-correction order; replace the stale UNEXECUTED header and the not-run clause in SKILL.md with the tested CRISPRcleanR 3.0.1 / R 4.4.3 versions.'),
    ('P2', 'qc.py silently skips the plasmid gate when plasmid= is omitted', [7],
     'Without plasmid= the plasmid sample is held to the endpoint Gini 0.3 gate; HAP1_T0 (0.288) passes where the 0.1 gate would fail it.',
     'plasmid= is optional with no warning.',
     'Print a one-line warning (or exit) when plasmid= is absent.'),
    ('P2', 'drugz paired mode and a real drug screen not exercised', [5],
     'Only the -unpaired variant ran, on HAP1 columns relabelled as a drug screen; the paired -c/-x two-replicate command and the vehicle-vs-drug biology are unverified.',
     'No staged public drug screen with two drug replicates.',
     'Tooling-delta pass: stage a real public drug screen; static-only until then.'),
    ('P2', 'no Skill-root LICENSE or provenance note', [],
     'skill_preflight warns: frontmatter says MIT, author GPTomics, but the Skill carries no LICENSE file and no origin statement.',
     'Recut dropped the license context.',
     'Cite the repository license evidence in the manifest or restore a LICENSE at the Skill root.'),
]
report = {
    'meta': {'skill_name': 'bio-workflows-crispr-screen-pipeline',
             'description': 'Use when analyzing a pooled CRISPR knockout, CRISPRi or CRISPRa screen from FASTQ or guide counts to hit genes.',
             'evaluated_on': '2026-10-04', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis',
             'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': n, 'performed_by': 'audit-scientific-skill worker (Claude Sonnet 5.5), initial audit run-002'},
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'FAIL',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated values; every number traced to tool output or recorded public input'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Research-only Skill; no clinical or prescriptive claims'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Baseline, control class, screen type and copy-number commitments are required before analysis; seeded BAGEL2; vehicle control for drug screens'},
            'code_usability': {'result': 'FAIL', 'detail': 'routes/chronos.md snippet raises on the first run and again after the first fix; routes/jacks.md command exits 2 as written (shipped scripts qc.py, rra.py, consensus.py and cn_correction.R all ran)'}}},
    'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': m, 'note': v[1]} for (k, v), m in zip(cats.items(), (12, 12, 8, 16, 8, 12, 12, 20))}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': total}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Reject', 'grade_symbol': '❌',
              'deployable': False, 'veto_override': True},
    'key_strengths': [
        'Four-commitment gate and "never call hits first" order guard the failures that throw no error',
        'Shipped scripts (qc.py, rra.py, consensus.py, cn_correction.R) ran on real public data and stop with the fix named on a normalized table or missing baseline',
        'cn_correction.R ran unchanged under CRISPRcleanR 3.0.1 and shifted amplified loci (BRAF, MYC) as expected',
        'Router stays short: routes and references load on demand'],
    'recommendations': [{'priority': p, 'title': t[:60], 'observed_in': o, 'problem': pr, 'root_cause': rc, 'fix': fx} for p, t, o, pr, rc, fx in recs],
}
assert all(len(i['assertions']) in (3, 4, 5) for i in inputs)
assert report['static_score']['subtotal'] == sum(c['score'] for c in report['static_score']['categories'].values())
for k, c in report['static_score']['categories'].items():
    assert 0 <= c['score'] <= c['max'], k
json.dump(report, open(os.path.join(RUN, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

ids = ['F-%02d' % (j + 1) for j in range(len(recs))]
lines = ['# Audit: bio-workflows-crispr-screen-pipeline (initial, run-002)', '',
         'Candidate e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (uncommitted recut, 19 files). Category Data Analysis, mode D, Complex, 7 inputs.', '',
         f'Static {sub}/100 (x0.4 = {sw}); execution average {avg} (x0.6 = {dw}); final {score} -> diagnostic grade Reject by research-veto M4. Assertions {passed}/{total}.', '',
         'This is a diagnostic score, not a readiness decision.', '', '## Routing check (routing/routing.json, rerun after Docker was up; 3 repeats per route)', '']
lines += ['| Route | Result |', '|---|---|']
for r, v in [('count', 'PASS 3/3'), ('qc', 'PASS 3/3'), ('cn-correction', 'FAIL 1/3'), ('rra', 'FAIL 0/3'), ('bagel2', 'PASS 3/3'),
             ('mle', 'FAIL 0/3'), ('drugz', 'PASS 3/3'), ('jacks', 'FAIL 0/3'), ('chronos', 'PASS 3/3'), ('consensus', 'PASS 3/3'), ('branches', 'PASS 3/3')]:
    lines.append(f'| {r} | {v} |')
lines += ['', 'First attempt (routing-attempt1-402/) had four routes errored by OpenRouter HTTP 402; its other results differed on noisy routes (bagel2 1/3, qc 2/3, drugz 2/3). The clean rerun is the record.', '',
          '## Findings (ordered)', '']
for i, (p, t, o, pr, rc, fx) in zip(ids, recs):
    lines += [f'- **{i} {p}** {t}. {pr} Fix: {fx}']
lines += ['', '## Execution map', '',
          '| Surface | Class |', '|---|---|',
          '| count, qc, rra, bagel2, consensus, mle, drugz (unpaired), jacks, chronos, cn-correction | executed (route text defects above) |',
          '| drugz paired mode | static-only (no staged data) |',
          '| branches (reference route), references/install.md | not-applicable (no runnable surface) |', '',
          '## Per-input scores', '', '| # | Type | Label | Status | Basic | Spec | Total |', '|---|---|---|---|---|---|---|']
for i in inputs:
    lines.append(f"| {i['index']} | {i['type']} | {i['label']} | {i['status']} | {i['basic']} | {i['specialized']} | {i['total']} |")
lines += ['', 'Assertions and notes per input are in report.json. Scripts, logs and outputs: run root scripts/, work/.']
open(os.path.join(RUN, 'viewer.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('score', score, 'avg', avg, 'static', sub, 'assert', passed, total)
