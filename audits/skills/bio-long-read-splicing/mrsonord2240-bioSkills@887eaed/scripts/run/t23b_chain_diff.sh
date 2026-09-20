#!/bin/bash
# how many REAL reads change intron chain between the default bonus and 16 / 17 (uses the BAMs of t23_real_dangle.sh); log: logs/chain_diff_real.log
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R/out/real_dangle
asenv as-lr python $R/chain_diff.py cdna_bdefault.bam cdna_b16.bam cdna.bed12 'real cDNA default->16'
asenv as-lr python $R/chain_diff.py cdna_bdefault.bam cdna_b17.bam cdna.bed12 'real cDNA default->17'
asenv as-lr python $R/chain_diff.py drna_bdefault.bam drna_b16.bam drna.bed12 'real dRNA default->16'
