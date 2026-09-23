#!/usr/bin/env bash
set -u -o pipefail

audit_root=/mnt/openscience/audits/bio-sra-data
run_root="$audit_root/run/phase2_20260923"
source_root=/mnt/openscience/wt/database-access-sra-data/database-access/sra-data
runtime=/home/sci/sra-audit-20260923
work="$run_root/copied_source"
output="$run_root/outputs"
private_home="$audit_root/private_runtime/home"

mkdir -p "$output" "$private_home" "$work"
cp -a "$source_root/." "$work/"
export HOME="$private_home"
export PATH="$runtime/bin:$PATH"

run_case() {
  local name="$1"
  shift
  (cd "$work" && "$@") >"$output/${name}.stdout.txt" 2>"$output/${name}.stderr.txt"
  local status=$?
  printf '%s=%s\n' "$name" "$status" >>"$output/exit_statuses.txt"
  return "$status"
}

: >"$output/exit_statuses.txt"
printf 'ERR10419835\n' >"$work/accessions_live.txt"
run_case input1_ena_live bash examples/download_batch.sh accessions_live.txt "$output/ena_live"
case1=$?
test "$case1" -eq 0
test "$(grep -c 'md5 OK' "$output/input1_ena_live.stdout.txt")" -eq 2
test ! -s "$output/ena_live/failed.txt"

run_case input2_sra_toolkit bash examples/download_single.sh ERR10419835 "$output/toolkit_fastq" 2 100G
case2=$?
test "$case2" -eq 0
test -s "$output/toolkit_fastq/ERR10419835_1.fastq.gz"
test -s "$output/toolkit_fastq/ERR10419835_2.fastq.gz"

run_case input3_pysradb python scripts/pysradb_resolve.py GSE110009
case3=$?
test "$case3" -eq 0
grep -q 'SRR' "$output/input3_pysradb.stdout.txt"

run_case input4_find_runs python examples/find_sra_runs.py
case4=$?

fakebin="$run_root/fakebin"
mkdir -p "$fakebin"
chmod +x "$fakebin/curl"
PATH="$fakebin:$PATH" run_case input5_controlled_guard bash examples/download_batch.sh <(printf 'CONTROLLEDTEST1\n') "$output/controlled_guard"
case5=$?
test "$case5" -eq 0
grep -q 'fastq_ftp, fastq_md5 not found' "$output/input5_controlled_guard.stdout.txt"
grep -qx 'CONTROLLEDTEST1' "$output/controlled_guard/failed.txt"

run_case input6_strides_fallback bash examples/prefetch_large.sh ERR10419835 "$output/strides_fastq" 2 no
case6=$?
test "$case6" -eq 0
test -s "$output/strides_fastq/ERR10419835_1.fastq.gz"
test -s "$output/strides_fastq/ERR10419835_2.fastq.gz"

run_case input7_edirect efetch -db sra -id 8 -rettype runinfo
case7=$?
test "$case7" -ne 0
grep -q 'Unrecognized option -rettype' "$output/input7_edirect.stderr.txt"

printf 'input1_ena_live=%s\ninput2_sra_toolkit=%s\ninput3_pysradb=%s\ninput4_find_runs=%s\ninput5_controlled_guard=%s\ninput6_strides_fallback=%s\ninput7_edirect=%s\n' \
  "$case1" "$case2" "$case3" "$case4" "$case5" "$case6" "$case7" >"$output/summary.txt"
