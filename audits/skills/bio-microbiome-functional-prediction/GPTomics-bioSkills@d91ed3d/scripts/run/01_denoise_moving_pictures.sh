#!/bin/bash
# Denoise the real moving-pictures 16S dataset with QIIME2 (env qiime2-amplicon-2024.10)
# to get REAL ASVs + rep-seqs + feature table for a real functional-prediction input.
# Run via: MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '<this script>'
set -euo pipefail

BASE=/mnt/openscience/audit-envs/microbiome-metagenomics-analyst
SRC=$BASE/public-data/moving-pictures
WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
mkdir -p "$WORK"
cd "$WORK"

eval "$(micromamba shell hook --shell bash)"
micromamba activate qiime2-amplicon-2024.10

# EMPSingleEndDirFmt requires ONLY sequences.fastq.gz + barcodes.fastq.gz in the dir (no README.md)
mkdir -p import-src
cp "$SRC/sequences.fastq.gz" "$SRC/barcodes.fastq.gz" import-src/

# 1. Import still-multiplexed EMP single-end reads
qiime tools import \
  --type EMPSingleEndSequences \
  --input-path import-src \
  --output-path emp-single-end-sequences.qza

# 2. Demultiplex using the real barcode-sequence column in sample_metadata.tsv
qiime demux emp-single \
  --i-seqs emp-single-end-sequences.qza \
  --m-barcodes-file "$SRC/sample_metadata.tsv" \
  --m-barcodes-column barcode-sequence \
  --o-per-sample-sequences demux.qza \
  --o-error-correction-details demux-details.qza

qiime demux summarize \
  --i-data demux.qza \
  --o-visualization demux-summary.qzv

# 3. Denoise with DADA2 (single-end, truncate at 120 per the QIIME2 moving-pictures tutorial)
qiime dada2 denoise-single \
  --i-demultiplexed-seqs demux.qza \
  --p-trim-left 0 \
  --p-trunc-len 120 \
  --p-n-threads 4 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --o-denoising-stats denoising-stats.qza \
  --verbose

# 4. Export rep-seqs (FASTA) and feature table (BIOM -> TSV) for PICRUSt2
qiime tools export --input-path rep-seqs.qza --output-path exported-rep-seqs
qiime tools export --input-path table.qza --output-path exported-table
biom convert -i exported-table/feature-table.biom -o exported-table/feature-table.tsv --to-tsv

qiime feature-table summarize --i-table table.qza --o-visualization table-summary.qzv
qiime tools export --input-path denoising-stats.qza --output-path exported-stats

echo "DONE: rep-seqs at $WORK/exported-rep-seqs/dna-sequences.fasta"
echo "DONE: table at $WORK/exported-table/feature-table.tsv"
