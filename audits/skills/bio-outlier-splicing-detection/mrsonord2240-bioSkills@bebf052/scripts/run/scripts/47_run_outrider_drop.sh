#!/bin/bash
# OUTRIDER block verbatim on OUTRIDER 1.28.1 (WSL as-drop), n=30 and n=100 (absolute block path; setwd happens inside the script)
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
cd $R
for n in 30 100; do
  micromamba run -n as-drop Rscript scripts/45_block_outrider.R $R/in2_drop$n $R/blocks/02_r.R > logs/47_outrider_drop_n$n.log 2>&1
done
