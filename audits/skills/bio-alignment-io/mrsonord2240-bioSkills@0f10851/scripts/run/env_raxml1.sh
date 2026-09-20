#!/bin/bash
# RAxML-NG 1.x (the '*' claim was written against 1.x era behaviour): private env
micromamba create -y -n aln-raxml1 -c conda-forge -c bioconda "raxml-ng=1.2.2" </dev/null 2>&1 | tail -2
micromamba run -n aln-raxml1 raxml-ng --version </dev/null 2>&1 | head -3
