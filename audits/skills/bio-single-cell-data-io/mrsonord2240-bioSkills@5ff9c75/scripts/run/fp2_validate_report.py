"""Validate required final-pass report fields and score arithmetic."""
import json
from pathlib import Path

p = Path('F:/OpenScience/audits/bio-single-cell-data-io/eval_report_bio-single-cell-data-io_result.json')
d = json.loads(p.read_text(encoding='utf-8'))
assert d['meta']['source'] == 'mrsonord2240/bioSkills@5ff9c75dc947fa7c7292315ae64198769d067faf:single-cell/data-io'
assert d['meta']['auditor_independent'] is False
assert d['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = d['dynamic_score']['inputs']
assert len(inputs) == d['meta']['n_inputs'] == 9
assert all(x['executed'] is True and x['execution_note'] for x in inputs)
assert all(3 <= len(x['assertions']) <= 5 for x in inputs)
assert all(x['basic'] + x['specialized'] == x['total'] for x in inputs)
assert sum(c['score'] for c in d['static_score']['categories'].values()) == d['static_score']['subtotal']
avg = round(sum(x['total'] for x in inputs) / len(inputs), 1)
assert avg == d['dynamic_score']['execution_avg']
assert d['final']['static_weighted'] == round(d['static_score']['subtotal'] * .4, 1)
assert d['final']['dynamic_weighted'] == round(avg * .6, 1)
assert d['final']['score'] == round(d['final']['static_weighted'] + d['final']['dynamic_weighted'])
print('report_valid', 'inputs', len(inputs), 'dynamic_avg', avg, 'final', d['final']['score'])
