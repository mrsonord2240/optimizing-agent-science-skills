#!/usr/bin/env bash
set -euo pipefail
for pkg in bioconductor-ssizerna bioconductor-proper bioconductor-deseq2 r-pwr; do
  echo "### ${pkg}"
  micromamba repoquery search -c conda-forge -c bioconda "${pkg}" | head -n 8
done
