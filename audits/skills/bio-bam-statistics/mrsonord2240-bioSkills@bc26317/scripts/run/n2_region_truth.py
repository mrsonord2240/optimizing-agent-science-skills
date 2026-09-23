#!/usr/bin/env python3
"""NEW: region_depth_stats() (SKILL.md block 029 verbatim) on own_ctg.bam/.cram vs the truth arrays built by construction (n1_make_new_data.py)
and vs `samtools depth -a -r`. Includes the read-less contig ctgB, the 100 bp ctgC, the supplementary window and the CRAM (reference= argument)."""
import os, subprocess, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(HERE, 'data', 'new')
src = open(os.path.join(HERE, 'blocks', '029_python.py'), encoding='utf-8').read().split('\nstats = region_depth_stats')[0]
ns = {}; exec(compile(src, 'block029', 'exec'), ns); f = ns['region_depth_stats']
cases = [('ctgA', 0, 20000), ('ctgA', 0, 10000), ('ctgA', 9950, 10050), ('ctgA', 3000, 3050), ('ctgA', 2990, 3060), ('ctgA', 14900, 15600),
         ('ctgB', 0, 5000), ('ctgB', 2000, 2001), ('ctgC', 0, 100), ('ctgC', 99, 100), ('ctgA', 19990, 20000)]
bad = 0
for label, path, kw in [('BAM', f'{N}/own_ctg.bam', {}), ('CRAM+ref', f'{N}/own_ctg.cram', {'reference': f'{N}/own_ctg.fa'})]:
    for c, s, e in cases:
        t = np.load(f'{N}/own_ctg.truth.{c}.npy')[s:e]
        st = f(path, c, s, e, **kw)
        truth = {'length': e - s, 'covered': int((t > 0).sum()), 'mean_depth': float(t.sum()) / (e - s), 'max_depth': int(t.max()),
                 'pct_ge_10x': float((t >= 10).sum()) / (e - s) * 100, 'pct_ge_20x': float((t >= 20).sum()) / (e - s) * 100}
        miss = [k for k in truth if abs(st[k] - truth[k]) > 1e-9]
        r = subprocess.run(['samtools', 'depth', '-a', '-r', f'{c}:{s+1}-{e}'] + (['--reference', kw['reference']] if kw else []) + [path], capture_output=True, text=True)
        v = [int(l.split('\t')[2]) for l in r.stdout.split('\n') if l]
        sd = len(v) == e - s and abs(sum(v) / (e - s) - truth['mean_depth']) < 1e-9
        bad += len(miss) + (not sd)
        print(f'{label:8s} {c}[{s},{e}) mean {st["mean_depth"]:.4f} truth {truth["mean_depth"]:.4f} max {st["max_depth"]}/{truth["max_depth"]} covered {st["covered"]}/{truth["covered"]} samtools_depth_eq_truth={sd} mismatches={miss}')
print('REGION_MISMATCHES', bad)
