#!/usr/bin/env bash
set -u -o pipefail
RUN=/f/OpenScience/audits/bio-proteomics-ptm-analysis/run/windows_teardown_bisect_20260923_8f22f4a0
R=/f/OpenScience/runtime/envs/.r/lib/R/bin/Rscript.exe
PROBE="$RUN/probe.R"
RPATH="/f/OpenScience/runtime/envs/.r/Library/bin:/f/OpenScience/runtime/envs/.r/Library/mingw-w64/bin:$PATH"
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)" > "$RUN/runtime_only_commands.tsv"
for pkg in rlang cli; do
  tag="runtime_only_${pkg}"
  printf '%s\truntime-only\tpackage\t%s\n' "$tag" "$pkg" >> "$RUN/runtime_only_commands.tsv"
  R_LIBS_USER= R_LIBS= PATH="$RPATH" "$R" "$PROBE" package "$pkg" > "$RUN/${tag}.stdout.log" 2> "$RUN/${tag}.stderr.log" &
  pid=$!
  printf '%s\n' "$pid" > "$RUN/${tag}.owned_pid"
  wait "$pid"
  printf '%s\n' "$?" > "$RUN/${tag}.exit_code"
done
printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)" >> "$RUN/runtime_only_commands.tsv"
