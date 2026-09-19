#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
cd "$WS"

echo "=== replay-provenance on table.qza ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools replay-provenance \
  --in-fp table.qza --out-fp replay.sh --usage-driver cli
echo "replay exit: $?"
echo "--- replay.sh head ---"
head -60 replay.sh

echo ""
echo "=== replay-citations on table.qza ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools replay-citations \
  --in-fp table.qza --out-fp citations.bib
echo "citations exit: $?"
echo "--- citations.bib head ---"
head -30 citations.bib

echo ""
echo "=== export table.qza -> biom -> tsv (the one-way door) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools export \
  --input-path table.qza --output-path exported
echo "export exit: $?"
ls -la exported/
micromamba run -n qiime2-amplicon-2024.10 biom convert \
  -i exported/feature-table.biom -o exported/feature-table.tsv --to-tsv
echo "biom convert exit: $?"
head -5 exported/feature-table.tsv

echo ""
echo "=== confirm export DROPPED provenance (no provenance/ dir in exported/) ==="
find exported -maxdepth 2

echo ""
echo "=== confirm 'qiime tools extract' KEEPS provenance ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools extract \
  --input-path table.qza --output-path extracted
find extracted -maxdepth 3 -type d
