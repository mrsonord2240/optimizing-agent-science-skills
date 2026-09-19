#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
FIX=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/casava_clean
mkdir -p "$WS"
cd "$WS"

echo "=== Casava import ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --type "SampleData[PairedEndSequencesWithQuality]" \
  --input-path "$FIX" \
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path demux_casava.qza
echo "import exit: $?"

echo "=== peek ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek demux_casava.qza

echo "=== validate ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools validate demux_casava.qza --level max

echo "=== demux summarize ==="
micromamba run -n qiime2-amplicon-2024.10 qiime demux summarize \
  --i-data demux_casava.qza --o-visualization demux_casava.qzv
echo "summarize exit: $?"

echo "=== ls ws ==="
ls -la "$WS"
