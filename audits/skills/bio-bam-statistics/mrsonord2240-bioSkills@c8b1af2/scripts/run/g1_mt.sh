#!/bin/bash
# build synth_MT.bam: synth.bam with chrM renamed to MT (Ensembl-style)
export LC_ALL=C; R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; S=$R/data/synth.bam
samtools view -H $S | sed 's/SN:chrM/SN:MT/' > mt.hdr
samtools view $S | awk -F'\t' 'BEGIN{OFS="\t"} {if($3=="chrM")$3="MT"; if($7=="chrM")$7="MT"; print}' | cat mt.hdr - | samtools view -b -o synth_MT.bam -
samtools index synth_MT.bam; samtools idxstats synth_MT.bam | head -4
