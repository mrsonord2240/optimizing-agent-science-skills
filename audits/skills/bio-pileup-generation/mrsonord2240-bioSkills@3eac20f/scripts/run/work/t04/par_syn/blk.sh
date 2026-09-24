#!/bin/bash
cd /mnt/f/OpenScience/audits/bio-pileup-generation/run/work/t04/par_syn
# Merge in header order: a chr*.vcf.gz glob sorts chr1, chr10, chr11, chr2 ... and bcftools concat
# accepts that silently (exit 0, valid index). Keep contigs.txt to primary contigs (no ':' or '*' names).
samtools idxstats /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/syn.bam | cut -f1 | grep -v '^\*$' > contigs.txt
xargs -a contigs.txt -P 4 -I{} bash -c \
    'set -o pipefail; bcftools mpileup -f /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/syn.fa -r {} -d 1000000 /mnt/f/OpenScience/audits/bio-pileup-generation/run/data/syn.bam | bcftools call -mv -Oz -o {}.vcf.gz' \
  && sed 's/$/.vcf.gz/' contigs.txt > vcf_list.txt \
  && bcftools concat -f vcf_list.txt -Oz -o all.vcf.gz && bcftools index all.vcf.gz
