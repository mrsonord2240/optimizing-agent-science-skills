#!/bin/bash
# content assertions on the shipped-example outputs vs planted truth (eval_example.py); SUF=sj for the SR_JUNCTIONS runs
R=/mnt/openscience/audits/bio-long-read-splicing/run
export PYTHONDONTWRITEBYTECODE=1
for v in "hifi hifi" "ont ontunstr" "drna drna"; do set -- $v; SUF=${SUF:-}
  asenv as-lr python $R/eval_example.py $R/out/ex_$1${SUF}/out $2 ctrl1 "shipped example PLATFORM=$1 ${SUF}"
done
