#!/bin/bash
# Input 1 (Canonical): "Build a BLAST+ protein database from reference_proteins.fasta and search
# query_proteins.fasta against it, using -parse_seqids and -blastdb_version 5 so I can extract hit
# sequences later. Give me the top hit per query by bit-score."
# Follows SKILL.md "Build and search a custom protein database" pattern exactly.
set -euo pipefail

BIN="/f/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
DATA="/f/OpenScience/audits/bio-local-blast/data"
WORK="/f/OpenScience/audits/bio-local-blast/run/work/input1"
mkdir -p "$WORK"
cd "$WORK"

REF="$DATA/ref_proteins.fasta"
QUERY="$DATA/query_proteins.fasta"
DB="ref_prot_db"
OUT="hits.tsv"

"$BIN/makeblastdb.exe" -in "$REF" -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index \
    -title "synthetic ref proteins 2026-09-17" \
    -out "$DB"

"$BIN/blastp.exe" -query "$QUERY" -db "$DB" \
    -evalue 1e-10 \
    -num_threads 8 \
    -max_target_seqs 500 \
    -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" \
    -out "$OUT"

echo "=== raw hits ==="
cat "$OUT"

echo
echo "=== top hit per query by bit-score (col 7) ==="
sort -k1,1 -k7,7gr "$OUT" | awk -F'\t' '!seen[$1]++' > top_hit_per_query.tsv
cat top_hit_per_query.tsv

echo
echo "=== db info ==="
"$BIN/blastdbcmd.exe" -db "$DB" -info
