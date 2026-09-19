#!/bin/bash
# Input 2 (Variant A) -- "twilight-zone" MMseqs2 default vs -s 7.5, per SKILL.md decision matrix
# and Failure Modes > "MMseqs2 default sensitivity".
set -euo pipefail
WORK=/tmp/mmseqs_test
rm -rf "$WORK"; mkdir -p "$WORK"; cd "$WORK"
cp /mnt/openscience/audit-envs/database-access/public-data/remote-homology/P17612.fasta query.fa
cp /mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta target.fa

mmseqs createdb target.fa targetDB > /dev/null

echo "=== MMseqs2 easy-search DEFAULT (-s 4.0, as usage-guide.md's own Quick Start line implies without -s) ==="
mmseqs easy-search query.fa target.fa default_results.m8 tmp_default --format-output query,target,fident,alnlen,evalue,bits > /dev/null 2>&1 || true
echo "hits: $(wc -l < default_results.m8 2>/dev/null || echo 0)"
grep -i Q197B6 default_results.m8 || echo "Q197B6 (the known twilight-zone homolog) NOT recovered at default sensitivity"

echo
echo "=== MMseqs2 easy-search -s 7.5 (SKILL.md's documented remedy) ==="
mmseqs easy-search query.fa target.fa sensitive_results.m8 tmp_sens -s 7.5 --format-output query,target,fident,alnlen,evalue,bits > /dev/null 2>&1
echo "hits: $(wc -l < sensitive_results.m8)"
grep -i Q197B6 sensitive_results.m8 && echo "Q197B6 recovered at -s 7.5, as SKILL.md's failure-mode section predicts"
