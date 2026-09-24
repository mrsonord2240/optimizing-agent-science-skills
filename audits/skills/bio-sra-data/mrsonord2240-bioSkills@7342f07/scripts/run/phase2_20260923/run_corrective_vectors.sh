#!/usr/bin/env bash
set -uo pipefail

audit_root=/mnt/openscience/audits/bio-sra-data
run_root="$audit_root/run/phase2_20260923/safety_final_tip"
source_root=/mnt/openscience/wt/database-access-sra-data/database-access/sra-data
runtime=/home/sci/sra-audit-20260923
private_home="$audit_root/private_runtime/home_corrective"
mkdir -p "$run_root/outputs" "$run_root/fakebin" "$private_home"
rm -rf "$run_root/copied_source"
cp -a "$source_root" "$run_root/copied_source"
export HOME="$private_home"
export PATH="$runtime/bin:$PATH"
source_copy="$run_root/copied_source"

status=0
record() {
  name="$1"
  shift
  "$@" >"$run_root/outputs/${name}.stdout.txt" 2>"$run_root/outputs/${name}.stderr.txt"
  code=$?
  printf '%s=%s\n' "$name" "$code" >>"$run_root/outputs/exit_statuses.txt"
  if [ "$code" -ne 0 ]; then status=1; fi
}

printf 'ERR10419835\n' >"$run_root/accessions_live.txt"
record input1_ena_live bash "$source_copy/examples/download_batch.sh" "$run_root/accessions_live.txt" "$run_root/outputs/ena_live"
record input2_sra_toolkit bash "$source_copy/examples/download_single.sh" ERR10419835 "$run_root/outputs/toolkit_fastq" 2 100G
record input3_pysradb python "$source_copy/scripts/pysradb_resolve.py" GSE110009
record input4_find_runs bash -c "cd '$source_copy' && python examples/find_sra_runs.py"

cp "$audit_root/run/phase2_20260923/corrective_fake_curl" "$run_root/fakebin/curl"
chmod +x "$run_root/fakebin/curl"
printf 'ERR99999999\n' >"$run_root/controlled_accessions.txt"
record input5_controlled_guard env PATH="$run_root/fakebin:$PATH" bash "$source_copy/examples/download_batch.sh" "$run_root/controlled_accessions.txt" "$run_root/outputs/controlled_guard"
record input6_strides_fallback bash "$source_copy/examples/prefetch_large.sh" ERR10419835 "$run_root/outputs/strides_fastq" 2 no
record input7_edirect efetch -db sra -id 8 -format runinfo

for dir in "$run_root/outputs/toolkit_fastq" "$run_root/outputs/strides_fastq"; do
  if ! compgen -G "$dir/*.fastq.gz" >/dev/null; then
    printf 'missing expected FASTQ in %s\n' "$dir" >&2
    status=1
  fi
done
if compgen -G "$run_root/outputs/controlled_guard/*.fastq*" >/dev/null; then
  printf 'controlled fixture produced FASTQ unexpectedly\n' >&2
  status=1
fi
printf 'overall=%s\n' "$status" >>"$run_root/outputs/exit_statuses.txt"
exit "$status"
