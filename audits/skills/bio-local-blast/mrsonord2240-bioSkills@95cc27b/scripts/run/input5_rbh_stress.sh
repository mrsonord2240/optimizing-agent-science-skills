#!/bin/bash
# Regression of pre-fix Input 5 (RBH + extraction) -- now exercising the fixer's NEW 4-line
# chaining guidance verbatim: "rbh.tsv columns are (B_accession, A_accession)... cut -f1 -> B,
# cut -f2 -> A" and the two blastdbcmd -entry_batch calls against the matching DB.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input5 && cd input5
cp ../../../data/species_A.fasta ../../../data/species_B.fasta .

"$BIN/makeblastdb.exe" -in species_A.fasta -dbtype prot -blastdb_version 5 -parse_seqids -out A_db
"$BIN/makeblastdb.exe" -in species_B.fasta -dbtype prot -blastdb_version 5 -parse_seqids -out B_db

"$BIN/blastp.exe" -query species_A.fasta -db B_db -outfmt 6 -evalue 1e-5 \
    -num_threads 8 -max_target_seqs 5 -out A_vs_B.tsv
"$BIN/blastp.exe" -query species_B.fasta -db A_db -outfmt 6 -evalue 1e-5 \
    -num_threads 8 -max_target_seqs 5 -out B_vs_A.tsv

awk '!seen[$1]++ {print $1"\t"$2}' A_vs_B.tsv | sort > A_best
awk '!seen[$1]++ {print $1"\t"$2}' B_vs_A.tsv | sort > B_best
awk 'NR==FNR{a[$1]=$2; next} a[$2]==$1' A_best B_best > rbh.tsv

echo "=== rbh.tsv (col1 = B accession per SKILL.md's own stated mapping, col2 = A accession) ==="
cat rbh.tsv
echo "RBH pair count: $(wc -l < rbh.tsv)"

echo
echo "=== SKILL.md's added chaining instructions, run verbatim ==="
cut -f1 rbh.tsv | sort -u > rbh_B_accessions.txt
cut -f2 rbh.tsv | sort -u > rbh_A_accessions.txt
echo "-- rbh_B_accessions.txt --"; cat rbh_B_accessions.txt
echo "-- rbh_A_accessions.txt --"; cat rbh_A_accessions.txt

"$BIN/blastdbcmd.exe" -db B_db -entry_batch rbh_B_accessions.txt -out rbh_B_hits.fasta
"$BIN/blastdbcmd.exe" -db A_db -entry_batch rbh_A_accessions.txt -out rbh_A_hits.fasta

echo
echo "=== extraction results ==="
echo "rbh_B_hits.fasta headers ($(grep -c '^>' rbh_B_hits.fasta) of $(wc -l < rbh_B_accessions.txt) requested):"
grep '^>' rbh_B_hits.fasta
echo "rbh_A_hits.fasta headers ($(grep -c '^>' rbh_A_hits.fasta) of $(wc -l < rbh_A_accessions.txt) requested):"
grep '^>' rbh_A_hits.fasta

echo
echo "=== column-swap check: does col1 (claimed B accession) actually exist as an accession in B_db, not A_db? ==="
first_col1=$(head -1 rbh_B_accessions.txt)
echo "Testing $first_col1 against A_db (should FAIL / not found, proving col1 is genuinely a B accession):"
"$BIN/blastdbcmd.exe" -db A_db -entry "$first_col1" -out /dev/stdout 2>&1 || true
