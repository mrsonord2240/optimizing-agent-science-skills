#!/bin/bash
# Microexon recipe (SKILL.md "Microexons (3-27 nt)") re-measured on MY OWN planted microexons: MX1 7 nt (+), MX2 12 nt (-), MX3 24 nt (+),
# 200 inclusion reads per gene per platform. Kept = read alignment carries BOTH junctions flanking the microexon (pysam CIGAR N).
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro; O=$R/out/micro; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
ev() { asenv as-lr python $R/eval_bam.py "$1" $D/truth_chains.tsv "$2"; }
gffread $D/ref_full.gtf --bed -o full.bed12          # SKILL: gffread annotation.gtf --bed -o annotation.bed12
gffread $D/ref_noexon.gtf --bed -o noexon.bed12
# SKILL awk (verbatim) on a STAR-layout SJ.out.tab
awk 'BEGIN{OFS="\t"} $4>0 {print $1,$2-1,$3,"sj"NR,$7,($4==1?"+":"-")}' $D/SJ.out.tab > sr_junctions.bed
echo "--- sr_junctions.bed (6 columns) from SKILL awk:"; cat sr_junctions.bed
for P in hifi ontunstr drna; do
  FQ=$D/$P.fastq
  case $P in hifi) PRE="splice:hq";; ontunstr) PRE="splice -k14";; drna) PRE="splice -uf -k14";; esac
  run() { # name, extra args
    minimap2 -ax $PRE --secondary=no $2 -t 8 $D/chrU.fa $FQ 2>/dev/null | samtools sort -o $P.$1.bam - 2>/dev/null; samtools index $P.$1.bam
    ev $P.$1.bam "$P $1"
  }
  run plain ""
  run juncbed_full "--junc-bed full.bed12"
  run juncbed_full_bonus20 "--junc-bed full.bed12 --junc-bonus 20"
  run juncbed_noexon_bonus20 "--junc-bed noexon.bed12 --junc-bonus 20"
  run srbed_bonus20 "--junc-bed sr_junctions.bed --junc-bonus 20"
  minimap2 -ax $PRE --secondary=no -k11 -w5 -t 8 $D/chrU.fa $FQ 2>/dev/null | samtools sort -o $P.k11w5.bam - 2>/dev/null; samtools index $P.k11w5.bam; ev $P.k11w5.bam "$P plain -k11 -w5"
done
echo "--- uLTRA 0.1 (as-sqanti), annotation containing the exon"
for P in hifi ontunstr drna; do
  if [ $P = hifi ]; then MODE=--isoseq; else MODE=--ont; fi
  ( micromamba run -n as-sqanti uLTRA pipeline $MODE --t 8 $D/chrU.fa $D/ref_full.gtf $D/$P.fastq ultra_$P > ultra_$P.log 2>&1 ); echo "uLTRA $P rc=$? files: $(ls ultra_$P | tr '\n' ' ')"
  SAM=$(ls ultra_$P/*.sam | head -1)
  samtools sort -o ultra_$P.bam $SAM 2>/dev/null; samtools index ultra_$P.bam; ev ultra_$P.bam "$P uLTRA full-annotation"
done
