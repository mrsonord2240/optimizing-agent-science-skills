#!/bin/bash
# Re-audit input 1 (Canonical, regression) — bac15cc
# datasets/dataformat 18.37.0, F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\
set -euo pipefail
export PATH="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli:$PATH"

datasets.exe download genome accession GCF_000819615.1 \
    --include genome,gff3,protein,cds,seq-report \
    --filename phix.zip --no-progressbar
unzip -q phix.zip -d phix/
ls phix/ncbi_dataset/data/GCF_000819615.1/
grep -c "^>" phix/ncbi_dataset/data/GCF_000819615.1/protein.faa

dataformat.exe tsv genome \
    --inputfile phix/ncbi_dataset/data/assembly_data_report.jsonl \
    --fields accession,organism-name,assminfo-level,assmstats-scaffold-n50,assmstats-contig-n50,assmstats-total-sequence-len

# NEW: also exercised a different --fields combination than the fixer's own test
# (SKILL.md's "Filter assemblies by quality and date" pattern)
datasets.exe summary genome taxon "Salmonella enterica" \
    --assembly-level chromosome,complete --released-after 2024-01-01 --as-json-lines \
  | dataformat.exe tsv genome \
        --fields accession,organism-name,assminfo-level,assmstats-scaffold-n50,assminfo-release-date \
  > sal_2024.tsv
wc -l sal_2024.tsv
head -4 sal_2024.tsv

# Result: all field names resolve cleanly on 18.37.0, no "not recognized" errors.
# phiX174: organism "Escherichia phage phiX174", 11 CDS, 5386/5386/5386 stats.
# Salmonella: 1764 real rows with dates >= 2024-01-01.
