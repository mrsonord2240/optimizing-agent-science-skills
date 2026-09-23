"""Contract checks for the final Phase 2 JSON report."""
from __future__ import annotations

import json
from pathlib import Path

report = json.loads(Path(r'F:/OpenScience/audits/bio-workflows-proteomics-pipeline/eval_report_bio-workflows-proteomics-pipeline_result.json').read_text(encoding='utf-8'))
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert report['source'].endswith(':workflows/proteomics-pipeline')
assert set(report['static_score']['categories']) == {'functional_suitability','reliability','performance_context','agent_usability','human_usability','security','maintainability','agent_specific'}
assert sum(x['score'] for x in report['static_score']['categories'].values()) == report['static_score']['subtotal'] == 92
inputs = report['dynamic_score']['inputs']
assert len(inputs) == report['meta']['n_inputs'] == 10
assert all('executed' in x and 'execution_note' in x for x in inputs)
assert all(3 <= len(x['assertions']) <= 5 for x in inputs)
assert all(x['basic'] + x['specialized'] == x['total'] for x in inputs)
assert all(x['assertions_passed'] == sum(a['result'] == 'PASS' for a in x['assertions']) for x in inputs)
assert sum(x['assertions_passed'] for x in inputs) == 40
assert round(sum(x['total'] for x in inputs) / len(inputs), 1) == report['dynamic_score']['execution_avg'] == 93.2
assert report['final']['static_weighted'] == 36.8 and report['final']['dynamic_weighted'] == 55.9 and report['final']['score'] == 93
assert report['final']['deployable'] is True and report['final']['veto_override'] is False
assert [x['priority'] for x in report['recommendations']] == ['P1', 'P1']
print('REPORT CONTRACT PASS: 10 inputs, 40 assertions, score 93, deployable true')
