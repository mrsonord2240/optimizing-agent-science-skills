#!/bin/bash
# Input 4 (Edge): case-control liability-scale h2 (samp-prev/pop-prev flags)
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
FIX=../data/ldsc_test_fixtures
$VENV driver_ldsc.py --h2 $FIX/simulate_test/sumstats/0 \
  --ref-ld $FIX/simulate_test/ldscore/oneld_onefile \
  --w-ld $FIX/simulate_test/ldscore/w \
  --samp-prev 0.08 --pop-prev 0.01 \
  --out out/input4_liability
