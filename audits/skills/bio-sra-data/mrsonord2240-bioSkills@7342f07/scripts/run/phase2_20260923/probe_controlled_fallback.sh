#!/usr/bin/env bash
set -uo pipefail
run_root=/mnt/openscience/audits/bio-sra-data/run/phase2_20260923/safety_final_tip
runtime=/home/sci/sra-audit-20260923
export HOME=/mnt/openscience/audits/bio-sra-data/private_runtime/home_corrective_controlled
export PATH="$run_root/fakebin:$runtime/bin:$PATH"
mkdir -p "$HOME" "$run_root/outputs/controlled_fallback"
bash "$run_root/copied_source/examples/download_single.sh" ERR99999999 "$run_root/outputs/controlled_fallback" 2 1G >"$run_root/outputs/input8_controlled_fallback.stdout.txt" 2>"$run_root/outputs/input8_controlled_fallback.stderr.txt"
status=$?
if [ "$status" -eq 0 ] || compgen -G "$run_root/outputs/controlled_fallback/*.fastq*" >/dev/null; then
    exit 1
fi
printf 'input8_controlled_fallback=%s\n' "$status" >>"$run_root/outputs/exit_statuses.txt"
