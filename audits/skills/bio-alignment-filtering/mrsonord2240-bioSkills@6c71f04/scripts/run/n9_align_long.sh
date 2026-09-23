#!/bin/bash
# NEW input 9, step 1: pbmm2 (and minimap2 map-hifi / map-ont) on the synthetic long reads.
set -u
D=$1; mkdir -p $D; cd $D
python /mnt/openscience/audits/bio-alignment-filtering/run/n9_make_longreads.py $D
pbmm2 --version
pbmm2 align --preset CCS --sort g.fa hifi.fq pbmm2_hifi.bam 2>pbmm2_hifi.log; tail -3 pbmm2_hifi.log
pbmm2 align --preset SUBREAD --sort g.fa ont.fq pbmm2_ont.bam 2>pbmm2_ont.log; tail -3 pbmm2_ont.log
minimap2 -ax map-hifi g.fa hifi.fq 2>/dev/null | samtools sort -o mm2_hifi.bam - && samtools index mm2_hifi.bam
minimap2 -ax map-ont g.fa ont.fq 2>/dev/null | samtools sort -o mm2_ont.bam - && samtools index mm2_ont.bam
for b in pbmm2_hifi pbmm2_ont mm2_hifi mm2_ont; do echo "$b: $(samtools view -c $b.bam) records, $(samtools view -c -F 2308 $b.bam) primary mapped, supplementary $(samtools view -c -f 2048 $b.bam)"; done
