#!/bin/bash
# Does Picard 3.5.0 ignore genome.fasta.dict (SKILL.md says "GATK and Picard look for <name>.dict ... a genome.fasta.dict is ignored")?
# Use a Picard tool that REQUIRES the dictionary (ScatterIntervalsByNs / CollectWgsMetrics) and vary which dict names exist.
R=/mnt/openscience/audits/bio-reference-operations/run
W=$R/work/r1c; rm -rf $W; mkdir -p $W; cd $W
for mode in only_fasta_dot_dict only_genome_dot_dict none; do
  mkdir $mode; cd $mode; cp $R/data/real/genome.fasta .; samtools faidx genome.fasta
  case $mode in only_fasta_dot_dict) samtools dict genome.fasta -o genome.fasta.dict;; only_genome_dot_dict) samtools dict genome.fasta -o genome.dict;; esac
  picard ScatterIntervalsByNs R=genome.fasta OT=BOTH O=out.interval_list > log.txt 2>&1
  echo "== $mode: picard ScatterIntervalsByNs rc=$? out_lines=$(grep -vc '^@' out.interval_list 2>/dev/null) :: $(grep -m2 -i -E 'exception|dictionary|error' log.txt | cut -c1-200 | tr '\n' ' ')"
  picard CollectWgsMetrics I=$R/data/real/test.paired_end.sorted.bam R=genome.fasta O=wgs.txt > log2.txt 2>&1
  echo "   CollectWgsMetrics rc=$? metrics_file_lines=$(wc -l < wgs.txt 2>/dev/null) :: $(grep -m1 -i -E 'exception|dictionary|error' log2.txt | cut -c1-200)"
  cd ..
done
