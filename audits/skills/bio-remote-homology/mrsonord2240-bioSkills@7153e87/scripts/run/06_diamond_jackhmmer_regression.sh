#!/bin/bash
# Regression of original audit Input 5: DIAMOND default vs --ultra-sensitive, cross-validated
# against jackhmmer, on the same twilight-zone pair.
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"

echo "=== jackhmmer -N 3 (P17612 vs swissprot sample) ==="
jackhmmer -N 3 --tblout jackhmmer.tbl --cpu 4 P17612.fasta swissprot_sample.fasta > jackhmmer.txt
grep -v '^#' jackhmmer.tbl || echo "(no hits)"

echo
echo "=== DIAMOND makedb ==="
diamond makedb --in swissprot_sample.fasta -d swissprot_sample

echo
echo "=== DIAMOND default ==="
diamond blastp -d swissprot_sample -q P17612.fasta -o diamond_default.tsv \
        --outfmt 6 qseqid sseqid pident length qcovhsp evalue bitscore stitle
echo "hits:"; wc -l < diamond_default.tsv; cat diamond_default.tsv

echo
echo "=== DIAMOND --ultra-sensitive -e 1 ==="
diamond blastp -d swissprot_sample -q P17612.fasta -o diamond_ultra.tsv \
        --ultra-sensitive -e 1 \
        --outfmt 6 qseqid sseqid pident length qcovhsp evalue bitscore stitle
echo "hits:"; wc -l < diamond_ultra.tsv; cat diamond_ultra.tsv
