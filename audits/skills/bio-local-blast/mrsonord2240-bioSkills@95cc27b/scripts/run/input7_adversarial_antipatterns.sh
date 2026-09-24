#!/bin/bash
# Regression of pre-fix Input 7 (Adversarial). Fix added a Common-errors row: native -out files
# are CRLF on Windows, pipelines emit LF -- normalize with tr -d '\r'. Re-verify that claim and
# the num_threads/max_target_seqs anti-pattern behavior.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input7 && cd input7
cp ../../../data/large_ref_proteins.fasta ../../../data/large_query_proteins.fasta .

"$BIN/makeblastdb.exe" -in large_ref_proteins.fasta -dbtype prot \
    -blastdb_version 5 -parse_seqids -out large_ref_db

echo "=== literal request: -num_threads 64 -max_target_seqs 10 ==="
"$BIN/blastp.exe" -query large_query_proteins.fasta -db large_ref_db \
    -num_threads 64 -max_target_seqs 10 -evalue 1e-5 \
    -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
    -out literal_request.tsv
echo "rows: $(wc -l < literal_request.tsv)"

echo
echo "=== corrected: -num_threads 8 -max_target_seqs 500, post-filter top 10 ==="
"$BIN/blastp.exe" -query large_query_proteins.fasta -db large_ref_db \
    -num_threads 8 -max_target_seqs 500 -evalue 1e-5 \
    -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
    -out full_search.tsv
echo "total hits: $(wc -l < full_search.tsv)"
sort -k7,7gr full_search.tsv | head -10 > top10.tsv

echo
echo "=== CRLF check on the raw native -out file (per SKILL.md's new Common-errors row) ==="
python -c "
data = open('literal_request.tsv', 'rb').read()
lines = data.split(b'\n')
crlf = sum(1 for l in lines if l.endswith(b'\r'))
total_nonempty = sum(1 for l in lines if l.strip(b'\r'))
print(f'CRLF-terminated lines: {crlf} / {total_nonempty} non-empty lines')
"
file literal_request.tsv 2>/dev/null || true

echo
echo "=== Diffing raw CRLF -out file against LF-emitting pipeline output WITHOUT normalizing ==="
diff literal_request.tsv top10.tsv > raw_diff.txt; echo "diff exit code (nonzero if 'different'): $?"
wc -l raw_diff.txt

echo
echo "=== Now normalized per SKILL.md's fix: tr -d '\r' before diffing ==="
tr -d '\r' < literal_request.tsv > literal_request_lf.tsv
tr -d '\r' < top10.tsv > top10_lf.tsv
diff literal_request_lf.tsv top10_lf.tsv > norm_diff.txt; echo "normalized diff exit code: $?"
cat norm_diff.txt
