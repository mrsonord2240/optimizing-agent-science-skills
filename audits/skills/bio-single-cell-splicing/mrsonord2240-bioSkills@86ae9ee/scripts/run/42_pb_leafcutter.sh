#!/bin/bash
# INPUT 5: generate the replicate-structured planted matrix, run S12/S13 (41_*), then SKILL.md block S14 (leafcutter_ds.R -i 5 -g 3 -c 20) LITERALLY, then score, then the n=1 (pooled) comparison.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
asenv as-sc python $R/40_pb_gen.py $R/data/pb_v2 31
mkdir -p $R/out/in5; cd $R/out/in5
asenv as-sc python $R/41_pb_S12_S13.py 2>&1 | grep -v 'cuda\|absl'
head -c 300 pb_groups.txt; echo
bash $R/blocks/S14_bash.sh 2>&1 | tr '\r' '\n' | tail -5
ls pb_ds*
asenv as-sc python $R/43_pb_score.py
