#!/bin/bash
# munge_sumstats.py leg used for Input 1 -- ran clean, no patch needed.
VENV=F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-ldsc/Scripts/python.exe
LDSC_DIR=F:/OpenScience/audit-envs/mendelian-randomization-analyst/ldsc-python3
FIX=../data/ldsc_test_fixtures
$VENV $LDSC_DIR/munge_sumstats.py \
  --sumstats $FIX/munge_test/sumstats \
  --merge-alleles $FIX/munge_test/merge_alleles \
  --N 6702 --signed-sumstats OR,1 \
  --out out/input1_munge
