#!/bin/bash
# Re-measure the SKILL's -uf / orientation-check claims on MY OWN planted reads (data/plant), 4 platforms, one sample each (ctrl1).
# Recipes: SKILL.md "Splice-Aware Alignment" (with --junc-bed annotation.bed12) with and without -uf; orientation-check awk copied verbatim from SKILL.md.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; O=$R/out/uf; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
gffread $D/ref.gtf --bed -o annotation.bed12
ev() { asenv as-lr python $R/eval_bam.py "$1" $D/truth_chains.tsv "$2"; }
orient() { samtools view -F 2308 "$1" | awk '{for(i=12;i<=NF;i++) if($i ~ /^ts:A:/){n++; if($i=="ts:A:+") p++}} END{printf "%.3f\n", p/n}'; }
for P in hifi ontunstr ontstr drna; do
  FQ=$D/$P/ctrl1.fastq
  if [ $P = hifi ]; then PRE="splice:hq"; else PRE="splice -k14"; fi
  minimap2 -ax $PRE --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa $FQ 2>/dev/null | samtools sort -o ${P}_nouf.bam - 2>/dev/null; samtools index ${P}_nouf.bam
  minimap2 -ax ${PRE/splice/splice -uf} --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa $FQ 2>/dev/null | samtools sort -o ${P}_uf.bam - 2>/dev/null; samtools index ${P}_uf.bam
  echo "== $P  orientation check (SKILL awk, on the no--uf alignment): ts:A:+ fraction = $(orient ${P}_nouf.bam)"
  ev ${P}_nouf.bam "$P  no -uf"
  ev ${P}_uf.bam   "$P  -uf"
done
