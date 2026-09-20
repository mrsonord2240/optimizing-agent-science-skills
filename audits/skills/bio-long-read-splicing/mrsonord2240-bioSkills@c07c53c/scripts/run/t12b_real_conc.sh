#!/bin/bash
# Second method (pysam vs GTF) on the REAL alignments: fraction of junction observations on annotated introns. Run after t5_real.sh and t12_realdrna.sh.
R=/mnt/openscience/audits/bio-long-read-splicing/run; export PYTHONDONTWRITEBYTECODE=1
cd $R/out/ex_realdrna; echo "real dRNA (example PLATFORM=drna alignment):"; asenv as-lr python $R/real_conc.py out/a549_aligned.bam annotation.gtf
cd $R/out/real
echo 'real LRGASP cDNA, ONT recipe (no -uf):'; asenv as-lr python $R/real_conc.py ont_cdna_aligned.bam gencode.v45.annotation.gtf
minimap2 -ax splice -uf -k14 --secondary=no --junc-bed annotation.bed12 -t 8 reference.fa ont_cdna.fastq.gz 2>/dev/null | samtools sort -o uf.bam - 2>/dev/null
echo 'real LRGASP cDNA, same recipe plus -uf:'; asenv as-lr python $R/real_conc.py uf.bam gencode.v45.annotation.gtf
