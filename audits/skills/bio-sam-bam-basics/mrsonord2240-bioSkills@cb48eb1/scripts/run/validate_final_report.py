#!/usr/bin/env python3
"""Schema-level assertions for the Phase-2 final report."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
report = json.loads((root / 'eval_report_bio-sam-bam-basics_result.json').read_text(encoding='utf-8'))
assert report['meta']['source'] == 'mrsonord2240/bioSkills@cb48eb16bf63f75098c865da4e8f7bf3191af733:alignment-files/sam-bam-basics'
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert len(report['dynamic_score']['inputs']) == report['meta']['n_inputs'] == 10
assert all(item.get('executed') is True for item in report['dynamic_score']['inputs'])
assert all('execution_note' in item for item in report['dynamic_score']['inputs'])
assert all(3 <= len(item['assertions']) <= 5 for item in report['dynamic_score']['inputs'])
assert all(item['basic'] + item['specialized'] == item['total'] for item in report['dynamic_score']['inputs'])
assert report['final']['score'] == 91 and report['final']['grade'] == 'Production Ready'
assert report['final']['deployable'] is True and report['final']['veto_override'] is False
print('PASS report source/meta/input/assertion/score contract')
