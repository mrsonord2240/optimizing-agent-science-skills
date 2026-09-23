#!/usr/bin/env bash
set -euo pipefail
micromamba create -y -n wikipathways-phase2 -c conda-forge -c bioconda \
  r-base=4.5 bioconductor-clusterprofiler bioconductor-rwikipathways \
  bioconductor-org.hs.eg.db bioconductor-enrichplot r-tidyr r-jsonlite
