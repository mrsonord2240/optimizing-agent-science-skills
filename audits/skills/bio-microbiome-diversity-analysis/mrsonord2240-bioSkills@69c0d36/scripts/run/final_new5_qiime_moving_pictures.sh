#!/usr/bin/env bash
# Fresh final-pass QIIME2 execution of the Skill's core-metrics and mandatory
# weighted/unweighted PERMANOVA+PERMDISP branch on the public moving-pictures data.
set -euo pipefail

RUN_DIR=/mnt/openscience/audits/bio-microbiome-diversity-analysis/run/final_new5_qiime_moving_pictures_r2
DATA_DIR=/mnt/openscience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures
QENV=qiime2-amplicon-2024.10
mkdir -p "$RUN_DIR/emp-single-end-sequences" "$RUN_DIR/exported"
cp "$DATA_DIR/sequences.fastq.gz" "$RUN_DIR/emp-single-end-sequences/"
cp "$DATA_DIR/barcodes.fastq.gz" "$RUN_DIR/emp-single-end-sequences/"
cp "$DATA_DIR/sample_metadata.tsv" "$RUN_DIR/sample_metadata.tsv"
cd "$RUN_DIR"

q() { micromamba run -n "$QENV" qiime "$@"; }
q tools import --type EMPSingleEndSequences --input-path emp-single-end-sequences --output-path emp-single-end-sequences.qza
q demux emp-single --i-seqs emp-single-end-sequences.qza --m-barcodes-file sample_metadata.tsv --m-barcodes-column barcode-sequence --o-per-sample-sequences demux.qza --o-error-correction-details demux-details.qza
q dada2 denoise-single --i-demultiplexed-seqs demux.qza --p-trim-left 0 --p-trunc-len 120 --o-representative-sequences rep-seqs.qza --o-table table.qza --o-denoising-stats stats.qza --p-n-threads 4
q phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs.qza --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza
q diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table.qza --p-sampling-depth 1103 --m-metadata-file sample_metadata.tsv --output-dir core-metrics-results
for metric in weighted_unifrac unweighted_unifrac; do
  q diversity beta-group-significance --i-distance-matrix "core-metrics-results/${metric}_distance_matrix.qza" --m-metadata-file sample_metadata.tsv --m-metadata-column body-site --p-method permanova --p-pairwise --o-visualization "core-metrics-results/${metric}-permanova.qzv"
  q diversity beta-group-significance --i-distance-matrix "core-metrics-results/${metric}_distance_matrix.qza" --m-metadata-file sample_metadata.tsv --m-metadata-column body-site --p-method permdisp --o-visualization "core-metrics-results/${metric}-permdisp.qzv"
done
q tools export --input-path core-metrics-results/weighted_unifrac_distance_matrix.qza --output-path exported/weighted_unifrac
q tools export --input-path core-metrics-results/unweighted_unifrac_distance_matrix.qza --output-path exported/unweighted_unifrac
q tools export --input-path core-metrics-results/faith_pd_vector.qza --output-path exported/faith_pd
q tools export --input-path core-metrics-results/weighted_unifrac-permanova.qzv --output-path exported/weighted_unifrac_permanova
q tools export --input-path core-metrics-results/weighted_unifrac-permdisp.qzv --output-path exported/weighted_unifrac_permdisp
for artifact in core-metrics-results/*.qza; do q tools peek "$artifact"; done > artifact_peek.txt
find exported -type f -printf '%p %s bytes\n' | sort > exported_files.txt
echo FINAL_NEW5_QIIME_COMPLETE
