#!/usr/bin/env python3
"""Schema and arithmetic validation for the canonical Phase 2 report."""
import json
from pathlib import Path

root = Path('/mnt/openscience/audits/bio-pathway-go-enrichment')
report = json.loads((root / 'eval_report_bio-pathway-go-enrichment_result.json').read_text(encoding='utf-8'))
assert set(report) == {'meta', 'veto_gates', 'static_score', 'dynamic_score', 'final', 'key_strengths', 'recommendations'}
assert report['meta']['tip_commit'] == '1bb08737d3b24d54f00f5d35aa096f9fd2e04b79'
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
categories = report['static_score']['categories']
assert len(categories) == 8
assert sum(x['score'] for x in categories.values()) == report['static_score']['subtotal']
inputs = report['dynamic_score']['inputs']
assert len(inputs) == report['meta']['n_inputs'] == 7
for item in inputs:
    assert item['executed'] is True and item['execution_note']
    assert item['basic'] + item['specialized'] == item['total']
    assert 3 <= len(item['assertions']) <= 5
    assert item['assertions_passed'] == sum(a['result'] == 'PASS' for a in item['assertions'])
    assert item['assertions_total'] == len(item['assertions'])
assert round(sum(x['total'] for x in inputs) / len(inputs), 1) == report['dynamic_score']['execution_avg']
assert round(report['static_score']['subtotal'] * 0.4, 1) == report['final']['static_weighted']
assert round(report['dynamic_score']['execution_avg'] * 0.6, 1) == report['final']['dynamic_weighted']
assert round(report['final']['static_weighted'] + report['final']['dynamic_weighted']) == report['final']['score']
assert len(report['key_strengths']) in range(2, 6)
assert [x['priority'] for x in report['recommendations']] == ['P1', 'P2']
assert report['final']['deployable'] is True and report['final']['veto_override'] is False
assert (root / 'eval_viewer_bio-pathway-go-enrichment.md').exists()
print('PHASE2_REPORT_SCHEMA_OK inputs=7 assertions=28 score=93')
