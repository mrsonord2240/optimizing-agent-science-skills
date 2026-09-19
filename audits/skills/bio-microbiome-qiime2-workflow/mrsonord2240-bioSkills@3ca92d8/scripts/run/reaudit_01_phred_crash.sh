#!/bin/bash
set -uo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws2
cd "$WS"

python3 /mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/gen_manifest.py
cp /mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws/manifest.tsv "$WS/manifest.tsv"
echo "=== manifest.tsv ==="
cat manifest.tsv

echo "=== Re-audit: Phred64V2 import of actually-Phred33 data (regression test of fixed wording) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
  --type "SampleData[PairedEndSequencesWithQuality]" \
  --input-path manifest.tsv \
  --input-format PairedEndFastqManifestPhred64V2 \
  --output-path demux_manifest_phred64.qza
echo "phred64 import exit: $?"
