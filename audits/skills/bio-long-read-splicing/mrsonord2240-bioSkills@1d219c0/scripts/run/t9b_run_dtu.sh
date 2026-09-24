#!/bin/bash
# (Git Bash) the SKILL's DTU R block, sourced verbatim by t9_dtu.R, on the planted FLAIR output (logs/t9_dtu_planted.log) and on the real 6-sample output (logs/t9_dtu_real.log); Windows R via r.sh
AS=/f/OpenScience/audit-envs/alternative-splicing; R=F:/OpenScience/audits/bio-long-read-splicing/run
$AS/r.sh $R/t9_dtu.R $R/out/hifi6 $R/data/plant/truth_dtu.tsv 2>&1 | tail -14 > $R/logs/t9_dtu_planted.log
$AS/r.sh $R/t9_dtu.R $R/out/real $R/data/plant/truth_dtu.tsv 2>&1 | tail -8 > $R/logs/t9_dtu_real.log
