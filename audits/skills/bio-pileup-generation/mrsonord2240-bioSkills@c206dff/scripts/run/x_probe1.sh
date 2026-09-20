#!/bin/bash
D=/mnt/openscience/audits/bio-pileup-generation/run/data
H=/mnt/openscience/audit-envs/alignment-files/public-data/human
samtools flagstat $D/syn.bam | head -8
samtools mpileup -f $D/syn.fa -r synA:95-105 $D/syn.bam
echo ---human; samtools mpileup -f $H/genome.fasta -r chr22:1950-1960 $H/test.paired_end.sorted.bam | cut -c1-200
