#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
cd "$WS"

python3 /mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/gen_manifest.py
echo "=== manifest.tsv ==="
cat manifest.tsv

echo "=== V2 manifest import ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --type "SampleData[PairedEndSequencesWithQuality]" \
  --input-path manifest.tsv \
  --input-format PairedEndFastqManifestPhred33V2 \
  --output-path demux_manifest.qza
echo "import exit: $?"

echo "=== peek manifest artifact ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek demux_manifest.qza

echo "=== validate ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools validate demux_manifest.qza --level max

echo "=== Try Phred64V2 on the SAME (actually Phred33) data - documents 'silently mis-decoded' claim ==="
set +e
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --type "SampleData[PairedEndSequencesWithQuality]" \
  --input-path manifest.tsv \
  --input-format PairedEndFastqManifestPhred64V2 \
  --output-path demux_manifest_phred64.qza
echo "phred64 import exit: $?"
set -e
