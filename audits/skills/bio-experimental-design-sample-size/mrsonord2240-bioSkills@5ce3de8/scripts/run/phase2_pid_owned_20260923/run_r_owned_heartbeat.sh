#!/usr/bin/env bash
# Foreground audit runner. It records its own Bash/R process tree, waits naturally,
# and never signals or enumerates any process outside that tree.
set -u
label="$1"
script="$2"
shift 2
root='/f/OpenScience/audits/bio-experimental-design-sample-size/run/phase2_pid_owned_20260923'
logroot="$root/logs"
printf '%s\t%s\tSTART\tbash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$label" "$$" >> "$logroot/pid_ownership_heartbeat.tsv"
'/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh' "$script" "$@" > "$logroot/${label}.stdout.log" 2> "$logroot/${label}.stderr.log" &
rpid="$!"
printf '%s\t%s\tR_CHILD\tr_pid=%s parent_bash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$label" "$rpid" "$$" >> "$logroot/pid_ownership_heartbeat.tsv"
while kill -0 "$rpid" 2>/dev/null; do
  printf 'HEARTBEAT label=%s bash_pid=%s owned_r_pid=%s\n' "$label" "$$" "$rpid"
  sleep 1
done
wait "$rpid"
rc="$?"
printf '%s\t%s\tEND\trc=%s\towned\tnatural_wait_only_no_external_intervention\n' "$(date -Iseconds)" "$label" "$rc" >> "$logroot/pid_ownership_heartbeat.tsv"
printf 'RESULT label=%s bash_pid=%s owned_r_pid=%s exit=%s\n' "$label" "$$" "$rpid" "$rc"
exit "$rc"
