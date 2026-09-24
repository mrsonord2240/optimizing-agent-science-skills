#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
FA=/mnt/openscience/as-spvp-reaudit-scratch/hg38_chr7_chr17.upper.fa
rm -rf ex_new && mkdir ex_new && cp skill/examples/*.py ex_new/ && cp data/panel_new_grch38.vcf ex_new/ && cd ex_new
echo "=== shipped example on the new panel"
micromamba run -n as-spliceai python spliceai_clingen_classify.py panel_new_grch38.vcf $FA --build grch38 --out-prefix new 2>&1 | tr '\r' '\n' | grep -av "━\|tf.function\|cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources\|^$"
cut -f1-3,4-8,9-12 new_classified.tsv
cd ..
for d in 500 2000; do micromamba run -n as-spliceai spliceai -I data/panel_new_grch38.vcf -O out/sai_new_D$d.vcf -R $FA -A grch38 -D $d -M 0 > out/sai_new_D$d.log 2>&1; echo "spliceai D$d rc=$?"; done
