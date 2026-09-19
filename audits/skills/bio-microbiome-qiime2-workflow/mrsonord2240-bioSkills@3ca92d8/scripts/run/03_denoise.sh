#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
cd "$WS"

echo "=== DADA2 denoise-paired (SKILL.md's own example: trunc-len-f 0, trunc-len-r 0) ==="
time micromamba run -n qiime2-amplicon-2024.10 qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux_casava.qza \
  --p-trunc-len-f 0 --p-trunc-len-r 0 \
  --o-table table.qza \
  --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats stats.qza \
  --verbose
echo "denoise exit: $?"

echo "=== peek table.qza (expect FeatureTable[Frequency]) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek table.qza

echo "=== peek rep-seqs.qza (expect FeatureData[Sequence]) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek rep-seqs.qza

echo "=== validate table.qza ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools validate table.qza --level max
