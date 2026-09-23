#!/usr/bin/env bash
# Corrective Phase 2 environment check for bio-differential-expression-deseq2-basics.
# Usage from WSL science: bash corrective_phase2_env.sh
set -euo pipefail

env_dir=/home/sci/micromamba/envs/deseq2-repair-20260923
lock_dir="$env_dir/auditlock"
if ! mkdir "$lock_dir"; then
  echo "Could not acquire isolated-environment audit lock: $lock_dir" >&2
  exit 1
fi
trap 'rmdir "$lock_dir"' EXIT

micromamba install -y -n deseq2-repair-20260923 -c conda-forge -c bioconda \
  r-ashr bioconductor-ihw bioconductor-tximport

micromamba run -n deseq2-repair-20260923 Rscript -e '
for (p in c("DESeq2", "apeglm", "ashr", "IHW", "tximport")) {
  cat(p, as.character(packageVersion(p)), "\n")
}
'
