#!/usr/bin/env bash
set -uo pipefail
run_root=/mnt/openscience/audits/bio-sra-data/run/phase2_20260923
runtime=/home/sci/sra-audit-20260923
export PATH="$runtime/bin:$PATH"
efetch -db sra -id 8 -format runinfo >"$run_root/outputs/input7_edirect_corrected_flag.stdout.txt" 2>"$run_root/outputs/input7_edirect_corrected_flag.stderr.txt"
status=$?
printf 'input7_edirect_corrected_flag=%s\n' "$status" >>"$run_root/outputs/exit_statuses.txt"
exit "$status"
