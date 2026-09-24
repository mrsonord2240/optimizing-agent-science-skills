#!/usr/bin/env bash
# Retained final-tip rerun.  This script deliberately records the documented
# EDirect spelling rather than the legacy -rettype spelling from a pre-final runner.
set -u -o pipefail

runtime=/home/sci/sra-audit-20260923
audit_root=/mnt/openscience/audits/bio-sra-data
out="$audit_root/run/phase2_20260923/safety_final_tip/outputs"
private_home="$audit_root/private_runtime/home"

export HOME="$private_home"
export PATH="$runtime/bin:$PATH"
printf '%s\n' 'efetch -db sra -id 8 -format runinfo' >"$out/input7_edirect_format_runinfo.command.txt"
efetch -db sra -id 8 -format runinfo >"$out/input7_edirect_format_runinfo.stdout.txt" 2>"$out/input7_edirect_format_runinfo.stderr.txt"
status=$?
printf '%s\n' "$status" >"$out/input7_edirect_format_runinfo.exit.txt"
exit "$status"
