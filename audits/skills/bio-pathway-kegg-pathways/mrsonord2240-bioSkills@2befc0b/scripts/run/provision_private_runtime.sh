#!/usr/bin/env bash
set -euo pipefail

micromamba create -y -n kegg-phase2 -c conda-forge -c bioconda \
  r-base=4.5 bioconductor-clusterprofiler bioconductor-fgsea \
  bioconductor-spia bioconductor-graphite bioconductor-pathview r-gson
