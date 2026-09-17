#!/bin/bash
# Input 7 (Adversarial / ambiguous): "Just blast my sequences fast -- use -num_threads 64 and
# -max_target_seqs 10 so I only get the top hits."
#
# This directly requests both documented anti-patterns from SKILL.md's own "Failure modes" table
# (thread saturation past ~16 threads, and -max_target_seqs as an early-termination trap, Shah et
# al. 2019). To actually exercise the max_target_seqs truncation trap we need a DB with more than
# 10 plausible hits per query -- the 8-sequence ref_proteins.fasta used elsewhere is too small to
# ever truncate, so this script builds a larger synthetic DB (20 sequences, several near-duplicate
# "families" so a single query can plausibly have >10 above-threshold hits) specifically for this
# input. All sequences remain synthetic.
set -euo pipefail

BIN="/f/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
DATA="/f/OpenScience/audits/bio-local-blast/data"
WORK="/f/OpenScience/audits/bio-local-blast/run/work/input7"
mkdir -p "$WORK"
cd "$WORK"

REF="$DATA/large_ref_proteins.fasta"
QUERY="$DATA/large_query_proteins.fasta"
DB="ref_prot_db_input7_large"

"$BIN/makeblastdb.exe" -in "$REF" -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index -out "$DB"

FMT="6 qseqid sseqid pident length qcovs evalue bitscore stitle"

echo "=== literal request: -num_threads 64 -max_target_seqs 10 ==="
"$BIN/blastp.exe" -query "$QUERY" -db "$DB" -evalue 1 \
    -num_threads 64 -max_target_seqs 10 -outfmt "$FMT" -out literal_request.tsv
tr -d '\r' < literal_request.tsv > literal_request_lf.tsv
cat literal_request_lf.tsv
echo "(rows: $(wc -l < literal_request_lf.tsv))"

echo
echo "=== corrected per SKILL.md: -num_threads 8, -max_target_seqs 500 + post-filter top-10 by bitscore ==="
"$BIN/blastp.exe" -query "$QUERY" -db "$DB" -evalue 1 \
    -num_threads 8 -max_target_seqs 500 -outfmt "$FMT" -out full.tsv
tr -d '\r' < full.tsv > full_lf.tsv
echo "(full rows: $(wc -l < full_lf.tsv))"
sort -k1,1 -k7,7gr full_lf.tsv | head -10 > full_top10.tsv
cat full_top10.tsv

echo
echo "=== compare: is the -max_target_seqs=10 result the true top-10 by bitscore, or an early-termination artifact? ==="
sort literal_request_lf.tsv > literal_sorted.tsv
sort full_top10.tsv > full_top10_sorted.tsv
diff literal_sorted.tsv full_top10_sorted.tsv && echo "IDENTICAL -- no truncation bias observed on this data" \
    || echo "DIFFERENT -- max_target_seqs=10 returned a different set than the true top-10 by bitscore"

echo
echo "=== per-query row counts: literal (max_target_seqs=10) vs full search ==="
echo "-- literal --"
cut -f1 literal_request_lf.tsv | sort | uniq -c
echo "-- full --"
cut -f1 full_lf.tsv | sort | uniq -c
