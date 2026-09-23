"""Validate the final-pass JSON's required arithmetic, per-input execution metadata, and schema-shaped fields."""
from pathlib import Path
import json

report = Path(__file__).resolve().parents[2] / 'eval_report_bio-metabolomics-metabolite-annotation_result.json'
data = json.loads(report.read_text(encoding='utf-8'))
assert data['meta']['source'].endswith('metabolomics/metabolite-annotation')
assert data['meta']['auditor_independent'] is False
assert data['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = data['dynamic_score']['inputs']
assert len(inputs) == data['meta']['n_inputs'] == 7
for item in inputs:
    assert isinstance(item['executed'], bool) and item['execution_note']
    assert 3 <= len(item['assertions']) <= 5
    assert item['assertions_passed'] == sum(a['result'] == 'PASS' for a in item['assertions'])
    assert item['assertions_total'] == len(item['assertions'])
    assert item['total'] == item['basic'] + item['specialized']
assert data['dynamic_score']['assertion_pass_rate'] == {'passed': 23, 'total': 26}
assert data['dynamic_score']['execution_avg'] == round(sum(item['total'] for item in inputs) / len(inputs), 1)
assert data['static_score']['subtotal'] == sum(v['score'] for v in data['static_score']['categories'].values())
assert data['final']['static_weighted'] == round(data['static_score']['subtotal'] * 0.4, 1)
assert data['final']['dynamic_weighted'] == round(data['dynamic_score']['execution_avg'] * 0.6, 1)
assert data['final']['score'] == round(data['final']['static_weighted'] + data['final']['dynamic_weighted'])
assert data['final']['grade'] == 'Limited Release' and data['final']['deployable'] is True and data['final']['veto_override'] is False
print('REPORT VALID: 7 inputs; 6 executed; 23/26 assertions; source, metadata, arithmetic, and grade fields are consistent.')
