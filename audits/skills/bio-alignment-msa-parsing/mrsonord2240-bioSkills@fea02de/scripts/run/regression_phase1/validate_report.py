"""Pre-emit checklist of skill-auditor/references/report_json_schema.md, applied to the emitted JSON."""
import json, os
p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eval_report_bio-alignment-msa-parsing_result.json')
j = json.load(open(p, encoding='utf-8'))
ok = lambda name, c: print(('OK   ' if c else 'FAIL ') + name) or c
r = []
r.append(ok('7 top-level nodes', set(j) == {'meta', 'veto_gates', 'static_score', 'dynamic_score', 'final', 'key_strengths', 'recommendations'}))
r.append(ok('skill_veto keys', set(j['veto_gates']['skill_veto']) == {'gate', 'stability', 'contract', 'determinism', 'security'}))
r.append(ok('research_veto keys', set(j['veto_gates']['research_veto']) == {'applicable', 'gate', 'scientific_integrity', 'practice_boundaries', 'methodological_ground', 'code_usability'}))
cats = j['static_score']['categories']
r.append(ok('8 static categories, {score,max,note}', set(cats) == {'functional_suitability', 'reliability', 'performance_context', 'agent_usability', 'human_usability', 'security', 'maintainability', 'agent_specific'} and all(set(v) == {'score', 'max', 'note'} and 0 <= v['score'] <= v['max'] for v in cats.values())))
r.append(ok('static subtotal == sum', j['static_score']['subtotal'] == sum(v['score'] for v in cats.values())))
ins = j['dynamic_score']['inputs']
r.append(ok('inputs == n_inputs', len(ins) == j['meta']['n_inputs']))
r.append(ok('3-5 assertions each; passed count; basic+specialized', all(3 <= len(i['assertions']) <= 5 and i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions']) and i['assertions_total'] == len(i['assertions']) and i['basic'] + i['specialized'] == i['total'] and all(set(a) == {'text', 'result', 'note'} for a in i['assertions']) for i in ins)))
r.append(ok('executed + execution_note on every input', all(i['executed'] is True and i['execution_note'] for i in ins)))
r.append(ok('execution_avg', abs(j['dynamic_score']['execution_avg'] - round(sum(i['total'] for i in ins) / len(ins), 1)) < 1e-9))
r.append(ok('assertion_pass_rate', j['dynamic_score']['assertion_pass_rate'] == {'passed': sum(i['assertions_passed'] for i in ins), 'total': sum(i['assertions_total'] for i in ins)}))
f = j['final']
r.append(ok('final arithmetic', f['static_weighted'] == round(j['static_score']['subtotal'] * 0.4, 1) and f['dynamic_weighted'] == round(j['dynamic_score']['execution_avg'] * 0.6, 1) and f['score'] == round(f['static_weighted'] + f['dynamic_weighted'])))
r.append(ok('grade vs score, veto_override', f['grade'] == 'Production Ready' and f['grade_symbol'] == '⭐' and f['score'] >= 85 and f['veto_override'] is False and f['deployable'] is True))
r.append(ok('key_strengths 2-5', 2 <= len(j['key_strengths']) <= 5))
pr = [x['priority'] for x in j['recommendations']]
r.append(ok('recommendations sorted, fields', pr == sorted(pr) and all(set(x) == {'priority', 'title', 'observed_in', 'problem', 'root_cause', 'fix'} for x in j['recommendations'])))
r.append(ok('meta.evaluated_on and source', j['meta']['evaluated_on'] == '2026-09-20' and j['meta']['source'] == 'mrsonord2240/bioSkills@53861ae5dcb3ba770ab1dc6d8cf1582925b49004:alignment/msa-parsing'))
print('ALL OK' if all(r) else 'PROBLEMS')
