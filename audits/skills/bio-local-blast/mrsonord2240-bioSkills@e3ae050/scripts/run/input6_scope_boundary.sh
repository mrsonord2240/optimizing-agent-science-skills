#!/bin/bash
# Regression of pre-fix Input 6 (Scope Boundary). Fix added an explicit "Practice boundaries"
# section to SKILL.md (P1). Re-run the real BLAST search; the accompanying agent response now
# has to be checked against SKILL.md's own new section text, not just baseline judgment.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input6 && cd input6
cp ../../../data/ref_proteins.fasta ../../../data/patient_variant.fasta .

"$BIN/makeblastdb.exe" -in ref_proteins.fasta -dbtype prot \
    -blastdb_version 5 -parse_seqids -hash_index -out ref_prot_db

"$BIN/blastp.exe" -query patient_variant.fasta -db ref_prot_db \
    -evalue 1e-10 -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore stitle" \
    -out patient_hit.tsv

echo "=== real blastp result ==="
cat patient_hit.tsv
