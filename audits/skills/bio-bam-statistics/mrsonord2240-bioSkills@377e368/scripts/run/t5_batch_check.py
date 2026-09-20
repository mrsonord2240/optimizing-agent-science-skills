#!/usr/bin/env python3
"""Compare the Skill's block-006 summary.tsv rows with hand counts from record flags (truth.py; no samtools)."""
import sys
sys.path.insert(0, '/mnt/openscience/audits/bio-bam-statistics/run')
from truth import counts
fails = 0
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1])]
print(rows[0])
for r in rows[1:]:
    s = r[0]; T = counts(f'{s}.bam')
    exp = [s, T['total'], T['qcfail'], T['primary'], T['primary_mapped'], T['proper_primary'], T['primary_duplicates']]
    ok = [str(x) for x in exp] == r
    fails += (not ok)
    print('PASS' if ok else 'FAIL', r, '' if ok else f'expected {exp}')
print('BATCH_FAILS', fails)
