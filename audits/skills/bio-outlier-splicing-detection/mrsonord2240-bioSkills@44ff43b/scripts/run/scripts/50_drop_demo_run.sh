#!/bin/bash
# Reproduce DROP's public demo (aberrantSplicing target) from a clean copy (no cached Output). Runs in WSL as-drop.
W=/mnt/openscience/audits/bio-outlier-splicing-detection/run/drop_demo
cd $W
export PYTHONDONTWRITEBYTECODE=1
D="micromamba run -n as-drop"
date > run_start.txt
timeout 6000 $D snakemake aberrantSplicing --cores 10 > run.log 2>&1
echo "rc=$?" > run_rc.txt; date >> run_rc.txt
find Output -name "*results*.tsv" -o -name "*results*.Rds" 2>/dev/null | head >> run_rc.txt
