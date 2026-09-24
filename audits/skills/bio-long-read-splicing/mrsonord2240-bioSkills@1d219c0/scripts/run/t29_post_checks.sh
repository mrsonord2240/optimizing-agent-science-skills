#!/bin/bash
# (1) uLTRA per-gene two-way table on micro2 (from t25 BAMs); (2) SQANTI3 classification of the planted FLAIR isoforms with the id-safe checker (sqanti_check.py).
R=/mnt/openscience/audits/bio-long-read-splicing/run; export PYTHONDONTWRITEBYTECODE=1
cd $R/out/ultra_micro2
for P in hifi ontunstr drna; do echo "--- $P uLTRA per gene (inc% / skip%)"; asenv as-lr python $R/micro2_eval.py ultra_$P.bam $R/data/micro2/truth_chains.tsv "$P uLTRA" --genes | head -14; done
cd $R/out/hifi6; echo "--- SQANTI3 on planted FLAIR isoforms"; asenv as-lr python $R/sqanti_check.py
