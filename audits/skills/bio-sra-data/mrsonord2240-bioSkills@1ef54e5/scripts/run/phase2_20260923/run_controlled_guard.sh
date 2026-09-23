#!/usr/bin/env bash
set -euo pipefail

run_root=/mnt/openscience/audits/bio-sra-data/run/phase2_20260923
work="$run_root/copied_source"
output="$run_root/outputs"
runtime=/home/sci/sra-audit-20260923

chmod +x "$run_root/fakebin/curl"
PATH="$run_root/fakebin:$runtime/bin:$PATH" bash "$work/examples/download_batch.sh" \
  "$run_root/controlled_accessions.txt" "$output/controlled_guard" \
  >"$output/input5_controlled_guard_recheck.stdout.txt" \
  2>"$output/input5_controlled_guard_recheck.stderr.txt"

grep -q 'fastq_ftp, fastq_md5 not found' "$output/input5_controlled_guard_recheck.stdout.txt"
grep -qx 'CONTROLLEDTEST1' "$output/controlled_guard/failed.txt"
test ! -e "$output/controlled_guard"/*.fastq.gz
printf 'input5_controlled_guard_recheck=0\n' >>"$output/exit_statuses.txt"
