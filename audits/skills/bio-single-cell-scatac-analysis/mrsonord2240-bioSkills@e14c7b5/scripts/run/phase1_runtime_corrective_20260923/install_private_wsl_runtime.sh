#!/usr/bin/env bash
# Create the isolated Linux Signac/chromVAR runtime; never modifies the shared Windows environment.
set -euo pipefail

/home/sci/.local/bin/micromamba create -y -p /home/sci/scatac-private-20260923 \
  -c conda-forge -c bioconda \
  r-base=4.5 r-signac=1.17.1 r-seurat \
  bioconductor-chromvar bioconductor-motifmatchr bioconductor-jaspar2020 \
  bioconductor-tfbstools bioconductor-bsgenome.hsapiens.ucsc.hg38 \
  bioconductor-biocparallel > /mnt/openscience/audits/bio-single-cell-scatac-analysis/run/phase1_runtime_corrective_20260923/private_wsl_install.out 2>&1
