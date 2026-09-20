#!/usr/bin/env python3
"""region_depth_stats() from SKILL.md block 030 (verbatim) vs the by-construction truth arrays of make_depth.py and vs `samtools depth -a -r`."""
import os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'blocks', '030_python.py'), encoding='utf-8').read().split('\nstats = region_depth_stats')[0]
ns = {}
exec(compile(src, 'block030', 'exec'), ns)
f = ns['region_depth_stats']
B = os.path.join(HERE, 'data', 'planted_depth.bam')
cases = [('chrA', 0, 10000), ('chrA', 1000, 2000), ('chrA', 500, 1500), ('chrA', 3000, 3100), ('chrA', 7000, 7150), ('chrA', 5000, 5100),
         ('chrB', 0, 5000), ('chrB', 4900, 5000), ('chrB', 4800, 5000), ('chrC', 0, 3000), ('chrD', 500, 610), ('chrD', 1000, 1600), ('chrD', 0, 4000)]
bad_total = 0
for c, s, e in cases:
    t = np.load(os.path.join(HERE, 'data', f'planted_depth.truth.{c}.npy'))[s:e]
    st = f(B, c, s, e)
    truth = {'length': e - s, 'covered': int((t > 0).sum()), 'mean_depth': float(t.sum()) / (e - s), 'max_depth': int(t.max()),
             'pct_ge_10x': float((t >= 10).sum()) / (e - s) * 100, 'pct_ge_20x': float((t >= 20).sum()) / (e - s) * 100}
    bad = [k for k in truth if abs(st[k] - truth[k]) > 1e-9]
    out = subprocess.run(['samtools', 'depth', '-a', '-r', f'{c}:{s+1}-{e}', B], capture_output=True, text=True).stdout.split('\n')
    d = [int(l.split('\t')[2]) for l in out if l]
    sd_ok = len(d) == e - s and abs(sum(d) / (e - s) - truth['mean_depth']) < 1e-9
    bad_total += len(bad) + (not sd_ok)
    print(f'{c}[{s},{e}) skill mean={st["mean_depth"]:.4f} truth={truth["mean_depth"]:.4f} covered {st["covered"]}/{truth["covered"]} max {st["max_depth"]}/{truth["max_depth"]} '
          f'ge10 {st["pct_ge_10x"]:.2f}/{truth["pct_ge_10x"]:.2f} samtools_depth_matches_truth={sd_ok} mismatches={bad}')
print('REGION_TRUTH_MISMATCHES', bad_total)
