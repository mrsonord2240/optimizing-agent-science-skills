# Purpose: Validate the final-pass report's schema-critical totals and explicit execution fields.
# Usage: python 10_validate_report.py
import json
from pathlib import Path

p = Path(r'F:\OpenScience\audits\bio-single-cell-scatac-analysis\eval_report_bio-single-cell-scatac-analysis_result.json')
r = json.loads(p.read_text(encoding='utf-8'))
assert set(r) == {'meta', 'veto_gates', 'static_score', 'dynamic_score', 'final', 'key_strengths', 'recommendations'}
assert r['meta']['auditor_independent'] is False
assert r['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
categories = r['static_score']['categories']
assert len(categories) == 8
assert r['static_score']['subtotal'] == sum(v['score'] for v in categories.values())
inputs = r['dynamic_score']['inputs']
assert len(inputs) == r['meta']['n_inputs'] == 7
for i in inputs:
    assert 'executed' in i and 'execution_note' in i
    assert 3 <= len(i['assertions']) <= 5
    assert i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions'])
    assert i['assertions_total'] == len(i['assertions'])
    assert i['total'] == i['basic'] + i['specialized']
assert r['dynamic_score']['assertion_pass_rate'] == {'passed': 24, 'total': 28}
assert r['final']['veto_override'] is True and r['final']['deployable'] is False
assert r['final']['grade'] == 'Reject' and r['final']['grade_symbol'] == '❌'
assert [x['priority'] for x in r['recommendations']] == ['P0', 'P1', 'P2']
print('report_schema_critical_checks=PASS')
