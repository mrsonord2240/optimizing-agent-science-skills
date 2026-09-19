#!/usr/bin/env bash
# Adapted verbatim from the Skill's examples/remove_primers.sh pattern (515F/806R EMP primers),
# pointed at the audit env's real DADA2 fixture (datagen/amplicon/raw_reads).
set -euo pipefail

CUTADAPT="/f/OpenScience/audit-envs/microbiome-metagenomics-analyst/Scripts/cutadapt.exe"
FWD='GTGYCAGCMGCCGCGGTAA'    # 515F
REV='GGACTACNVGGGTWTCTAAT'   # 806R

raw_dir='/f/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/raw_reads'
out_dir='/f/OpenScience/audits/bio-amplicon-processing/work/trimmed'
mkdir -p "$out_dir"

for r1 in "$raw_dir"/*_R1_001.fastq.gz; do
    r2="${r1/_R1_/_R2_}"
    base=$(basename "$r1" _R1_001.fastq.gz)
    "$CUTADAPT" \
        -g "$FWD" \
        -G "$REV" \
        --discard-untrimmed \
        -o "$out_dir/${base}_R1_001.fastq.gz" \
        -p "$out_dir/${base}_R2_001.fastq.gz" \
        "$r1" "$r2" >> "$out_dir/../cutadapt_log.txt" 2>&1
done

echo "DONE cutadapt on $(ls "$raw_dir"/*_R1_001.fastq.gz | wc -l) sample pairs"
