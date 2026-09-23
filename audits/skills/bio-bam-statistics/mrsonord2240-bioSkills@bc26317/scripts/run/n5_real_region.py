#!/usr/bin/env python3
"""NEW (real data not used for depth before): region_depth_stats() (block 029 verbatim) on the REAL 1000G chr20 slice (duplicate-flagged reads, mate pairs on other contigs)
and the REAL spliced RNA-seq BAM (N-skips, 1786 secondary), vs (1) truth from alignment blocks (get_blocks, flag filter UNMAP|SECONDARY|QCFAIL|DUP, no pileup engine)
and (2) `samtools depth -a -r`."""
import os, subprocess, numpy as np, pysam
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.environ['AFDATA']
src = open(os.path.join(HERE, 'blocks', '029_python.py'), encoding='utf-8').read().split('\nstats = region_depth_stats')[0]
ns = {}; exec(compile(src, 'block029', 'exec'), ns); f = ns['region_depth_stats']
def truth_region(path, c, s, e):
    d = np.zeros(e - s, dtype=np.int64)
    with pysam.AlignmentFile(path) as b:
        for r in b.fetch(c, s, e):
            if r.flag & (4 | 256 | 512 | 1024): continue
            for bs, be in r.get_blocks():
                lo, hi = max(bs, s), min(be, e)
                if lo < hi: d[lo - s:hi - s] += 1
    return d
bad = 0
for label, path, c, wins in [('1000G chr20', f'{D}/1000g/HG00349.chr20_1400000-1500000.bam', 'chr20', [(1400000, 1500000), (1400000, 1400500), (1450000, 1450001), (1499000, 1500500), (1300000, 1400000)]),
                             ('RNA chr22', os.path.join(HERE, 'work', 'rna5.bam'), 'chr22', [(0, 40001), (0, 5000), (10000, 20000), (39990, 40001)])]:
    for s, e in wins:
        t = truth_region(path, c, s, e); L = e - s
        st = f(path, c, s, e)
        truth = {'length': L, 'covered': int((t > 0).sum()), 'mean_depth': float(t.sum()) / L, 'max_depth': int(t.max()),
                 'pct_ge_10x': float((t >= 10).sum()) / L * 100, 'pct_ge_20x': float((t >= 20).sum()) / L * 100}
        miss = [k for k in truth if abs(st[k] - truth[k]) > 1e-9]
        out = subprocess.run(['samtools', 'depth', '-a', '-r', f'{c}:{s+1}-{e}', path], capture_output=True, text=True).stdout.split('\n')
        v = [int(l.split('\t')[2]) for l in out if l]
        sd = len(v) == L and abs(sum(v) / L - truth['mean_depth']) < 1e-9
        bad += len(miss) + (not sd)
        print(f'{label} [{s},{e}) mean {st["mean_depth"]:.4f} truth {truth["mean_depth"]:.4f} samtools_depth_a {sum(v)/max(len(v),1):.4f} max {st["max_depth"]}/{truth["max_depth"]} covered {st["covered"]}/{truth["covered"]} ge20 {st["pct_ge_20x"]:.3f}/{truth["pct_ge_20x"]:.3f} rows_ok={sd} mismatches={miss}')
print('REAL_REGION_MISMATCHES', bad)
