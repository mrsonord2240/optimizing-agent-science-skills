#!/bin/bash
# regenerate the SYNTHETIC cohort (seed 20260920) with the audit's generator, in WSL as-core
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-core python scripts/01_make_synth_cohort.py data/synth 2>&1 | tail -5
ls data/synth | head -80
