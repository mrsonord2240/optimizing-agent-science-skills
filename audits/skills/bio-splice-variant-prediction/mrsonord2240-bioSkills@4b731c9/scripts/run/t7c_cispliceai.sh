#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
FA=/mnt/openscience/as-spvp-reaudit-scratch/hg38_chr7_chr17.upper.fa
# SKILL.md CI-SpliceAI command
( time micromamba run -n as-cispliceai cis-vcf -a grch38 -d 500 --all -i data/panel_new_grch38.vcf -o out/ci_new.vcf $FA ) 2>&1 | tr '\r' '\n' | grep -av "━\|cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|^$" | tail -8
grep -v '^#' out/ci_new.vcf | cut -f3,8 | cut -c1-200
