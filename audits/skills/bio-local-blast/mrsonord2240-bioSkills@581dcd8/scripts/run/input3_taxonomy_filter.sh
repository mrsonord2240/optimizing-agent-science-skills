#!/bin/bash
# Input 3 (Variant B): "Build a v5 protein DB with per-sequence taxids (-taxid_map) and run a
# taxonomy-filtered blastp restricted to the human taxid (9606) using -taxids, so fly-tagged
# sequences are excluded even if they'd otherwise be a hit."
set -euo pipefail

BIN="/f/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
DATA="/f/OpenScience/audits/bio-local-blast/data"
WORK="/f/OpenScience/audits/bio-local-blast/run/work/input3"
mkdir -p "$WORK"
cd "$WORK"

REF="$DATA/ref_proteins.fasta"
QUERY="$DATA/taxid_query.fasta"
DB="taxid_db"

"$BIN/makeblastdb.exe" -in "$REF" -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index \
    -taxid_map "$DATA/taxid_map.tsv" \
    -title "synthetic taxid-tagged proteins" -out "$DB"

echo "=== db -info (confirms v5 + taxonomy) ==="
"$BIN/blastdbcmd.exe" -db "$DB" -info

echo
echo "=== unfiltered search (both TQ_HUMANLIKE and TQ_FLYLIKE queries) ==="
"$BIN/blastp.exe" -query "$QUERY" -db "$DB" \
    -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -evalue 1e-5 -out unfiltered.tsv
cat unfiltered.tsv

echo
echo "=== filtered: -taxids 9606,10090 (human+mouse only) ==="
"$BIN/blastp.exe" -query "$QUERY" -db "$DB" \
    -taxids 9606,10090 \
    -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -evalue 1e-5 -out filtered_taxids.tsv
cat filtered_taxids.tsv
echo "(rows: $(wc -l < filtered_taxids.tsv))"

echo
echo "=== filtered: -taxidlist (human only, 9606) ==="
echo 9606 > human_only.txt
"$BIN/blastp.exe" -query "$QUERY" -db "$DB" -taxidlist human_only.txt \
    -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -evalue 1e-5 -out filtered_taxidlist.tsv
cat filtered_taxidlist.tsv
echo "(rows: $(wc -l < filtered_taxidlist.tsv))"
