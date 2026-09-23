"""Validate the required Phase 2 report invariants before handoff."""
from __future__ import annotations
import json
from pathlib import Path

report_path = Path(__file__).resolve().parents[2] / 'eval_report_bio-crispr-screens-prime-editing-screens_result.json'
r = json.loads(report_path.read_text(encoding='utf-8'))
assert r['meta']['source_ref'] == 'mrsonord2240/bioSkills@0abbf4d40d0df260ca60b346a9d6dc307b80fa5d:crispr-screens/prime-editing-screens'
assert r['meta']['auditor_independent'] is False
assert r['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert len(r['dynamic_score']['inputs']) == r['meta']['n_inputs'] == 9
assert all(i['executed'] is True and i['execution_note'] for i in r['dynamic_score']['inputs'])
assert r['dynamic_score']['assertion_pass_rate'] == {'passed': 28, 'total': 28}
assert r['final']['score'] == 95 and r['final']['deployable'] is True and r['final']['veto_override'] is False
assert r['veto_gates']['skill_veto']['gate'] == 'PASS' and r['veto_gates']['research_veto']['gate'] == 'PASS'
assert all(a['result'] == 'PASS' for i in r['dynamic_score']['inputs'] for a in i['assertions'])
print('PASS: report schema invariants, explicit execution fields, source ref, final-pass exception, and score verified')
