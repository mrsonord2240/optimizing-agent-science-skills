#!/usr/bin/env bash
# Run in WSL science distro: MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '<this>'
# Sets up the real ASVs (moving-pictures, already denoised during tooling) and the real SILVA
# reference, then runs extract-reads (515F/806R) to build the region-matched reference.
set -euo pipefail
mkdir -p /home/sci/taxassign
cd /home/sci/taxassign
cp /mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/silva-138/silva-138-99-seqs.qza .
cp /mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/silva-138/silva-138-99-tax.qza .
cp /home/sci/rep-seqs.qza .      # real 770 V4 ASVs denoised from public moving-pictures dataset
cp /home/sci/table.qza .

micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier extract-reads \
    --i-sequences silva-138-99-seqs.qza \
    --p-f-primer GTGYCAGCMGCCGCGGTAA --p-r-primer GGACTACNVGGGTWTCTAAT \
    --p-min-length 50 --p-max-length 0 \
    --o-reads ref-seqs-515-806.qza
# Real run: ~28 minutes, single process (no --p-n-jobs in QIIME2 2024.10 for this step).
# Produced 432,916 region-matched sequences (from 436,680 full-length input).

micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path rep-seqs.qza --output-path rep-seqs-export
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path silva-138-99-seqs.qza --output-path silva-fulllength-export
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path silva-138-99-tax.qza --output-path tax-export
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path ref-seqs-515-806.qza --output-path regionmatched-export
