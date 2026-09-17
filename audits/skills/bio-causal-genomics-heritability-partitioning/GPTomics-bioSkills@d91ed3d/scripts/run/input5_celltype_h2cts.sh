#!/bin/bash
# Input 5 (Stress): Finucane 2018 cell-type prioritization via --h2-cts.
# CONFIRMED BROKEN even with the CLI-dispatch patch applied: a SEPARATE bug
# -- ldscore/sumstats.py:572 calls ps.ldscore_fromlist(..., n_chr=NUM_CHROMOSOMES)
# and ps.M_fromlist(..., n_chr=...) but ldscore/parse.py defines both
# functions with parameter name `num`, not `n_chr`. Every --h2-cts call
# raises TypeError: ldscore_fromlist() got an unexpected keyword argument
# 'n_chr'. No workaround short of patching ldscore/parse.py itself.
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
FIX=../data/ldsc_test_fixtures
$VENV driver_ldsc.py --h2-cts $FIX/simulate_test/sumstats/0 \
  --ref-ld-chr $FIX/simulate_test/ldscore/oneld_onefile \
  --ref-ld-chr-cts $FIX/simulate_test/test.ldcts \
  --w-ld $FIX/simulate_test/ldscore/w \
  --out out/input5_cts
# LDAK reconciliation leg: not installed this session (dougspeed.com/LDAK has
# no native Windows binary; official guidance is "run LDAK on Windows" via
# WSL). Scored by inspection against ldak_sumher.sh's documented flags.
