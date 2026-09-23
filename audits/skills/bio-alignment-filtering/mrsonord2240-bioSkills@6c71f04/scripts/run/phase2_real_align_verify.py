#!/usr/bin/env python3
"""Phase-2 real Illumina re-alignment check for the table's selected thresholds."""
import pathlib
import subprocess

ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run/p2_real_dna')
rules = {'bwa': (1, 30), 'bowtie2': (2, 23), 'hisat2': (2, 60), 'minimap2': (1, 30), 'star': (255, 255)}
fails = []; checks = 0
def count(name, q):
    p = subprocess.run(['samtools', 'view', '-c', '-F', '2308', '-q', str(q), str(ROOT / f'{name}.bam')], text=True, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return int(p.stdout)
def check(name, ok, detail=''):
    global checks
    checks += 1; print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok: fails.append(name)
for tool, (drop, high) in rules.items():
    total = count(tool, 0); at_drop = count(tool, drop); at_high = count(tool, high)
    check(f'{tool}: drop-ambiguous threshold preserves >=97% mapped real reads', at_drop / total >= .97, f'{at_drop}/{total}')
    check(f'{tool}: high-confidence threshold is non-empty and no less selective than drop threshold', 0 < at_high <= at_drop, f'{at_high}/{at_drop}')
check('minimap2 short-read Q60 is demonstrably stricter than documented Q30', count('minimap2', 60) < count('minimap2', 30), f'{count("minimap2", 60)}/{count("minimap2", 30)}')
print(f'ASSERTIONS {checks-len(fails)}/{checks}')
if fails: raise SystemExit(1)
