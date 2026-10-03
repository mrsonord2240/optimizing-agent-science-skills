"""Build report.json, source-identity.json and viewer.md for the final re-audit of bio-splicing-quantification.
Run: python build_record.py <run_root>"""
import hashlib, json, os, sys
root = sys.argv[1]
SKILL = r'F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification'
IDENT = '0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf'

files = []
for dp, _, fn in os.walk(SKILL):
    for f in fn:
        p = os.path.join(dp, f)
        b = open(p, 'rb').read()
        files.append({'path': os.path.relpath(p, SKILL).replace('\\', '/'), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x['path'])
manifest = '\n'.join(f"{x['path']}\t{x['bytes']}\t{x['sha256']}" for x in files)
assert hashlib.sha256(manifest.encode()).hexdigest() == IDENT, 'candidate identity differs'
nbytes = sum(x['bytes'] for x in files)

identity = {
    'origin': {
        'repository': 'GPTomics/bioSkills',
        'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
        'path': 'alternative-splicing/splicing-quantification',
        'subtree': '6e11b64e5f1c319983ec851f3d922655291db35a',
        'checkout': r'F:\optimizing-agent-science-skills\external\GPTomics__bioSkills',
        'status': 'clean',
        'files': [
            {'path': 'SKILL.md', 'git_blob': '686fd3bbca0044c82f86e05ce7cf3231e2fdcb83'},
            {'path': 'examples/quantify_splicing.py', 'git_blob': '43c5d63b74589c582c327559064c47e53696a47a'},
            {'path': 'usage-guide.md', 'git_blob': '37b3fa27d836861548f6e32755e4b72dd757d4a4'},
        ],
        'normalization_note': 'The audited tree moves examples/quantify_splicing.py to scripts/, extracts two references/ files from SKILL.md, and edits SKILL.md, usage-guide.md and the script (run-fix-1); origin identifies the source Skill subtree, not a one-to-one file mapping.',
    },
    'candidate': {
        'branch': 'normalize/bio-splicing-quantification',
        'commit': '29f5446',
        'path': SKILL,
        'status_before': 'untracked Skill subtree only',
        'status_after_execution': 'untracked Skill subtree only; candidate files unchanged (identity re-verified with skill_preflight --offline before and after)',
        'content_sha256': IDENT,
        'content_manifest': {
            'file_count': len(files), 'bytes': nbytes,
            'recipe': 'relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; records sorted by path and separated by LF; no trailing LF',
        },
    },
    'files': files,
    'tooling': {
        'tools_md': r'F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md',
        'tools_md_sha256': '13b0c7a4db587df809e02aac2bc52e87921ac05ec42036be8c0a86e0c7fadcec',
        'rubric_zip_sha256': 'recorded from repository skill-auditor.zip',
        'environment': 'WSL science: as-core (rMATS-turbo 4.4.0, regtools 1.0.0, leafcutter 0.2.9 scripts, STAR 2.7.11b, samtools 1.24; pandas 2.3.3, statsmodels 0.15.0), as-suppa (SUPPA 2.4, statsmodels 0.14.6, pandas 3.0.6), as-irfinder (IRFinder 1.3.1); combined env sha256 20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c re-fingerprinted at audit start (unchanged); staged public data (nf-core rnasplice chrX 2v2, synthetic planted)',
    },
    'prior_audit': {'identity': '1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c', 'run': 'run-initial-1', 'score': 64, 'grade': 'Reject'},
    'candidate_cache_artifacts_after_execution': [],
}

A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
inputs = [
    dict(index=1, type='Canonical', label='Fresh rMATS-turbo 4.4.0 on real chrX 2v2 BAMs, then parse per the Skill (inline snippet, 5 types x JC/JCEC)', status='COMPLETED', status_flag='\u2705',
         note='rMATS rc 0 (SE 958, A5SS 216, A3SS 251, MXE 51, RI 174); SKILL.md snippet extracted and executed verbatim (20 reliable SE rows); parse_rmats_output vs an independent stdlib-csv oracle on 36 file x min-reads cases: 0 failures, max error 0',
         basic=36, specialized=53, assertions=[
             A('rMATS runs with the flags the Skill states and writes all five JC and JCEC files', 'PASS', 'rc 0; row counts equal the earlier audit (958/216/251/51/174)'),
             A('SKILL.md inline snippet runs on the real JC output', 'PASS', 'executed verbatim from the extracted code block; 20 reliable rows (was TypeError)'),
             A('mean_PSI, mean_PSI_group1/2 equal an independent mean of IncLevel1+IncLevel2 for every event type, JC and JCEC', 'PASS', '30 real-data cases (5 types x JC/JCEC x min reads 0/10/20): maxerr 0.0 vs independent oracle (SQ-03)'),
             A('Reliability keeps an event only if every replicate of BOTH groups has IJC+SJC >= N', 'PASS', 'kept ID sets equal the oracle in all 30 cases; e.g. JC SE 958/38/20, A5SS 216/12/9, A3SS 251/12/6, MXE 51/0/0, RI 174/10/7 at N 0/10/20 (SQ-03)'),
             A('Per-event coordinate columns exist for A5SS, A3SS, MXE and RI', 'PASS', 'no KeyError for any of the five types, JC or JCEC (SQ-02)'),
             A('IncLevelDifference never enters mean_PSI', 'PASS', 'engineered and real tables: pooled mean equals the hand value (SQ-03)')]),
    dict(index=2, type='Variant A', label='Planted hand-checkable SE data: effective-length PSI and IncFormLen statements', status='COMPLETED', status_flag='\u2705',
         note='Planted IJC 80/SJC 10 gives IncLevel 0.8 (naive 0.889); mean_PSI_group1/2 0.7897/0.2027; JC IncFormLen 98 / SkipFormLen 49, JCEC 149; formula reproduces IncLevel (maxabs 0.0005, 1465 real replicate values); real JC IncFormLen is 148 in only 719 of 958 SE rows',
         basic=35, specialized=52, assertions=[
             A('rMATS IncLevel on planted data equals the hand value', 'PASS', '0.8/0.8/0.769 and 0.2/0.2/0.208; mean 0.7897/0.2027 equal expected.json'),
             A('Skill formula reproduces IncLevel on real JC and JCEC output', 'PASS', 'real JC n=1465 maxabs 0.0005; JCEC n=1549 maxabs 0.0005; planted 0.0003/0.0004'),
             A('JC vs JCEC IncFormLen description matches the files (SQ-08)', 'PASS', 'planted JC 98/49, JCEC 149/49; naive 0.889 vs normalised 0.800'),
             A('IncLevelDifference sign matches b1 minus b2', 'PASS', 'planted +0.587 with b1 the high group'),
             A('Statement that JC lengths are 2*(readLength-1) and readLength-1 holds across real events', 'FAIL', 'real chrX JC SE: 148/74 in 719 of 958 rows; the others (58 distinct pairs) are smaller where short exons or introns limit read positions (SQ-13)')]),
    dict(index=3, type='Variant B', label='SUPPA2 PSI via run_suppa2_quantification, write_suppa_tpm and filter_reliable_events on planted and real chrX TPM', status='COMPLETED', status_flag='\u2705',
         note='Planted PSI 0.8/0.2/0.5 exact; all seven psi files; 3,903 real PSI events (6,475 values) checked across 7 classes against an independent ioe+TPM recomputation (max error 1.1e-16); filter counts equal hand counts at default 0.05-0.95 and at 0.1-0.9; pandas-default header reproducibly fails, written header works; as-core statsmodels 0.15 breaks suppa.py as stated',
         basic=36, specialized=53, assertions=[
             A('SUPPA2 PSI equals the planted PSI through write_suppa_tpm', 'PASS', 'header line is A<TAB>B<TAB>C; G1;SE row 0.8 0.2 0.5 (SQ-06)'),
             A('Real chrX PSI equals an independent recomputation from the .ioe and TPM', 'PASS', '7 classes, 3,903 events and 6,475 values, max |diff| 1.1e-16'),
             A('filter_reliable_events default range 0.05-0.95 matches hand counts, and psi_range is a parameter (SQ-07)', 'PASS', 'SE 185, A5 87, A3 102, MX 11, RI 42, AF 215, AL 71; (0.1,0.9) gives 159/75/84/10/32/182/62, all equal hand'),
             A('Skill states a TPM header contract and a SUPPA2 dependency pin that work', 'PASS', 'pandas-default header: "N expected, N-1 given", no psi file; as-suppa statsmodels 0.14.6 works; as-core 0.15.0 raises ImportError multipletests'),
             A('Skill does not over-claim filter defaults', 'PASS', 'text says psi_range is a script filter, not a rMATS or SUPPA2 default')]),
    dict(index=4, type='Edge', label='parse_rmats_output on engineered NA/low-read tables for all 5 types x JC/JCEC, and on zero-event files', status='PARTIAL', status_flag='\u26a0\ufe0f',
         note='Engineered hand-valued tables pass for all 10 type/count combinations (low-read replicate in group 2 only, in group 1 only, NA replicate); a legitimate header-only rMATS file (type with zero events, as in the planted run) raises a raw KeyError',
         basic=33, specialized=48, assertions=[
             A('Low-read replicate in either group removes the event', 'PASS', 'group-2-only and group-1-only low-read events excluded at N=20 in all 10 combinations (SQ-03)'),
             A('NA replicate values are excluded from the mean, not read as zero', 'PASS', 'group-1 mean 0.9 and pooled (0.9+0.1+0.3)/3 at N=0'),
             A('Output carries the event-specific coordinate columns', 'PASS', 'column order equals RMATS_COORD_COLUMNS for every type'),
             A('A header-only rMATS file (zero events of a type) is handled', 'FAIL', "KeyError: 'min_reads_per_replicate' on planted A5SS/A3SS/MXE/RI (SQ-12)"),
             A('Unsupported event_type gives an actionable message', 'PASS', "ValueError: event_type must be one of ['A3SS', 'A5SS', 'MXE', 'RI', 'SE']")]),
    dict(index=5, type='Stress', label='regtools junctions + leafcutter clustering on STAR BAMs with and without XS tags, using the Skill strand check', status='COMPLETED', status_flag='\u2705',
         note='Untagged BAMs: strand ? for all 2,838 junctions, 0 clusters at -m 50 and -m 5, rc 0; XS-tagged: + 1398, - 1343, ? 99 and 115 clusters at -m 5 (0 at -m 50 on this tiny data, as the Skill states)',
         basic=34, specialized=51, assertions=[
             A('Skill states the XS prerequisite beside the regtools command (SQ-04)', 'PASS', 'prerequisite paragraph with STAR --outSAMstrandField intronMotif and HISAT2 note'),
             A('The Skill strand-check command distinguishes tagged from untagged junction files', 'PASS', 'tail -n +2 | cut -f6 | sort | uniq -c gives only ? versus + - ?'),
             A('Tagged route yields clusters', 'PASS', '115 clusters at -m 5 from XS-tagged BAMs'),
             A('Zero clusters with rc 0 on untagged BAMs is warned about', 'PASS', 'Skill says the run still exits 0 with zero clusters; reproduced'),
             A('leafcutter_cluster_regtools.py source is named and exists', 'PASS', 'clustering/ of davidaknowles/leafcutter; file present in the staged clone')]),
    dict(index=6, type='Scope Boundary', label='IRFinder 1.3.1 reference build and FastQ quantification exactly as references/ states', status='COMPLETED', status_flag='\u2705',
         note='Old syntax rc 1 (-r is required); BuildRefFromSTARRef rc 0 in 4m12s through the repaired staged wrapper; -m FastQ single-end and paired-end rc 0, 7,955 intron rows each, SE IRratio identical (r 1.0) to the tooling-delta rebuild, SE vs PE r 0.85',
         basic=35, specialized=51, assertions=[
             A('BuildRefFromSTARRef command runs as documented', 'PASS', 'rc 0; ref holds IRFinder, Mapability, STAR, genome.fa, transcripts.gtf (SQ-05)'),
             A('IRFinder -m FastQ single-end runs and writes IRFinder-IR-nondir.txt', 'PASS', 'rc 0; 7,955 rows; IRratio 0-1'),
             A('Paired-end form (two FASTQ) runs', 'PASS', 'rc 0; 7,955 rows; 98 vs 74 introns above IRratio 0.1 (PE vs SE of the same sample)'),
             A('Old broken syntax is gone from the Skill', 'PASS', 'literal old form rc 1 reproduced; Skill now shows -m FastQ'),
             A('IRFinder-S 2.0 is not presented as executed', 'PASS', 'labelled "not executed" in SKILL.md and the reference'),
             A('Scope: IR route stays within quantification', 'PASS', 'no differential testing claimed')]),
    dict(index=7, type='Adversarial', label='Restricted and heavy surfaces (MAJIQ V3/VOILA, VAST-TOOLS) and unreproduced figures: must not be presented as verified', status='COMPLETED', status_flag='\u2705',
         note='Document inspection by design: MAJIQ V3/VOILA (restricted licence) and VAST-TOOLS (6.7 GB VASTDB) were not executed and not bypassed; the Skill labels both, Shiba, MicroExonator, S-IRFindeR, iREAD and IRFinder-S 2.0 as not executed, and literature figures as not reproduced',
         basic=35, specialized=52, assertions=[
             A('MAJIQ V3/VOILA commands carry a not-executed label with the licence reason', 'PASS', '"Not executed here" block precedes the commands'),
             A('VAST-TOOLS and the other unexecuted tools are labelled', 'PASS', 'Version Compatibility paragraph and matrix cells'),
             A('Benchmark figures are marked as literature, not reproduced', 'PASS', 'FDR 15-30%, ~14% junctions, ~70% microexons, 94% marked reported/not reproduced'),
             A('Related Skills resolve on the shelf (SQ-10)', 'PASS', 'all seven shelf IDs exist under F:\\optimized-scientific-skills\\skills')]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
cats = {
    'functional_suitability': (11, 12, 'Taxonomy, tool selection, effective-length PSI, SUPPA2, regtools/leafcutter and IRFinder commands all reproduce on real tool output; the shipped parser agrees with an independent oracle for all five event types; JC length statement is exact only for typical events (SQ-13)'),
    'reliability': (8, 12, 'XS-tag prerequisite and strand check, SUPPA2 header and pin, and clear unsupported-event errors; a legitimate zero-event rMATS file still raises a raw KeyError (SQ-12) and leafcutter exits 0 with zero clusters on untagged BAMs (documented)'),
    'performance_context': (6, 8, 'SKILL.md 294 lines with failure modes and IR/microexon detail routed to references; tool matrix and decision tree still overlap'),
    'agent_usability': (14, 16, 'Decision tables, thresholds and reconciliation rules are clear; BAM-list format, TPM header contract, XS prerequisite and JC/JCEC lengths are now stated'),
    'human_usability': (7, 8, 'Good pitfalls and prompts; literature figures are labelled; one unhelpful raw error on empty rMATS files'),
    'security': (11, 12, 'No credentials; subprocess calls use argument lists; no shell interpolation'),
    'maintainability': (9, 12, 'Small modular script with per-type column map and parameterised thresholds and docstrings; no tests and a single dependency pin'),
    'agent_specific': (18, 20, 'Precise trigger description; progressive disclosure works; Related Skills resolve; restricted and heavy surfaces are labelled not executed'),
}
static = sum(v[0] for v in cats.values())
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
n_pass = sum(i['assertions_passed'] for i in inputs)
n_tot = sum(i['assertions_total'] for i in inputs)
sw, dw = round(static * 0.4, 1), round(avg * 0.6, 1)
final = round(static * 0.4 + avg * 0.6, 1)
score = round(final)
l1 = sum(i['basic'] for i in inputs) / len(inputs)
l2 = sum(i['specialized'] for i in inputs) / len(inputs)
gate = static >= 80 and avg >= 85 and l1 >= 32 and l2 >= 48 and n_pass / n_tot >= 0.9 and final >= 85
print('static', static, 'avg', avg, 'L1', round(l1, 1), 'L2', round(l2, 1), 'assertions', n_pass, n_tot, f'{n_pass / n_tot:.3f}', 'final', final, 'gate', gate)
assert gate

recs = [
    ('P2', 'parse_rmats_output raises a raw KeyError on an rMATS file with zero events', [4],
     "A header-only MATS file (an event type with no events, as in the planted rMATS run for A5SS, A3SS, MXE and RI) makes DataFrame.apply return an empty frame, then df['min_reads_per_replicate'] raises KeyError.",
     'The per-row statistics are added with concat on an apply result that is empty for an empty table.',
     'Return an empty frame with the expected columns (or raise a ValueError naming the empty file) when the table has no rows; add a header-only test. (SQ-12)'),
    ('P2', 'JC IncFormLen/SkipFormLen stated as constants', [2],
     'SKILL.md says JC lengths are 2*(readLength-1) and readLength-1; on real chrX data only 719 of 958 SE rows have 148/74 (58 distinct pairs), the rest are smaller where short exons or introns limit read positions.',
     'Planted single-exon data (98/49) was generalised to all events.',
     'Say the values are the maximum for exons and introns longer than a read, and that rMATS prints the per-event lengths in the file. (SQ-13)'),
]
report = {
    'meta': {
        'skill_name': 'bio-splicing-quantification',
        'description': 'Quantifies alternative splicing as PSI from RNA-seq with rMATS-turbo, SUPPA2, MAJIQ V3, leafcutter, VAST-TOOLS, Shiba and IRFinder, with event taxonomy, tool selection, quality thresholds and reconciliation rules.',
        'evaluated_on': '2026-10-03',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'D',
        'complexity': 'Complex',
        'n_inputs': len(inputs),
        'performed_by': 'Claude (Anthropic) final re-audit worker, lane 2',
        'auditor_independent': True,
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated values; planted PSI, formula, SUPPA2 and rMATS values reproduce; unexecuted tools and literature figures are labelled'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Research-method Skill with no clinical conclusions; disease signatures are cited literature'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Effective-length PSI, both-group replicate reliability, tool-family reconciliation and sign conventions held'},
            'code_usability': {'result': 'PASS', 'detail': 'Inline snippet and parse_rmats_output run on real rMATS output for all five event types, JC and JCEC, and match an independent oracle; SUPPA2, regtools/leafcutter and IRFinder commands run as written; a zero-event file raises a loud KeyError (SQ-12, P2)'},
        },
    },
    'static_score': {'subtotal': static, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': n_pass, 'total': n_tot}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Production Ready', 'grade_symbol': '\u2b50', 'deployable': True, 'veto_override': False},
    'key_strengths': [
        'Silent wrong-answer defects of the initial audit (mean PSI polluted by IncLevelDifference, group-1-only reliability filter) are fixed: independent recomputation matches on 30 real-output cases and all engineered cases',
        'Every runnable surface the Skill states now runs as written: inline snippet, five-type parser, SUPPA2 with header writer, regtools/leafcutter with XS check, IRFinder BuildRefFromSTARRef and FastQ SE/PE',
        'Restricted (MAJIQ V3/VOILA) and heavy (VAST-TOOLS) surfaces are labelled not executed and not bypassed',
        'No credentials, and subprocess calls use argument lists',
    ],
    'recommendations': [dict(priority=p, title=t, observed_in=o, problem=pr, root_cause=rc, fix=f) for p, t, o, pr, rc, f in recs],
}
json.dump(report, open(os.path.join(root, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
json.dump(identity, open(os.path.join(root, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)

disp = [
    ('SQ-01', 'inline snippet TypeError', 'fixed', 'snippet extracted from SKILL.md and executed verbatim on fresh real JC output: 20 reliable rows (32_snippet_and_forms)'),
    ('SQ-02', 'parser KeyError on 4 of 5 types', 'fixed', 'all five types x JC/JCEC run; row counts equal the files; coordinate columns per type (31, 33)'),
    ('SQ-03', 'wrong mean_PSI; group-1-only reliability', 'fixed', 'independent stdlib oracle: 30 real-output cases (5 types x JC/JCEC x N 0/10/20) maxerr 0, kept IDs equal; 10 engineered combinations incl. NA and low-read-in-one-group (31, 33)'),
    ('SQ-04', 'XS prerequisite / silent empty leafcutter', 'fixed', 'untagged: strand ? for all junctions, 0 clusters, rc 0; tagged: 115 clusters at -m 5; Skill check command works (35)'),
    ('SQ-05', 'IRFinder command and version', 'fixed', 'old syntax rc 1; BuildRefFromSTARRef rc 0; -m FastQ SE and PE rc 0, 7,955 rows (36); 1.3.1 stated, IRFinder-S 2.0 labelled not executed'),
    ('SQ-06', 'SUPPA2 TPM header and statsmodels pin', 'fixed', 'write_suppa_tpm output accepted, pandas default header fails, as-core statsmodels 0.15 ImportError, as-suppa 0.14.6 works (34, 37)'),
    ('SQ-07', 'hard-coded 0.1-0.9 filter', 'fixed', 'psi_range default 0.05-0.95 equals hand counts for 7 classes; (0.1,0.9) also equals (34)'),
    ('SQ-08', 'IncFormLen JC vs JCEC', 'fixed with caveat', 'planted JC 98/49, JCEC 149/49 confirmed; the constants hold only for typical events on real data (new SQ-13, P2) (32)'),
    ('SQ-09', 'unlabelled MAJIQ/VAST, unsourced figures', 'fixed', 'static inspection (input 7); not executed by design'),
    ('SQ-10', 'Related Skills names', 'fixed', 'all seven IDs exist on the shelf'),
    ('SQ-11', 'BAM list format, leafcutter source, LICENSE', 'fixed / not-a-defect', 'BAM list sentence present; clustering/ source exists; license: MIT frontmatter plus repository licence evidence, expected preflight warning only'),
]
rows = '\n'.join(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status']} |" for i in inputs)
dtab = '\n'.join(f'| {a} | {b} | {c} | {d} |' for a, b, c, d in disp)
detail = ''
for i in inputs:
    detail += f"\n### Input {i['index']} - {i['type']}: {i['label']}\n\n{i['note']}\n\nScores: Basic {i['basic']}/40, Specialized {i['specialized']}/60, Total {i['total']}/100\n\n" + '\n'.join(f"- [{a['result']}] {a['text']} - {a['note']}" for a in i['assertions']) + '\n'
viewer = f"""# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: independent final re-audit (lane 2) of the fixed candidate; certification run
Exact candidate content SHA-256: `{IDENT}` ({len(files)} files, {nbytes} bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Prior audit: identity 1e34dbd9664e, 64, Reject (veto M4), findings SQ-01..SQ-11
Category: Data Analysis | Mode: D (hybrid) | Complexity: Complex, 7 inputs

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
{rows}

**Static {static}/100; Execution average {avg}/100; Final {final} ({score}); assertion pass rate {n_pass}/{n_tot}; Layer 1 average {l1:.1f}/40; Layer 2 average {l2:.1f}/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `{IDENT[:12]}`. The final score has a narrow margin over the 85 gate.

## Prior finding dispositions (reproduced on real tool output, not inherited)

| ID | Finding | Verdict | Evidence |
|---|---|---|---|
{dtab}

## New findings

- SQ-12 (P2): `parse_rmats_output` raises a raw `KeyError` on a header-only rMATS file (an event type with zero events). Loud failure, not a wrong result.
- SQ-13 (P2): SKILL.md states the JC `IncFormLen`/`SkipFormLen` as constants; real chrX data show them only for 719 of 958 SE rows.

## Not executed

MAJIQ V3/VOILA (restricted licence, not bypassed), VAST-TOOLS (6.7 GB VASTDB, heavy optional), Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0 (installable is 1.3.1). The Skill labels each as not executed.

## Evidence

Run root `F:\\OpenScience\\audits\\bio-splicing-quantification\\run-reaudit-1\\` (`scripts/` published; `evidence/` logs and `out/` raw outputs stay local). Fresh rMATS 4.4.0 runs, independent oracles in scripts 31, 33 and 34, and a re-fingerprint of the three environments (unchanged, combined 20c07bbb...).

## Detailed outputs
{detail}
"""
open(os.path.join(root, 'viewer.md'), 'w', encoding='utf-8').write(viewer)
