#!/bin/bash
# Runtime state: env list, live env fingerprints (same recipe as TOOLS.md), GPU, host load, mount/interop boundary.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
L=/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/logs
micromamba env list
for n in bio-atac-seq-footprinting bio-atac-seq-footprinting-rgt bio-atac-seq-footprinting-pydnase bio-atac-seq-footprinting-scprinter; do
  micromamba list -n $n --explicit --md5 > $L/env_explicit_$n.txt 2>&1
  micromamba run -n $n pip freeze > $L/pipfreeze_$n.txt 2>&1
  echo "$n $(cat $L/env_explicit_$n.txt $L/pipfreeze_$n.txt | sha256sum | cut -c1-16)"
done
nvidia-smi --query-gpu=name,memory.used,memory.total,driver_version --format=csv
uptime; free -g | head -2; nproc
mount | grep -c /mnt/ ; ls /mnt; cat /proc/sys/fs/binfmt_misc/WSLInterop 2>&1 | head -1
