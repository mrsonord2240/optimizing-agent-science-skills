#!/bin/bash
D=$AFDATA
for f in human/test.paired_end.sorted.bam human/test.rna.paired_end.sorted.bam human/test.paired_end.umi_unsorted.bam 1000g/HG00349.chr20_1400000-1500000.bam sarscov2/sars-cov-2_v5.3.2.nanopore.bam sarscov2/test.paired_end.sorted.bam sarscov2/test.single_end.sorted.bam derived/planted_dups.bam; do
 echo "=== $f"; samtools view -H $D/$f | grep -v '^@SQ' | cut -c1-150 | head -5; echo "SQ lines: $(samtools view -H $D/$f | grep -c '^@SQ')  with M5: $(samtools view -H $D/$f | grep '^@SQ' | grep -c M5:)"; samtools view $D/$f | head -1 | cut -c1-200
done
echo; samtools dict $D/human/genome.fasta; grep -c '' $D/human/genome.dict; cat $D/human/genome.dict | cut -c1-200
