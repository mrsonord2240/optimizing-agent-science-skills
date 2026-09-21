#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-core python scripts/03_gen_B.py data/synthB 2>&1 | tail -3
