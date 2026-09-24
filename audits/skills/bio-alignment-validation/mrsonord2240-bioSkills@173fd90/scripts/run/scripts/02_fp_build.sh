#!/bin/bash
R=/mnt/openscience/audits/bio-alignment-validation/run
export PYTHONIOENCODING=utf-8
python $R/scripts/make_fp_fixtures.py $R/data/fp
cd $R/data/fp
picard ConvertHaplotypeDatabaseToVcf -I hap.txt -O hap.vcf.gz -R /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta 2>&1 | grep -v -E '^\*|setlocale|restricted|WARNING|Runtime|^$' | tail -5 | cut -c1-220
zcat hap.vcf.gz | grep -v '^##' | head -3 | cut -c1-200
