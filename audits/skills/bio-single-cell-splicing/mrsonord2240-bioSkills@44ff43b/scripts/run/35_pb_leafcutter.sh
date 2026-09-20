#!/bin/bash
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; O=$R/out/pb_lc
asenv as-sc python $R/35_pb_leafcutter.py
cd $O
echo "=== (a) n=1 vs n=1 (Skill's pseudobulk_junctions output) ==="
leafcutter_ds.R --num_threads 4 -i 1 -g 1 -c 20 -o a_out a_counts.gz a_groups.txt 2>&1 | tr '\r' '\n' | tail -6
ls a_out* 2>/dev/null
echo "=== (b) 5 v 5 replicate pseudobulks ==="
leafcutter_ds.R --num_threads 4 -i 3 -g 3 -c 20 -o b_out b_counts.gz b_groups.txt 2>&1 | tr '\r' '\n' | tail -6
ls b_out* 2>/dev/null
