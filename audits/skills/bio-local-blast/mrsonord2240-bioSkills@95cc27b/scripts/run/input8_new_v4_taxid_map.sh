#!/bin/bash
# NEW input (not in the pre-fix audit). Tests SKILL.md's rewritten v4-vs-v5 table claim:
# "Per-sequence taxid at build time (-taxid_map): v4 No / v5 Yes." Build a v4-format DB with
# -taxid_map and see what actually happens -- does makeblastdb reject/ignore it as documented?
set -uo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input8 && cd input8
cp ../../../data/ref_proteins.fasta ../../../data/taxid_map.tsv ../../../data/taxid_query.fasta .

echo "=== Attempt: v4-format DB (-blastdb_version 4) with -taxid_map ==="
"$BIN/makeblastdb.exe" -in ref_proteins.fasta -dbtype prot \
    -blastdb_version 4 -parse_seqids -taxid_map taxid_map.tsv \
    -out v4_taxid_db > build_v4.log 2>&1
rc=$?
echo "makeblastdb exit code: $rc"
cat build_v4.log

echo
echo "=== blastdbcmd -info on the resulting DB ==="
"$BIN/blastdbcmd.exe" -db v4_taxid_db -info

echo
echo "=== Does staxids come back populated on a v4 DB search, despite -taxid_map having been passed? ==="
"$BIN/blastp.exe" -query taxid_query.fasta -db v4_taxid_db \
    -evalue 1e-10 -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -out v4_search.tsv 2>v4_search.stderr
echo "stderr:"; cat v4_search.stderr
echo "v4_search.tsv:"; cat v4_search.tsv

echo
echo "=== Compare: does -taxidlist filtering do anything at all on this v4 DB? ==="
echo 9606 > human_only.txt
"$BIN/blastp.exe" -query taxid_query.fasta -db v4_taxid_db \
    -taxidlist human_only.txt \
    -evalue 1e-10 -outfmt "6 qseqid sseqid staxids sscinames evalue bitscore" \
    -out v4_filtered.tsv 2>v4_filtered.stderr
rc2=$?
echo "exit code: $rc2"
cat v4_filtered.stderr
echo "v4_filtered.tsv:"; cat v4_filtered.tsv
echo "row count unfiltered vs filtered: $(wc -l < v4_search.tsv) vs $(wc -l < v4_filtered.tsv)"
