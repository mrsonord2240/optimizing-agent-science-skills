#!/bin/bash
# Input 4 (Variant B) -- PSI-BLAST 3-iteration PSSM build + reuse via -in_pssm against a different DB,
# per SKILL.md "PSI-BLAST with saved PSSM" code pattern.
set -euo pipefail
WORK=/tmp/psiblast_test
rm -rf "$WORK"; mkdir -p "$WORK"; cd "$WORK"
cp /mnt/openscience/audit-envs/database-access/public-data/remote-homology/P17612.fasta query.fa
DB=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample_db

echo "=== psiblast, 3 iterations, -inclusion_ethresh 0.002, save PSSM ==="
psiblast -query query.fa -db "$DB" \
  -num_iterations 3 -inclusion_ethresh 0.002 -evalue 0.01 -num_threads 4 \
  -out_pssm distant.pssm.asn -out_ascii_pssm distant.pssm.txt \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
  -out psiblast_results.txt 2>&1 | tail -20
echo "PSSM saved: $(ls -la distant.pssm.asn distant.pssm.txt 2>&1 | wc -l) files"
echo "Hits found:"
cat psiblast_results.txt

echo
echo "=== Reuse saved PSSM with -in_pssm against the SAME sample DB (documented pattern: reuse against a DIFFERENT db) ==="
psiblast -in_pssm distant.pssm.asn -db "$DB" -out reused_pssm_results.txt \
  -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" 2>&1 | tail -10
cat reused_pssm_results.txt
