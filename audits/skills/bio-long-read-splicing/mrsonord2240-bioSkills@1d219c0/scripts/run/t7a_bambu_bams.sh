#!/bin/bash
# sorted+indexed HiFi BAMs (SKILL HiFi recipe with --junc-bed) for ctrl1..3 -> out/bambu/sample1..3.bam (names the Bambu block expects)
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; O=$R/out/bambu; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
gffread $D/ref.gtf --bed -o annotation.bed12
i=1; for s in ctrl1 ctrl2 ctrl3; do
  minimap2 -ax splice:hq --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa $D/hifi/$s.fastq 2>/dev/null | samtools sort -o sample$i.bam - 2>/dev/null; samtools index sample$i.bam; i=$((i+1)); done
cp $D/chrQ.fa reference.fa; cp $D/ref.gtf gencode.v45.annotation.gtf; ls -la
