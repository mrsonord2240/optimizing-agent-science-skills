#!/usr/bin/env bash
set -euo pipefail
root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928
bash "$root/scripts/environment_check.sh" >"$root/evidence/environment-live-verification.txt" 2>"$root/evidence/environment-live-verification.stderr"
