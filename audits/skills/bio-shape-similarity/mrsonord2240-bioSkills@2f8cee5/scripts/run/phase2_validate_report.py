"""Schema and arithmetic checks for the Phase 2 final-pass report."""
import json
from pathlib import Path

report_path = Path(__file__).parents[1] / 'eval_report_bio-shape-similarity_result.json'
report = json.loads(report_path.read_text(encoding='utf-8'))

assert report['meta']['source'] == (
    'mrsonord2240/bioSkills@2f8cee570c21b48f08e0b15b1662c6d363bbf09b:'
    'chemoinformatics/shape-similarity'
)
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = report['dynamic_score']['inputs']
assert len(inputs) == report['meta']['n_inputs'] == 7
assert all('executed' in row and 'execution_note' in row for row in inputs)
assert all(3 <= len(row['assertions']) <= 5 for row in inputs)
assert all(row['basic'] + row['specialized'] == row['total'] for row in inputs)
assert all(row['assertions_passed'] == sum(a['result'] == 'PASS' for a in row['assertions']) for row in inputs)
assert report['dynamic_score']['assertion_pass_rate']['passed'] == sum(row['assertions_passed'] for row in inputs)
assert report['dynamic_score']['assertion_pass_rate']['total'] == sum(row['assertions_total'] for row in inputs)
assert report['dynamic_score']['execution_avg'] == round(sum(row['total'] for row in inputs) / len(inputs), 1)
assert report['static_score']['subtotal'] == sum(v['score'] for v in report['static_score']['categories'].values())
assert report['final']['static_weighted'] == round(report['static_score']['subtotal'] * 0.4, 1)
assert report['final']['dynamic_weighted'] == round(report['dynamic_score']['execution_avg'] * 0.6, 1)
assert report['final']['score'] == round(report['final']['static_weighted'] + report['final']['dynamic_weighted'])
assert all('executed' in row and 'execution_note' in row for row in report['dynamic_score']['supplemental_regressions'])
print('PASS: report schema, arithmetic, source, final-pass metadata, and execution fields validate.')
