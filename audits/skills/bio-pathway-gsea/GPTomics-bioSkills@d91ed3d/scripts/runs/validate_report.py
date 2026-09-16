# -*- coding: utf-8 -*-
import json, io, sys
p = 'F:/OpenScience/audits/bio-pathway-gsea/eval_report_bio-pathway-gsea_result.json'
r = json.load(io.open(p, encoding='utf-8'))
fails = []
def chk(c, m):
    if not c: fails.append(m)

for k in ('meta','veto_gates','static_score','dynamic_score','final','key_strengths','recommendations'):
    chk(k in r, 'missing top-level node ' + k)
sv = r['veto_gates']['skill_veto']
chk(set(sv) == {'gate','stability','contract','determinism','security'}, 'skill_veto keys')
rv = r['veto_gates']['research_veto']
chk(set(rv) == {'applicable','gate','scientific_integrity','practice_boundaries','methodological_ground','code_usability'}, 'research_veto keys')
for k in ('scientific_integrity','practice_boundaries','methodological_ground','code_usability'):
    chk(set(rv[k]) == {'result','detail'}, 'research_veto.%s shape' % k)

s = r['static_score']
want = ['functional_suitability','reliability','performance_context','agent_usability',
        'human_usability','security','maintainability','agent_specific']
chk(list(s['categories']) == want, 'static category keys/order')
tot = 0
for k, v in s['categories'].items():
    chk(set(v) == {'score','max','note'}, k + ' shape')
    chk(isinstance(v['score'], int) and 0 <= v['score'] <= v['max'], k + ' range')
    chk(isinstance(v['note'], str) and v['note'], k + ' note')
    tot += v['score']
chk(tot == s['subtotal'], 'static subtotal %d != %d' % (tot, s['subtotal']))

d = r['dynamic_score']
ins = d['inputs']
chk(len(ins) == r['meta']['n_inputs'], 'input count')
T = AP = AT = B = SP = 0
for i in ins:
    for k in ('index','type','label','status','status_flag','note','basic','specialized','total',
              'assertions_passed','assertions_total','assertions','executed','execution_note'):
        chk(k in i, 'input %s missing %s' % (i.get('index'), k))
    chk(i['basic'] + i['specialized'] == i['total'], 'input %s basic+spec' % i['index'])
    chk(3 <= len(i['assertions']) <= 5, 'input %s assertion cardinality %d' % (i['index'], len(i['assertions'])))
    pa = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    chk(pa == i['assertions_passed'], 'input %s assertions_passed' % i['index'])
    chk(len(i['assertions']) == i['assertions_total'], 'input %s assertions_total' % i['index'])
    for a in i['assertions']:
        chk(set(a) == {'text','result','note'}, 'assertion shape input %s' % i['index'])
        chk(a['result'] in ('PASS','FAIL'), 'assertion result')
    ok = i['status'] == 'COMPLETED' and i['total'] >= 75
    chk(i['status_flag'] == ('\u2705' if ok else '\u26a0\ufe0f'), 'input %s status_flag' % i['index'])
    T += i['total']; AP += pa; AT += len(i['assertions']); B += i['basic']; SP += i['specialized']
n = len(ins)
avg = round(T / n, 1)
chk(avg == d['execution_avg'], 'execution_avg %s != %s' % (avg, d['execution_avg']))
chk(d['assertion_pass_rate'] == {'passed': AP, 'total': AT}, 'assertion_pass_rate')

f = r['final']
chk(f['static_weighted'] == round(s['subtotal'] * 0.4, 1), 'static_weighted')
chk(f['dynamic_weighted'] == round(avg * 0.6, 1), 'dynamic_weighted')
chk(f['score'] == round(f['static_weighted'] + f['dynamic_weighted']), 'final score')
chk(f['veto_override'] == (sv['gate'] == 'FAIL' or rv['gate'] == 'FAIL'), 'veto_override')
chk(2 <= len(r['key_strengths']) <= 5, 'key_strengths cardinality')
order = {'P0': 0, 'P1': 1, 'P2': 2}
pr = [x['priority'] for x in r['recommendations']]
chk(pr == sorted(pr, key=lambda x: order[x]), 'recommendation order')
for x in r['recommendations']:
    chk(set(x) == {'priority','title','observed_in','problem','root_cause','fix'}, 'rec shape: ' + x['title'])
    chk(isinstance(x['observed_in'], list), 'observed_in must be a list: ' + x['title'])
    chk(len(x['title']) <= 60, 'title >60 chars (%d): %s' % (len(x['title']), x['title']))

print('Layer 1 avg %.1f/40   Layer 2 avg %.1f/60   exec avg %.1f' % (B/n, SP/n, avg))
print('static %d   final %.1f -> %d   assertions %d/%d = %.1f%%' %
      (s['subtotal'], f['static_weighted'] + f['dynamic_weighted'], f['score'], AP, AT, 100.0*AP/AT))
print('floors: static>=80 %s | exec>=85 %s | L1>=32 %s | L2>=48 %s | assert>=90%% %s' %
      (s['subtotal'] >= 80, avg >= 85, B/n >= 32, SP/n >= 48, 100.0*AP/AT >= 90))
print('P0=%d P1=%d P2=%d' % (pr.count('P0'), pr.count('P1'), pr.count('P2')))
if fails:
    print('\nFAILED CHECKS:'); [print(' -', m) for m in fails]; sys.exit(1)
print('\nALL SCHEMA CHECKS PASSED')
