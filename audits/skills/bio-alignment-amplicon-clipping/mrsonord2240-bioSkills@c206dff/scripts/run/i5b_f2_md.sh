#!/bin/bash
# What did the shipped example leave in the "successful" BAM when the calmd reference had the wrong contig name (F2)?
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
W=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i5
echo "records: $(samtools view -c $W/f2.bam)"
echo "reads with MD tag: $(samtools view $W/f2.bam | grep -c 'MD:Z')"
echo "reads with NM tag: $(samtools view $W/f2.bam | grep -c 'NM:i')"
samtools view $W/f2.bam | head -2 | cut -f1-9,12- | cut -c1-200
