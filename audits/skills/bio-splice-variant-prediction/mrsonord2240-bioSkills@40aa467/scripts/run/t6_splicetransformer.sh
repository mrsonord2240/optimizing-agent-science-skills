#!/bin/bash
# Input 6: SpliceTransformer as in SKILL.md ("python sptransformer.py -I input.vcf -O out.csv --reference hg38"), GPU env, auditor GRCh38 panel.
export PYTHONDONTWRITEBYTECODE=1
R=/mnt/openscience/audits/bio-splice-variant-prediction/run
cd /mnt/openscience/as-spvp-scratch/SpliceTransformer
grep -c '^>' data/data_package/hg38.fa 2>/dev/null; cat data/data_package/hg38.fa.fai | cut -f1,2
( time micromamba run -n as-spvp-gpu python sptransformer.py -I $R/data/panel_grch38_auditor.vcf -O $R/out/st_panel.csv --reference hg38 ) 2>&1 | tail -8
head -3 $R/out/st_panel.csv | cut -c1-300
