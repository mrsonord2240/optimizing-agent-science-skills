#!/usr/bin/env python3
"""Validate final-pass report arithmetic and mandatory audit metadata."""
import json
from pathlib import Path

p = Path('/mnt/openscience/audits/bio-alignment-filtering/eval_report_bio-alignment-filtering_result.json')
r = json.loads(p.read_text(encoding='utf-8'))
assert r['meta']['source'] == 'mrsonord2240/bioSkills@6c71f04151377fe0d412ece85d9dc52cdccdf747:alignment-files/alignment-filtering'
assert r['meta']['auditor_independent'] is False
assert r['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert sum(x['score'] for x in r['static_score']['categories'].values()) == r['static_score']['subtotal'] == 95
inputs = r['dynamic_score']['inputs']
assert len(inputs) == r['meta']['n_inputs'] == 11
for x in inputs:
    assert x['executed'] is True and x['basic'] + x['specialized'] == x['total']
    assert 3 <= len(x['assertions']) <= 5
    print(x['index'], x['assertions_passed'], x['assertions_total'], len(x['assertions']), sum(a['result'] == 'PASS' for a in x['assertions']))
    assert x['assertions_passed'] == sum(a['result'] == 'PASS' for a in x['assertions']) == x['assertions_total']
avg = round(sum(x['total'] for x in inputs) / len(inputs), 1)
assert avg == r['dynamic_score']['execution_avg'] == 96.4
assert r['final']['static_weighted'] == round(95 * .4, 1)
assert r['final']['dynamic_weighted'] == round(96.4 * .6, 1)
assert r['final']['score'] == 96 and r['final']['grade'] == 'Production Ready' and r['final']['deployable'] is True
assert r['dynamic_score']['assertion_pass_rate'] == {'passed': 49, 'total': 49}
print('PASS report JSON schema-relevant fields, arithmetic, per-input assertions, source, and final-pass metadata')
