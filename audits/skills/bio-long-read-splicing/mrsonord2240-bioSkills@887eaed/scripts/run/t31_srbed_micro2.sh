#!/bin/bash
# SKILL "Other routes": a microexon in no annotation is rescued from short-read junctions: STAR-layout SJ.out.tab (make_sj.py from micro2 truth) -> the SKILL's awk -> 6-column BED -> --junc-bed (HiFi at default bonus, ONT/dRNA --junc-bonus 16). No annotation is given to minimap2.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro2; O=$R/out/srbed_micro2; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
asenv as-lr python $R/make_sj.py $D/truth_chains.tsv chrM2 SJ.out.tab
awk 'BEGIN{OFS="\t"} $4>0 {print $1,$2-1,$3,"sj"NR,$7,($4==1?"+":"-")}' SJ.out.tab > sr_junctions.bed; head -2 sr_junctions.bed
for P in hifi ontunstr drnalow; do
  case $P in hifi) PRE="splice:hq"; B="";; ontunstr) PRE="splice -k14"; B="--junc-bonus 16";; drnalow) PRE="splice -uf -k14"; B="--junc-bonus 16";; esac
  minimap2 -ax $PRE --secondary=no --junc-bed sr_junctions.bed $B -t 6 $D/chrM2.fa $D/$P.fastq 2>/dev/null | samtools sort -o $P.bam - 2>/dev/null; samtools index $P.bam
  asenv as-lr python $R/micro2_eval.py $P.bam $D/truth_chains.tsv "$P SJ-bed $B"
done
