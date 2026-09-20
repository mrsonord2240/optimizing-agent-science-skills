#!/usr/bin/env python3
"""INPUT 4 support: the depth-cap trap. Planted stack: 9500 reads at amp:101-200, 500 reads at amp:301-400 (SYNTHETIC deep.bam).
Also pysam pileup keyword defaults (ignore_orphans etc.) on synth.bam."""
import subprocess, sys, os
import numpy as np, pysam
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout
def maxdepth_lines(txt, col): 
    v=[int(l.split('\t')[col]) for l in txt.splitlines() if l and not l.startswith('#')]; return max(v) if v else None
B='data/deep.bam'
print('TRUTH: max depth at amp:101-200 = 9500, at 301-400 = 500; total base-depth = 9500*100+500*100 =', 9500*100+500*100)
print('samtools depth (default)            max =', maxdepth_lines(sh(f'samtools depth -a {B}'), 2))
print('samtools depth -d 100 (Skill: "silently ignored") max =', maxdepth_lines(sh(f'samtools depth -a -d 100 {B}'), 2))
print('samtools depth -m 100 (older cap flag)       max =', maxdepth_lines(sh(f'samtools depth -a -m 100 {B} 2>&1'), 2))
print('samtools coverage meandepth          =', sh(f'samtools coverage {B}').splitlines()[1].split('\t')[6], '(truth', (9500*100+500*100)/1000, ')')
print('samtools coverage -d 8000 meandepth  =', sh(f'samtools coverage -d 8000 {B}').splitlines()[1].split('\t')[6])
print('samtools mpileup (default -d 8000)   max =', maxdepth_lines(sh(f'samtools mpileup -aa -Q0 {B}'), 3))
print('samtools mpileup -d 1000000 (Skill)  max =', maxdepth_lines(sh(f'samtools mpileup -aa -Q0 -d 1000000 {B}'), 3))
print('bcftools mpileup default -d 250: INFO/DP max at pos 101 =', sh(f'bcftools mpileup -f data/deep.fa -r amp:101 -a FORMAT/DP {B} 2>/dev/null | grep -v "^#" | cut -f8 | head -1'))
print(sh(f'mosdepth -n work/deep {B} 2>&1'))
print('mosdepth summary   :', [l for l in open('work/deep.mosdepth.summary.txt').read().splitlines() if l.startswith('amp\t')])
def pile(**kw):
    d=np.zeros(1000,int)
    with pysam.AlignmentFile(B) as f:
        for c in f.pileup('amp',0,1000,truncate=True,**kw): d[c.reference_pos]=c.n
    return d
d=pile(); print('SKILL pysam pileup default     max =', d.max(), ' mean(region) =', d.sum()/1000)
d=pile(max_depth=1000000); print('pysam pileup max_depth=1000000 max =', d.max(), ' mean(region) =', d.sum()/1000)
import skill_snippets as S
print('SKILL mean_depth() amp:0-1000 =', S.skill_mean_depth(B,'amp',0,1000), '| coverage_stats mean =', S.skill_coverage_stats(B,'amp',0,1000)['mean_depth'], '| truth 100.0 base-depth mean = 1000.0')
print('--- orphan handling (synth.bam synth2: 20 G/I paired-not-proper reads):')
def pile2(contig,L,**kw):
    d=np.zeros(L,int)
    with pysam.AlignmentFile('data/synth.bam') as f:
        for c in f.pileup(contig,0,L,truncate=True,**kw): d[c.reference_pos]=c.n
    return d
print('  pysam default              total depth synth2 =', pile2('synth2',5000).sum(), ' (truth 3500 = samtools depth)')
print('  pysam ignore_orphans=False total depth synth2 =', pile2('synth2',5000,ignore_orphans=False).sum())
print('  samtools depth -a total synth2 =', sum(int(l.split("\t")[2]) for l in sh('samtools depth -a -r synth2 data/synth.bam').splitlines()))
print('  samtools mpileup -A -Q0 total synth2 =', sum(int(l.split("\t")[3]) for l in sh('samtools mpileup -A -aa -Q0 -r synth2 data/synth.bam').splitlines()))
