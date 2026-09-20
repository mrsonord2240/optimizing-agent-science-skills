#!/bin/bash
# look at the real 1000G slice used as the base of the NEW planted-defect set
B=/mnt/openscience/audit-envs/alignment-files/public-data/1000g/HG00349.chr20_1400000-1500000.bam
samtools flagstat $B
echo "SQ lines: $(samtools view -H $B | grep -c '^@SQ')"
samtools view -H $B | grep -v '^@SQ'
samtools view $B | head -2 | cut -f1-9,12-
samtools view $B | cut -f3 | sort | uniq -c | sort -nr | head -3
