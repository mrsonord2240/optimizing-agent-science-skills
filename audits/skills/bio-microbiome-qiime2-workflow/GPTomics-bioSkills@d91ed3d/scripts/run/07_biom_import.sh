#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
cd "$WS"

echo "=== BIOM import path: re-import the exported feature-table.biom as FeatureTable[Frequency] ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --input-path exported/feature-table.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV210Format \
  --output-path table_from_biom.qza
echo "biom import exit: $?"
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek table_from_biom.qza
micromamba run -n qiime2-amplicon-2024.10 qiime tools validate table_from_biom.qza --level max
