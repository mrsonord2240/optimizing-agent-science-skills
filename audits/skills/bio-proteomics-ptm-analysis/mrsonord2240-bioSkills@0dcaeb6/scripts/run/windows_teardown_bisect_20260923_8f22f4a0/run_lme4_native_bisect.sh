#!/usr/bin/env bash
set -u -o pipefail
RUN=/f/OpenScience/audits/bio-proteomics-ptm-analysis/run/windows_teardown_bisect_20260923_8f22f4a0
RSH=/f/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh
PROBE="$RUN/probe.R"
run_one() {
  local tag=$1 mode=$2 target=$3
  printf '%s\t%s\t%s\n' "$tag" "$mode" "$target" >> "$RUN/native_commands.tsv"
  "$RSH" "$PROBE" "$mode" "$target" > "$RUN/${tag}.stdout.log" 2> "$RUN/${tag}.stderr.log" &
  local pid=$!
  printf '%s\n' "$pid" > "$RUN/${tag}.owned_pid"
  wait "$pid"
  printf '%s\n' "$?" > "$RUN/${tag}.exit_code"
}
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)" > "$RUN/native_commands.tsv"
run_one minqa package minqa
run_one nloptr package nloptr
run_one rlang package rlang
run_one cli package cli
run_one rbibutils package rbibutils
run_one nlme package nlme
run_one dll_lme4 dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/lme4/libs/x64/lme4.dll'
run_one dll_minqa dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/minqa/libs/x64/minqa.dll'
run_one dll_nloptr dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/nloptr/libs/x64/nloptr.dll'
printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)" >> "$RUN/native_commands.tsv"
