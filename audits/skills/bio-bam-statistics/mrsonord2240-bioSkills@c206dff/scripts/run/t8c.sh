#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run/work/t8
{ echo "== stats on CRAM with --reference (decode ref) + -r (GC ref)"; samtools stats --reference genome.fasta -r genome.fasta test.paired_end.sorted.cram | grep -E '^SN\s(raw total|error rate)';
  echo "== stats on CRAM with -r ONLY (as Skill's table shows)"; samtools stats -r genome.fasta test.paired_end.sorted.cram 2>&1 | grep -E '^SN\s(raw total|error rate)|Failure' | head -2; } > ../../out/t8c_cram_stats.txt 2>&1; cat ../../out/t8c_cram_stats.txt
