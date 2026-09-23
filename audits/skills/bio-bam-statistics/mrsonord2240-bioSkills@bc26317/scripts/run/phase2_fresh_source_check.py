#!/usr/bin/env python3
"""Fresh Phase-2 structural check of the exact staged source copied into run/skill."""
from __future__ import annotations

import ast
import hashlib
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path('/mnt/openscience/audits/bio-bam-statistics/run')
SOURCE = ROOT / 'skill'
STAGED = Path('/mnt/openscience/wt/alignment-files-bam-statistics/alignment-files/bam-statistics')
DOCS = [SOURCE / 'SKILL.md', SOURCE / 'usage-guide.md', *sorted((SOURCE / 'references').glob('*.md'))]

assert (SOURCE / 'examples/qc_report.py').is_file(), 'missing shipped qc_report.py'
assert len(DOCS) == 5, f'expected 5 documentation files, found {len(DOCS)}'
assert (SOURCE / 'SKILL.md').read_bytes() == (STAGED / 'SKILL.md').read_bytes(), 'copied source differs from staged source'
assert hashlib.sha1((STAGED / 'SKILL.md').read_bytes()).hexdigest(), 'empty source hash'

fences = 0
runnable_fences = 0
for doc in DOCS:
    text = doc.read_text(encoding='utf-8')
    fences += len(re.findall(r'^```[^\n]*\n.*?^```', text, flags=re.M | re.S))
    for lang, body in re.findall(r'^```(bash|python)\n(.*?)^```', text, flags=re.M | re.S):
        runnable_fences += 1
        if lang == 'python':
            ast.parse(body, filename=str(doc))
        else:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', encoding='utf-8') as handle:
                handle.write(body)
                handle.flush()
                subprocess.run(['bash', '-n', handle.name], check=True)
assert fences == 31, f'expected 31 fenced blocks, found {fences}'
assert runnable_fences == 28, f'expected 28 runnable fences, found {runnable_fences}'
ast.parse((SOURCE / 'examples/qc_report.py').read_text(encoding='utf-8'), filename='qc_report.py')

for required in ('references/depth-coverage.md', 'references/pysam.md', 'references/qc-pitfalls.md'):
    assert (SOURCE / required).is_file(), f'missing linked reference {required}'

print('ASSERT source_copy_matches_exact_staged_SKILL_md PASS')
print(f'ASSERT all_fenced_blocks_present count={fences}; runnable_fences_parse_or_bash_n count={runnable_fences} PASS')
print('ASSERT shipped_example_and_linked_references_present PASS')
