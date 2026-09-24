#!/bin/bash
# runs 3 scripts x 4 datasets in parallel, NB=2000 PRESSO draws
cd F:/OpenScience/comparisons/pleiotropy-same-id/run
export NB=2000
rm -f out/*.log out/*.rds out/*.done
for d in A_balanced B_directional C_outliers D_chp; do
  F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh theirs_run.R $d > out/theirs_$d.log 2>&1 &
  F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh ours_run.R $d > out/ours_$d.log 2>&1 &
  F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh ours_example_adapted.R $d > out/oursex_$d.log 2>&1 &
done
wait
echo done > out/all.done
