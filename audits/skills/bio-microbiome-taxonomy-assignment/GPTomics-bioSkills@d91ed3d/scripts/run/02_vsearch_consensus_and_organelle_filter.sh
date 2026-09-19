#!/usr/bin/env bash
# Input 5: classify-consensus-vsearch directly against the full-length SILVA reference (SKILL's
# own documented command, no training step), then host-organelle filtering on the result.
set -euo pipefail
cd /home/sci/taxassign

micromamba run -n qiime2-amplicon-2024.10 qiime feature-classifier classify-consensus-vsearch \
    --i-query rep-seqs.qza \
    --i-reference-reads silva-138-99-seqs.qza \
    --i-reference-taxonomy silva-138-99-tax.qza \
    --p-maxaccepts 10 --p-perc-identity 0.8 --p-min-consensus 0.51 \
    --p-threads 16 \
    --o-classification taxonomy-vsearch.qza --o-search-results vsearch-hits.qza
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path taxonomy-vsearch.qza --output-path taxonomy-vsearch-export

# Real result: 699/770 (90.8%) genus-assigned; 29 ASVs classified as Mitochondria/Chloroplast.

micromamba run -n qiime2-amplicon-2024.10 qiime taxa filter-table --i-table table.qza --i-taxonomy taxonomy-vsearch.qza \
    --p-exclude mitochondria,chloroplast \
    --o-filtered-table table-no-organelle.qza

micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path table.qza --output-path table-export
micromamba run -n qiime2-amplicon-2024.10 qiime tools export --input-path table-no-organelle.qza --output-path table-no-organelle-export
micromamba run -n qiime2-amplicon-2024.10 biom summarize-table -i table-export/feature-table.biom -o table-summary.txt
micromamba run -n qiime2-amplicon-2024.10 biom summarize-table -i table-no-organelle-export/feature-table.biom -o table-no-organelle-summary.txt
# Real result: 770 -> 741 features (29 removed); 153807 -> 151500 reads (2307 removed, 1.5%).
