#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/out/sv
S=../../skill/examples
for v in "chr7 117587738 G A" "chr7 117559463 G A" "chr17 43095924 T G" "chr17 43067607 C T" "chr17 43106453 T C" "chr7 117639961 C T"; do
  set -- $v; echo "== $v"; micromamba run -n as-spvp python $S/splicevault_lookup.py $1 $2 $3 $4 --tbi SpliceVault_data_GRCh38.tsv.gz.tbi 2>&1 | head -7
done
