#!/bin/bash
cd /mnt/openscience/audits/bio-alignment-validation/run/data/fp
picard ConvertHaplotypeDatabaseToVcf -I hap.txt -O hap.vcf.gz -R /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta 2>&1 | grep -E 'Exception|ERROR|Caused' | head -4 | cut -c1-250
head -8 hap.txt | cut -c1-120
