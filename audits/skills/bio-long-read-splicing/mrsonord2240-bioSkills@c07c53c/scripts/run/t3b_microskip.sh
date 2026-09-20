#!/bin/bash
# Same table for the main micro set (7/12/24 nt) so the inclusion AND skipping controls are on record
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro; O=$R/out/micro; cd $O
export PYTHONDONTWRITEBYTECODE=1
for P in hifi ontunstr drna; do for S in plain juncbed_full juncbed_full_bonus20 srbed_bonus20; do
  asenv as-lr python $R/micro_table.py $P.$S.bam $D/truth_chains.tsv "$P $S"; done; done
for P in hifi ontunstr drna; do asenv as-lr python $R/micro_table.py ultra_$P.bam $D/truth_chains.tsv "$P uLTRA"; done
