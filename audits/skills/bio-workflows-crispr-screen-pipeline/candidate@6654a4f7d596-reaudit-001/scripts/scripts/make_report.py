import json, hashlib, os, subprocess
R = r'F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-001'
SK = r'F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline'
prev = json.load(open(r'F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\candidate@e242270b6fc0-run-002\source-identity.json', encoding='utf-8'))
files = []
for d, _, fs in os.walk(SK):
    for f in fs:
        p = os.path.join(d, f)
        rel = os.path.relpath(p, SK).replace('\\', '/')
        b = open(p, 'rb').read()
        blob = subprocess.run(['git', 'hash-object', p], capture_output=True, text=True).stdout.strip()
        files.append({'path': rel, 'git_blob': blob, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)})
files.sort(key=lambda x: x['path'])
ident = {
    'origin': prev['origin'],
    'candidate': {
        'branch': 'recut/crispr-screen-pipeline',
        'commit': 'f162b3a9fd54e41c8f9e06bb969f86d079788518',
        'base_note': 'commit is the worktree base; the candidate bytes are uncommitted',
        'content_sha256': '6654a4f7d596c13a76b5b68b0346c9f521335f10e4d4a38ae7b58e2f3067d6dc',
        'path': SK,
        'status_before': 'uncommitted recut after fix-001 and one orchestrator edit to routes/chronos.md',
        'status_after_execution': 'unchanged; skill_preflight --offline --shape re-verified the identity (PASS, 19 files)'},
    'files': files,
    'routing_model': 'cli:claude-haiku-4-5-20251001 (OpenRouter out of credit)',
    'tooling': {'routing_cases': 'scripts/routing-cases.json (copy of the lane file; differs from the initial audit copy in cn-correction request and data, rra data, allow_before on cn-correction, rra, mle, jacks)'},
    'candidate_cache_artifacts_after_execution': []}
json.dump(ident, open(R + r'\source-identity.json', 'w', encoding='utf-8'), indent=2)


def A(t, r, n):
    return {'text': t, 'result': r, 'note': n}


inputs = [
    dict(index=1, type='Canonical', label='HAP1 TKOv3: qc.py then rra.py (route commands), real and QC-passing simulated tables', status='COMPLETED', status_flag='\u26a0\ufe0f',
         note='rra.py on real HAP1 reproduces the benchmark (848 negative / 3 positive hits, TSC1/TSC2 enriched). qc.py FAILs the real plasmid and endpoint columns on a raw-count Gini that is not the statistic its 0.1/0.2 gates come from.',
         basic=35, specialized=48, assertions=[
             A('rra.py on real HAP1 returns 18,056 genes with core essentials at the top (POLR2L, EIF3A, GTPBP10, PES1, MRPL53) and TSC1/TSC2 enriched', 'PASS', 'negative hits 848, all lfc<0, max fdr 0.0500; volcano rendered legibly'),
             A('Hit tables are filtered by fdr 0.05 and |lfc| 0.5 and read from gene_summary', 'PASS', '848 / 3 hits; positive TSC2 1.93, TSC1 1.66'),
             A('qc.py reports the same Gini the cited MAGeCK-VISPR gate (plasmid <0.1, negative selection <0.2) is defined on', 'FAIL', 'qc.py Gini on raw counts: T0 0.288, T18 0.34-0.38; MAGeCK definition (ln(count+1)): T0 0.057, T18 0.091-0.101'),
             A('qc.py exits 1 and states the failed gate rather than hiding it', 'PASS', 'exit 1, QC FAIL printed; Pearson 0.789 also reported BELOW 0.8')]),
    dict(index=2, type='Variant A', label='HAP1: BAGEL2 fc/bf/pr with --seed 42 (route commands), then consensus.py on three methods', status='COMPLETED', status_flag='\u2705',
         note='BAGEL2 seeded rerun identical; consensus tiers match the earlier recorded run.', basic=36, specialized=56, assertions=[
             A('bf with --seed 42 is reproducible', 'PASS', 'two seeded runs: max |dBF| 0.0'),
             A('BF output has GENE and BF with essentials at the top', 'PASS', '18,053 genes, BF>6 1,746; POLR2L 131.6, POLR3H 129.5, RRM1 116.4; CEGv2 mean BF 42.9'),
             A('pr file carries Recall, Precision and FDR for the PR-AUC gate', 'PASS', 'columns Gene, BF, Recall, Precision, FDR'),
             A('consensus.py tiers three methods and refuses a single method', 'PASS', 'Tier-1 481, Tier-2 399, Tier-3 874, none 16,302 on the real three-method inputs; one method exits 1')]),
    dict(index=3, type='Edge', label='count route: FASTQ to guide counts with library.csv columns as the route text states', status='COMPLETED', status_flag='\u2705',
         note='The corrected route text (guide id, sequence, gene) maps 100% of simulated reads.', basic=36, specialized=52, assertions=[
             A('route command runs on library.csv with columns sgRNA,Sequence,Gene', 'PASS', 'exit 0'),
             A('count table has 240 guides x 4 samples with 25,000 mapped reads per sample, 100% mapped', 'PASS', 'countsummary Percentage 1 for all four'),
             A('countsummary Gini agrees with the Gini qc.py later reports for the same sample', 'FAIL', 'MAGeCK 0.074 vs qc.py 0.269 for Plasmid (log vs raw scale); same defect as input 1'),
             A('Skill states the mapping gate as a stop', 'PASS', 'routes/count.md: below 65-70% check trim and library before going on')]),
    dict(index=4, type='Variant B', label='Cancer line: cn_correction.R (WSL crispr-ccr, CRISPRcleanR 3.0.1) then rra.py on raw and corrected tables', status='COMPLETED', status_flag='\u2705',
         note='Script ran as shipped on the simulated KY-library table; non-integer guard fires.', basic=35, specialized=52, assertions=[
             A('cn_correction.R writes <prefix>_cleanr_corrected_counts.txt with the input layout', 'PASS', '90,709 x 6, 0 NA, non-integer counts as the route says'),
             A('non-integer input is refused', 'PASS', 'EXIT_GUARD=1'),
             A('rra.py accepts the corrected table and the corrected run changes hit counts', 'PASS', 'negative genes at fdr<0.05: raw 897, corrected 622; MYC lfc -0.63 raw, -0.62 corrected'),
             A('route statement that low-count guides are dropped is exercised', 'PASS', 'reused: tooling-delta evidence 86,881 of 90,709 on the real A375 table (script body unchanged); this simulated table has no low-count guide')]),
    dict(index=5, type='Variant B', label='mle on MAGeCK demo leukemia table; drugz -unpaired on HAP1 columns relabelled as a drug screen', status='COMPLETED', status_flag='\u26a0\ufe0f',
         note='Both commands run; drugz paired mode and a real drug screen remain unexercised (F-10).', basic=33, specialized=48, assertions=[
             A('mageck mle with --permutation-round 10 writes per-cell-line beta/z/p/fdr', 'PASS', '1,000 genes x 14 columns for HL60 and KBM7, top beta C1orf109 -1.80'),
             A('drugz route command runs and writes the documented columns', 'PASS', 'GENE,sumZ,numObs,normZ,pval/rank/fdr for synth and supp; 18,054 genes, 0 NaN'),
             A('drugz paired -c/-x two-replicate command executed on a real drug screen', 'FAIL', 'not exercised: no staged real drug-screen counts (F-10); relabelled HAP1 data carries no drug signal'),
             A('mle run time and genome-scale caveat are stated', 'PASS', 'route says genome-scale takes hours')]),
    dict(index=6, type='Stress', label='Five-line Project Score panel: jacks command and chronos snippet verbatim from the routes', status='COMPLETED', status_flag='\u2705',
         note='Both run as shipped, including the chronos snippet against the standard NEGv1 file.', basic=36, specialized=54, assertions=[
             A('chronos snippet extracted verbatim runs on the standard NEGv1.txt (header GENE)', 'PASS', 'exit 0, 2m36s; 5 x 4,502, 0 NaN; ribosomal mean -2.72 to -2.95; all-gene mean 0.00-0.01'),
             A('jacks command as written runs and gives per-line gene effects', 'PASS', '4,502 genes x 5 lines; RPL/RPS mean -1.04 (MV411) to -1.83 (A375); all-gene mean -0.03 to 0.02'),
             A('Ribosomal genes are clearly more depleted than the all-gene mean in every line for both methods', 'PASS', 'see values above'),
             A('Route states the dict-of-DataFrames and column-name requirements', 'PASS', 'routes/chronos.md lists readcounts=, nepochs, cell_line_name, pDNA')]),
    dict(index=7, type='Adversarial', label='Trap trips: normalized table, missing baseline, baseline inside treatment, absent or wrong plasmid label, non-integer cn input', status='COMPLETED', status_flag='\u2705',
         note='Every guard exits non-zero with a specific message.', basic=36, specialized=52, assertions=[
             A('qc.py refuses the normalized count table', 'PASS', 'counts are not integers ... exit 1'),
             A('qc.py warns when plasmid= is omitted (F-09)', 'PASS', 'WARNING line prints first; HAP1_T0 then passes only the 0.3 gate'),
             A('rra.py refuses missing control= and a sample in both arms', 'PASS', 'exit 1 each with a message naming the baseline rule / overlap'),
             A('qc.py names unknown plasmid samples and lists columns', 'PASS', "plasmid sample(s) not in the table: ['Plasmid']; exit 1")]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_total'] = len(i['assertions'])
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs)
at = sum(i['assertions_total'] for i in inputs)
static = {
    'functional_suitability': (9, 12, 'qc.py computes Gini on raw counts while its 0.1/0.2 gates and the count route (MAGeCK) use ln(count+1); real screens fail QC falsely (F-12).'),
    'reliability': (10, 12, 'All route commands ran as shipped; guards exit non-zero; seeded BAGEL2 reproducible.'),
    'performance_context': (7, 8, 'Routes of 0.7-2.4 KB, background and citations split out; context-lean.'),
    'agent_usability': (12, 16, 'Confirm-four-commitments rule halts a non-interactive agent before the route command on rra and cn-correction (F-13).'),
    'human_usability': (7, 8, 'Plain routes with done-when lines; background separated.'),
    'security': (11, 12, 'No network, no shell injection; rra.py runs mageck by argument list.'),
    'maintainability': (11, 12, 'Tested-with line present; stale UNEXECUTED header removed; no Skill-root LICENSE (F-11).'),
    'agent_specific': (16, 20, 'Router table, order line and route files work for 9 of 11 first-table cases under Haiku; two stop to ask.')}
sub = sum(v[0] for v in static.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
report = {
    'meta': {'skill_name': 'bio-workflows-crispr-screen-pipeline', 'description': 'Use when analyzing a pooled CRISPR knockout, CRISPRi or CRISPRa screen from FASTQ or guide counts to hit genes.',
             'evaluated_on': '2026-10-04', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 7},
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'FAIL',
            'scientific_integrity': {'result': 'PASS', 'detail': 'Citations and tested versions are stated; background.md discloses non-sourced thresholds.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Failed gates must be stated, not hidden; core-essential PR-AUC gate blocks novel hits.'},
            'methodological_ground': {'result': 'FAIL', 'detail': 'qc.py applies the MAGeCK-VISPR Gini gates (plasmid <0.1, negative selection <0.2) to a raw-count Gini; MAGeCK defines it on ln(count+1). Real HAP1 T0 (0.288 vs 0.057) and Project Score plasmid (0.342 vs 0.089) fail falsely. The endpoint gate is also 0.3, not the cited 0.2.'},
            'code_usability': {'result': 'PASS', 'detail': 'Every shipped command and script ran; the chronos snippet works verbatim.'}}},
    'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': round(100 * ap / at, 1), 'assertions_passed': ap, 'assertions_total': at,
                      'layer1_avg': round(sum(i['basic'] for i in inputs) / 7, 1), 'layer2_avg': round(sum(i['specialized'] for i in inputs) / 7, 1), 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': round(sw + dw), 'max': 100, 'grade': 'Reject', 'grade_symbol': '\u274c', 'deployable': False, 'veto_override': True},
    'key_strengths': [
        'All eleven routes execute as shipped; the chronos snippet, jacks command and count route that failed initially now run and give meaningful values',
        'Guards fail loudly with specific messages (rra.py, qc.py, cn_correction.R)',
        'BAGEL2 seeding is reproducible; consensus tiers reproduce on real HAP1 inputs (481/399/874)',
        'Lean router: short routes, with background and citations split from the run path'],
    'recommendations': [
        {'priority': 'P0', 'title': 'qc.py Gini gate uses the wrong statistic (F-12)', 'observed_in': [1, 3],
         'problem': 'qc.py computes Gini on raw counts and gates plasmid at 0.1 and endpoints at 0.3. The cited MAGeCK-VISPR gates (plasmid or initial <=0.1, negative selection <=0.2) are on the MAGeCK Gini, computed on ln(count+1). On real data the two differ about 5x: HAP1 T0 0.288 vs 0.057, T18 0.34-0.38 vs 0.09-0.10, Project Score plasmid 0.342 vs 0.089, A375 endpoints 0.46-0.48 vs 0.16-0.17. A good screen is reported QC FAIL, and qc.py disagrees with the countsummary the count route points to (0.269 vs 0.074).',
         'root_cause': 'gini() in scripts/qc.py is a textbook Gini of raw counts; the thresholds were copied from MAGeCK-VISPR without its definition.',
         'fix': 'Compute Gini on ln(count+1) as mageck count does; set the endpoint gate to the cited 0.2 (drop or source the 0.55 drug-screen figure); state which sample may be passed as plasmid= (the cloned library pool, not Day-0 cells). Rerun qc.py on the real HAP1 and A375 tables and expect Gini to pass; replicate Pearson 0.789 on HAP1 still fails. The simulated QC-passing inputs are then unnecessary.'},
        {'priority': 'P1', 'title': 'Confirm-four-commitments rule stops agents before the route command (F-13)', 'observed_in': [1, 4],
         'problem': 'With Haiku, cn-correction 0/3 (twice) and rra 0/3 then 1/3 open the right route first, then stop to ask for baseline, control classes, screen type and CN profile that the request or data already answer. No command is issued.',
         'root_cause': 'SKILL.md rule 1 requires confirming all four with the user before any code, whatever the request states.',
         'fix': 'Ask only for a commitment the request and file do not state; otherwise state the four as assumptions in the answer and run the route command.'},
        {'priority': 'P2', 'title': 'qc.py prints but does not enforce the guides>25 and skew gates; skew<2 attribution unverified (F-14)', 'observed_in': [1],
         'problem': 'pass uses only Gini and depth; the 99% above 25 reads and p90/p10<2 gates appear in qc.md but never fail a run (real HAP1 T0: 98.99%, 4.25). The Joung 2017 skew figure was not confirmed.',
         'root_cause': 'The gate list in the route is wider than the script.', 'fix': 'Enforce or label them advisory; verify the skew number against Joung 2017.'},
        {'priority': 'P2', 'title': 'Tooling delta edited a routing request and widened allow_before (F-15)', 'observed_in': [4],
         'problem': 'The cn-correction request text gained ", then three day-14 replicates" against the audit copy; allow_before was added to cn-correction, rra, mle, jacks. Neither explains the failures here (the stop is the confirmation rule), but the contract expects unchanged requests.',
         'root_cause': 'Cases were reworked to match new inputs.', 'fix': 'Record the intent in TOOLS.md, or restore the text once real QC-passing screens replace the simulated inputs.'},
        {'priority': 'P2', 'title': 'drugz paired mode and a real drug screen still unexercised (F-10, open)', 'observed_in': [5],
         'problem': 'Only -unpaired on relabelled HAP1 columns ran.', 'root_cause': 'No staged real drug-screen counts.', 'fix': 'Stage a public drug-modifier counts table, or leave static-only and labelled.'},
        {'priority': 'P2', 'title': 'No Skill-root LICENSE (F-11, open)', 'observed_in': [1],
         'problem': 'skill_preflight warns; frontmatter says MIT, author GPTomics.', 'root_cause': 'The recut dropped the file.', 'fix': 'Cite repository license evidence in the manifest or restore LICENSE.'}]}
json.dump(report, open(R + r'\report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(sub, avg, sw, dw, round(sw + dw), ap, at, report['dynamic_score']['layer1_avg'], report['dynamic_score']['layer2_avg'])
