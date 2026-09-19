#!/bin/bash
zcat /mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/casava_clean/S01_S1_L001_R1_001.fastq.gz | head -20 | awk 'NR%4==2{print length($0)}'
echo "---R2---"
zcat /mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/casava_clean/S01_S1_L001_R2_001.fastq.gz | head -20 | awk 'NR%4==2{print length($0)}'
