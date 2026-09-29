#!/usr/bin/env bash
set -euo pipefail

script=/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction/tools/wsl_isolated_exec.sh

case "${1-}" in
  --inside)
    shift
    cd /mnt/openscience
    mount --make-rprivate /
    if mountpoint -q /mnt/f; then
      umount -l /mnt/f
    fi
    exec runuser -u sci -- env -u WSL_INTEROP \
      HOME=/home/sci USER=sci LOGNAME=sci \
      "$script" --run "$@"
    ;;
  --run)
    shift
    test "$(id -un)" = sci
    test -z "${WSL_INTEROP-}"
    if mountpoint -q /mnt/f; then
      echo "refusing to run: /mnt/f remains mounted" >&2
      exit 70
    fi
    mountpoint -q /mnt/openscience
    exec "$@"
    ;;
  *)
    exec sudo -n unshare --mount "$script" --inside "$@"
    ;;
esac

