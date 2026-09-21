#!/bin/bash
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
cd $R; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript scripts/16_block_extras.R $R/in7_drop $R/blocks > logs/17_extras_2.6.1.log 2>&1
grep -n "==\|LINE\|AE \|PCA \|Error\|error" logs/17_extras_2.6.1.log | cut -c1-220 | tail -n 40
