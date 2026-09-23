#!/usr/bin/env bash
set -euo pipefail

run_root=/mnt/openscience/audits/bio-sra-data/run/phase2_20260923
runtime=/home/sci/sra-audit-20260923
export HOME=/mnt/openscience/audits/bio-sra-data/private_runtime/home_original_format
export PATH="$runtime/bin:$PATH"
mkdir -p "$HOME" "$run_root/outputs/toolkit_original_fastq"
cd "$run_root/copied_source"
prefetch --type sra ERR10419835 --max-size 100G -p >"$run_root/outputs/input2_original_probe.stdout.txt" 2>"$run_root/outputs/input2_original_probe.stderr.txt"
vdb-validate ERR10419835 >>"$run_root/outputs/input2_original_probe.stdout.txt" 2>>"$run_root/outputs/input2_original_probe.stderr.txt"
fasterq-dump ERR10419835 -O "$run_root/outputs/toolkit_original_fastq" -e 2 -p --split-files --skip-technical >>"$run_root/outputs/input2_original_probe.stdout.txt" 2>>"$run_root/outputs/input2_original_probe.stderr.txt"
test -s "$run_root/outputs/toolkit_original_fastq/ERR10419835_1.fastq"
test -s "$run_root/outputs/toolkit_original_fastq/ERR10419835_2.fastq"
printf 'input2_original_probe=0\n' >>"$run_root/outputs/exit_statuses.txt"
