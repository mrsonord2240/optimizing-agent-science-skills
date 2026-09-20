#!/usr/bin/env python3
"""Input 1 helper: independent flag counts (truth.py, no samtools) vs `samtools flagstat -O tsv` and vs the Skill's pysam snippet numbers."""
import sys, subprocess, json
sys.path.insert(0, '/mnt/openscience/audits/bio-bam-statistics/run')
import truth
bam = sys.argv[1]
t = truth.counts(bam)
out = subprocess.run(['samtools', 'flagstat', '-O', 'tsv', bam], capture_output=True, text=True).stdout
fs = {}
for l in out.splitlines():
    p = l.split('\t')
    fs[p[2]] = (int(p[0]), int(p[1])) if p[0].isdigit() else p[0]
def tot(k): return fs[k][0] + fs[k][1]
pairs = [('total', tot('total (QC-passed reads + QC-failed reads)') , t['total']), ('primary', tot('primary'), t['primary']),
         ('secondary', tot('secondary'), t['secondary']), ('supplementary', tot('supplementary'), t['supplementary']),
         ('primary mapped', tot('primary mapped'), t['primary_mapped']), ('primary dup', tot('primary duplicates'), t['primary_duplicates']),
         ('properly paired', tot('properly paired'), t['proper_primary']), ('singletons', tot('singletons'), t['singletons'])]
ok = True
for name, a, b in pairs:
    flag = 'OK ' if a == b else 'BAD'; ok &= a == b
    print(f'  {flag} {name:16s} flagstat={a} truth(record flags)={b}')
print('ALL MATCH' if ok else 'MISMATCH', bam.split('/')[-1])
