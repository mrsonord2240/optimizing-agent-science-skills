#!/usr/bin/env python3
"""Fresh Phase-2 Input 10: test the shipped helper with unordered BED and malformed BED."""
from pathlib import Path
import subprocess
import sys

ROOT = Path('/mnt/openscience/audits/bio-sam-bam-basics/run')
BAM = Path('/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam')
SKILL_SCRIPTS = ROOT / 'skill' / 'scripts'
sys.path.insert(0, str(SKILL_SCRIPTS))
from fetch_regions import fetch_regions, read_bed  # noqa: E402
import pysam  # noqa: E402

case = ROOT / 'data' / 'fresh10'
case.mkdir(parents=True, exist_ok=True)
bed = case / 'unordered_overlap.bed'
bed.write_text('# comments are accepted\nchr22\t2499\t3500\nchr22\t1999\t3000\n', encoding='utf-8')
regions = read_bed(bed)
with pysam.AlignmentFile(BAM) as bam:
    observed = [r.to_string() for r in fetch_regions(bam, regions)]
assert len(observed) == len(set(observed)) == 5426, (len(observed), len(set(observed)))
expected = subprocess.check_output(['samtools', 'view', '-M', '-L', str(bed), str(BAM)], text=True).splitlines()
assert observed == expected, (len(observed), len(expected))

bad = case / 'bad_columns.bed'
bad.write_text('chr22\t2000\n', encoding='utf-8')
proc = subprocess.run([sys.executable, str(SKILL_SCRIPTS / 'fetch_regions.py'), str(BAM), str(bad)], text=True, capture_output=True)
assert proc.returncode == 1, proc.returncode
assert 'IndexError' in proc.stderr, proc.stderr
print('PASS unordered-overlap records=5426 exact-samtools-match; malformed-BED rc=1 raw-IndexError (source behavior)')
