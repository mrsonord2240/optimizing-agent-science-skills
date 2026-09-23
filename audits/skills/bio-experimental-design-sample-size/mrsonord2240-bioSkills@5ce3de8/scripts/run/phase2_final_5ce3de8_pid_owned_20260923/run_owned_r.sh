#!/usr/bin/env bash
set -u
label="$1"
script="$2"
shift 2
root='/mnt/openscience/audits/bio-experimental-design-sample-size/run/phase2_final_5ce3de8_pid_owned_20260923'
private_lib='/mnt/openscience/audit-envs/crispr-screen-analyst/tools/sample-size-r443-r-lib'
logroot="$root/logs"
export MAMBA_ROOT_PREFIX='/home/sci/micromamba'
export R_LIBS_USER="$private_lib"
mamba='/home/sci/.local/bin/micromamba'
cd "$root"
printf '%s\t%s\tSTART\tbash_pid=%s\towned\tprivate_r443_fresh_phase2\n' "$(date -Iseconds)" "$label" "$$" >> "$logroot/pids.tsv"
"$mamba" run -n deseq2-repair-20260923 Rscript "$script" "$@" > "$logroot/$label.stdout.log" 2> "$logroot/$label.stderr.log" &
child="$!"
printf '%s\t%s\tCHILD\tpid=%s parent_bash_pid=%s\towned\tprivate_r443_fresh_phase2\n' "$(date -Iseconds)" "$label" "$child" "$$" >> "$logroot/pids.tsv"
while kill -0 "$child" 2>/dev/null; do echo "HEARTBEAT $label bash_pid=$$ child_pid=$child"; sleep 5; done
wait "$child"; rc="$?"
printf '%s\t%s\tEND\trc=%s\towned\tnatural_wait_only_no_external_intervention\n' "$(date -Iseconds)" "$label" "$rc" >> "$logroot/pids.tsv"
echo "RESULT $label rc=$rc"
exit "$rc"
