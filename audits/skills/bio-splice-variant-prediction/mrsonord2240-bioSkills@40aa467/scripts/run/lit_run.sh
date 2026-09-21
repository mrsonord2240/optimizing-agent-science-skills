#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/lit
for b in B03 B12; do echo "=== literal SKILL.md block $b"; micromamba run -n as-spvp python - < ../blocks/$b.py 2>&1; done
