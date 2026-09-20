#!/bin/bash
cd /mnt/openscience/audits/bio-bam-statistics/run/work/t8
{
echo "== index CRAM then run Skill mosdepth CRAM command"
samtools index test.paired_end.sorted.cram && ls test.paired_end.sorted.cram*
mosdepth -t 4 -f genome.fasta cr test.paired_end.sorted.cram
grep '^chr22' cr.mosdepth.summary.txt bm.mosdepth.summary.txt
echo "== samtools flagstat/stats on CRAM (no --reference option on flagstat; Skill 'stats -r ref.fa' as reference for GC)"
samtools flagstat test.paired_end.sorted.cram | head -3
samtools stats -r genome.fasta test.paired_end.sorted.cram | grep -E '^SN\s(raw total|error rate)'
} > ../../out/t8b_cram.txt 2>&1; cat ../../out/t8b_cram.txt
