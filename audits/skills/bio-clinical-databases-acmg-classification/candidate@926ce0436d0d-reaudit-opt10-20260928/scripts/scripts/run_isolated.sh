#!/usr/bin/env bash
set -euo pipefail

self=/mnt/openscience/audits/bio-clinical-databases-acmg-classification/reaudit-opt10-20260928/scripts/run_isolated.sh
audit_root=/mnt/openscience/audits/bio-clinical-databases-acmg-classification/reaudit-opt10-20260928
candidate=/mnt/openscience/wt/opt10-acmg-classification/skills/bio-clinical-databases-acmg-classification
python=/mnt/openscience/audit-envs/bio-clinical-databases-acmg-classification/conda-env-delta/bin/python

case "${1-}" in
  --inside)
    mount --make-rprivate /
    if mountpoint -q /mnt/f; then
      umount -l /mnt/f
    fi
    exec runuser -u sci -- env -u WSL_INTEROP \
      HOME=/home/sci USER=sci LOGNAME=sci \
      ACMG_REAUDIT_ROOT="$audit_root" ACMG_CANDIDATE="$candidate" \
      "$self" --run
    ;;
  --run)
    test "$(id -un)" = sci
    test -z "${WSL_INTEROP-}"
    if mountpoint -q /mnt/f; then
      echo "refusing to run: /mnt/f remains mounted" >&2
      exit 70
    fi
    mountpoint -q /mnt/openscience
    exec "$python" -B "$audit_root/scripts/run_reaudit.py"
    ;;
  *)
    exec sudo -n unshare --mount "$self" --inside
    ;;
esac
