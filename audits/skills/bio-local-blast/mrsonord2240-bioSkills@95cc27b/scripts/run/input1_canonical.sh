#!/bin/bash
# Regression of pre-fix Input 1 (Canonical). Unaffected by the fix -- sanity check only.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input1 && cd input1
cp ../../../data/ref_proteins.fasta ../../../data/query_proteins.fasta .

"$BIN/makeblastdb.exe" -in ref_proteins.fasta -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index \
    -title "ref_proteins" -out ref_prot_db

"$BIN/blastp.exe" -query query_proteins.fasta -db ref_prot_db \
    -evalue 1e-10 -num_threads 8 -max_target_seqs 500 \
    -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" \
    -out hits.tsv

echo "=== hits.tsv ==="
cat hits.tsv
echo "=== db info ==="
"$BIN/blastdbcmd.exe" -db ref_prot_db -info

sort -k1,1 -k7,7gr hits.tsv | awk '!seen[$1]++' > top_hit_per_query.tsv
echo "=== top_hit_per_query.tsv ==="
cat top_hit_per_query.tsv
