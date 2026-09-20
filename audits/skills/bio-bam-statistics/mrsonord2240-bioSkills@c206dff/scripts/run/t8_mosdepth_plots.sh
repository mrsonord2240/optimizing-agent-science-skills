#!/bin/bash
# Verify the Skill's mosdepth / coverage -b / plot-bamstats commands against planted truth
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
D=/mnt/openscience/audit-envs/alignment-files/public-data
mkdir -p work/t8 && cd work/t8
cp ../../data/synth.bam* ../../data/synth.fa* . ; cp $D/human/test.paired_end.sorted.cram* . 2>/dev/null; cp $D/human/genome.fasta* $D/human/test.paired_end.sorted.bam* .
{
echo "##### mosdepth default flag set on synth.bam: per-contig sum of per-base depth"
echo "truth (nooverlap: mates once; dups/QCfail/secondary/unmapped excluded; supplementary INCLUDED): synth1=28500 synth2=3500 chrM=4000"
mosdepth -t 2 sd synth.bam
python - <<'PY'
import gzip, collections
t = collections.Counter()
for l in gzip.open('sd.per-base.bed.gz','rt'):
    c,s,e,v = l.split('\t'); t[c] += (int(e)-int(s))*int(v)
print('mosdepth default   :', dict(t))
PY
mosdepth -F 3844 -t 2 sd2 synth.bam; python - <<'PY'
import gzip, collections
t = collections.Counter()
for l in gzip.open('sd2.per-base.bed.gz','rt'):
    c,s,e,v = l.split('\t'); t[c] += (int(e)-int(s))*int(v)
print('mosdepth --flag 3844 (also drop supplementary; truth synth2 = 3500-500 = 3000):', dict(t))
PY
echo "##### Skill: mosdepth -t 4 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base sample input.bam   (BED = chr22:1951-4617, human real)"
printf "chr22\t1951\t4617\n" > exome.bed
mosdepth -t 4 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base ex test.paired_end.sorted.bam
zcat ex.thresholds.bed.gz; zcat ex.regions.bed.gz
python - <<'PY'
import sys; sys.path.insert(0,'../..')
from truth import depth_arrays
d = depth_arrays('test.paired_end.sorted.bam','chr22',40001,no_overlap=True)[1951:4617]
print('TRUTH (mates once) region 1951-4617: mean=%.4f' % d.mean(), ' bases>=1:', int((d>=1).sum()), ' >=10:', int((d>=10).sum()), ' >=20:', int((d>=20).sum()), ' >=30:', int((d>=30).sum()), ' >=100:', int((d>=100).sum()))
PY
echo "##### Skill: mosdepth --quantize 0:1:10:100: "
mosdepth -t 4 --quantize 0:1:10:100: q test.paired_end.sorted.bam; zcat q.quantized.bed.gz | head -6
echo "##### Skill: mosdepth -t 4 -f ref.fa sample input.cram  (CRAM vs BAM summary rows)"
mosdepth -t 4 -f genome.fasta cr test.paired_end.sorted.cram; mosdepth -t 4 bm test.paired_end.sorted.bam
grep '^chr22' cr.mosdepth.summary.txt bm.mosdepth.summary.txt
echo "##### Skill: samtools coverage -b regions.bed input.bam  (flag is --bam-list!)"
samtools coverage -b exome.bed test.paired_end.sorted.bam 2>&1 | head -4; echo "rc=$?"
echo "##### Skill: samtools coverage -r chr22:1952-4617 / samtools depth -b BED / -r"
samtools coverage -r chr22:1952-4617 test.paired_end.sorted.bam | tail -1
samtools depth -b exome.bed test.paired_end.sorted.bam | awk '{s+=$3;n++} END {print "depth -b: covered positions", n, "sum", s}'
echo "##### plot-bamstats -p plots/ stats.txt  (plots/ does not exist yet; and usage-guide prefix)"
samtools stats test.paired_end.sorted.bam > stats.txt
plot-bamstats -p plots/ stats.txt 2>&1 | tail -3; ls plots | head -20; echo "PNG count: $(ls plots/*.png 2>/dev/null | wc -l)"
} > ../../out/t8_mosdepth_plots.txt 2>&1
cd ../..; cat out/t8_mosdepth_plots.txt
