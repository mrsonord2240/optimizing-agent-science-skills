#!/bin/bash
# FRASER 2.2.0 (Windows R via r.sh): SKILL.md block verbatim
R=/f/OpenScience/audits/bio-outlier-splicing-detection/run
cd $R
bash /f/OpenScience/audit-envs/alternative-splicing/r.sh scripts/10_block_fraser.R F:/OpenScience/audits/bio-outlier-splicing-detection/run/in1_win F:/OpenScience/audits/bio-outlier-splicing-detection/run/blocks/01_r.R F:/OpenScience/audits/bio-outlier-splicing-detection/run/data/synth block_2.2.0 > logs/12_block_fraser_2.2.0.log 2>&1
tail -25 logs/12_block_fraser_2.2.0.log
