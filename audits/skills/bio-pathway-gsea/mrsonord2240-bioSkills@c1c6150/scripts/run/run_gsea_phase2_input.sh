#!/usr/bin/env bash
set -euo pipefail

input="$1"
out="/mnt/openscience/audits/bio-pathway-gsea/run/input${input}.out"
/home/sci/micromamba/envs/gsea-phase1-lite/bin/Rscript \
  /mnt/openscience/audits/bio-pathway-gsea/run/gsea_phase2_inputs.R "$input" >"$out" 2>&1
printf 'exit=0\n' >>"$out"
