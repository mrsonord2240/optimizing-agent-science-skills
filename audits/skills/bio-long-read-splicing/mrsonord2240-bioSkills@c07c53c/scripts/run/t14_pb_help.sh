#!/bin/bash
# skera / lima / isoseq CLI check against --help only (env as-pb, no Kinnex data). SKILL block: `skera split raw_kinnex.bam mas12_primers.fasta demuxed.bam` then lima -> isoseq refine -> isoseq cluster2.
for c in "skera --version" "skera split --help" "lima --version" "isoseq --version" "isoseq refine --help" "isoseq cluster2 --help"; do
  echo "##### $c"; micromamba run -n as-pb $c 2>&1 | head -${N:-22}; done
