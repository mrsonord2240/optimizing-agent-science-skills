#!/bin/bash
# Regression of pre-fix Input 3 (the P0). Re-verify SKILL.md's REWRITTEN "Database format: v5 vs v4"
# claims: (a) v5 + -taxid_map alone is NOT sufficient for -taxids/-taxidlist; (b) it silently
# no-ops at exit 0; (c) fetching taxdb.tar.gz fixes it; (d) detect by row count, not exit code.
set -uo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input3 && cd input3
cp ../../../data/ref_proteins.fasta ../../../data/taxid_map.tsv ../../../data/taxid_query.fasta .

echo "=== Build v5 DB with -taxid_map (exactly as SKILL.md instructs) ==="
"$BIN/makeblastdb.exe" -in ref_proteins.fasta -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index -taxid_map taxid_map.tsv \
    -out taxid_db
"$BIN/blastdbcmd.exe" -db taxid_db -info

echo
echo "=== UNFILTERED search (baseline row count) ==="
"$BIN/blastp.exe" -query taxid_query.fasta -db taxid_db \
    -evalue 1e-10 -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -out unfiltered.tsv
echo "unfiltered.tsv:"; cat unfiltered.tsv
echo "unfiltered row count: $(wc -l < unfiltered.tsv)"

echo
echo "=== -taxidlist human_only.txt (9606) WITHOUT taxdb.tar.gz present ==="
echo 9606 > human_only.txt
rc=0
"$BIN/blastp.exe" -query taxid_query.fasta -db taxid_db \
    -taxidlist human_only.txt \
    -evalue 1e-10 -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -out filtered_no_taxdb.tsv 2>filtered_no_taxdb.stderr
rc=$?
echo "exit code: $rc"
echo "stderr:"; cat filtered_no_taxdb.stderr
echo "filtered_no_taxdb.tsv:"; cat filtered_no_taxdb.tsv
echo "filtered_no_taxdb row count: $(wc -l < filtered_no_taxdb.tsv)"

echo
echo "=== Fetch taxdb.tar.gz per SKILL.md's exact command ==="
curl -sS -O https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz
ls -la taxdb.tar.gz
tar -xzf taxdb.tar.gz
ls -la taxdb.bti taxdb.btd

echo
echo "=== -taxidlist human_only.txt (9606) WITH taxdb.tar.gz present ==="
"$BIN/blastp.exe" -query taxid_query.fasta -db taxid_db \
    -taxidlist human_only.txt \
    -evalue 1e-10 -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -out filtered_with_taxdb.tsv 2>filtered_with_taxdb.stderr
rc=$?
echo "exit code: $rc"
echo "stderr:"; cat filtered_with_taxdb.stderr
echo "filtered_with_taxdb.tsv:"; cat filtered_with_taxdb.tsv
echo "filtered_with_taxdb row count: $(wc -l < filtered_with_taxdb.tsv)"

echo
echo "=== taxonomy4blast.sqlite3 auto-fetched? ==="
ls -la taxonomy4blast.sqlite3 2>&1 || echo "not present in CWD"
find "F:/OpenScience/audit-envs/database-access" -iname "taxonomy4blast.sqlite3" 2>/dev/null
