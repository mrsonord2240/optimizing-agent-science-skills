#!/usr/bin/env bash
set -u

printf 'login_path=%s\n' "$PATH"
for tool in bcftools vcftools python3; do
  printf 'login_%s=' "$tool"
  command -v "$tool" || true
done
printf '%s\n' 'existing_vcftools_candidates:'
find /home/sci/micromamba/envs -maxdepth 4 -type f -name vcftools -print 2>/dev/null || true
for candidate in /home/sci/micromamba/envs/atac-core/bin/vcftools /home/sci/micromamba/envs/atac-jvm/bin/vcftools; do
  if test -x "$candidate"; then
    "$candidate" --version || true
  fi
done
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
for tool in bcftools vcftools python3; do
  printf 'alignment_%s=' "$tool"
  command -v "$tool" || true
done
