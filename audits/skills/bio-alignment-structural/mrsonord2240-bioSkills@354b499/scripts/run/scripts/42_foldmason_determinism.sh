#!/bin/bash
# Foldmason reproducibility: same 5 structures, N runs, compare aa MSA md5. Variables: --refine-iters (0 vs 100), --threads.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run; cd $R/work/det; S=$R/data/real_pdb
try() { tag=$1; shift; for i in 1 2 3; do rm -rf t_$tag$i; foldmason easy-msa st/1MBN.pdb st/1A3N.pdb st/1ATP.pdb st/1HCK.pdb st/2LHB.pdb o_$tag$i t_$tag$i "$@" -v 0 >/dev/null 2>&1; done; echo "$tag: $(md5sum o_${tag}1_aa.fa o_${tag}2_aa.fa o_${tag}3_aa.fa | cut -c1-8 | tr '\n' ' ')"; }
try r0 --refine-iters 0
try r100 --refine-iters 100
try r100t1 --refine-iters 100 --threads 1
try seed42 --refine-iters 100 --refine-seed 42
