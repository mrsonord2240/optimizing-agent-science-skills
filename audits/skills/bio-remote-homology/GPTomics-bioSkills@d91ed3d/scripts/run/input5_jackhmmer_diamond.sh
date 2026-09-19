#!/bin/bash
# Input 5 (Stress/multi-part) -- "large-scale metagenomic ORF search vs UniRef90-scale, cross-validate with jackhmmer"
# Reproduces SKILL.md's Failure Modes > "DIAMOND default mode lossy" + Decision Matrix scale guidance.
set -euo pipefail
WORK=/tmp/diamond_jack_test
rm -rf "$WORK"; mkdir -p "$WORK"; cd "$WORK"
cp /mnt/openscience/audit-envs/database-access/public-data/remote-homology/P17612.fasta query.fa
cp /mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta target.fa

echo "=== jackhmmer -N 3 (cross-validation method SKILL.md recommends) ==="
jackhmmer -N 3 --tblout jack.tbl --cpu 4 query.fa target.fa > jack.out 2>&1
grep -v '^#' jack.tbl | awk '{print $1, $5}' || echo "no hits"

echo
echo "=== DIAMOND default blastp (documented as lossy) ==="
diamond makedb --in target.fa -d targetdb --quiet
diamond blastp -d targetdb -q query.fa -o default.tsv --outfmt 6 qseqid sseqid pident evalue bitscore --quiet
echo "default hits: $(wc -l < default.tsv)"
cat default.tsv

echo
echo "=== DIAMOND --ultra-sensitive (SKILL.md's documented remedy for remote homology) ==="
diamond blastp -d targetdb -q query.fa -o ultra.tsv --ultra-sensitive -e 1e-5 --outfmt 6 qseqid sseqid pident evalue bitscore --quiet
echo "ultra-sensitive hits: $(wc -l < ultra.tsv)"
cat ultra.tsv
