#!/usr/bin/env bash
set -euo pipefail

ROOT=/mnt/openscience/audit-envs/bio-chipseq-allele-specific-binding
AUDIT=/mnt/openscience/audits/bio-chipseq-allele-specific-binding/initial-opt10-20260928
OUT="$AUDIT/evidence"
mkdir -p "$OUT"

run_and_capture() {
  local name=$1
  shift
  local stdout="$OUT/${name}.stdout"
  local stderr="$OUT/${name}.stderr"
  local status="$OUT/${name}.status"
  if "$@" >"$stdout" 2>"$stderr"; then
    printf 'exit_code\t0\nstatus\tPASS\n' >"$status"
  else
    local rc=$?
    printf 'exit_code\t%s\nstatus\tFAIL\n' "$rc" >"$status"
    return "$rc"
  fi
}

run_and_capture wasp bash "$ROOT/run_wasp_smoke.sh"
run_and_capture wasp_hdf5 bash "$ROOT/run_wasp_hdf5_smoke.sh"
run_and_capture rasqual bash "$ROOT/run_rasqual_smoke.sh"
run_and_capture intervals bash "$ROOT/run_interval_smoke.sh"
run_and_capture alleleseq_probe bash "$ROOT/probe_alleleseq.sh"

cp "$ROOT/evidence/wasp-smoke.txt" "$OUT/wasp-smoke.txt"
cp "$ROOT/evidence/wasp-hdf5-smoke.txt" "$OUT/wasp-hdf5-smoke.txt"
cp "$ROOT/evidence/wasp-snp2h5.stderr" "$OUT/wasp-snp2h5.stderr"
cp "$ROOT/evidence/rasqual-smoke.log" "$OUT/rasqual-smoke.log"
cp "$ROOT/evidence/rasqual-output.tsv" "$OUT/rasqual-output.tsv"
cp "$ROOT/evidence/interval-smoke.txt" "$OUT/interval-smoke.txt"
cp "$ROOT/evidence/alleleseq-probe.txt" "$OUT/alleleseq-probe.txt"
cp "$ROOT/evidence/alleleseq-make-dryrun.stdout" "$OUT/alleleseq-make-dryrun.stdout"
cp "$ROOT/evidence/alleleseq-make-dryrun.stderr" "$OUT/alleleseq-make-dryrun.stderr"

printf 'status\tPASS\n' >"$OUT/accessible-surfaces.status"
