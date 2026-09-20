#!/usr/bin/env python3
"""usage: t4_helper.py <bam> <contig> <length> <start> <end> [<start> <end> ...] : Skill block 030 region_depth_stats vs truth from alignment blocks."""
import sys; sys.path.insert(0, '/mnt/openscience/audits/bio-bam-statistics/run')
import depth_truth as T
bam, c, L = sys.argv[1], sys.argv[2], int(sys.argv[3]); a = list(map(int, sys.argv[4:]))
f = T.load_block030(); d = T.truth.depth_arrays(bam, c, L)
for s, e in zip(a[::2], a[1::2]):
    r = f(bam, c, s, e); t = T.summarize(d[s:e])
    ok = abs(r['mean_depth'] - t['mean']) < 1e-9 and r['max_depth'] == t['mx'] and r['covered'] == t['covered'] and abs(r['pct_ge_20x'] - t['ge20']) < 1e-9
    print(f"  [{'OK' if ok else 'BAD'}] {c}[{s},{e}) skill mean {r['mean_depth']:.4f} max {r['max_depth']} | truth mean {t['mean']:.4f} max {t['mx']}")
