#!/usr/bin/env bash
# Fresh small QIIME2 fixture: runs the shipped region-matched example and the organelle filters.
set -euo pipefail
OUT='/mnt/openscience/audits/bio-microbiome-taxonomy-assignment/data/2026-09-23-final-pass/qiime2_pass'
SKILL='/mnt/openscience/wt/microbiome-taxonomy-assignment/microbiome/taxonomy-assignment'
mkdir -p "$OUT"
cd "$OUT"
cat > references.fasta <<'EOF'
>ref_a
GTGCCAGCAGCCGCGGTAAACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACATTAGATACCCCTGTAGTCC
>ref_b
GTGCCAGCAGCCGCGGTAATGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTATTAGATACCCCTGTAGTCC
>ref_c
GTGCCAGCAGCCGCGGTAAGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGATTAGATACCCCTGTAGTCC
EOF
printf '%b' 'ref_a\tk__Bacteria; p__Firmicutes; c__Bacilli; o__Lactobacillales; f__Lactobacillaceae; g__Lactobacillus\nref_b\tk__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Enterobacterales; f__Enterobacteriaceae; g__Escherichia\nref_c\tk__Bacteria; p__Actinobacteriota; c__Actinobacteria; o__Bifidobacteriales; f__Bifidobacteriaceae; g__Bifidobacterium\n' > references-taxonomy.tsv
cat > rep-seqs.fasta <<'EOF'
>asv_a
GTGCCAGCAGCCGCGGTAAACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACACATTAGATACCCCTGTAGTCC
>asv_b
GTGCCAGCAGCCGCGGTAATGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTATTAGATACCCCTGTAGTCC
>asv_c
GTGCCAGCAGCCGCGGTAAGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGATTAGATACCCCTGTAGTCC
EOF
qiime tools import --type 'FeatureData[Sequence]' --input-path references.fasta --output-path silva-138-99-seqs.qza
qiime tools import --type 'FeatureData[Taxonomy]' --input-path references-taxonomy.tsv --input-format HeaderlessTSVTaxonomyFormat --output-path silva-138-99-tax.qza
qiime tools import --type 'FeatureData[Sequence]' --input-path rep-seqs.fasta --output-path rep-seqs.qza
bash "$SKILL/examples/assign_qiime2_region.sh"
qiime tools peek taxonomy.qza
qiime tools export --input-path taxonomy.qza --output-path exported-taxonomy
test -s exported-taxonomy/taxonomy.tsv
printf '%b' '#OTU ID\tS1\tS2\nasv_a\t10\t0\nasv_b\t2\t8\nasv_c\t0\t4\n' > table.tsv
biom convert -i table.tsv -o feature-table.biom --table-type='OTU table' --to-hdf5
qiime tools import --type 'FeatureTable[Frequency]' --input-path feature-table.biom --input-format BIOMV210Format --output-path table.qza
printf '%b' 'asv_a\tk__Bacteria; p__Firmicutes; g__Lactobacillus\nasv_b\tk__Bacteria; p__Cyanobacteria; o__Chloroplast\nasv_c\tk__Bacteria; p__Proteobacteria; f__Mitochondria\n' > filter-taxonomy.tsv
qiime tools import --type 'FeatureData[Taxonomy]' --input-path filter-taxonomy.tsv --input-format HeaderlessTSVTaxonomyFormat --output-path filter-taxonomy.qza
qiime taxa filter-table --i-table table.qza --i-taxonomy filter-taxonomy.qza --p-exclude mitochondria,chloroplast --o-filtered-table table-no-organelle.qza
qiime taxa filter-seqs --i-data rep-seqs.qza --i-taxonomy filter-taxonomy.qza --p-exclude mitochondria,chloroplast --o-filtered-data rep-seqs-no-organelle.qza
qiime tools export --input-path table-no-organelle.qza --output-path exported-filtered-table
biom convert -i exported-filtered-table/feature-table.biom -o filtered-table.tsv --to-tsv
grep -q '^asv_a' filtered-table.tsv
! grep -q '^asv_b' filtered-table.tsv
! grep -q '^asv_c' filtered-table.tsv
echo 'QIIME2_END_TO_END_PASS: classifier, consensus and both organelle filters produced valid outputs; only asv_a retained.'
