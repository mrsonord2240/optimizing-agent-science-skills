#!/usr/bin/env bash
# Dry-run an isolated Linux Signac/chromVAR environment for the post-output Windows R crash.
set -euo pipefail

/home/sci/.local/bin/micromamba create --dry-run -y -p /home/sci/scatac-private-20260923 \
  -c conda-forge -c bioconda \
  r-base=4.5 r-signac=1.17.1 r-seurat \
  bioconductor-chromvar bioconductor-motifmatchr bioconductor-jaspar2020 \
  bioconductor-tfbstools bioconductor-bsgenome.hsapiens.ucsc.hg38 \
  bioconductor-biocparallel > /mnt/openscience/audits/bio-single-cell-scatac-analysis/run/phase1_runtime_corrective_20260923/private_wsl_dry_run.out 2>&1
