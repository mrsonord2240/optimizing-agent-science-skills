#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 TF_CPP_MIN_LOG_LEVEL=3
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
for b in grch37 grch38; do echo "=== $b"; micromamba run -n as-mmsplice python t3_mmsplice.py $b 2>&1 | grep -av "cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources"| tail -8; ls -la out/mmsplice_$b.csv; done
