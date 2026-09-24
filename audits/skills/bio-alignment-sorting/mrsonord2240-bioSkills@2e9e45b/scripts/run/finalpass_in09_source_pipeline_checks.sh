#!/bin/bash
# Final-pass fresh input 9: run the source-tip pipeline's new atomic-output and
# thread-validation behavior against real FASTQs prepared by archived input 7.
set -euo pipefail
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
ROOT=/mnt/openscience/audits/bio-alignment-sorting/run
SOURCE=/mnt/openscience/worktrees/bio-alignment-sorting-finalpass/alignment-files/alignment-sorting/examples/sort_pipeline.sh
DATA=/mnt/openscience/audit-envs/alignment-files/public-data
WORK=$ROOT/work/finalpass_in09
rm -rf "$WORK"
mkdir -p "$WORK"
cd "$WORK"

bash -n "$SOURCE"
cp "$DATA/human/genome.fasta" ref.fa
bwa index ref.fa >/dev/null 2>&1
samtools collate -O -u "$DATA/human/test.paired_end.sorted.bam" tmp | \
    samtools fastq -1 r1.fq -2 r2.fq -0 /dev/null -s /dev/null -n - >/dev/null

# A fourth positional numeric argument is now single-end thread count.
bash "$SOURCE" ref.fa r1.fq se_threads.bam 3
test -s se_threads.bam
test -s se_threads.bam.bai
test "$(samtools view -c -F 0x900 se_threads.bam)" -eq "$(($(wc -l < r1.fq) / 4))"

# Preserve a valid published result across two failures.
cp se_threads.bam keep.bam
cp se_threads.bam.bai keep.bam.bai
before=$(samtools view keep.bam | md5sum)
if bash "$SOURCE" ref.fa r1.fq keep.bam r2.fq abc; then
    echo "expected bad thread value to fail" >&2
    exit 1
fi
test "$(samtools view keep.bam | md5sum)" = "$before"

head -n $((($(wc -l < r2.fq) / 4 - 20) * 4)) r2.fq > r2_short.fq
if bash "$SOURCE" ref.fa r1.fq keep.bam r2_short.fq 2; then
    echo "expected unequal mate files to fail" >&2
    exit 1
fi
test "$(samtools view keep.bam | md5sum)" = "$before"
test -z "$(find . -maxdepth 1 -name 'keep.bam.partial.*' -print -quit)"
echo "PASS: source-tip pipeline validates threads, accepts SE threads, and publishes no partial output"
