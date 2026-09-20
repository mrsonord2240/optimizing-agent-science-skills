#!/bin/bash
# New isolated WSL env for verifying downstream-tool claims (RAxML-NG '*' and PhyML 100-char claims). Does not touch `bio` or `alignment`.
micromamba create -y -n aln-treetools -c conda-forge -c bioconda raxml-ng phyml < /dev/null 2>&1 | tail -5
micromamba run -n aln-treetools raxml-ng --version </dev/null 2>&1 | head -5
micromamba run -n aln-treetools phyml --version </dev/null 2>&1 | head -3
# added: MrBayes to check Biopython NEXUS output loads (install is additive in this private env)
micromamba install -y -n aln-treetools -c conda-forge -c bioconda mrbayes < /dev/null 2>&1 | tail -3
micromamba run -n aln-treetools mb </dev/null 2>&1 | head -8
