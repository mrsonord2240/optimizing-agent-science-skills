#!/bin/bash
# NEW input 7: my own microexon set (data/micro2, gen_micro2.py): 12 single microexons of 3-27 nt + 2 tandem pairs, 150 inclusion + 150 skipping reads per gene.
# SKILL recipes (plain / --junc-bed / +--junc-bonus 16 ...) for the 3 platforms; two-way check from pysam CIGAR N ops; dangling junctions counted.
# usage: t22_micro2_sweep.sh <hifi|ontunstr|drna>
P=$1; R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro2; O=$R/out/micro2_$P; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
gffread $D/ref_full.gtf --bed -o annotation.bed12
case $P in hifi) PRE="splice:hq";; ontunstr) PRE="splice -k14";; drna|drnalow) PRE="splice -uf -k14";; esac
run() { # name, extra
  minimap2 -ax $PRE --secondary=no $2 -t 6 $D/chrM2.fa $D/$P.fastq 2>/dev/null | samtools sort -o $1.bam - 2>/dev/null; samtools index $1.bam
  asenv as-lr python $R/micro2_eval.py $1.bam $D/truth_chains.tsv "$P $1" $3
}
run plain ""
run juncbed "--junc-bed annotation.bed12"
run bonus9 "--junc-bed annotation.bed12 --junc-bonus 9"
for b in 12 14 15 16 17 18 20; do run bonus$b "--junc-bed annotation.bed12 --junc-bonus $b"; done
asenv as-lr python $R/micro2_eval.py bonus16.bam $D/truth_chains.tsv "$P bonus16 per gene" --genes
asenv as-lr python $R/micro2_eval.py juncbed.bam $D/truth_chains.tsv "$P juncbed per gene" --genes
