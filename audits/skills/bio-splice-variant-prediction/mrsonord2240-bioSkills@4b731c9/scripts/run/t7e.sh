#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 TF_CPP_MIN_LOG_LEVEL=3
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
micromamba run -n as-mmsplice python t7e_mmsplice.py 2>&1 | grep -av "cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources\|tf.function" | tr '\r' '\n' | tail -5
ls -la out/mmsplice_new.csv
