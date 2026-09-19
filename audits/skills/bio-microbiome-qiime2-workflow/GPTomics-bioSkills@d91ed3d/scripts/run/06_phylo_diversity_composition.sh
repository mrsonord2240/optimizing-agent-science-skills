#!/bin/bash
set -euo pipefail
WS=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws
RUN=/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run
cd "$WS"

echo "=== Phylogeny (Pipeline): align-to-tree-mafft-fasttree ==="
time micromamba run -n qiime2-amplicon-2024.10 qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences rep-seqs.qza \
  --o-alignment aln.qza \
  --o-masked-alignment masked-aln.qza \
  --o-tree unrooted-tree.qza \
  --o-rooted-tree rooted-tree.qza
echo "phylogeny exit: $?"
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek rooted-tree.qza

echo ""
echo "=== Diversity (Pipeline): core-metrics-phylogenetic ==="
echo "feature-table summarize first to pick a real sampling depth (not the SKILL.md placeholder of 10000)"
micromamba run -n qiime2-amplicon-2024.10 qiime feature-table summarize \
  --i-table table.qza --o-visualization table.qzv --m-sample-metadata-file "$RUN/metadata_typed.tsv"
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path table.qza --output-path table_exported
micromamba run -n qiime2-amplicon-2024.10 biom summarize-table -i table_exported/feature-table.biom -o table_summary.txt
cat table_summary.txt

echo ""
echo "Using sampling depth 300 (below the min sample total observed) for a real core-metrics run"
time micromamba run -n qiime2-amplicon-2024.10 qiime diversity core-metrics-phylogenetic \
  --i-phylogeny rooted-tree.qza \
  --i-table table.qza \
  --p-sampling-depth 300 \
  --m-metadata-file "$RUN/metadata_typed.tsv" \
  --output-dir core-metrics
echo "core-metrics exit: $?"
ls -la core-metrics/

echo ""
echo "=== Differential abundance: qiime composition ancombc ==="
time micromamba run -n qiime2-amplicon-2024.10 qiime composition ancombc \
  --i-table table.qza \
  --m-metadata-file "$RUN/metadata_typed.tsv" \
  --p-formula 'group' \
  --o-differentials ancombc.qza
echo "ancombc exit: $?"
micromamba run -n qiime2-amplicon-2024.10 qiime tools peek ancombc.qza

echo ""
echo "=== da-barplot ==="
micromamba run -n qiime2-amplicon-2024.10 qiime composition da-barplot \
  --i-data ancombc.qza --o-visualization ancombc-barplot.qzv
echo "da-barplot exit: $?"
ls -la ancombc-barplot.qzv

echo ""
echo "=== Reproducibility check: re-run ancombc, compare exported differentials (T3 determinism) ==="
micromamba run -n qiime2-amplicon-2024.10 qiime composition ancombc \
  --i-table table.qza \
  --m-metadata-file "$RUN/metadata_typed.tsv" \
  --p-formula 'group' \
  --o-differentials ancombc_run2.qza
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path ancombc.qza --output-path ancombc_exp1
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path ancombc_run2.qza --output-path ancombc_exp2
diff ancombc_exp1/data.jsonl ancombc_exp2/data.jsonl && echo "IDENTICAL: ancombc is deterministic across 2 runs" || echo "DIFFERS: ancombc output changed between runs"
