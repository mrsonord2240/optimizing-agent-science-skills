#!/usr/bin/env bash
set -e
WD=/home/sci/audit_bio_microbiome_diversity_analysis_20260919
rm -rf "$WD" && mkdir -p "$WD" && cd "$WD"
micromamba activate qiime2-amplicon-2024.10
mkdir emp-single-end-sequences
cp /mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sequences.fastq.gz emp-single-end-sequences/
cp /mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/barcodes.fastq.gz emp-single-end-sequences/
cp /mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sample_metadata.tsv .
echo IMPORT_START
qiime tools import --type EMPSingleEndSequences --input-path emp-single-end-sequences --output-path emp-single-end-sequences.qza
echo DEMUX_START
qiime demux emp-single --i-seqs emp-single-end-sequences.qza --m-barcodes-file sample_metadata.tsv --m-barcodes-column barcode-sequence --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza
echo DADA2_START
qiime dada2 denoise-single --i-demultiplexed-seqs demux.qza --p-trim-left 0 --p-trunc-len 120 --o-representative-sequences rep-seqs.qza --o-table table.qza --o-denoising-stats stats.qza --p-n-threads 4
echo TREE_START
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs.qza --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza
echo COREMETRICS_START
qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza --p-sampling-depth 1103 --m-metadata-file sample_metadata.tsv --output-dir core-metrics-results
echo BETASIG_START
for METRIC in weighted_unifrac unweighted_unifrac bray_curtis; do
  qiime diversity beta-group-significance --i-distance-matrix core-metrics-results/${METRIC}_distance_matrix.qza --m-metadata-file sample_metadata.tsv --m-metadata-column body-site --p-method permanova --p-pairwise --o-visualization core-metrics-results/${METRIC}-permanova.qzv
  qiime diversity beta-group-significance --i-distance-matrix core-metrics-results/${METRIC}_distance_matrix.qza --m-metadata-file sample_metadata.tsv --m-metadata-column body-site --p-method permdisp --o-visualization core-metrics-results/${METRIC}-permdisp.qzv
done
echo EXPORT_START
mkdir -p exported
for METRIC in weighted_unifrac unweighted_unifrac bray_curtis; do
  qiime tools export --input-path core-metrics-results/${METRIC}_distance_matrix.qza --output-path exported/${METRIC}
done
for VEC in faith_pd observed_features shannon evenness; do
  qiime tools export --input-path core-metrics-results/${VEC}_vector.qza --output-path exported/${VEC}
done
qiime tools export --input-path core-metrics-results/weighted_unifrac-permanova.qzv --output-path exported/wu_permanova_viz
qiime tools export --input-path core-metrics-results/unweighted_unifrac-permanova.qzv --output-path exported/uwu_permanova_viz
qiime tools export --input-path core-metrics-results/bray_curtis-permanova.qzv --output-path exported/bc_permanova_viz
qiime tools export --input-path core-metrics-results/weighted_unifrac-permdisp.qzv --output-path exported/wu_permdisp_viz
qiime tools export --input-path core-metrics-results/unweighted_unifrac-permdisp.qzv --output-path exported/uwu_permdisp_viz
qiime tools export --input-path core-metrics-results/bray_curtis-permdisp.qzv --output-path exported/bc_permdisp_viz
echo ALL_DONE
