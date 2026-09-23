#!/usr/bin/env python3
"""Phase-2 new input: tumor-normal --like downsampling with a larger normal target."""
import os
import pathlib
import subprocess

import pysam

ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run/p2_match_like')
SK = pathlib.Path('/mnt/openscience/wt/alignment-files-alignment-filtering/alignment-files/alignment-filtering')
DATA = pathlib.Path(os.environ['AFDATA'])
ROOT.mkdir(exist_ok=True)
tumor = DATA / 'human/test.paired_end.sorted.bam'
normal = DATA / '1000g/HG00349.chr20_1400000-1500000.bam'
out = ROOT / 'tumor_matched.bam'
p = subprocess.run(['bash', str(SK / 'scripts/match_read_count.sh'), str(tumor), str(out), '--like', str(normal)], text=True, capture_output=True)
def rows(path): return [r.to_string() for r in pysam.AlignmentFile(path)]
same = out.exists() and rows(out) == rows(tumor)
print('rc', p.returncode)
print('stderr', p.stderr.strip())
print('records', len(rows(tumor)), len(rows(out)) if out.exists() else -1)
print('PASS --like does not upsample and preserves the input bytewise-at-record-level' if p.returncode == 0 and same and 'copying unchanged' in p.stderr else 'FAIL --like guard')
if not (p.returncode == 0 and same and 'copying unchanged' in p.stderr): raise SystemExit(1)
