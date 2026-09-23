"""Validate canonical placement and required fields after artifact normalization."""
import json
from pathlib import Path

root = Path(r'F:\OpenScience\audits\bio-single-cell-cnv-inference')
report_path = root / 'eval_report_bio-single-cell-cnv-inference_result.json'
viewer_path = root / 'eval_viewer_bio-single-cell-cnv-inference.md'
report = json.loads(report_path.read_text(encoding='utf-8'))
assert viewer_path.is_file()
assert report['meta']['source'] == 'mrsonord2240/bioSkills@fa1bbada93ada3e111be9f85eb0aa62be0ffdbac:single-cell/cnv-inference'
assert report['meta']['auditor_independent'] is False
assert report['meta']['note'] == 'final pass: fixed and audited under one brief, see CHECKPOINT.md'
assert len(report['dynamic_score']['inputs']) == 10
assert all(x['executed'] is True and isinstance(x['execution_note'], str) and x['execution_note'] for x in report['dynamic_score']['inputs'])
assert (root / 'run' / '2026-09-23-final-pass' / 'input1_infercnv_fresh.log').is_file()
assert (root / 'run' / '2026-09-23-final-pass' / 'input9_copykat_selector_fresh.log').is_file()
print('canonical report placement and metadata: PASS')
