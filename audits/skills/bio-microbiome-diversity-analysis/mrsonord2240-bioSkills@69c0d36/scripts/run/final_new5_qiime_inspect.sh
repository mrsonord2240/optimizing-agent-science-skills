#!/usr/bin/env bash
# Post-run assertions for the fresh final-pass QIIME2 execution; no source artifacts are changed.
set -euo pipefail
RUN_DIR=/mnt/openscience/audits/bio-microbiome-diversity-analysis/run/final_new5_qiime_moving_pictures_r2
QENV=qiime2-amplicon-2024.10
cd "$RUN_DIR"
for artifact in core-metrics-results/*.qza; do micromamba run -n "$QENV" qiime tools peek "$artifact"; done > artifact_peek.txt
find exported -type f -printf '%p %s bytes\n' | sort > exported_files.txt
test -s core-metrics-results/weighted_unifrac-permanova.qzv
test -s core-metrics-results/weighted_unifrac-permdisp.qzv
test -s core-metrics-results/unweighted_unifrac-permanova.qzv
test -s core-metrics-results/unweighted_unifrac-permdisp.qzv
test -s exported/weighted_unifrac/distance-matrix.tsv
test -s exported/unweighted_unifrac/distance-matrix.tsv
echo FINAL_NEW5_QIIME_ASSERTIONS_PASS
