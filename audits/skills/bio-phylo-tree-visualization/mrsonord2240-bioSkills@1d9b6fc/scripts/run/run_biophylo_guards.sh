#!/usr/bin/env bash
set -euo pipefail

out=/mnt/openscience/audits/bio-phylo-tree-visualization/run/biophylo_guards.out
/home/sci/micromamba/envs/phylo-phase2/bin/python \
  /mnt/openscience/audits/bio-phylo-tree-visualization/run/verify_biophylo_guards.py >"$out" 2>&1
printf 'exit=0\n' >>"$out"
