#!/usr/bin/env python3
"""Phase-2 live replay of the PBMM2 row on a deterministic long-read fixture."""
import pathlib
import subprocess

ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run/p2_pbmm2')
fails = []; checks = 0
def rows(path):
    p = subprocess.run(['samtools', 'view', '-F', '2308', str(path)], text=True, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return [x.split('\t') for x in p.stdout.splitlines()]
def check(name, ok, detail=''):
    global checks
    checks += 1; print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok: fails.append(name)
for name in ('pbmm2_hifi', 'pbmm2_ont', 'mm2_hifi', 'mm2_ont'):
    r = rows(ROOT / f'{name}.bam')
    exact = [x for x in r if x[0].startswith('A2_')]
    unique = [x for x in r if x[0].startswith('u_')]
    check(f'{name}: -q 1 drops all exact-repeat reads', all(int(x[4]) < 1 for x in exact), f'{sum(int(x[4]) >= 1 for x in exact)}/{len(exact)}')
    check(f'{name}: -q 60 retains all unique reads', all(int(x[4]) >= 60 for x in unique), f'{sum(int(x[4]) >= 60 for x in unique)}/{len(unique)}')
print(f'ASSERTIONS {checks-len(fails)}/{checks}')
if fails: raise SystemExit(1)
