#!/bin/bash
# Input 1 step C: the Skill's brie-quant line, flag-for-flag, on the real counts (covariate = rand_group; null test)
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
asenv as-sc python $R/03a_make_cellfeat.py
cd $R/out
time brie-quant -i real_counts/brie_count.h5ad -c real_cellfeat.tsv -o real_quant.h5ad --interceptMode gene --LRTindex All --testBase null --MCsize 3 --batchSize 1000000 -p 16 2>&1 | tr '\r' '\n' | tail -25
ls -la real_quant.h5ad
