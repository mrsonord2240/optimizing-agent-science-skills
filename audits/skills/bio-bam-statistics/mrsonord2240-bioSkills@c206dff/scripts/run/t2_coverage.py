#!/usr/bin/env python3
"""INPUT 2 (variant A, REAL data): mean depth / breadth on the human chr22 slice with every tool the Skill names,
against an independent block-based truth. Usage: t2_coverage.py <bam> <contig> <length>"""
import subprocess, sys, os, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_snippets as S
from truth import depth_arrays

bam, contig, L = sys.argv[1], sys.argv[2], int(sys.argv[3])
outdir = 'work/t2'; os.makedirs(outdir, exist_ok=True)

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

def stat(d):
    return dict(mean=round(float(d.sum()) / L, 4), covered=int((d > 0).sum()), pct=round(100 * (d > 0).sum() / L, 4),
                ge10=round(100 * (d >= 10).sum() / L, 4), ge20=round(100 * (d >= 20).sum() / L, 4), max=int(d.max()))

truth_plain = depth_arrays(bam, contig, L)
truth_noov = depth_arrays(bam, contig, L, no_overlap=True)
print('TRUTH (blocks, default excl flags, overlaps double counted)', stat(truth_plain))
print('TRUTH (blocks, mates overlap counted once)                 ', stat(truth_noov))

# --- samtools depth variants
def depth_arr(args):
    d = np.zeros(L, dtype=np.int64)
    for line in sh(f'samtools depth -a {args} {bam}').splitlines():
        c, p, v = line.split('\t'); d[int(p) - 1] = int(v)
    return d
print('samtools depth -a           ', stat(depth_arr('')))
print('samtools depth -a -s        ', stat(depth_arr('-s')))

# Skill recipe: mean depth WITHOUT -a
nz = [int(l.split('\t')[2]) for l in sh(f'samtools depth {bam}').splitlines()]
print('SKILL recipe "samtools depth | awk sum/n" (no -a): mean =', round(sum(nz) / len(nz), 4), ' over', len(nz), 'covered positions')
tot = len(nz); c10 = sum(1 for v in nz if v >= 10); c20 = sum(1 for v in nz if v >= 20)
print('SKILL recipe ">=10x / >=20x pct" (no -a): %.1f%% / %.1f%%  (denominator = covered positions only)' % (c10 / tot * 100, c20 / tot * 100))
print('  same with -a (denominator = whole contig): %.3f%% / %.3f%%' % (100 * (truth_plain >= 10).sum() / L, 100 * (truth_plain >= 20).sum() / L))

# --- samtools coverage
print('samtools coverage :', sh(f'samtools coverage {bam}').splitlines()[1])

# --- mosdepth default and --fast-mode
for tag, extra in (('mosdepth default', ''), ('mosdepth --fast-mode', '--fast-mode')):
    pre = f'{outdir}/{tag.replace(" ", "_").replace("-", "")}'
    sh(f'mosdepth {extra} {pre} {bam}')
    row = [l for l in open(pre + '.mosdepth.summary.txt').read().splitlines() if l.startswith(contig + '\t')][0].split('\t')
    d = np.zeros(L, dtype=np.int64)
    for line in gzip.open(pre + '.per-base.bed.gz', 'rt'):
        c, s, e, v = line.split('\t'); d[int(s):int(e)] = int(v)
    print(tag, ' summary mean =', row[3], ' from per-base:', stat(d))

# --- bedtools genomecov (counts everything not unmapped incl. secondary/dups)
d = np.zeros(L, dtype=np.int64)
for line in sh(f'bedtools genomecov -ibam {bam} -d').splitlines():
    c, p, v = line.split('\t'); d[int(p) - 1] = int(v)
print('bedtools genomecov -d       ', stat(d))

# --- Skill pysam snippets (0-based half-open, whole contig)
print('SKILL pysam mean_depth()        :', round(S.skill_mean_depth(bam, contig, 0, L), 4), '(mean over pileup columns only)')
cs = S.skill_coverage_stats(bam, contig, 0, L)
print('SKILL pysam coverage_stats()    :', {k: round(v, 4) for k, v in cs.items()})
gr = S.guide_region_coverage(bam, contig, 0, L)
print('GUIDE pysam region_coverage()   :', {k: round(v, 4) for k, v in gr.items()})
# sub-region as a user would ask: the covered window
print('Window 1951-4617 (0-based half-open) truth mean =', round(truth_plain[1951:4617].mean(), 4),
      '| SKILL mean_depth() =', round(S.skill_mean_depth(bam, contig, 1951, 4617), 4),
      '| SKILL coverage_stats mean =', round(S.skill_coverage_stats(bam, contig, 1951, 4617)['mean_depth'], 4))
