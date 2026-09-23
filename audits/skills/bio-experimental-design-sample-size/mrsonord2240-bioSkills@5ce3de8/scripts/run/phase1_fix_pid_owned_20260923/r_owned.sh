#!/usr/bin/env bash
set -u
label="$1"
script="$2"
shift 2
root='/f/OpenScience/audits/bio-experimental-design-sample-size/run/phase1_fix_pid_owned_20260923'
logroot="$root/logs"
printf '%s\t%s\tSTART\tbash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$label" "$$" >> "$logroot/pids.tsv"
'/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh' "$script" "$@" > "$logroot/${label}.stdout.log" 2> "$logroot/${label}.stderr.log" &
rpid="$!"
printf '%s\t%s\tR_CHILD\tr_pid=%s parent_bash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$label" "$rpid" "$$" >> "$logroot/pids.tsv"
while kill -0 "$rpid" 2>/dev/null; do printf 'HEARTBEAT label=%s bash_pid=%s owned_r_pid=%s\n' "$label" "$$" "$rpid"; sleep 1; done
wait "$rpid"; rc="$?"
printf '%s\t%s\tEND\trc=%s\towned\tnatural_wait_only_no_external_intervention\n' "$(date -Iseconds)" "$label" "$rc" >> "$logroot/pids.tsv"
printf 'RESULT label=%s exit=%s\n' "$label" "$rc"
exit "$rc"
