#!/bin/bash
# Input 3 (Variant B): cross-trait genetic correlation via LDSC --rg
# (HDL leg not installed this session -- inspected only, see eval_viewer).
# Requires numpy<2 in the venv: abdenlab/ldsc-python3's own regressions.py
# does float(rg.jknife_est) on a >0-d array, which numpy>=2.0 (the fork's
# OWN pinned dependency, pyproject.toml numpy=^2.1.2) raises TypeError on.
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
FIX=../data/ldsc_test_fixtures
$VENV driver_ldsc.py --rg $FIX/simulate_test/sumstats/0,$FIX/simulate_test/sumstats/1 \
  --ref-ld $FIX/simulate_test/ldscore/twold_onefile \
  --w-ld $FIX/simulate_test/ldscore/w \
  --out out/input3_rg
