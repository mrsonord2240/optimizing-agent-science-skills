#!/bin/bash
# Regression of pre-fix Input 4 (Edge, blastn-short). Unaffected by the fix -- sanity check.
set -euo pipefail
BIN="F:/OpenScience/audit-envs/database-access/tools/blast/ncbi-blast-2.17.0+/bin"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input4 && cd input4
cp ../../../data/human_refseq_rna.fasta ../../../data/primers.fasta .

"$BIN/makeblastdb.exe" -in human_refseq_rna.fasta -dbtype nucl \
    -blastdb_version 5 -parse_seqids -out human_refseq_rna

echo "=== default megablast (should find nothing, primers <25nt) ==="
"$BIN/blastn.exe" -query primers.fasta -db human_refseq_rna \
    -evalue 1000 -outfmt 6 -out default_megablast.tsv
echo "rows: $(wc -l < default_megablast.tsv)"
cat default_megablast.tsv

echo "=== -task blastn-short -word_size 7 ==="
"$BIN/blastn.exe" -query primers.fasta -db human_refseq_rna \
    -task blastn-short -word_size 7 -evalue 1000 -outfmt 6 \
    -out primer_hits.tsv
cat primer_hits.tsv
