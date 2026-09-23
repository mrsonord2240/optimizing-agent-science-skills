"""Validate the required arithmetic and per-input contract of the final report."""
import json
from pathlib import Path

path = Path(__file__).parents[1] / 'eval_report_bio-single-cell-cnv-inference_result.json'
report = json.loads(path.read_text(encoding='utf-8'))
assert report['static_score']['subtotal'] == sum(x['score'] for x in report['static_score']['categories'].values())
assert len(report['dynamic_score']['inputs']) == report['meta']['n_inputs'] == 10
assert all(x['executed'] is True and len(x['assertions']) == 4 and x['basic'] + x['specialized'] == x['total'] for x in report['dynamic_score']['inputs'])
assert report['dynamic_score']['assertion_pass_rate'] == {'passed': 40, 'total': 40}
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
print('final report contract: PASS')
