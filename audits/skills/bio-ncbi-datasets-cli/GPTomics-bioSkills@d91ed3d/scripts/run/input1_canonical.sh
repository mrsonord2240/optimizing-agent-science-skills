#!/bin/bash
# Input 1 (Canonical) — "Download the reference genome for Escherichia phage phiX174
# (GCF_000819615.1) with genome, protein, and CDS files, then give me the assembly
# stats (organism, length, N50) as a table."
# Follows SKILL.md's "Download a single reference genome" pattern verbatim, substituting
# a small real accession for the (huge) human reference used in the doc's own example.
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"
DF="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/dataformat.exe"
ACC="GCF_000819615.1"

echo "=== Download ${ACC} ==="
"$DS" download genome accession "${ACC}" \
    --include genome,protein,cds,seq-report \
    --filename input1_phix174.zip \
    --no-progressbar

echo "=== Unzip ==="
rm -rf input1_phix174
unzip -q input1_phix174.zip -d input1_phix174/
find input1_phix174/ncbi_dataset/data -type f

echo "=== dataformat tsv genome, SKILL.md's documented field names (as written) ==="
JSONL="input1_phix174/ncbi_dataset/data/assembly_data_report.jsonl"
set +e
"$DF" tsv genome --inputfile "$JSONL" \
    --fields accession,organism-name,assembly-level,scaffold-n50,contig-n50,total-sequence-length
DOC_FIELDS_EXIT=$?
set -e
echo "exit code (doc field names): $DOC_FIELDS_EXIT"

echo
echo "=== dataformat tsv genome, corrected field names ==="
"$DF" tsv genome --inputfile "$JSONL" \
    --fields accession,organism-name,assminfo-level,assmstats-total-sequence-len,assmstats-contig-n50 \
    | column -t -s $'\t'

echo
echo "=== Sanity: FASTA header count / length, protein count ==="
grep -c '^>' input1_phix174/ncbi_dataset/data/${ACC}/*.fna
grep -c '^>' input1_phix174/ncbi_dataset/data/${ACC}/protein.faa
