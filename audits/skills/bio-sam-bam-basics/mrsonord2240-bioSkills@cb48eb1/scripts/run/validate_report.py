"""Pre-emit checklist of skill-auditor/references/report_json_schema.md, applied to the written report."""
import json, os
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eval_report_bio-sam-bam-basics_result.json')
r = json.load(open(p, encoding='utf-8'))
assert set(r) == {'meta', 'veto_gates', 'static_score', 'dynamic_score', 'final', 'key_strengths', 'recommendations'}
sv = r['veto_gates']['skill_veto']
assert set(sv) == {'gate', 'stability', 'contract', 'determinism', 'security'}
rv = r['veto_gates']['research_veto']
assert set(rv) == {'applicable', 'gate', 'scientific_integrity', 'practice_boundaries', 'methodological_ground', 'code_usability'}
cats = r['static_score']['categories']
assert set(cats) == {'functional_suitability', 'reliability', 'performance_context', 'agent_usability', 'human_usability', 'security', 'maintainability', 'agent_specific'}
assert all(0 <= v['score'] <= v['max'] and v['note'] for v in cats.values())
assert r['static_score']['subtotal'] == sum(v['score'] for v in cats.values())
d = r['dynamic_score']
assert len(d['inputs']) == r['meta']['n_inputs'] == 8
for i in d['inputs']:
    assert 3 <= len(i['assertions']) <= 5
    assert i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions']) and i['assertions_total'] == len(i['assertions'])
    assert i['basic'] + i['specialized'] == i['total']
    assert i['executed'] is True and i['execution_note']
    assert all(set(a) == {'text', 'result', 'note'} for a in i['assertions'])
assert d['execution_avg'] == round(sum(i['total'] for i in d['inputs']) / len(d['inputs']), 1)
assert d['assertion_pass_rate'] == {'passed': sum(i['assertions_passed'] for i in d['inputs']), 'total': sum(i['assertions_total'] for i in d['inputs'])}
f = r['final']
assert f['static_weighted'] == round(r['static_score']['subtotal'] * 0.4, 1) and f['dynamic_weighted'] == round(d['execution_avg'] * 0.6, 1)
assert f['score'] == round(f['static_weighted'] + f['dynamic_weighted'])
assert (f['grade'], f['grade_symbol']) == ('Production Ready', '⭐') and f['deployable'] is True and f['veto_override'] is False
assert 2 <= len(r['key_strengths']) <= 5
pr = [x['priority'] for x in r['recommendations']]
assert pr == sorted(pr)
assert r['meta']['source'].endswith('35712f5f1c1177aec6e6f1fab165b8c49a832aab:alignment-files/sam-bam-basics') and r['meta']['evaluated_on'] == '2026-09-20'
print('report OK: score', f['score'], f['grade'], 'inputs', len(d['inputs']), 'recs', pr)
