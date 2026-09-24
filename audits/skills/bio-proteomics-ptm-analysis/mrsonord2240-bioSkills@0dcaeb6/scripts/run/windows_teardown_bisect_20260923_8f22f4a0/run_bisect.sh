#!/usr/bin/env bash
set -u -o pipefail
RUN=/f/OpenScience/audits/bio-proteomics-ptm-analysis/run/windows_teardown_bisect_20260923_8f22f4a0
RSH=/f/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh
PROBE="$RUN/probe.R"
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)" > "$RUN/commands.tsv"
run_one() {
  local tag=$1 mode=$2 target=$3
  printf '%s\t%s\t%s\n' "$tag" "$mode" "$target" >> "$RUN/commands.tsv"
  "$RSH" "$PROBE" "$mode" "$target" > "$RUN/${tag}.stdout.log" 2> "$RUN/${tag}.stderr.log" &
  local pid=$!
  printf '%s\n' "$pid" > "$RUN/${tag}.owned_pid"
  wait "$pid"
  local status=$?
  printf '%s\n' "$status" > "$RUN/${tag}.exit_code"
}
run_one base base none
run_one rcpp package Rcpp
run_one datatable package data.table
run_one stringi package stringi
run_one matrix package Matrix
run_one rcpparmadillo package RcppArmadillo
run_one lme4 package lme4
run_one msstatsconvert package MSstatsConvert
run_one msstats package MSstats
run_one msstatstmt package MSstatsTMT
run_one biostrings package Biostrings
run_one msstatsptm package MSstatsPTM
run_one dll_msstatsptm dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/MSstatsPTM/libs/x64/MSstatsPTM.dll'
printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)" >> "$RUN/commands.tsv"
exit 0
