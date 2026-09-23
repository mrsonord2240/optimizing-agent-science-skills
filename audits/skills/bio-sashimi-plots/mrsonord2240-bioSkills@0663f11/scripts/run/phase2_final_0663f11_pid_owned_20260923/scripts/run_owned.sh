#!/usr/bin/env bash
# Execute exactly one audit test in a child process owned by this runner.
set -euo pipefail
label=$1
script=$2
root=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
log="$root/logs/$label.log"
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
export PATH="$root/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
printf 'runner_pid=%s label=%s start=%s\n' "$$" "$label" "$(date -Is)" | tee "$log"
bash "$script" > >(tee -a "$log") 2> >(tee -a "$log" >&2) &
child=$!
printf 'owned_child_pid=%s\n' "$child" | tee -a "$log"
wait "$child"
rc=$?
printf 'owned_child_exit=%s end=%s\n' "$rc" "$(date -Is)" | tee -a "$log"
exit "$rc"
