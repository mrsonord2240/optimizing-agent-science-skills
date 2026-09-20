#!/usr/bin/env python3
"""NEW: per-position arrays from bcftools mpileup / samtools mpileup / mosdepth / depth on own_del.bam vs the truth arrays (by construction).
usage: n4_overlap_del.py   (run inside WSL env; writes nothing but stdout)"""
import subprocess, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(HERE, 'data', 'new')
B, F = f'{N}/own_del.bam', f'{N}/own_del.fa'
T = {k: np.load(f'{N}/own_del.truth_{k}.npy') for k in ('default', 'matesonce', 'dn_covered')}
L = 3000
def sh(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True, executable='/bin/bash').stdout
def arr_from(lines, pos_col, val_col):
    a = np.zeros(L, dtype=int)
    for l in lines:
        c = l.split('\t')
        if len(c) > max(pos_col, val_col) and c[val_col] not in ('.', ''): a[int(c[pos_col]) - 1] = int(c[val_col])
    return a
def rep(name, a):
    eq = {k: bool((a == v).all()) for k, v in T.items()}
    print(f'{name:44s} sum {int(a.sum()):5d} mean {a.sum()/L:.4f}  == truth_default {eq["default"]} | matesonce {eq["matesonce"]} | D+N covered {eq["dn_covered"]}')
print('TRUTH sums: default(mates twice, D/N uncovered)', int(T['default'].sum()), '| mates once', int(T['matesonce'].sum()), '| D+N covered', int(T['dn_covered'].sum()))
rep('samtools depth -aa', arr_from(sh(f'samtools depth -aa {B}').splitlines(), 1, 2)[:L] if False else arr_from([l.replace(l.split("\t")[1], str(int(l.split("\t")[1]))) for l in sh(f'samtools depth -aa {B}').splitlines()], 1, 2))
rep('samtools depth -aa -s', arr_from(sh(f'samtools depth -aa -s {B}').splitlines(), 1, 2))
rep('samtools depth -aa -J (include deletions)', arr_from(sh(f'samtools depth -aa -J {B}').splitlines(), 1, 2))
for tag, opt in (('mosdepth default', ''), ('mosdepth --fast-mode', '--fast-mode')):
    sh(f'cd {HERE}/work && mosdepth {opt} -t 1 md_{opt.strip("-") or "def"} {B}')
    rows = subprocess.run(f'zcat {HERE}/work/md_{opt.strip("-") or "def"}.per-base.bed.gz', shell=True, capture_output=True, text=True).stdout.splitlines()
    a = np.zeros(L, dtype=int)
    for l in rows:
        c, s, e, d = l.split('\t'); a[int(s):int(e)] = int(d)
    rep(tag, a)
for tag, opt in (('samtools mpileup default (-Q13)', ''), ('samtools mpileup -x', '-x'), ('samtools mpileup -Q 0', '-Q 0'), ('samtools mpileup -Q 0 -x', '-Q 0 -x'), ('samtools mpileup -B', '-B')):
    rep(tag, arr_from(sh(f'samtools mpileup -d 1000000 {opt} -f {F} {B} 2>/dev/null').splitlines(), 1, 3))
for tag, opt in (('bcftools mpileup default', ''), ('bcftools mpileup -x', '-x'), ('bcftools mpileup -Q 0', '-Q 0'), ('bcftools mpileup -B', '-B'), ('bcftools mpileup -B -x', '-B -x')):
    out = sh(f"bcftools mpileup -d 1000000 {opt} -a FORMAT/DP -f {F} {B} 2>/dev/null | bcftools query -f '%CHROM\t%POS\t%INFO/DP\t[%DP]\n'").splitlines()
    rep(tag + '  FORMAT/DP', arr_from(out, 1, 3)); rep(tag + '  INFO/DP', arr_from(out, 1, 2))
