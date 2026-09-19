#!/bin/bash
# Regression of original audit Input 2: MMseqs2 default (-s 4.0) vs -s 7.5 on the P17612 twilight-zone
# query against the cached 300-seq Swiss-Prot sample. Independent re-run, not reuse of prior output.
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"
cp /mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta .
mkdir -p mmseqs_tmp

echo "=== MMseqs2 default (-s 4.0) ==="
mmseqs easy-search P17612.fasta swissprot_sample.fasta mmseqs_default.m8 mmseqs_tmp --threads 4
echo "hits:"; cat mmseqs_default.m8 2>/dev/null | wc -l

echo
echo "=== MMseqs2 -s 7.5 ==="
mmseqs easy-search P17612.fasta swissprot_sample.fasta mmseqs_s75.m8 mmseqs_tmp -s 7.5 --threads 4
echo "hits:"; cat mmseqs_s75.m8
