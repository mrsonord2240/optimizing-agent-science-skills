"""Validate canonical-report invariants required by the Phase 2 brief."""
import json
from pathlib import Path

report = json.loads(Path('../eval_report_bio-single-cell-multimodal-integration_result.json').read_text(encoding='utf-8'))
expected = 'mrsonord2240/bioSkills@71a686293613d3e5e11c5e5b34aa792e923f552d:single-cell/multimodal-integration'
assert report['source'] == expected
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
inputs = report['dynamic_score']['inputs']
assert len(inputs) == report['meta']['n_inputs']
assert all(row['executed'] is True and row['execution_note'] for row in inputs)
assert all(3 <= len(row['assertions']) <= 5 for row in inputs)
assert report['final']['veto_override'] is True and report['final']['deployable'] is False
print('REPORT_VALID', len(inputs), report['final']['grade'], report['final']['score'])
