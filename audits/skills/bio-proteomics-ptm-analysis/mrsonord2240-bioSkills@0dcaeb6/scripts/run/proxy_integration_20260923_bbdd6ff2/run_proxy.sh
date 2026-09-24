#!/usr/bin/env bash
set -euo pipefail
RUN=/mnt/openscience/audits/bio-proteomics-ptm-analysis/run/proxy_integration_20260923_bbdd6ff2
PREFIX=/mnt/openscience/audit-envs/mass-spec-proteomics-analyst/tools/quantification-r443-conda
SRC=/mnt/openscience/wt/proteomics-ptm-corrective/proteomics/ptm-analysis/scripts/msstatsptm_labelfree.R
printf 'started_utc=%s\n' "$(date -u +%FT%TZ)" > "$RUN/command.meta"
printf 'command=timeout --kill-after=10s 120s micromamba run -p %q Rscript %q dir=%q out=%q use_unmod=TRUE\n' "$PREFIX" "$SRC" "$RUN/fixture" "$RUN/out" >> "$RUN/command.meta"
sha256sum "$SRC" > "$RUN/source.sha256.before"
set +e
timeout --kill-after=10s 120s micromamba run -p "$PREFIX" Rscript "$SRC" "dir=$RUN/fixture" "out=$RUN/out" use_unmod=TRUE > "$RUN/stdout.log" 2> "$RUN/stderr.log" &
pid=$!
printf '%s\n' "$pid" > "$RUN/owned_pid"
wait "$pid"
status=$?
set -e
printf '%s\n' "$status" > "$RUN/exit_code"
printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)" >> "$RUN/command.meta"
sha256sum "$SRC" > "$RUN/source.sha256.after"
exit "$status"
