#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 TF_CPP_MIN_LOG_LEVEL=3
AS=/mnt/openscience/audit-envs/alternative-splicing
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
CB=/home/sci/micromamba/envs/as-core/bin
$CB/bgzip -c data/panel_grch37.vcf > data/panel_grch37.vcf.gz && $CB/tabix -f -p vcf data/panel_grch37.vcf.gz
for m in plain gz; do echo "=== mode $m"; $AS/tools/bin/asenv as-mmsplice python t3_mmsplice.py $m 2>&1 | grep -av "cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources" | tail -25; ls -la out/mmsplice_$m.csv 2>&1; done
