import json
from pathlib import Path
p = Path(r'F:\OpenScience\audits\bio-microbiome-amplicon-processing\eval_report_bio-microbiome-amplicon-processing_result.json')
d = json.loads(p.read_text(encoding='utf-8'))
assert d['meta']['source'] == 'mrsonord2240/bioSkills@0e9a568381ac039886853ff13f167acce8e92229:microbiome/amplicon-processing'
assert d['meta']['auditor_independent'] is False
assert d['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = d['dynamic_score']['inputs']
assert len(inputs) == d['meta']['n_inputs'] == 11
for x in inputs:
    assert isinstance(x['executed'], bool) and x['execution_note']
    assert 3 <= len(x['assertions']) <= 5
    assert x['assertions_passed'] == sum(a['result'] == 'PASS' for a in x['assertions'])
    assert x['assertions_total'] == len(x['assertions'])
    assert x['basic'] + x['specialized'] == x['total']
assert d['static_score']['subtotal'] == sum(x['score'] for x in d['static_score']['categories'].values())
avg = round(sum(x['total'] for x in inputs) / len(inputs), 1)
assert avg == d['dynamic_score']['execution_avg']
assert d['dynamic_score']['assertion_pass_rate'] == {'passed': 35, 'total': 37}
assert d['final']['score'] == round(d['final']['static_weighted'] + d['final']['dynamic_weighted']) == 94
assert d['final']['deployable'] and not d['final']['veto_override']
print(f"REPORT_SCHEMA_PASS inputs={len(inputs)} dynamic={avg} final={d['final']['score']}")
