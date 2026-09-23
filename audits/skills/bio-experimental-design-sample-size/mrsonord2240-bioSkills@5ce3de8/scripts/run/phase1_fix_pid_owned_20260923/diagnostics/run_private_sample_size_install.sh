#!/usr/bin/env bash
set -u
root='/mnt/openscience/audits/bio-experimental-design-sample-size/run/phase1_fix_pid_owned_20260923'
target='/mnt/openscience/audit-envs/crispr-screen-analyst/tools/sample-size-r443-r-lib'
logroot="$root/logs"
export MAMBA_ROOT_PREFIX='/home/sci/micromamba'
mamba='/home/sci/.local/bin/micromamba'
printf '%s\tprivate_install\tSTART\tbash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$$" >> "$logroot/pids.tsv"
"$mamba" run -n deseq2-repair-20260923 Rscript "$root/diagnostics/install_private_sample_size_lib.R" "$target" > "$logroot/private_install.stdout.log" 2> "$logroot/private_install.stderr.log" &
child="$!"
printf '%s\tprivate_install\tCHILD\tpid=%s parent_bash_pid=%s\towned\tno_external_intervention\n' "$(date -Iseconds)" "$child" "$$" >> "$logroot/pids.tsv"
while kill -0 "$child" 2>/dev/null; do echo "HEARTBEAT private_install bash_pid=$$ child_pid=$child"; sleep 5; done
wait "$child"; rc="$?"
printf '%s\tprivate_install\tEND\trc=%s\towned\tnatural_wait_only_no_external_intervention\n' "$(date -Iseconds)" "$rc" >> "$logroot/pids.tsv"
echo "RESULT private_install rc=$rc"
exit "$rc"
