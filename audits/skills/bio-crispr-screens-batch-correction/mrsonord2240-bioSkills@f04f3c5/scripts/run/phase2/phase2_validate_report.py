"""Audit-artifact consistency checks for the Phase-2 JSON report."""
from pathlib import Path
import json

report = Path(__file__).resolve().parents[2] / 'eval_report_bio-crispr-screens-batch-correction_result.json'
d = json.loads(report.read_text(encoding='utf-8'))
assert d['source'] == 'mrsonord2240/bioSkills@f04f3c5168224974c7879822c33f364c5e4fd034:crispr-screens/batch-correction'
assert d['meta']['source'] == 'mrsonord2240/bioSkills@f04f3c5168224974c7879822c33f364c5e4fd034:crispr-screens/batch-correction'
assert d['meta']['auditor_independent'] is False
assert d['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = d['dynamic_score']['inputs']
assert len(inputs) == d['meta']['n_inputs'] == 9
for row in inputs:
    assert isinstance(row['executed'], bool) and row['execution_note']
    assert row['basic'] + row['specialized'] == row['total']
    assert row['assertions_passed'] == sum(a['result'] == 'PASS' for a in row['assertions'])
    assert row['assertions_total'] == len(row['assertions'])
assert round(sum(r['total'] for r in inputs) / len(inputs), 1) == d['dynamic_score']['execution_avg']
assert sum(d['static_score']['categories'][k]['score'] for k in d['static_score']['categories']) == d['static_score']['subtotal']
assert d['final']['deployable'] and not d['final']['veto_override']
print('ASSERT report: exact source tip, required final-pass meta, 9 explicit execution records, totals and weights are internally consistent')
print('PHASE2_REPORT_VALIDATE_PASS')
