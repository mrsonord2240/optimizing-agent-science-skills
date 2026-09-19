#!/bin/bash
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
RUN=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run
cd "$WS"

echo "=== TEST A: semantic-type mismatch (FeatureData[Sequence] where FeatureTable[Frequency] expected) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime feature-table summarize \
  --i-table rep-seqs.qza --o-visualization bad_summary.qzv
echo "TEST A exit: $?"

echo ""
echo "=== TEST B: feed a .qzv (Visualization) where an Artifact input (.qza) is expected ==="
micromamba run -n qiime2-amplicon-2024.10 qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux_casava.qzv \
  --p-trunc-len-f 0 --p-trunc-len-r 0 \
  --o-table bad_table.qza \
  --o-representative-sequences bad_rep.qza \
  --o-denoising-stats bad_stats.qza
echo "TEST B exit: $?"

echo ""
echo "=== TEST C: metadata numeric-cast - subject column WITHOUT #q2:types row ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools inspect-metadata "$RUN/metadata.tsv"
echo "TEST C exit: $?"

echo ""
echo "=== TEST D: metadata WITH #q2:types row annotating subject categorical ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools inspect-metadata "$RUN/metadata_typed.tsv"
echo "TEST D exit: $?"

echo ""
echo "=== TEST E: try using the untyped metadata's 'subject' column as a --p-formula-style categorical grouping column in taxa barplot style action (feature-table group) to see practical effect ==="
micromamba run -n qiime2-amplicon-2024.10 qiime metadata tabulate \
  --m-input-file "$RUN/metadata.tsv" --o-visualization metadata_untyped.qzv
echo "TEST E exit: $?"
