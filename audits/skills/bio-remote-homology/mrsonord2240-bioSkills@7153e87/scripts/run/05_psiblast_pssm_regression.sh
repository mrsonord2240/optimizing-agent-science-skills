#!/bin/bash
# Regression of original audit Input 4: PSI-BLAST 3-iteration PSSM build + reuse, per SKILL.md's
# saved-PSSM pattern. Independent re-run against the cached Swiss-Prot sample BLAST DB.
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"
DB=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample_db

psiblast -query P17612.fasta -db "$DB" \
         -num_iterations 3 \
         -inclusion_ethresh 0.002 \
         -evalue 0.01 \
         -num_threads 4 \
         -out_pssm psiblast.pssm.asn \
         -out_ascii_pssm psiblast.pssm.txt \
         -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" \
         -out psiblast.tsv
echo "=== hits ==="
cat psiblast.tsv
echo "=== PSSM files ==="
ls -la psiblast.pssm.asn psiblast.pssm.txt

echo
echo "=== Reuse saved PSSM (-in_pssm) against the same DB ==="
psiblast -in_pssm psiblast.pssm.asn -db "$DB" -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" -out psiblast_reuse.tsv
cat psiblast_reuse.tsv
