#!/bin/bash
# FRASER 2.6.1 (as-drop): SKILL.md block verbatim
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
cd $R; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript scripts/10_block_fraser.R $R/in1_drop $R/blocks/01_r.R $R/data/synth block_2.6.1 > logs/11_block_fraser_2.6.1.log 2>&1
tail -25 logs/11_block_fraser_2.6.1.log
