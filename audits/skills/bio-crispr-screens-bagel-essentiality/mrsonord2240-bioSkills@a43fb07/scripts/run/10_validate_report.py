import json
from pathlib import Path

p = Path('../eval_report_bio-crispr-screens-bagel-essentiality_result.json')
r = json.loads(p.read_text(encoding='utf-8'))
assert r['meta']['source'] == 'mrsonord2240/bioSkills@a43fb0726ecb90a9ca8ea660404cd98ba2989c18:crispr-screens/bagel-essentiality'
assert r['meta']['auditor_independent'] is False
assert r['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert len(r['static_score']['categories']) == 8
assert sum(x['score'] for x in r['static_score']['categories'].values()) == r['static_score']['subtotal']
inputs = r['dynamic_score']['inputs']
assert len(inputs) == r['meta']['n_inputs'] == 7
assert all(i['executed'] for i in inputs)
assert all(3 <= len(i['assertions']) <= 5 for i in inputs)
assert all(i['basic'] + i['specialized'] == i['total'] for i in inputs)
assert sum(i['assertions_passed'] for i in inputs) == r['dynamic_score']['assertion_pass_rate']['passed']
assert sum(i['assertions_total'] for i in inputs) == r['dynamic_score']['assertion_pass_rate']['total']
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
assert avg == r['dynamic_score']['execution_avg']
assert round(r['static_score']['subtotal'] * 0.4, 1) == r['final']['static_weighted']
assert round(avg * 0.6, 1) == r['final']['dynamic_weighted']
assert round(r['final']['static_weighted'] + r['final']['dynamic_weighted']) == r['final']['score']
assert r['final']['deployable'] and not r['final']['veto_override']
assert Path('../eval_viewer_bio-crispr-screens-bagel-essentiality.md').is_file()
print(f"PASS report schema and arithmetic: final={r['final']['score']}, inputs={len(inputs)}, assertions=20/21")
