#!/bin/bash
D=/mnt/openscience/audits/bio-alignment-validation/run/data/new
for f in n_mate_other_chrom n_qual_out_of_range n_md_wrong; do
  echo "=== $f"; picard ValidateSamFile I=$D/$f.bam MODE=SUMMARY R=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta 2>&1 | grep -v -E '^\*|setlocale|restricted|^$|Runtime|Version|INFO|WARNING: (Use|Native)' | tail -6 | cut -c1-200
done
echo "--- 1000G ones without R"
for f in n_mate_other_chrom n_qual_out_of_range; do
  echo "=== $f"; picard ValidateSamFile I=$D/$f.bam MODE=SUMMARY 2>&1 | grep -v -E '^\*|setlocale|restricted|^$|Runtime|Version|INFO' | tail -8 | cut -c1-200
done
