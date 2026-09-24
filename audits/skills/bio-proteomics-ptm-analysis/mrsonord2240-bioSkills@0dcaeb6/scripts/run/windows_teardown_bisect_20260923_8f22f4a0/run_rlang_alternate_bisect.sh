#!/usr/bin/env bash
set -u -o pipefail
RUN=/f/OpenScience/audits/bio-proteomics-ptm-analysis/run/windows_teardown_bisect_20260923_8f22f4a0
RSH=/f/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh
R=/f/OpenScience/runtime/envs/.r/lib/R/bin/Rscript.exe
PROBE="$RUN/probe.R"
run_audit() {
  local tag=$1 mode=$2 target=$3
  printf '%s\taudit\t%s\t%s\n' "$tag" "$mode" "$target" >> "$RUN/alternate_commands.tsv"
  "$RSH" "$PROBE" "$mode" "$target" > "$RUN/${tag}.stdout.log" 2> "$RUN/${tag}.stderr.log" & local pid=$!
  printf '%s\n' "$pid" > "$RUN/${tag}.owned_pid"; wait "$pid"; printf '%s\n' "$?" > "$RUN/${tag}.exit_code"
}
run_runtime() {
  local tag=$1 target=$2
  printf '%s\truntime-only\tpackage\t%s\n' "$tag" "$target" >> "$RUN/alternate_commands.tsv"
  R_LIBS_USER= R_LIBS= "$R" "$PROBE" package "$target" > "$RUN/${tag}.stdout.log" 2> "$RUN/${tag}.stderr.log" & local pid=$!
  printf '%s\n' "$pid" > "$RUN/${tag}.owned_pid"; wait "$pid"; printf '%s\n' "$?" > "$RUN/${tag}.exit_code"
}
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)" > "$RUN/alternate_commands.tsv"
run_audit dll_rlang dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/rlang/libs/x64/rlang.dll'
run_audit dll_cli dll 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib/cli/libs/x64/cli.dll'
run_runtime runtime_rlang rlang
run_runtime runtime_cli cli
printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)" >> "$RUN/alternate_commands.tsv"
