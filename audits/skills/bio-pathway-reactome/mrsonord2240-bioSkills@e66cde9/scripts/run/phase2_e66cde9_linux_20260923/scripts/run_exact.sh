#!/usr/bin/env bash
set -u
label=$1; script=$2
root=/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923
log="$root/logs/$label.log"
printf 'runner_pid=%s start=%s script=%s\n' "$$" "$(date -Is)" "$script" > "$log"
micromamba run -n reactome-phase1-private Rscript "$script" >"$log.stdout" 2>"$log.stderr"
rc=$?
printf 'exit=%s end=%s\n' "$rc" "$(date -Is)" >> "$log"
exit "$rc"
