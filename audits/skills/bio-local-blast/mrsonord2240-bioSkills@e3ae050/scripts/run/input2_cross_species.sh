#!/bin/bash
# Regression of pre-fix Input 2 (Variant A, dc-megablast). Unaffected by the fix -- sanity check.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input2 && cd input2
cp ../../../data/human_refseq_rna.fasta ../../../data/mouse_cdna.fasta .

"$BIN/makeblastdb.exe" -in human_refseq_rna.fasta -dbtype nucl \
    -blastdb_version 5 -parse_seqids -out human_refseq_rna

echo "=== default megablast ==="
"$BIN/blastn.exe" -query mouse_cdna.fasta -db human_refseq_rna \
    -evalue 1e-10 -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
    -out default_megablast.tsv
cat default_megablast.tsv

echo "=== dc-megablast ==="
"$BIN/blastn.exe" -query mouse_cdna.fasta -db human_refseq_rna \
    -task dc-megablast -word_size 11 -evalue 1e-10 \
    -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
    -num_threads 8 -out dc_megablast.tsv
cat dc_megablast.tsv
