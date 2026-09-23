#!/usr/bin/env python3
"""Fresh Phase-2 error-boundary run for the shipped qc_report.py."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path('/mnt/openscience/audits/bio-bam-statistics/run')
DATA = Path('/mnt/openscience/audit-envs/alignment-files/public-data')
SCRIPT = ROOT / 'skill/examples/qc_report.py'


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(['python', str(SCRIPT), *args], text=True, capture_output=True, check=False)


cases = [
    ('real_bam', run(str(DATA / 'human/test.paired_end.sorted.bam')), 0, 'primary 5,642'),
    ('ubam_no_sq', run(str(ROOT / 'data/edge/ubam_no_sq.bam')), 0, 'primary 30'),
    ('all_qcfail', run(str(ROOT / 'data/edge/all_qcfail.bam')), 0, 'nothing to report'),
    ('missing', run(str(ROOT / 'data/new/absent.bam')), 1, 'cannot read'),
    ('cram_no_reference', run(str(DATA / 'human/test.paired_end.sorted.cram')), 1, 'CRAM cannot be decoded without its reference'),
    ('cram_with_reference', run(str(DATA / 'human/test.paired_end.sorted.cram'), str(DATA / 'human/genome.fasta')), 0, 'primary 5,642'),
]

for name, result, expected_rc, expected_text in cases:
    combined = result.stdout + result.stderr
    assert result.returncode == expected_rc, f'{name}: rc {result.returncode}, expected {expected_rc}: {combined[-300:]}'
    assert expected_text in combined, f'{name}: missing {expected_text!r}: {combined[-300:]}'
    assert 'Traceback' not in combined, f'{name}: traceback: {combined[-300:]}'
    print(f'ASSERT {name} rc={expected_rc} expected_message_or_count PASS')

real = cases[0][1].stdout
assert re.search(r'QC-passed primary:\s+5,642', real), real
assert re.search(r'Mapped:\s+5,640', real), real
print('ASSERT real_bam_primary_and_mapped_counts_match_flagstat PASS')
