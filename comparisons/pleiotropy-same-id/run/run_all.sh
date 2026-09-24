#!/bin/bash
# usage: run_all.sh <script.R> <prefix>   runs the script on datasets A-D in sequence
cd F:/OpenScience/comparisons/pleiotropy-same-id/run
for d in A_balanced B_directional C_outliers D_chp; do
  F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh $1 $d > out/$2_$d.log 2>&1
done
echo done > out/$2.done
