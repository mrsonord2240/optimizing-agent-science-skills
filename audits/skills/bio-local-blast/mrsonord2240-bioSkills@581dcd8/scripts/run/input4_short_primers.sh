#!/bin/bash
# Input 4 (Edge): "I have 20nt-ish primers to check against my synthetic human reference. They're
# too short for default megablast. Use -task blastn-short."
set -euo pipefail

BIN="/f/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
DATA="/f/OpenScience/audits/bio-local-blast/data"
WORK="/f/OpenScience/audits/bio-local-blast/run/work/input4"
mkdir -p "$WORK"
cd "$WORK"

REF="$DATA/human_refseq_rna.fasta"
QUERY="$DATA/primers.fasta"
DB="genome_db"

"$BIN/makeblastdb.exe" -in "$REF" -dbtype nucl \
    -blastdb_version 5 -parse_seqids -hash_index -out "$DB"

echo "=== default megablast on short primers (expected to fail/miss short queries) ==="
set +e
"$BIN/blastn.exe" -query "$QUERY" -db "$DB" -task megablast \
    -evalue 1000 -outfmt 6 -out default_megablast.tsv 2>default_megablast.err
echo "exit=$?"
set -e
cat default_megablast.tsv 2>/dev/null || echo "(no output file / empty)"
echo "--- stderr ---"
cat default_megablast.err

echo
echo "=== -task blastn-short, word_size 7 ==="
"$BIN/blastn.exe" -query "$QUERY" -db "$DB" -task blastn-short -word_size 7 \
    -evalue 1000 -outfmt 6 -out short_hits.tsv
cat short_hits.tsv
echo "(rows: $(wc -l < short_hits.tsv))"
