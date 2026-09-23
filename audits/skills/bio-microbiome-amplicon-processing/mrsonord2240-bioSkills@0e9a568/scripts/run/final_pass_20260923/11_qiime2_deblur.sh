#!/usr/bin/env bash
set -euo pipefail
base='/mnt/openscience/audits/bio-microbiome-amplicon-processing/work/final_pass_20260923/qiime2_deblur_real2'
source_demux='/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws/demux_manifest.qza'
mkdir -p "$base"
cp "$source_demux" "$base/demux.qza"
micromamba run -n qiime2-amplicon-2024.10 qiime deblur denoise-16S --i-demultiplexed-seqs "$base/demux.qza" --p-trim-length 100 --p-sample-stats --o-representative-sequences "$base/rep-seqs.qza" --o-table "$base/table.qza" --o-stats "$base/stats.qza"
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek "$base/table.qza" > "$base/table.peek.txt"
grep -q 'FeatureTable\[Frequency\]' "$base/table.peek.txt"
test -s "$base/rep-seqs.qza" && test -s "$base/stats.qza"
echo 'QIIME2_DEBLUR_PASS table_repseqs_stats_present=true'
