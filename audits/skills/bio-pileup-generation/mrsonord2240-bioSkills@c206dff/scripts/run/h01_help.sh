#!/bin/bash
# Capture actual --help / usage of the tools the Skill makes claims about
samtools --version | head -2; bcftools --version | head -2
echo "=== samtools mpileup (usage) ==="; samtools mpileup 2>&1 | head -80
echo "=== bcftools mpileup (usage) ==="; bcftools mpileup 2>&1 | head -120
echo "=== samtools mpileup -g ==="; samtools mpileup -g -f /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam 2>&1 | head -3; echo "rc=${PIPESTATUS[0]}"
echo "=== samtools mpileup -u ==="; samtools mpileup -u -f /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam 2>&1 | head -3
