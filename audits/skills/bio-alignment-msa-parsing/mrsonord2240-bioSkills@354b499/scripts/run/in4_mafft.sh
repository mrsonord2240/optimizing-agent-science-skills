#!/bin/bash
# Align the 8 REAL UniProt globins with MAFFT (WSL env alignment) to give a REAL alignment with a PDB ground truth.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
mafft --version 2>&1 | head -1
mafft --localpair --maxiterate 1000 --quiet /mnt/openscience/audit-envs/alignment/public-data/msa/globins_uniprot.fasta < /dev/null > /mnt/openscience/audits/bio-alignment-msa-parsing/run/data/globins8_mafft_linsi.fasta
wc -c /mnt/openscience/audits/bio-alignment-msa-parsing/run/data/globins8_mafft_linsi.fasta
