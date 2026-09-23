#!/usr/bin/env python3
"""Phase-2 live MAPQ verification for the current split minimap2 table."""
import pathlib
import subprocess

ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run/p2_mapq')
rules = {'bwa': (1, 30), 'bowtie2': (2, 23), 'hisat2': (2, 60), 'minimap2': (1, 30), 'star': (255, 255)}
fails = []
checks = 0
def sam(args):
    p = subprocess.run(['samtools', 'view', *args], text=True, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return [x.split('\t') for x in p.stdout.splitlines()]
def check(name, ok, detail=''):
    global checks
    checks += 1; print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok: fails.append(name)
for tool, (drop, high) in rules.items():
    rows = sam(['-F', '2308', str(ROOT / f'{tool}.bam')])
    exact = [r for r in rows if r[0].startswith(('A2_', 'D8_'))]
    for threshold, label in ((drop, 'drop ambiguous'), (high, 'high confidence')):
        kept = [r for r in exact if int(r[4]) >= threshold]
        check(f'{tool} {label} threshold removes exact-repeat reads', not kept, f'{len(kept)}/{len(exact)}')
star_q = {int(r[4]) for r in sam(['-F', '2308', str(ROOT / 'star.bam')])}
check('STAR emits only documented sentinel MAPQs', star_q <= {0, 1, 3, 255}, str(sorted(star_q)))
print(f'ASSERTIONS {checks-len(fails)}/{checks}')
if fails: raise SystemExit(1)
