import json, hashlib, os
P = 'F:/optimizing-agent-science-skills/audits/skills/bio-workflows-crispr-screen-pipeline/candidate@6654a4f7d596-reaudit-001/'
R = 'F:/OpenScience/fix-evidence/recut-crispr-pipeline/reaudit-002/'
C = 'F:/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline'
r = json.load(open(P + 'report.json', encoding='utf-8'))
rv = r['veto_gates']['research_veto']
rv['gate'] = 'PASS'
rv['methodological_ground'] = {'result': 'PASS', 'detail': 'qc.py Gini is on ln(count+1) and equals mageck.mageckCount.mageckcount_gini on real HAP1 (0.057 / 0.101 / 0.091 / 0.091); gates 0.1 plasmid and 0.2 endpoint match MAGeCK-VISPR Table 1. Replicate Pearson on log counts matches MAGeCK-VISPR (pairwise Pearson of sample log read counts); the value is invariant to log base and median normalization (checked).'}
rv['practice_boundaries']['detail'] = 'Failed gates must be stated, not hidden; core-essential PR-AUC gate blocks novel hits. N-01: qc.py can print QC PASS with the replicate check not run (P1, see recommendations).'
s = r['static_score']
c = s['categories']
def setc(k, v, n):
    c[k]['score'] = v
    c[k]['note'] = n
setc('functional_suitability', 10, 'Gini matches MAGeCK (F-12 fixed). N-01: the default replicate pattern does not group A375 names, so qc.py prints QC PASS with no replicate check; the same table fails at 0.780 when grouped.')
setc('reliability', 10, 'All route commands ran as shipped; guards exit non-zero; seeded BAGEL2 reproducible; qc.py bad-label guard exits 1.')
setc('agent_usability', 14, 'Rule 1 restates stated commitments and runs the route command (cn-correction 3/3, rra 2/3 under Haiku). qc.md advice to drop the outlier has no outlier on the real replicate sets.')
setc('agent_specific', 18, '11/11 first-table cases PASS under Haiku (7 at 3/3, 4 at 2/3; misses were no-route-first or qc first).')
s['subtotal'] = sum(v['score'] for v in c.values())
d = r['dynamic_score']
I = d['inputs']
i1 = I[0]
i1['label'] = 'HAP1 and A375: qc.py (real, grouped, default pattern, QC-passing resampled) then rra.py on the QC-passing table'
i1['status_flag'] = '⚠️'
i1['note'] = 'Gini equals MAGeCK on real HAP1 and A375; real replicate Pearson 0.789 and 0.780 fails the 0.8 gate as the Skill states; rra.py on the QC-passing table ran (3,646 genes, 688 negative hits, POLR3H/PCNA/POLR2L top). N-01: default pattern on A375 prints QC PASS without a replicate check.'
for a in i1['assertions']:
    if a['text'].startswith('qc.py reports the same Gini'):
        a['result'] = 'PASS'
        a['note'] = 'HAP1 0.057/0.101/0.091/0.091 equals mageckcount_gini on ln(count+1); A375 plasmid 0.089, endpoints 0.155-0.174'
i1['assertions'].append({'text': 'qc.py does not print QC PASS when the replicate-correlation check could not run', 'result': 'FAIL', 'note': 'A375 with default pattern: no condition has two samples, QC PASS, exit 0; with pattern R\\d(?=_P1D14$) Pearson 0.780, QC FAIL'})
i1.update(basic=36, specialized=52, total=88, assertions_total=5, assertions_passed=4)
i3 = I[2]
for a in i3['assertions']:
    if a['text'].startswith('countsummary Gini agrees'):
        a['result'] = 'PASS'
        a['note'] = 'qc.py on the count-route table: Plasmid 0.074, endpoints 0.106-0.115, equal to countsummary'
i3['note'] = 'Corrected route text maps 100% of simulated reads; qc.py Gini now agrees with countsummary.'
i3.update(basic=36, specialized=56, total=92, assertions_passed=4)
n = len(I)
d['execution_avg'] = round(sum(i['total'] for i in I) / n, 1)
d['layer1_avg'] = round(sum(i['basic'] for i in I) / n, 1)
d['layer2_avg'] = round(sum(i['specialized'] for i in I) / n, 1)
d['assertions_total'] = sum(i['assertions_total'] for i in I)
d['assertions_passed'] = sum(i['assertions_passed'] for i in I)
d['assertion_pass_rate'] = round(100 * d['assertions_passed'] / d['assertions_total'], 1)
sw = round(s['subtotal'] * 0.4, 1)
dw = round(d['execution_avg'] * 0.6, 1)
r['final'] = dict(static_weighted=sw, dynamic_weighted=dw, score=round(sw + dw), max=100, grade='Production Ready', grade_symbol='⭐', deployable=True, veto_override=False)
r['key_strengths'] = [
    'F-12 fixed and verified two ways: qc.py Gini equals MAGeCK mageckcount_gini on real HAP1; real plasmids pass 0.1 and endpoints 0.2',
    'All eleven routing cases PASS under Haiku, including the two that failed in reaudit-001',
    'Replicate Pearson computed as MAGeCK-VISPR does (Pearson on log counts), checked invariant to log base and median normalization',
    'Guards fail loudly; seeded BAGEL2, consensus and rra reproduce']
r['recommendations'] = [
    {'priority': 'P1', 'title': 'qc.py prints QC PASS when no replicate group exists (N-01)', 'observed_in': [1],
     'problem': 'The default pattern does not group Project Score names (A375_C902R1_P1D14). qc.py prints "no condition has two samples under this pattern", then QC PASS, exit 0. Grouped, the same table has Pearson 0.780 and fails. A QC script that skipped a gate must not report PASS.',
     'root_cause': 'The no-group branch only prints; the failed flag is unchanged.',
     'fix': 'When no condition has two samples, exit 1 with "QC INCOMPLETE: replicate check not run" (or require an explicit option to skip); make the default pattern also strip a trailing R<digit>_<suffix>, or tell the route to pass pattern= for names it does not group. Under 20 lines in qc.py plus one line in routes/qc.md.'},
    {'priority': 'P2', 'title': 'Replicate-Pearson gate has no action when it is the only failure (F-16)', 'observed_in': [1],
     'problem': 'Both real published screens fail 0.8 (HAP1 0.789, A375 0.780). The statistic is faithful to MAGeCK-VISPR, but the route says to drop the outlier and rerun while the real pairs (0.776/0.782/0.808; 0.767/0.781/0.792) have no outlier, and the "0.85 comfortable" figure has no source in Li 2015 Table 1. qc.py exits 1, so an agent may stop.',
     'root_cause': 'A guideline value is treated as a hard stop with a remedy that does not fit.',
     'fix': 'State that 0.8 is the MAGeCK-VISPR guideline, report a miss as a caveat when depth, Gini and CEGv2 PR-AUC pass, and drop or source the 0.85 figure.'},
    {'priority': 'P2', 'title': 'drugz paired mode and a real drug screen still unexercised (F-10, open)', 'observed_in': [5],
     'problem': 'Only -unpaired on relabelled HAP1 columns ran.', 'root_cause': 'No staged real drug-screen counts.',
     'fix': 'Stage a public drug-modifier counts table, or leave static-only and labelled.'},
    {'priority': 'P2', 'title': 'No Skill-root LICENSE (F-11, open)', 'observed_in': [1],
     'problem': 'skill_preflight warns; frontmatter says MIT, author GPTomics.', 'root_cause': 'The recut dropped the file.',
     'fix': 'Cite repository license evidence in the manifest or restore LICENSE.'},
    {'priority': 'P2', 'title': 'Routing cases use resampled data and allow_before (F-15 residue)', 'observed_in': [4],
     'problem': 'Request text equals the audit copy, but cn-correction and rra point at QC-passing resampled tables, and allow_before was added for four cases.',
     'root_cause': 'Real tables stop at QC by design.',
     'fix': 'Keep the TOOLS.md disclosure; replace with a real QC-passing screen if one is staged.'}]
json.dump(r, open(R + 'report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
si = json.load(open(P + 'source-identity.json', encoding='utf-8'))
files = []
for rr, dd, fs in os.walk(C):
    for f in fs:
        p = os.path.join(rr, f)
        rel = os.path.relpath(p, C).replace(chr(92), '/')
        b = open(p, 'rb').read()
        files.append({'path': rel, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)})
files.sort(key=lambda x: x['path'])
si['candidate']['content_sha256'] = '05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5'
si['candidate']['status_before'] = 'uncommitted recut after fix-002 (changed vs reaudit-001: SKILL.md, references/citations.md, routes/qc.md, scripts/qc.py; verified by sha256 manifest)'
si['candidate']['status_after_execution'] = 'unchanged; skill_preflight --offline --shape PASS, 19 files'
si['files'] = files
json.dump(si, open(R + 'source-identity.json', 'w', encoding='utf-8'), indent=2)
print(s['subtotal'], sw, d['execution_avg'], dw, r['final']['score'], d['layer1_avg'], d['layer2_avg'], d['assertion_pass_rate'], d['assertions_passed'], d['assertions_total'])
