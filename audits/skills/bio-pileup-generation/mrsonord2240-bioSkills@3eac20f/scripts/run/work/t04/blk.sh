#!/bin/bash
cd /mnt/f/OpenScience/audits/bio-pileup-generation/run/work/t04
bcftools mpileup -f /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/syn.fa --threads 4 -d 100000 -q 20 -Q 20 \
    -a FORMAT/AD,FORMAT/DP /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/s1.bam /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/s2.bam | \
  bcftools call -mv --threads 4 -Oz -o joint.vcf.gz
