#!/usr/bin/env bash
set -euo pipefail

out=/mnt/openscience/audits/bio-phylo-tree-visualization/run/ggtree.out
/home/sci/micromamba/envs/phylo-phase2/bin/Rscript \
  /mnt/openscience/audits/bio-phylo-tree-visualization/run/verify_ggtree.R >"$out" 2>&1
printf 'exit=0\n' >>"$out"
