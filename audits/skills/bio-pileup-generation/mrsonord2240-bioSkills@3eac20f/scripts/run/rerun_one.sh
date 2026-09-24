#!/bin/bash
# re-run a single script (used once, after the last label edit in t07): rerun_one.sh t07_new_real_matrix
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-pileup-generation/run
mkdir -p work; python $1.py > log_$1.txt 2>&1; echo "$1 rc=$? : $(grep -a -c '^\[PASS\]' log_$1.txt) PASS, $(grep -a -c '^\[FAIL\]' log_$1.txt) FAIL"; rm -rf work
