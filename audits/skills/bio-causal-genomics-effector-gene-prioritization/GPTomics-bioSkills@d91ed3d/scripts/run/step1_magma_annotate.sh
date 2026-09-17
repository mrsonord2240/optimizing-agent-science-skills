#!/usr/bin/env bash
# Step 1 of the Skill's own examples/magma_genebased.sh, run against a synthetic
# chr1:54.9-55.7Mb window (see make_synthetic_gwas.py) that genuinely spans the real
# PCSK9 locus. Reference: real 1000G EUR PLINK bfile shipped with MAGMA.
set -euo pipefail
MAGMA="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/magma.exe"

"$MAGMA" --annotate window=35,10 \
    --snp-loc gwas_synthetic.snploc \
    --gene-loc gene_loc_chr1_window.txt \
    --out magma_annot

# Result: 7248/7370 (98.34%) SNPs mapped to >=1 of the 5 synthetic gene bins.
