#!/bin/bash
# Input 2 (Variant A): partitioned h2 across functional categories
# (stand-in for baseline-LD v2.2's 97 categories: the bundled 2-category
# twold_onefile fixture, since real baseline-LD annotations are a multi-GB
# download not available in this environment -- see eval_viewer notes).
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
FIX=../data/ldsc_test_fixtures
$VENV driver_ldsc.py --h2 $FIX/simulate_test/sumstats/0 \
  --ref-ld $FIX/simulate_test/ldscore/twold_onefile \
  --w-ld $FIX/simulate_test/ldscore/w \
  --print-coefficients \
  --out out/input2_partitioned
