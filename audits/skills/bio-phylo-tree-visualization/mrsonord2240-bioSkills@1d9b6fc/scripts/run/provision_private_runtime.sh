#!/usr/bin/env bash
set -euo pipefail

micromamba create -y -n phylo-phase2 -c conda-forge -c bioconda \
  python=3.12 biopython matplotlib r-base=4.5 r-ape r-ggplot2 \
  bioconductor-ggtree bioconductor-treeio bioconductor-ggtreeextra
