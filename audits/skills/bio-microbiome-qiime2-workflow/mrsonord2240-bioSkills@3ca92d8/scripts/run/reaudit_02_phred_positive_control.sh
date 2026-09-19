#!/bin/bash
set -uo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws2
cd "$WS"

echo "=== Re-audit positive control: correct Phred33V2 import of the same data (should succeed) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --type "SampleData[PairedEndSequencesWithQuality]" \
  --input-path manifest.tsv \
  --input-format PairedEndFastqManifestPhred33V2 \
  --output-path demux_manifest_phred33.qza
echo "exit: $?"

echo "=== peek ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek demux_manifest_phred33.qza

echo "=== validate ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools validate demux_manifest_phred33.qza --level max
