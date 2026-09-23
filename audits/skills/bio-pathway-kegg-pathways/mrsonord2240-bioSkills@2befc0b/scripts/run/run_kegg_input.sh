#!/usr/bin/env bash
set -euo pipefail

input="$1"
out="/mnt/openscience/audits/bio-pathway-kegg-pathways/run/input${input}.out"
/home/sci/micromamba/envs/kegg-phase2/bin/Rscript \
  /mnt/openscience/audits/bio-pathway-kegg-pathways/run/verify_kegg_input.R "$input" >"$out" 2>&1
printf 'exit=0\n' >>"$out"
