#!/usr/bin/env bash
set -euo pipefail
input="$1"
audit="/mnt/openscience/audits/bio-pathway-wikipathways"
env="/home/sci/micromamba/envs/wikipathways-phase2/bin"
"$env/Rscript" "$audit/run/verify_wikipathways_input.R" "$input" >"$audit/run/input${input}.out" 2>&1
printf 'exit=0\n' >>"$audit/run/input${input}.out"
