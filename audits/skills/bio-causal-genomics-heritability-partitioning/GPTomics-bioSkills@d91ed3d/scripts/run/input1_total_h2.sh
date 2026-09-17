#!/bin/bash
# Input 1 (Canonical): total h2 from EUR sumstats via LDSC --h2
# Requires driver_ldsc.py's monkeypatch (see file header) because
# abdenlab/ldsc-python3 v2.0.0's ldsc.py calls sumstats.estimate_h2,
# which does not exist (module defines estimate_heritability instead).
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
FIX=../data/ldsc_test_fixtures
$VENV driver_ldsc.py --h2 $FIX/simulate_test/sumstats/0 \
  --ref-ld $FIX/simulate_test/ldscore/oneld_onefile \
  --w-ld $FIX/simulate_test/ldscore/w \
  --out out/input1_h2
