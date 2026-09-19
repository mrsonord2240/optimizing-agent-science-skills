#!/usr/bin/env bash
# Input 1 (Canonical): QIIME2 classify-sklearn, region-matched via extract-reads -> fit-classifier-
# naive-bayes, on real 770 V4 ASVs denoised from the public moving-pictures dataset.
set -euo pipefail
cd /home/sci/taxassign

echo "=== Step 2: fit-classifier-naive-bayes on the region-matched (515-806) reference ==="
time micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier fit-classifier-naive-bayes \
    --i-reference-reads ref-seqs-515-806.qza \
    --i-reference-taxonomy silva-138-99-tax.qza \
    --o-classifier silva-138-99-515-806-nb-classifier.qza

echo "=== Step 3: classify-sklearn at default confidence 0.7 ==="
time micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier classify-sklearn \
    --i-classifier silva-138-99-515-806-nb-classifier.qza \
    --i-reads rep-seqs.qza \
    --p-confidence 0.7 --p-read-orientation auto --p-n-jobs 1 \
    --o-classification taxonomy-sklearn.qza

echo "=== Export ==="
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path taxonomy-sklearn.qza --output-path taxonomy-sklearn-export
wc -l taxonomy-sklearn-export/taxonomy.tsv
echo "done"
