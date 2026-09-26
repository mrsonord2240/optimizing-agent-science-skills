#!/usr/bin/env bash
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925
LOCK="$ROOT/data/input2_wsl_install.lock"
mkdir "$LOCK"
trap 'rmdir "$LOCK"' EXIT
echo "BIO_ENV_SNAPSHOT_BEGIN"
micromamba list -n bio
echo "BIO_ENV_SNAPSHOT_END"
if ! micromamba env list | grep -qE '^[[:space:]]*cellann-reaudit-2dee47f[[:space:]]'; then
  micromamba create -y -n cellann-reaudit-2dee47f --strict-channel-priority \
    -c conda-forge -c bioconda \
    r-base=4.4 bioconductor-singler bioconductor-celldex \
    bioconductor-singlecellexperiment bioconductor-scuttle r-matrix
fi
micromamba run -n cellann-reaudit-2dee47f Rscript -e \
  "cat('R=',R.version.string,'\n'); cat('SingleR=',as.character(packageVersion('SingleR')),'\n'); cat('celldex=',as.character(packageVersion('celldex')),'\n'); cat('SingleCellExperiment=',as.character(packageVersion('SingleCellExperiment')),'\n'); cat('scuttle=',as.character(packageVersion('scuttle')),'\n')"
