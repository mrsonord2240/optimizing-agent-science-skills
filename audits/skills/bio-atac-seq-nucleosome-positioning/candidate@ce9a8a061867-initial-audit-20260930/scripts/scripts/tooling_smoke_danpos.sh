#!/bin/bash
# Skill recipes (method-reference DANPOS3): (1) differential `dpos cond2:cond1 --paired 1 --smooth_width 80`, (2) ATAC-tuned single sample.
# Shared atac-danpos env (danpos3 conda 3.2.4, reports 3.1.1), read-only. Input: GM12878 rep1 vs K562 rep1, chr1 slice.
export PATH=$SHARED/tools/bin:$PATH
D=$ATACDATA/encode; W=$NP/work/danpos; rm -rf $W; mkdir -p $W; cd $W
G=$D/GM12878_rep1_filtered.chr1_1-30000000.bam; K=$D/K562_rep1_filtered.chr1_1-30000000.bam
( time danpos dpos $K:$G -o diff --paired 1 --smooth_width 80 ) > diff.log 2>&1; echo "diff rc=$?"; tail -5 diff.log | cut -c1-200
( time danpos dpos $G --paired 1 --width 145 --smooth_width 80 -jd 145 --pheight 1e-5 --frsz 200 --out tuned ) > tuned.log 2>&1; echo "tuned rc=$?"; tail -5 tuned.log | cut -c1-200
find diff tuned -type f | head -30
