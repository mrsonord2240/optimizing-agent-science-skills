#!/bin/bash
# Input 2 (Variant A): "I'm comparing a synthetic mouse cDNA panel against a synthetic human
# reference mRNA. Run cross-species homology search. Compare default megablast against
# -task dc-megablast so I can see why the skill recommends dc-megablast for cross-species."
set -euo pipefail

BIN="/f/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
DATA="/f/OpenScience/audits/bio-local-blast/data"
WORK="/f/OpenScience/audits/bio-local-blast/run/work/input2"
mkdir -p "$WORK"
cd "$WORK"

REF="$DATA/human_refseq_rna.fasta"
QUERY="$DATA/mouse_cdna.fasta"
DB="human_refseq_rna_db"

"$BIN/makeblastdb.exe" -in "$REF" -dbtype nucl \
    -blastdb_version 5 -parse_seqids -hash_index \
    -title "synthetic human refseq rna" -out "$DB"

FMT="6 qseqid sseqid pident length qcovs qcovhsp evalue bitscore"

echo "=== default megablast (word=28, exact-seed) ==="
"$BIN/blastn.exe" -query "$QUERY" -db "$DB" -task megablast \
    -evalue 1e-10 -outfmt "$FMT" -num_threads 8 -out megablast.tsv
cat megablast.tsv
echo "(rows: $(wc -l < megablast.tsv))"

echo
echo "=== dc-megablast (word=11, discontiguous seed) ==="
"$BIN/blastn.exe" -query "$QUERY" -db "$DB" -task dc-megablast -word_size 11 \
    -evalue 1e-10 -outfmt "$FMT" -num_threads 8 -out dc_megablast.tsv
cat dc_megablast.tsv
echo "(rows: $(wc -l < dc_megablast.tsv))"
