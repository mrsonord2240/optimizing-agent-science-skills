#!/usr/bin/env bash
# Complete the post-parallel checks for archived stress input 5.
set -euo pipefail
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
W=$R/out/in5
N=$W/n6/lc
for cfg in "6 6 10" "5 5 10" "5 3 20"; do
  set -- $cfg
  for cmp in AvB AvC; do
    $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 6 -i $1 -g $2 -c $3 -o $N/x_${1}_${2}_${3}_$cmp $N/lc_perind_numers.counts.gz $N/groups_$cmp.txt > $N/x_${1}_${2}_${3}_$cmp.log 2>&1
    echo "6v6 -i $1 -g $2 -c $3 $cmp rc=$? clusters tested: $(ntested $N/x_${1}_${2}_${3}_${cmp}_cluster_significance.txt) p.adjust<0.05: $(nsig $N/x_${1}_${2}_${3}_${cmp}_cluster_significance.txt)"
  done
done
$CORE python $R/eval_sim2.py $R/data/sim2/truth.tsv $W 1 2 3 4 6 > $W/eval.txt 2>&1
cat $W/eval.txt
