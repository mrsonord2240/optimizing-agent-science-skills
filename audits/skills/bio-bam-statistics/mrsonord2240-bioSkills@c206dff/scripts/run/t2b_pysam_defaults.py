#!/usr/bin/env python3
"""Why does the Skill's pysam pileup snippet differ from samtools depth? Vary pysam pileup defaults on real + synthetic data."""
import sys, os, subprocess
import numpy as np, pysam
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from truth import depth_arrays
print('pysam', pysam.__version__)
def pile(bam, contig, L, **kw):
    d = np.zeros(L, dtype=np.int64)
    with pysam.AlignmentFile(bam) as f:
        for col in f.pileup(contig, 0, L, truncate=True, **kw):
            d[col.reference_pos] = col.n
    return d
def show(tag, d, L): print(f'  {tag:52s} mean={d.sum()/L:9.4f} covered={(d>0).sum():5d} max={d.max()}')
for bam, contig, L in (('work/test.paired_end.sorted.bam', 'chr22', 40001), ('data/synth.bam', 'synth1', 20000), ('data/synth.bam', 'synth2', 5000)):
    print(bam, contig)
    show('TRUTH blocks (overlap double-counted = samtools depth)', depth_arrays(bam, contig, L), L)
    show('TRUTH blocks (mate overlap counted once)', depth_arrays(bam, contig, L, no_overlap=True), L)
    show('pysam pileup DEFAULTS (as in Skill)', pile(bam, contig, L), L)
    show('pysam pileup min_base_quality=0', pile(bam, contig, L, min_base_quality=0), L)
    show('pysam pileup ignore_overlaps=False', pile(bam, contig, L, ignore_overlaps=False), L)
    show('pysam pileup min_base_quality=0, ignore_overlaps=False', pile(bam, contig, L, min_base_quality=0, ignore_overlaps=False), L)
    show('pysam pileup min_base_quality=0, ignore_overlaps=True', pile(bam, contig, L, min_base_quality=0, ignore_overlaps=True), L)
    o = subprocess.run(f'samtools mpileup -aa -Q 0 -r {contig} {bam}', shell=True, capture_output=True, text=True).stdout
    d = np.array([int(l.split("\t")[3]) for l in o.splitlines()]); show('samtools mpileup -Q0 (overlap removal default on)', d, L)
    o = subprocess.run(f'samtools mpileup -aa -Q 0 -x -r {contig} {bam}', shell=True, capture_output=True, text=True).stdout
    d = np.array([int(l.split("\t")[3]) for l in o.splitlines()]); show('samtools mpileup -Q0 -x (overlap removal off)', d, L)
    o = subprocess.run(f'samtools depth -a -q 13 -r {contig} {bam}', shell=True, capture_output=True, text=True).stdout
    d = np.array([int(l.split("\t")[2]) for l in o.splitlines()]); show('samtools depth -a -q 13', d, L)
