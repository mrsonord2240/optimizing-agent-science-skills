#!/bin/bash
# REGRESSION of the pre-fix inputs (old generators, same seeds): BRIE2 planted Smart-seq-like (input 2 pre-fix), null control, 10x planted, real 10x. Paths adapted; helper renamed.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; cd $R
asenv as-core python regress/10_gen_planted_sc.py $R/data/synth_ss2 ss2 20 | tail -1
asenv as-core python regress/10_gen_planted_sc.py $R/data/synth_10x 10x 22 | tail -1
bash regress/11_brie_planted.sh 2>&1 | tr '\r' '\n' | grep -v "cuda\|absl" | tail -8
asenv as-sc python regress/12_eval_planted.py 2>&1 | grep -v "cuda\|absl\|GPU\|cpu_feature\|rebuild" | tail -30
bash regress/13_null_ss2.sh 2>&1 | tr '\r' '\n' | grep "NULL run"
asenv as-sc python regress/14_brie_10x.py 2>&1 | grep -v "cuda\|absl\|GPU\|cpu_feature\|rebuild" | tail -22
asenv as-sc python regress/15_real_10x.py 2>&1 | grep -v "cuda\|absl\|GPU\|cpu_feature\|rebuild" | tail -12
