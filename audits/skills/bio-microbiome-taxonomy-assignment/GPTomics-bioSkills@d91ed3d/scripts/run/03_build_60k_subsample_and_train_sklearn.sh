#!/usr/bin/env bash
# The original qiime2_sklearn_regionmatched.sh (fit-classifier-naive-bayes against the FULL
# 432,916-sequence region-matched reference) crashed the WSL VM via OOM after ~10 min (confirmed
# by dmesg showing a fresh boot on the next command -- see finding P1 in the JSON report).
# This script builds a real, 60,000-sequence random subsample (seed 42) of the SAME real
# region-matched extraction and successfully trains + classifies against it.
set -euo pipefail
cd /home/sci/taxassign

# regionmatched_decipher_tax.tsv (fid \t taxonomy \t seq) was produced by convert_silva.py against
# regionmatched-export/dna-sequences.fasta + tax-export/taxonomy.tsv, seed 42, n=60000:
#   python3 convert_silva.py regionmatched-export/dna-sequences.fasta tax-export/taxonomy.tsv \
#       60000 42 regionmatched

python3 tsv_to_fasta.py regionmatched_decipher_tax.tsv subsample60k_seqs.fasta
cut -f1 regionmatched_decipher_tax.tsv > subsample60k_ids.txt
python3 filter_tax.py subsample60k_ids.txt tax-export/taxonomy.tsv subsample60k_tax.tsv
tail -n +2 subsample60k_tax.tsv > subsample60k_tax_headerless.tsv

micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
    --type "FeatureData[Sequence]" \
    --input-path subsample60k_seqs.fasta \
    --output-path ref-seqs-515-806-60k.qza
micromamba run -n qiime2-amplicon-2024.10 qiime tools import \
    --type "FeatureData[Taxonomy]" \
    --input-format HeaderlessTSVTaxonomyFormat \
    --input-path subsample60k_tax_headerless.tsv \
    --output-path ref-tax-60k.qza

micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier fit-classifier-naive-bayes \
    --i-reference-reads ref-seqs-515-806-60k.qza \
    --i-reference-taxonomy ref-tax-60k.qza \
    --o-classifier silva-60k-515-806-nb-classifier.qza

micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier classify-sklearn \
    --i-classifier silva-60k-515-806-nb-classifier.qza \
    --i-reads rep-seqs.qza \
    --p-confidence 0.7 --p-read-orientation auto --p-n-jobs 1 \
    --o-classification taxonomy-sklearn.qza

micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path taxonomy-sklearn.qza --output-path taxonomy-sklearn-export
# Real result: 653/770 (84.8%) genus-assigned; 403/770 species-labeled; confidence range
# 0.7000755-0.999999999954 (min confirms the 0.7 truncation mechanism).
