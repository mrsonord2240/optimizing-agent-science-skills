#!/bin/bash
# Do the package names on the SKILL "Install" lines exist on bioconda/conda-forge? (search only, nothing installed) + dry-run of the one-line conda install
for p in flair isoquant minimap2 samtools bedtools gffread sqanti3 rmats-long ultra_bioinformatics pbskera lima isoseq; do
  n=$(micromamba search -c conda-forge -c bioconda "$p" 2>/dev/null | grep -c -E "^\s*$p\s" ); echo "$p: $(micromamba search -c conda-forge -c bioconda "$p" 2>&1 | tail -3 | head -1 | cut -c1-110)"; done
echo "##### dry-run of the SKILL one-line install (flair isoquant minimap2 samtools bedtools gffread)"
micromamba create -n as-dryrun --dry-run -y -c conda-forge -c bioconda flair isoquant minimap2 samtools bedtools gffread 2>&1 | tail -4 | cut -c1-200
