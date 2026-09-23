#!/usr/bin/env python3
"""Phase-2 new input: invalid-region and documented zero-width BED boundaries."""
import os
import pathlib
import subprocess

import pysam

ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run/p2_boundaries')
SK = pathlib.Path('/mnt/openscience/wt/alignment-files-alignment-filtering/alignment-files/alignment-filtering')
DATA = pathlib.Path(os.environ['AFDATA'])
ROOT.mkdir(exist_ok=True)
human = DATA / 'human/test.paired_end.sorted.bam'

def go(args):
    return subprocess.run(args, text=True, capture_output=True)

def count(path):
    return sum(1 for _ in pysam.AlignmentFile(path))

checks = 0
fails = []
def check(name, ok, detail=''):
    global checks
    checks += 1
    print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok: fails.append(name)

bad_out = ROOT / 'bad-region.bam'
p = go(['python', str(SK / 'examples/filter_bam.py'), str(human), str(bad_out), '-r', 'chr22:bad'])
check('invalid region exits cleanly with a useful message and creates no BAM',
      p.returncode != 0 and 'error: region' in p.stderr and not bad_out.exists(), p.stderr.strip()[:160])

bed = ROOT / 'zero-width.bed'
bed.write_text('chr22\t2000\t2000\n', encoding='utf-8')
p = go(['python', str(SK / 'scripts/filter_by_bed.py'), str(human), str(bed), str(ROOT / 'zero-width.bam')])
sam = go(['samtools', 'view', '-c', '-L', str(bed), str(human)])
script_n = count(ROOT / 'zero-width.bam') if (ROOT / 'zero-width.bam').exists() else -1
check('zero-width BED divergence is explicitly disclosed rather than falsely promised equivalent',
      p.returncode == 0 and sam.returncode == 0 and int(sam.stdout) > script_n and 'zero-width row' in (SK / 'references/pysam.md').read_text(encoding='utf-8'),
      f'script={script_n}, samtools={sam.stdout.strip()}')

print(f'ASSERTIONS {checks-len(fails)}/{checks}')
if fails: raise SystemExit(1)
