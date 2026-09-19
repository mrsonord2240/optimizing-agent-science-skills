#!/bin/bash
# Input 1 (Canonical) -- following SKILL.md "Pfam domain annotation (canonical)" pattern,
# using the shipped examples/pfam_annotation.sh awk line verbatim, against cached PF00069 (Pkinase) + P17612.
set -euo pipefail
cd /mnt/openscience/audit-envs/database-access/public-data/remote-homology

echo "=== hmmscan --cut_ga (already-pressed PF00069.hmm) ==="
hmmscan --cut_ga --domtblout /tmp/query.domtbl --tblout /tmp/query.tbl --cpu 4 PF00069.hmm P17612.fasta > /tmp/query.hmmscan.txt

echo
echo "=== Shipped examples/pfam_annotation.sh awk line, VERBATIM ==="
echo "awk '!/^#/ {print \$4\"\t\"\$1\"\t\"\$2\"\t\"\$5\"\t\"\$6}' query.domtbl"
echo "Columns: query_name | pfam_name | pfam_acc | full_evalue | full_score"
awk '!/^#/ {print $4"\t"$1"\t"$2"\t"$5"\t"$6}' /tmp/query.domtbl

echo
echo "=== SKILL.md's own awk line (the correct one) ==="
echo "awk '!/^#/ {print \$1, \$2, \$4, \$5, \$7, \$8, \$13}' query.domtbl"
echo "Columns: target_name, accession, query_name, accession, full_evalue, full_score, i_evalue"
awk '!/^#/ {print $1, $2, $4, $5, $7, $8, $13}' /tmp/query.domtbl

echo
echo "=== Raw domtblout header for column reference ==="
grep '^#' /tmp/query.domtbl | head -3
